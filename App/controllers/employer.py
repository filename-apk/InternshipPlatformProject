from App.models.employer import Employer
from App.database import db 
from App.models.shortlist import Shortlist
from App.models.position import Position
from App.models.position import PositionStatus
from App.models.shortlist import DecisionStatus

def createPosition(title, employerID, description,numberOfPositions):
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
    shortlist = Shortlist.query.filter_by(shortlistID = shortlistID).first()
    if shortlist and status in ["Accepted", "Rejected", "Pending"]: 
        shortlist.status =  DecisionStatus(status.lower())
        db.session.commit()

def editPosition( employerID, positionID, title, description, numberOfPositions, shortlistID):
    position = Position.query.get(positionID)
    shortlist = Shortlist.query.get(shortlistID)
    if not position or position.employerID  != employerID:
        return None
    if not shortlist:
        return None
  

   
    if title:
        position.title = title
    if description:
        position.description = description 
    if numberOfPositions:
        position.numberOfPositions = numberOfPositions

    allShortlist = Shortlist.query.filter_by(positonID = positionID).all()

    accepted = sum( 1 for s in allShortlist if s.status == DecisionStatus.accepted)

    if accepted >= position.numberOfPositions:
        position.status = PositionStatus.closed
    else:
          position.status = PositionStatus.open
    
    
    db.session.commit()
    return position