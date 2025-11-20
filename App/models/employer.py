from App.database import db
from .user import User

class Employer(User):
    __tablename__ = 'employer'

    employerID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(256), nullable=False)

    positions = db.relationship("Position", back_populates="createdBy", lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'employer'
    }

    def __init__(self, username, password, name, company):
        super().__init__(username, password)
        self.name = name
        self.company = company