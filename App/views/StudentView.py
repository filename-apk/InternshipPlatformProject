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
    return jsonify({
        'message': f"Student {student.username} created with ID {student.id}",
        'student': {
            'id': student.id,
            'username': student.username,
            'name': student.name,
            'degree': student.degree,
            'resume': student.resume,
            'GPA': student.GPA
        }
    }), 201

@student_views.route('/api/student/shortlist', methods=['GET'])
@login_required(Student)
def view_shortlisted_positions_endpoint():
    choice = request.args.get('choice', type=int)

    if choice is None:
        return jsonify({'error':'Missing required field: choice'}), 400
    
    # 0 - Returns Closed Positions If Any (For Applied State Only)
    # 1 - View Open Positions (Shortlisted, Accepted and Rejected State Only)
    # 2 - View Closed Positions & Their Status (Shortlisted, Accepted and Rejected State Only)

    shortlisedFor = viewShortlist(jwt_current_user, choice)
    return jsonify({'message': shortlisedFor}), 200

@student_views.route('/api/student/decision', methods=['GET'])
@login_required(Student)
def view_employer_decision_endpoint():
    employerDecision = viewEmployerDecision(jwt_current_user)
    return jsonify({'message': employerDecision}), 200