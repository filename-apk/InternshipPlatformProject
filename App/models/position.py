from App.database import db
from sqlalchemy import Enum
import enum

class PositionStatus(enum.Enum):
    open = "Open"
    closed = "Closed"

class Position(db.Model):
    __tablename__ = 'position'

    positionID = db.Column(db.Integer, primary_key=True)
    employerID = db.Column(db.Integer, db.ForeignKey('employer.employerID'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    numberOfPositions = db.Column(db.Integer, nullable=False)
    status = db.Column(Enum(PositionStatus, native_enum=False), nullable=False, default=PositionStatus.open)

    createdBy = db.relationship("Employer", back_populates="positions", lazy=True)
    shortlist = db.relationship("Shortlist", back_populates="position", lazy=True, cascade="all, delete-orphan")

    def __init__(self, employer, title, description, numPositions):
        self.createdBy = employer
        self.title = title
        self.description = description
        self.numberOfPositions = numPositions

    def update_status(self, status):
        self.status = PositionStatus(status)
        db.session.commit()
        return self.status

    def toJSON(self):
        return {
            "id": self.positionID,
            "title": self.title,
            "number_of_positions": self.numberOfPositions,
            "status": self.status.value,
            "description": self.description,
            "employer_id": self.employerID
        }