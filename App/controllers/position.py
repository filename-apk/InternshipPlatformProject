from App.models import Position, Employer
from App.database import db


def getPositionsByERmployer(employerID):
    employer = Employer.query.filter_by(employerID = employerID).first()
    if not employer:
        return [] 
    
    return Position.query.filter_by(employerID = employerID).all()

def getAllPositions_json():
    positions =  Position.query.all()
    return [p.toJSON() for p in positions] if positions else[]


def getPositionsByEmployer_json(employerID):
    employer = Employer.query.filter_by(employerID = employerID).first()
    if not employer:
        return []
    positions = Position.query.filter_by(employerID = employerID).all()
    return[p.TOJSON() for p in positions] if positions else []