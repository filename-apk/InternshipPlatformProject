from .user import create_user
from .staff import addToshortlist
from .employer import createPosition
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', "student")
    create_user('frank', 'frankpass', "employer")
    create_user('john', 'johnpass', "staff")
    createPosition( title='Software Engineer', employerID = 2, description = ' ', positionID = 4 , number_of_positions= 6)
    createPosition( title='Web Designer', employerID = 2, description = ' ', positionID = 5 , number_of_positions= 6)
   
    addToshortlist(1, 1, 3)
