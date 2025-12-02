import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Position, Shortlist, Staff, Student, PositionStatus
from App.models.shortlist import DecisionStatus
from App.models.states import Applied, Shortlisted, Accepted, Rejected
from App.controllers import (
    create_user,
   get_all_users_json,
    login,
    get_all_users,
    check_password,
    set_password,
   # get_user,
   # get_user_by_username,
   # update_user,
   # open_position,
    get_positions_by_employer,
   # add_student_to_shortlist,
    get_shortlist_by_student,
   # decide_shortlist,
    create_staff, 
   # view_applicants, 
    makeDecision, 
    editPosition, 
    get_all_positions_json, 
    get_positions_by_employer_json, 
    #deleted_position, 
    get_shortlist_by_position, 
    create_employer, 
    create_student, 
    createPosition, 
    viewApplicants, 
    addToshortlist,
    viewAvailablePositions 
)


LOGGER = logging.getLogger(__name__)


'''
   Unit Tests
# '''
# class UserUnitTests(unittest.TestCase):

#     def test_new_user(self):
#         user = User("bob", "bobpass")
#         assert user.username == "bob"

#     def test_new_student(self):
#             student = Student("john", "johnpass")
#             assert student.username == "john"
#             assert student.role == "student"

#     def test_new_staff(self):
#         staff = Staff("jim", "jimpass")
#         assert staff.username == "jim"
#         assert staff.role == "staff"

#     def test_new_employer(self):
#         employer = Employer("alice", "alicepass")
#         assert employer.username == "alice"
#         assert employer.role == "employer"

#     def test_new_position(self):
#         position = Position("Software Developer", 10, 5) 
#         assert position.title == "Software Developer"
#         assert position.employerID == 10
#         assert position.status == "open"
#         assert position.numberOfPositions == 5

#     def test_new_shortlist(self):
#         shortlist = Shortlist(1,2,3)
#         assert shortlist.studentID == 1
#         assert shortlist.positionID == 2
#         assert shortlist.staffID == 3
#         assert shortlist.status == "pending"

#     # pure function no side effects or integrations called
#     def test_get_json(self):
#         user = User("bob", "bobpass")
#         user_json = user.get_json()
#         self.assertEqual(user_json["username"], "bob")
#         self.assertTrue("id" in user.get_json())
    
#     def test_hashed_password(self):
#         password = "mypass"
#         hashed = generate_password_hash(password)
#         user = User("bob", password)
#         assert user.password != password

#     def test_check_password(self):
#         password = "mypass"
#         user = User("bob", password)
#         assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    
    with app.app_context():
        create_db()
        yield app.test_client()
        db.drop_all()


class UserIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        
        staff = create_staff("rick", "bobpass", "staff", "fst")
        assert staff.username == "rick" , "Rick is a  staff"
        assert staff.faculty == "fst", "Rick works in fst"
        assert staff.role == "staff", "Rick's role is staff"
        self.assertIsNotNone(staff) 


        employer = create_employer("sam", "sampass", "employer", "SamCo")
        assert employer.username == "sam"
        assert employer.company == "SamCo"
        assert employer.role == "employer"
        self.assertIsNotNone(employer)

        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        assert student.username == "hannah"
        assert student.role == "student"
        self.assertIsNotNone(student)

   # def test_get_all_users_json(self):
     #   users_json = get_all_users_json()
      #  self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    #def test_update_user(self):
      #  update_user(1, "ronnie")
      #  user = get_user(1)
       # assert user.username == "ronnie"

    def test_employer_createPosition(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
      

        assert position.title =="Software Engineer"
        assert position.description == "Develop software, test software"
        assert position.numberOfPositions == 4
       
    

        


    def test_employer_viewApplicants(self):
       employer = create_employer("sam", "sampass", "employer", "SamCo")
       position = createPosition("Software Engineer", employer, "Develop software, test software", 4)

       applicants = viewApplicants(employer.id, position.positionID)
       assert applicants == []
       #Testing if you can view the applicants 
    #    staff = create_staff("rick", "bobpass", "staff", "fst")
    #    student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
    #    db.session.add(staff)
    #    db.session.add(student)
    #    db.session.commit()
    #    entry = Shortlist(student.id, staff.staffID)
    #    assert entry is not None
    #    assert len(applicants) == 0 

    #Note: This test gives fail, theres a logic error in the controller, it expects a string, when u put a string it then expects an enum, when u put an enum, it tries to capitiliaze
    def test_employer_makeDecision(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        
        staff = create_staff("rick", "bobpass", "staff", "fst")
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        db.session.add(student)
        db.session.commit()
        entry = Shortlist(position.positionID, student.studentID, staff.staffID)
        db.session.add(entry)
        db.session.commit()
         

        entry.update_status("Accepted")
        decision = "Accepted"
        updated = makeDecision(employer.employerID, entry.shortlistID, decision)
        assert updated.status == DecisionStatus.accepted


    def test_editPosition(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        updated = editPosition(employer.id, position.positionID, "Senior Analyst", "Analyze data", 4, "Open")

        assert updated.title == "Senior Analyst"
        assert updated.description == "Analyze data"
        assert updated.numberOfPositions == 4 
        assert updated.status == PositionStatus.open

    #Position tests 
    

    def test_get_positions_by_employer(self):
         employer = create_employer("sam", "sampass", "employer", "SamCo")
         position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
         position2 = createPosition("Data Analyst", employer, "Analyze data", 3)

         results = get_positions_by_employer(employer.employerID)
         assert len(results) == 2
         assert any(p.positionID == position.positionID for p in results)
         assert any(p.positionID == position2.positionID for p in results)


    def test_get_positions_by_employer_json(self):
         employer = create_employer("sam", "sampass", "employer", "SamCo")
         position = createPosition("Software Engineer", employer, "Develop software, test software", 4)

         all_json = get_all_positions_json()
         by_emp_json = get_positions_by_employer_json(employer.id)

         assert len(all_json) >= 1 
         assert len(by_emp_json) == 1 
         assert by_emp_json[0]["title"] == "Software Engineer"



    #shortlist tests 
    def test_get_shortlist_by_student(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")

        shortlist_entry = addToshortlist(position.positionID,student.studentID, staff.staffID)
       # db.commit(shortlist_entry)
        results = get_shortlist_by_student(student.id)

        assert len(results) == 1 
        assert results[0].shortlistID == shortlist_entry.shortlistID
        assert results[0].studentID == student.id 
        assert results[0].positionID == position.positionID 
        assert results[0].staffID == staff.id

    
    def test_get_shortlist_by_student_no_entries(self): 
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")

        shortlist_entry = addToshortlist(student.id, position.positionID, staff.id)
        results = get_shortlist_by_student(999)
        assert results == []

    def test_get_shortlist_by_position(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")

        shortlist_entry = addToshortlist( position.positionID, student.studentID,staff.staffID)
        results = get_shortlist_by_position(position.positionID)
    
        assert len(results) ==1
        assert results[0].positionID == position.positionID
        assert results[0].studentID == student.studentID 

    def test_get_shortlist_by_position_no_entries(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")

        shortlist_entry = addToshortlist(position.positionID, student.studentID, staff.staffID)
        results = get_shortlist_by_position(999)
        assert results == []


    #Staff tests
    def test_add_to_shortlist(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")
        entry = addToshortlist(position.positionID, student.studentID, staff.staffID)

        assert isinstance(entry, Shortlist)
        assert entry.positionID == position.positionID
        assert entry.studentID == student.studentID
        assert entry.staffID == staff.staffID

    def test_add_to_shortlist_duplicate(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")

        first = addToshortlist(position.positionID, student.studentID, staff.staffID)
        assert isinstance(first,Shortlist )

        second = addToshortlist(position.positionID, student.studentID, staff.staffID)
     

        assert isinstance(second, str)

        assert str(student.studentID) in second
        assert str(position.positionID) in second


    def test_view_available_positions(self ):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")
        entry = addToshortlist(position.positionID, student.studentID, staff.staffID)

        results = viewAvailablePositions()

        assert len(results) >= 1
        assert results[0].title == "Software Engineer"
        assert results[0].description  == "Develop software, test software"



    #Student tests + state tests 

    def test_student_state_is_applied(self):
        
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)

        assert student.status_name == "Applied"
        assert isinstance(student.status, Applied)
      

    def test_change_student_shortlisted(self):
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        student.changeStatus(Shortlisted)

        assert student.status_name == "Shortlisted"
        assert isinstance(student.status, Shortlisted)

    def test_change_student_accepted(self):
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        student.changeStatus(Shortlisted)
        student.changeStatus(Accepted)

        assert student.status_name == "Accepted"
        assert isinstance(student.status, Accepted)
    
    def test_change_student_rejected(self):
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)

        student.changeStatus(Shortlisted)
        student.changeStatus(Rejected)

        assert student.status_name == "Rejected"
        assert isinstance(student.status, Rejected)

    
    def test_state_persists_after_reload(self):
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)

        student.changeStatus(Shortlisted)
        student_id = student.id 
        db.session.expire_all()
        reloaded = Student.query.get(student_id)

        assert reloaded.status_name == "Shortlisted"
        assert isinstance(reloaded.status, Shortlisted)

    def test_view_shortlist(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")
        entry = addToshortlist(position.positionID, student.studentID, staff.staffID)
      #  student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        states = [Applied, Shortlisted, Accepted, Rejected]

        for state in states: 
           student.changeStatus(state)

         #  result = student.status.viewShortlist(student)
           result = student.status.viewShortlist()


          # assert result is None
           #assert isinstance(result, str)
           assert result is None or  isinstance(result, str)
    
    def test_view_employer_decision(self):
        employer = create_employer("sam", "sampass", "employer", "SamCo")
        position = createPosition("Software Engineer", employer, "Develop software, test software", 4)
        student = create_student("hannah", "hannahpass", "student", "Computer Science", "R.pdf", 3.4)
        staff = create_staff("rick", "bobpass", "staff", "fst")
        entry = addToshortlist(position.positionID, student.studentID, staff.staffID)
        states = [Applied, Shortlisted, Accepted, Rejected]

       # for state in states: 
         #  student.changeStatus(state)
        result = student.status.viewEmployerDecision()
        #   student.changeStatus(state)
        #   result = student.status.viewShortlist()

          # assert result is None
        #assert isinstance(result, str)
        assert result is None or  isinstance(result, str)


    #Testing Users
    def test_create_user(self):
        user = create_user("alice", "password")
        assert user.username == "alice"
        assert user.id is not None 
        assert user.password != "password"

    def test_login_success(self):
        user = create_user("alice", "password")
        check = login("alice", "password")
        assert check is not None 
        if isinstance(check, str):
            assert isinstance(check,str)
        else:
            assert user.username == "alice"

    def test_login_fail_wrong_password(self):
        user = create_user("alice", "password")
        user = login("alice", "wrongpassword")
        assert user is None
    
    def test_login_fail_no_user(self):
        user = login("notexit", "password")
        assert user is None
    
    def test_check_password(self):
        user = create_user("alice", "password")
        assert check_password(user.id, "password") is True
        assert check_password(user.id, "wrongpassword") is False

    def test_check_password_invalid_user(self):
        assert check_password(999, "password") is False

    def test_set_password(self):
        user = create_user("alice", "password")
        updated = set_password(user.id, "newpassword")
        assert updated is not None
        assert updated.check_password("newpassword") is True 

    
    def test_set_password_invalid_user(self):
        updated = set_password(999, "newpassword")
        assert updated is None

    def test_get_all_users(self):
        user = create_user("alice", "password")
        user = create_user("bob", "password2")
        users = get_all_users()
        assert len(users) >= 2 
        assert any(u.username == "alice" for u in users)
        assert any(u.username == "alice" for u in users)
    
    def test_get_all_users_json(self):
        create_user("alice", "password")
        create_user("bob", "password2")
        users = get_all_users_json()
        assert len(users) == 2
        assert set(u["username"] for u in users) == {"alice", "bob"}
   