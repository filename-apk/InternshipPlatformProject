from App.models import Shortlist, Position, DecisionStatus, Student
from App.database import db

def get_shortlist_by_student(studentID):
    student = Student.query.filter_by(studentID = studentID).first()
    if not student:
        return[]
    return Shortlist.query.filter_by(studentID = studentID).all()

def get_shortlist_by_position(positionID):
    return Shortlist.query.filter_by(positionID = positionID).all()