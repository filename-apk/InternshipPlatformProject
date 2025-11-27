from App.database import db
from .user import User
from App.models.states import Accepted, Rejected, Shortlisted, Applied
from sqlalchemy import orm

class Student(User):
    __tablename__ = 'student'
    
    studentID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(256), nullable=False)
    resume = db.Column(db.String(256), nullable=False)
    GPA = db.Column(db.Float, nullable=False)
    status_name = db.Column(db.String(50), default='Applied')
    
    # Reference to applicant state
    # Default state is Applied. This refers to a student who has applied to the intersnship programme
    status = None

    @orm.reconstructor
    def init_on_load(self):
        mapping = {
            "Accepted": Accepted,
            "Rejected": Rejected,
            "Shortlisted": Shortlisted,
            "Applied": Applied
        }
        if self.status_name in mapping:
            self.status = mapping[self.status_name](self)
        else:
            self.status = Applied(self)

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

    def changeStatus(self, nextStatus):
        self.status = nextStatus(self)
        self.status_name = nextStatus.__name__
        db.session.add(self)
        db.session.commit()