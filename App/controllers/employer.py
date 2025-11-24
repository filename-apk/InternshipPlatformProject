from .employer import Employer
from App.database import db 
from .position import Position
from .status import DecisionStatus

def createPosition(title, employerID,  description, positionID,numberOfPositions):
    employer = Employer.query.filter_by(employerID = employerID).first()
    if not employer:
        return None
    position = Position(employerID = employerID, title = title , description = description, numberOfPositions = numberOfPositions)
    db.session.add(position)
    db.session.commit()

def viewApplicants(positionID):
    position = Position.query.filter_by(positionID = positionID).first()
    applicants = position.shortlist if position else [] 

    return applicants 


def makeDecision(shortlistID, status ):
    shortlist = shortlist.query.filter_by(shortlistID = shortlistID).first()
    if shortlist and status in ["Accepted", "Rejected", "Pending"]: 
        shortlist.status =  DecisionStatus(status.lower())
        db.session.commit()


