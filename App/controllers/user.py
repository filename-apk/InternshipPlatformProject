from App.models import User, Student, Employer, Staff
from App.database import db

def create_user(username, password):
    newUser =  User (username = username, password = password)
    db.session.add(newUser)
    db.session.commit()
    return newUser

def login(username, password):
    user = User.query.filter_by(username = username).first()
    if user and user.check_password(password):
        return user
    return None

def check_password(userID, password):
    user = User.query.get(userID)
    if not user: 
        return False
    return user.check_password(password)

def set_password(userID, newPassword):
    user = User.query.get(userID)
    if not user:
        return None
    user.set_password(newPassword)
    db.session.commit()
    return user

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if users:
        return [user.get_json() for user in users]
    return []