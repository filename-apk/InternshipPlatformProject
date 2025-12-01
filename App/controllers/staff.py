from App.database import db 
from App.models.shortlist import Shortlist 
from App.models.student import Student
from App.models.position import Position, PositionStatus
from App.models.staff import Staff
from App.models.states import Shortlisted

def create_staff(username, password, name, faculty):
    new_staff = Staff(username = username, password = password, name = name, faculty = faculty)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff

def addToshortlist(positionID, studentID, staffID):
    entry_exists = Shortlist.query.filter_by(positionID = positionID, studentID = studentID, staffID = staffID).first()
    if entry_exists:
        return f"Student{studentID} is already shortlisted for position {positionID}"
    
    student = Student.query.filter_by(studentID = studentID).first()
    if not student:
        return f"Student{studentID} does not exist"

    new_shortlist_entry = Shortlist(positionID = positionID, studentID = studentID, staffID = staffID)

    student.changeStatus(Shortlisted)
    db.session.add(new_shortlist_entry)
    db.session.commit()
    return new_shortlist_entry

def viewAvailablePositions():
    all_positions = sorted(Position.query.all(), key=lambda position: position.positionID, reverse=True)
    open_positions = []

    for position in all_positions:
        if position.status == PositionStatus.open:
            open_positions.append(position)

    return open_positions