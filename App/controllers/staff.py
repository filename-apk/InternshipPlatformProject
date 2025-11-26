from App.database import db 
from App.models.shortlist import Shortlist 
from App.models.student import Student
from App.models.position import Position

def addToshortlist(positionID, studentID ):
    exists = Shortlist.query.filter_by(positionID = positionID, studentID= studentID).first()
    if exists: 
        return f"Student{studentID} is already shortlisted for position {positionID}"
    shortlist = Shortlist(positionID = positionID, studentID= studentID)
    db.session.add(shortlist)
    db.session.commit()

def viewAvailablePositions():
    return Position.query.all()




