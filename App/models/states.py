from abc import ABC, abstractmethod
from .position import Position, PositionStatus
from .shortlist import DecisionStatus

# State Interface

class ApplicationStatus(ABC):
    def __init__(self, student):
        # Reference to the student context
        self.student = student

    @abstractmethod
    def viewShortlist(self):
        pass

    @abstractmethod
    def viewEmployerDecision(self):
        pass

# Applied State - Student has entered the system but not shortlisted. Unable to view shortlist or employer decision

class Applied(ApplicationStatus):
    def viewShortlist(self, choice):
        if not choice == 0:
            return "Invalid Choice For Applied State"
        
        result = [f"{self.student.name} Has Not Been Shortlisted For An Open Position"]
        
        # Sort By shortlistID In Descending Order (most recent first)
        shortlist_entrys = sorted(self.student.shortlist, key=lambda entry: entry.shortlistID, reverse=True)

        for entry in shortlist_entrys:
            position = entry.position
            if position.status == PositionStatus.closed:
                result.append(f"Position ID: {position.positionID} | Position Status: {position.status.value} | Title: {position.title} | Employer: {position.createdBy.name} | Company: {position.createdBy.company} | Description: {position.description} | Number of Interns Required: {position.numberOfPositions}")
        
        return result

    def viewEmployerDecision(self):
        return f"Unable To View Employer Decision. {self.student.name} Has Not Been Shortlisted For An Open Position"

# Shortlisted State
class Shortlisted(ApplicationStatus):
    def viewShortlist(self, choice):
        # Sort By shortlistID In Descending Order (most recent first)
        shortlist_entrys = sorted(self.student.shortlist, key=lambda entry: entry.shortlistID, reverse=True)
        shortlistedPositions = []

        if choice == 1:
            for entry in shortlist_entrys:
                position = entry.position
                if position.status == PositionStatus.open:
                    shortlistedPositions.append(f"Position ID: {position.positionID} | Position Status: {position.status.value} | Title: {position.title} | Employer: {position.createdBy.name} | Company: {position.createdBy.company} | Description: {position.description} | Number of Interns Required: {position.numberOfPositions}")
        
        if choice == 2:
            for entry in shortlist_entrys:
                position = entry.position
                if position.status == PositionStatus.closed:
                    shortlistedPositions.append(f"Position ID: {position.positionID} | Position Status: {position.status.value} | Title: {position.title} | Employer: {position.createdBy.name} | Company: {position.createdBy.company} | Description: {position.description} | Number of Interns Required: {position.numberOfPositions}")

        return shortlistedPositions

    def viewEmployerDecision(self):
        return f"Decision Pending. No Decision Has Been Made For {self.student.name}."

# Accepted State
class Accepted(ApplicationStatus):
    def viewShortlist(self, choice):
        return Shortlisted.viewShortlist(self, choice)

    def viewEmployerDecision(self):
        # Sort By shortlistID In Descending Order (most recent first)
        shortlist_entrys = sorted(self.student.shortlist, key=lambda entry: entry.shortlistID, reverse=True)
        shortlistedPositions = []
        
        # Display Open Positions Accepted For First
        for entry in shortlist_entrys:
            position = entry.position
            if entry.status == DecisionStatus.accepted and position.status == PositionStatus.open:
                shortlistedPositions.append(f"Position ID: {position.positionID} | Position Status: {position.status.value} | Title: {position.title} | Employer: {position.createdBy.name} | Company: {position.createdBy.company} | Description: {position.description} | Number of Interns Required: {position.numberOfPositions}")
        
        for entry in shortlist_entrys:
            position = entry.position
            if entry.status == DecisionStatus.rejected and position.status == PositionStatus.open:
                shortlistedPositions.append(f"Position ID: {position.positionID} | Position Status: {position.status.value} | Title: {position.title} | Employer: {position.createdBy.name} | Company: {position.createdBy.company} | Description: {position.description} | Number of Interns Required: {position.numberOfPositions}")
                
        return shortlistedPositions

# Rejected State
class Rejected(ApplicationStatus):
    def viewShortlist(self, choice):
        return Shortlisted.viewShortlist(self, choice)

    def viewEmployerDecision(self):
        # Sort By shortlistID In Descending Order (most recent first)
        shortlist_entrys = sorted(self.student.shortlist, key=lambda entry: entry.shortlistID, reverse=True)
        shortlistedPositions = []
        
        # Display Open Positions Rejected For First
        for entry in shortlist_entrys:
            position = entry.position
            if entry.status == DecisionStatus.rejected and position.status == PositionStatus.open:
                shortlistedPositions.append(f"Position ID: {position.positionID} | Position Status: {position.status.value} | Title: {position.title} | Employer: {position.createdBy.name} | Company: {position.createdBy.company} | Description: {position.description} | Number of Interns Required: {position.numberOfPositions}")
        
        for entry in shortlist_entrys:
            position = entry.position
            if entry.status == DecisionStatus.accepted and position.status == PositionStatus.open:
                shortlistedPositions.append(f"Position ID: {position.positionID} | Position Status: {position.status.value} | Title: {position.title} | Employer: {position.createdBy.name} | Company: {position.createdBy.company} | Description: {position.description} | Number of Interns Required: {position.numberOfPositions}")
                
        return shortlistedPositions