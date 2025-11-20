from App.database import db
from .user import User
from sqlalchemy import Enum
import enum  

class DecisionStatus(enum.Enum):
    accepted = "Accepted"
    rejected = "Rejected"
    pending = "Pending"

class Shortlist(db.Model):
    __tablename__ = 'shortlist'

    shortlistID = db.Column(db.Integer, primary_key=True)
    positionID = db.Column(db.Integer, db.ForeignKey('position.positionID'))
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=False)
    status = db.Column(Enum(DecisionStatus, native_enum=False), nullable=False, default=DecisionStatus.pending)

    staff = db.relationship('Staff', back_populates='shortlist', lazy=True)
    student = db.relationship('Student', back_populates='shortlist', lazy=True)
    position = db.relationship('Position', back_populates='shortlist', lazy=True)

    def __init__(self, positionID, studentID, staffID):
        self.positionID = positionID
        self.studentID = studentID
        self.staffID = staffID
        
    def update_status(self, status):
        self.status = DecisionStatus(status)
        db.session.commit()
        return self.status

    # These two commented out methods should be added to the shortlist controller

    # def student_shortlist(self, student_id):
    #     return db.session.query(Shortlist).filter_by(student_id=student_id).all()

    # def position_shortlist(self, position_id):
    #     return db.session.query(Shortlist).filter_by(position_id=position_id).all()
        
    def toJSON(self):
        return{
            "id": self.shortlistID,
            "title": self.title,
            "student_id": self.studentID,
            "position_id": self.positionID,
            "staff_id": self.staffID,
            "status": self.status.value
        }
      