from abc import ABC, abstractmethod

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


# Accepted State
class Accepted(ApplicationStatus):
    def viewShortlist(self):
        return

    def viewEmployerDecision(self):
        return


# Rejected State
class Rejected(ApplicationStatus):
    def viewShortlist(self):
        return

    def viewEmployerDecision(self):
        return


# Shortlisted State
class Shortlisted(ApplicationStatus):
    def viewShortlist(self):
        return

    def viewEmployerDecision(self):
        return


# Applied State
class Applied(ApplicationStatus):
    def viewShortlist(self):
        return

    def viewEmployerDecision(self):
        return