
from App.database import db 
from App.models.student import Student
from App.models.shortlist import Shortlist
from App.models.states import Accepted, Rejected, Applied, Shortlisted 


def viewShortlist(studentID):
    student = Student.query.filter_by(studentID=studentID).first()
    entries = student.shortlist if student else []

    return{ 
        "studentID" : studentID, 
        "shortlist": [
            {
                "shortlistID" : s.shortlistID, 
                "positionID": s.positionID, 
                "status": s.status.value}
                for s in entries] 
            
        
    }

def updateStatus(studentID, state): 
    student = Student.query.filter_by(studentID = studentID).first()

    if not student:
        return None
    
    if student and state:
      
       mapping = {
           "Accepted": Accepted, 
           "Rejected": Rejected, 
           "Shortlisted": Shortlisted, 
           "Applied" : Applied
       }

       if state in mapping:
           student.changeStatus(mapping[state])
          

    db.session.commit()


def viewEmployerDecision( studentID):
    return Shortlist.query.filter_by(studentID = studentID).all()
    

