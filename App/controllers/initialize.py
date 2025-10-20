from .user import create_user
from .shortlist import add_student_to_shortlist
from .position import open_position
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', "student")
    create_user('frank', 'frankpass', "employer")
    create_user('john', 'johnpass', "staff")
    open_position('Software Engineer', 2, 5)
    add_student_to_shortlist(1, 1, 1)
