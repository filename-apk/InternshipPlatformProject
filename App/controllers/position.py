from App.models import Position, Employer
from App.database import db

def get_positions_by_employer(employerID):
    return db.session.query(Position).filter_by(employerID = employerID).all()

def get_all_positions_json():
    positions = Position.query.all()
    if positions:
        return [position.toJSON() for position in positions]
    return []

def get_positions_by_employer_json(employerID):
    positions = db.session.query(Position).filter_by(employerID = employerID).all()
    if positions:
        return [position.toJSON() for position in positions]
    return []

def delete_position(positionID):
    position = Position.query.get(positionID)
    if not position:
        return None
    db.session.delete(position)
    db.session.commit()
    return position