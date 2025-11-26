
from App.models import Shortlist, Position, DecisionStatus, Student
from App.database import db


def shortlistedStudent(studentID):
    student = Student.query.filter_by(studentID = studentID).first()
    if not student:
        return[ ]
    return Shortlist.query.filter_by(studentID =studentID).all()


def shortlistedByPosition(positionID):
    return Shortlist.query.filter_by(positionID = positionID).all()


def decideShortlist(studentID, positionID, decision):
    student = Student.query.filter_by(studentID = studentID).first()
    if not student:
        return False 
    
    shortlist = Shortlist.query.filter_by(studentID= studentID, positionID = positionID,status = DecisionStatus.pending ).first()
    if not shortlist:
        return False 
    
    position = Position.query.filter_by(positionID = positionID).first()
    if not position or position.numberOfPositions <= 0:
        return False
    

    shortlist.update_status(decision)

    if decision == "accepted":
        position.update_number_of_positions(position.numberOfPositions -1)
    
    return shortlist