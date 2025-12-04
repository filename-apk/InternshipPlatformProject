from flask_jwt_extended import create_access_token
import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import (create_user, get_all_users_json, get_all_users, initialize, get_shortlist_by_student, get_shortlist_by_position, get_positions_by_employer, login)
from App.models.employer import Employer
from App.models.position import Position
from App.models.shortlist import Shortlist
from App.models.staff import Staff
from App.models.student import Student
from App.controllers.student import create_student, viewShortlist as student_viewShortlist, viewEmployerDecision as student_viewEmployerDecision
from App.controllers.employer import create_employer, createPosition, viewApplicants as employer_viewApplicants, makeDecision as employer_makeDecision
from App.controllers.staff import addToshortlist as staff_addToshortlist, create_staff, viewAvailablePositions as staff_viewAvailablePositions
import warnings
from sqlalchemy import exc as sa_exc

# Suppress the specific warning
warnings.filterwarnings('ignore', 
    category=sa_exc.SAWarning,
    message='Loading context.*has changed within a load/refresh handler'
)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)


@app.cli.command("init-default", help="Creates and initializes the database with a default dataset")
def initDefault():
    initialize()
    
    print('Creating default users...')
    
    try:
        # Create Employers using your controller function
        BillGates = create_employer("billygates", "iLoveMicrosoft", "Bill Gates", "Microsoft")
        JeffBezos = create_employer("thereal_baldy", "amazon123", "Jeff Bezos", "Amazon")
        VinceMcMahon = create_employer("moneybagsvince", "wwe4life", "Vince McMahon", "WWE")
        print('Default Employers created')
        db.session.add_all([BillGates, JeffBezos, VinceMcMahon])

        
        # Create Students using your controller function
        # Note: Adjust parameters based on your create_student function
        Alice = create_student("alice_w", "alicepass", "Alice Wonderland", "Computer Science", "resume.pdf", 3.8)
        Bob = create_student("bob_b", "bobpass", "Bobby Brown", "Business Administration", "resume.pdf", 3.5)
        Charlie = create_student("charlie_b", "charliepass", "Charlie Brown", "Mechanical Engineering", "resume.pdf", 3.9)
        print('Default Students created')
        db.session.add_all([Alice, Bob, Charlie])
        
        # Create Staff using your controller function
        ProfJohnson = create_staff("prof_johnson", "johnsonpass", "Prof. Emily Johnson", "Business")
        DrLee = create_staff("dr_lee", "leepass", "Dr. Michael Lee", "Computer Science")
        Keith = create_staff("keith_r", "greatistheUNC", "Keith BaldHead RowRow", "Poli-Tricks Science")
        print('Default Staff created')
        db.session.add_all([ProfJohnson, DrLee, Keith])
        
        # Create Positions using your controller function
        # Note: Adjust parameters based on your createPosition function
        Position1 = createPosition("Software Engineering Intern", BillGates, "Work on cutting-edge software solutions.", 5)
        Position2 = createPosition("Data Analyst Intern", JeffBezos, "Analyze large datasets to drive business decisions.", 3)
        Position3 = createPosition("Marketing Intern", VinceMcMahon, "Assist in marketing campaigns and social media management.", 1)
        print('Default Positions created')
        db.session.add_all([Position1, Position2, Position3])
        
        db.session.commit()
        print('\nDatabase initialized and populated successfully!')
        
        print('\nDefault users created:')
        print('Students: alice_w (pass: alicepass), bob_b (bobpass), charlie_b (charliepass)')
        print('Employers: billygates (iLoveMicrosoft), real_baldy (amazon123), moneybagsvince (wwe4life)')
        print('Staff: prof_johnson (johnsonpass), dr_lee (leepass), keith_r (greatistheUNC)')
        
        
    except Exception as e:
        print(f'Error creating default dataset: {e}')
        db.session.rollback()



# Create CLI groups

student_cli = AppGroup('student', help='Student commands')
employer_cli = AppGroup('employer', help='Employer commands')
staff_cli = AppGroup('staff', help='Staff commands')

# Helper function to login and get user info
def get_user_info(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        if hasattr(user, 'studentID'):
            role = 'student'
            user_id = user.studentID
            user_obj = Student.query.get(user.studentID)
        elif hasattr(user, 'id') and hasattr(user, 'company'):
            role = 'employer'
            user_id = user.id
            user_obj = Employer.query.get(user.id)
        elif hasattr(user, 'id') and hasattr(user, 'faculty'):
            role = 'staff'
            user_id = user.id
            user_obj = Staff.query.get(user.id)
        else:
            role = 'user'
            user_id = user.id
            user_obj = user
        
        return {
            'user': user_obj,
            'role': role,
            'user_id': user_id,
            'token': create_access_token(identity=str(user.id))
        }
    return None

# User commands
@user_cli.command("login", help="Login to the system")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def login_command(username, password):
    user_info = get_user_info(username, password)
    if user_info:
        print(f'{username} ({user_info["role"]}) logged in successfully!')
        print(f'User ID: {user_info["user_id"]}')
    else:
        print("Login failed - Invalid username or password")

# Student commands
@student_cli.command("shortlist", help="View your shortlist")
@click.argument("username")
@click.argument("password")
@click.argument("choice", type=int)
def student_shortlist_command(username, password, choice):
    user_info = get_user_info(username, password)
    if not user_info or user_info['role'] != 'student':
        print("Error: Invalid credentials or not a student")
        return
    
    if not user_info['user']:
        print("Error: Student not found")
        return
    
    result = student_viewShortlist(user_info['user'], choice)
    if isinstance(result, list):
        print(f"Found {len(result)} items in shortlist:")
        for item in result:
            print(f"  - {item}")
    elif result:
        print(f"Result: {result}")
    else:
        print("No results found")

@student_cli.command("decision", help="View employer decisions on your applications")
@click.argument("username")
@click.argument("password")
def student_decision_command(username, password):
    user_info = get_user_info(username, password)
    if not user_info or user_info['role'] != 'student':
        print("Error: Invalid credentials or not a student")
        return
    
    if not user_info['user']:
        print("Error: Student not found")
        return
    
    # Get the student object
    student = user_info['user']

    
    shortlists = Shortlist.query.filter_by(studentID=student.studentID).all()
    
    if not shortlists:
        print("No applications found.")
        return
    
    print(f"Found {len(shortlists)} applications:")
    print("=" * 60)
    
    decisions_found = False
    
    for sl in shortlists:
        position = Position.query.get(sl.positionID)
        employer = Employer.query.get(position.employerID) if position else None
        
        # Get status as readable string
        status = str(sl.status)
        if "DecisionStatus." in status:
            status = status.replace("DecisionStatus.", "")
        
        print(f"Position: {position.title if position else 'Unknown'}")
        print(f"Company: {employer.company if employer else 'Unknown'}")
        print(f"Status: {status}")
        
        # Show specific message based on status
        if status.lower() == "accepted":
            print(f"CONGRATULATIONS! You have been ACCEPTED for this position!")
            decisions_found = True
        elif status.lower() == "rejected":
            print(f"You have been REJECTED for this position.")
            decisions_found = True
        elif status.lower() == "pending":
            print(f"Decision is still PENDING. The employer hasn't made a decision yet.")
        else:
            print(f"Current status: {status}")
        
        print("-" * 60)
    
    if not decisions_found:
        print("\nNo final decisions (Accepted/Rejected) have been made on your applications yet.")
        print("All applications are still pending employer review.")

# Employer commands
@employer_cli.command("create-position", help="Create a new job position")
@click.argument("username")
@click.argument("password")
@click.argument("title")
@click.argument("description")
@click.argument("number_of_positions", type=int)
def employer_create_position_command(username, password, title, description, number_of_positions):
    user_info = get_user_info(username, password)
    if not user_info or user_info['role'] != 'employer':
        print("Error: Invalid credentials or not an employer")
        return
    
    if not user_info['user']:
        print("Error: Employer not found")
        return
    
    position = createPosition(title, user_info['user'], description, number_of_positions)
    print(f"Position '{position.title}' created with ID {position.positionID}")

@employer_cli.command("view-applicants", help="View applicants for a position")
@click.argument("username")
@click.argument("password")
@click.argument("position_id", type=int)
def employer_view_applicants_command(username, password, position_id):
    user_info = get_user_info(username, password)
    if not user_info or user_info['role'] != 'employer':
        print("Error: Invalid credentials or not an employer")
        return
    
    applicants = employer_viewApplicants(user_info['user_id'], position_id)
    if applicants is None:
        print("Error: Position not found or you don't have permission")
    elif applicants:
        print(f"Found {len(applicants)} applicants:")
        for app in applicants:
           print(f"  - Student ID: {app.studentID}, Status: {str(app.status)}")
    else:
        print("No applicants found")

@employer_cli.command("make-decision", help="Make decision on applicant")
@click.argument("username")
@click.argument("password")
@click.argument("shortlist_id", type=int)
@click.argument("decision")
def employer_make_decision_command(username, password, shortlist_id, decision):
    user_info = get_user_info(username, password)
    if not user_info or user_info['role'] != 'employer':
        print("Error: Invalid credentials or not an employer")
        return
    
    result = employer_makeDecision(user_info['user_id'], shortlist_id, decision)
    if result:
        print(f"Decision '{decision}' recorded for shortlist ID {shortlist_id}")
    else:
        print("Error: Failed to make decision")

# Staff commands
@staff_cli.command("shortlist", help="Shortlist a student for a position")
@click.argument("username")
@click.argument("password")
@click.argument("position_id", type=int)
@click.argument("student_id", type=int)
def staff_shortlist_command(username, password, position_id, student_id):
    user_info = get_user_info(username, password)
    if not user_info or user_info['role'] != 'staff':
        print("Error: Invalid credentials or not staff")
        return
    
    if not user_info['user']:
        print("Error: Staff not found")
        return
    
    result = staff_addToshortlist(position_id, student_id, user_info['user'].id)
    if isinstance(result, str):
        print(f"Result: {result}")
    else:
        print(f"Student {student_id} shortlisted for position {position_id}")
        print(f"Shortlist ID: {result.shortlistID}")

@staff_cli.command("positions", help="View available positions")
@click.argument("username")
@click.argument("password")
def staff_positions_command(username, password):
    user_info = get_user_info(username, password)
    if not user_info or user_info['role'] != 'staff':
        print("Error: Invalid credentials or not staff")
        return
    
    positions = staff_viewAvailablePositions()
    if positions:
        print(f"Found {len(positions)} available positions:")
        for pos in positions:
            print(f"  ID: {pos.positionID}, Title: {pos.title}, "
                  f"Positions: {pos.numberOfPositions}")
    else:
        print("No available positions found")

@staff_cli.command("list-students", help="List all students")
@click.argument("username")
@click.argument("password")
def staff_list_students_command(username, password):
    user_info = get_user_info(username, password)
    if not user_info or user_info['role'] != 'staff':
        print("Error: Invalid credentials or not staff")
        return
    
    from App.models.student import Student
    
    students = Student.query.all()
    
    if not students:
        print("No students found")
        return
    
    print(f"Students ({len(students)} total):")
    for student in students:
        print(f"  ID: {student.studentID} - {student.name} ({student.username})")
        print(f"     Degree: {student.degree}, GPA: {student.GPA}, Status: {student.status_name}")




'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)


    # ... your app configuration ...

# Register CLI commands
app.cli.add_command(user_cli)
app.cli.add_command(student_cli)
app.cli.add_command(employer_cli)
app.cli.add_command(staff_cli)

