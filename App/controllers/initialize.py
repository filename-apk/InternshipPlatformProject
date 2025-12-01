from .student import create_student
from .employer import create_employer, createPosition
from .staff import create_staff, addToshortlist
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    
    # Create users
    student = create_student('bob', 'bobpass', 'Bob Smith', 'Computer Science', 'trust_me_bro.pdf', 3.5)
    employer = create_employer('frank', 'frankpass', 'Frank Jones', 'Tech Corp')
    staff = create_staff('john', 'johnpass', 'John Doe', 'Engineering')
    
    # Create positions
    pos1 = createPosition('Software Engineer', employer, 'Full-stack developer position', 6)
    pos2 = createPosition('Mechanical Engineer', employer, 'Design and testing role', 6)
    
    # Add student to shortlist
    addToshortlist(pos1.positionID, student.studentID, staff.staffID)
