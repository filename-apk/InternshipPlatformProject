from App.database import db
from .user import User
from App.models.shortlist import Shortlist

class Staff(User):
    __tablename__ = 'staff'

    staffID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(256), nullable=False)

    shortlist = db.relationship("Shortlist", back_populates="staff", lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

    def __init__(self, username, password, name, faculty):
        super().__init__(username, password)
        self.name = name
        self.faculty = faculty

    # This method should be added to the staff controller

    # def add_to_shortlist(self, student_id, position_id):
    #     shortlist = Shortlist(student_id=student_id, position_id=position_id, staff_id=self.id)
    #     db.session.add(shortlist)
    #     db.session.commit()
    #     return shortlist