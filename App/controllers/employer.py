from App.database import db
from App.models.employer import Employer
from App.models.student import Student
from App.models.shortlist import Shortlist, DecisionStatus
from App.models.position import Position, PositionStatus
from App.models.states import Accepted, Rejected

def create_employer(username, password, name, company):
    new_employer = Employer(username = username, password = password, name = name, company = company)
    db.session.add(new_employer)
    db.session.commit()
    return new_employer

def createPosition(title, employer, description, numberOfPositions):
    new_position = Position(employer = employer, title = title , description = description, numPositions = numberOfPositions)
    db.session.add(new_position)
    db.session.commit()
    return new_position

def viewApplicants(employerID, positionID):
    position = Position.query.filter_by(positionID = positionID).first()
    
    if not position or position.employerID != employerID:
        return None

    applicants = position.shortlist if position else [] 
    return applicants

def makeDecision(employerID, shortlistID, decision):
    shortlist = Shortlist.query.filter_by(shortlistID = shortlistID).first()
    if not shortlist:
        return None
    
    # Get the position to verify employer ownership
    position = Position.query.filter_by(positionID = shortlist.positionID).first()
    if not position or position.employerID != employerID:
        return None
    
    decision = decision.capitalize()

    if decision in ["Accepted", "Rejected"]:
        shortlist.update_status(decision)
        student = Student.query.filter_by(studentID = shortlist.studentID).first()

        if decision == "Accepted":
            student.changeStatus(Accepted)
        else:
            student.changeStatus(Rejected)
    
    db.session.commit()
    return shortlist

def editPosition(employerID, positionID, title, description, numberOfPositions, status):
    position = Position.query.get(positionID)
    if not position or position.employerID != employerID:
        return None
   
    if title:
        position.title = title

    if description:
        position.description = description

    if numberOfPositions:
        position.numberOfPositions = numberOfPositions

    if status and status in ["Open", "Closed"]:
        position.status = PositionStatus(status)
    
    db.session.commit()
    return position