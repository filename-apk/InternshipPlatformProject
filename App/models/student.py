from App.database import db
from .user import User
from App.models.states import Accepted, Rejected, Shortlisted, Applied

class Student(User):
    __tablename__ = 'student'
    
    studentID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(256), nullable=False)
    resume = db.Column(db.String(256), nullable=False)
    GPA = db.Column(db.Float, nullable=False)

    # Reference to applicant state
    # Default state is Applied. This refers to a student who has applied to the intersnship programme
    status = None

    shortlist = db.relationship("Shortlist", back_populates="student", lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, password, name, degree, resume, GPA):
        super().__init__(username, password)
        self.name = name
        self.degree = degree
        self.resume = resume
        self.GPA = GPA
        self.changeStatus(Applied)

    def viewShortlist(self):
        self.status.viewShortlist()
    
    def viewEmployerDecision(self):
        self.status.viewEmployerDecision()

    def changeStatus(self, nextStatus):
        self.status = nextStatus(self)
        db.session.add(self)
        db.session.commit()