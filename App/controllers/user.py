from App.models import User, Student, Employer, Staff
from App.database import db

def create_user(self, username, password , role = "user"):
    newUser =  User (username=username, password = password)
    newUser.Role = role
    db.session.add(newUser)
    db.session.commit()
    return newUser

def login(self, username, password):
    user = user.query.filter_by(username =username).first()
    if user and user.check_password(password):
        return user
    return None 

def check_password(self, userID, password):
    user= User.query.get(userID)
    if not user: 
        return False
    return user.check_password(password)

def set_password(self, userID, newPassword):
    user = User.query.get(userID)
    if not user:
        return None
    user.set_password(newPassword)
    db.session.commit()
    return user

