from App.database import db 
from App.models.shortlist import Shortlist 
from App.models.student import Student
from App.models.position import Position
from App.models.staff import Staff

def create_staff(username, password, name, faculty):
    new_staff = Staff(username = username, password = password, name = name, faculty = faculty)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff

def addToshortlist(positionID, studentID, staffID):
    entry_exists = Shortlist.query.filter_by(positionID = positionID, studentID = studentID, staffID = staffID).first()

    if entry_exists:
        return f"Student{studentID} is already shortlisted for position {positionID}"

    new_shortlist_entry = Shortlist(positionID = positionID, studentID = studentID, staffID = staffID)
    db.session.add(new_shortlist_entry)
    db.session.commit()
    return new_shortlist_entry

def viewAvailablePositions():
    return Position.query.all()