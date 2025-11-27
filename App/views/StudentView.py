from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user as jwt_current_user

from App.controllers import create_student, viewShortlist, viewEmployerDecision

from App.controllers.decorators import login_required
from App.models import Student
from App.database import db

student_views = Blueprint('student_views', __name__)

# API Endpoints

@student_views.route('/api/student', methods=['POST'])
def create_student_endpoint():
    data = request.json

    # Validate required fields
    if not data.get('username') or not data.get('password') or not data.get('name') or not data.get('degree') or not data.get('resume') or not data.get('GPA'):
        return jsonify({'error': 'Missing required fields: username, password, name, degree, resume, GPA'}), 400

    student = create_student(data['username'], data['password'], data['name'], data['degree'], data['resume'], data['GPA'])
    return jsonify({'message': f"Student {student.username} created with ID {student.id}"}), 201

# TO DO: Implement viewShortlist and viewEmployerDecision; Requires state logic to be implemented first

