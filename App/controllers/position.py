from App.models import Position, Employer
from App.database import db

def open_position(title, employer_id, number):
    employer = db.session.query(Employer).filter_by(id=employer_id).first()
    if employer:
        new_position = Position(title=title, employer_id=employer_id, number=number)
        db.session.add(new_position)
        db.session.commit()
        return new_position
    return False

def get_positions_by_employer(employer_id):
    return db.session.query(Position).filter_by(employer_id=employer_id).all()

def get_all_positions_json():
    positions = Position.query.all()
    if positions:
        return [position.toJSON() for position in positions]
    return []

def get_positions_by_employer_json(employer_id):
    positions = db.session.query(Position).filter_by(employer_id=employer_id).all()
    if positions:
        return [position.toJSON() for position in positions]
    return []