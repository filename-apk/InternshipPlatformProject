from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'role'
    }

    # This implementation uses joined-table inheritance.
    # Although all user types are treated as a single logical entity (User) in Python, SQLAlchemy creates a separate table for each subclass (e.g., student).
    # Each subclass table contains only the fields specific to that subtype and uses a primary key that is also a foreign key referencing the user table.
    # SQLAlchemy then performs joins between the base and child tables when loading subclass objects.
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'role': self.role
        }
