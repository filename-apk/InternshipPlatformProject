from App.database import db 
from App.models.student import Student
from App.models.shortlist import Shortlist
from App.models.states import Accepted, Rejected, Applied, Shortlisted

def create_student(username, password, name, degree, resume, GPA):
    new_student = Student(username = username, password = password, name = name, degree = degree, resume = resume, GPA = GPA)
    db.session.add(new_student)
    db.session.commit()
    return new_student

def viewShortlist(student, choice):
    return student.status.viewShortlist(choice)

def viewEmployerDecision(student):
    return student.status.viewEmployerDecision()