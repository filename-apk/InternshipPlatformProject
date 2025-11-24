from App.database import db 
from .staff import Staff
from .shortlist import Shortlist 
from .student import Student

def addToshortlist(staffID, positionID,studentID ):
    exists = Shortlist.query.filter_by(positionID = positionID, studentID= studentID).first()

    if exists: 
        return{"message": "Student already shortlisted for this position"}
    shortlist = Shortlist(positionID = positionID, studentID= studentID)
    db.session.add(shortlist)
    db.session.commit()



