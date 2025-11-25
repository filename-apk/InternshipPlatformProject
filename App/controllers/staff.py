from App.database import db 
from App.models.shortlist import Shortlist 
from App.models.student import Student
from App.models.position import Position

def addToshortlist( positionID, studentID ):
    exists = Shortlist.query.filter_by(positionID = positionID, studentID= studentID).first()
    if exists: 
        return{"message": "Student already shortlisted for this position"}
    shortlist = Shortlist(positionID = positionID, studentID= studentID)
    db.session.add(shortlist)
    db.session.commit()

def viewAvailablePositions(self):
    return Position.query.all()




