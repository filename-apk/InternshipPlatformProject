from App.database import db 
from .states.accepted import Accepted
from states.rejected import Rejected
from .states.shortlisted import Shortlisted
from .states.applied import Applied
from .student import Student


STATUS_MAP = {
        "Applied": Applied, 
        "Shortlisted": Shortlisted, 
        "Accepted": Accepted, 
        "Rejected": Rejected
    }


class StudentController:

  

    @staticmethod
    def updateStatus(studentID, newStatus):

        if newStatus not in STATUS_MAP:
            return {"error": "Invalid status"}
        
        student = Student.query.filter_by(studentID =  studentID).first()
        if not student:
            return {"error": "Student not found"}
        
        student.status = newStatus

        StateClass = STATUS_MAP[newStatus]
        student.state = StateClass(student)

        db.session.commit()
