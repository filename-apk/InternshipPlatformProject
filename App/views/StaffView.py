from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user as jwt_current_user

from App.controllers import create_staff, addToshortlist, viewAvailablePositions
from App.controllers.decorators import login_required
from App.models import Staff
from App.database import db

staff_views = Blueprint('staff_views', __name__)

# API Endpoints

@staff_views.route('/api/staff', methods=['POST'])
def create_staff_endpoint():
    data = request.json
    
    # Validate required fields
    if not data.get('username') or not data.get('password') or not data.get('name') or not data.get('faculty'):
        return jsonify({'error': 'Missing required fields: username, password, name, faculty'}), 400
    
    staff = create_staff(data['username'], data['password'], data['name'], data['faculty'])
    return jsonify({
        'message': f"Staff member {staff.username} created with ID {staff.id}",
        'staff': {
            'id': staff.id,
            'username': staff.username,
            'name': staff.name,
            'faculty': staff.faculty
        }
    }), 201

@staff_views.route('/api/shortlist', methods=['POST'])
@login_required(Staff)
def add_to_shortlist_endpoint():
    data = request.json
    
    # Validate required fields
    if not data.get('positionID') or not data.get('studentID'):
        return jsonify({'error': 'Missing required fields: positionID, studentID'}), 400
    
    # Validate IDs are integers
    try:
        position_id = int(data['positionID'])
        student_id = int(data['studentID'])
    except ValueError:
        return jsonify({'error': 'positionID and studentID must be valid integers'}), 400
    
    # Add student to shortlist
    result = addToshortlist(position_id, student_id, jwt_current_user.id)
    
    # Check if result is an error message (string) returned from controller method
    if isinstance(result, str):
        return jsonify({'error': result}), 400
    
    return jsonify({
        'message': f'Student {student_id} added to shortlist for position {position_id}',
        'shortlist': {
            'id': result.shortlistID,
            'positionID': result.positionID,
            'studentID': result.studentID,
            'staffID': result.staffID,
            'status': result.status.value
        }
    }), 201

@staff_views.route('/api/positions/available', methods=['GET'])
@login_required(Staff)
def view_available_positions_endpoint():
    positions = viewAvailablePositions()
    
    # Check if positions list is empty
    if not positions:
        return jsonify({'message': 'No positions available'}), 404
    
    # Convert positions to JSON
    positions_json = [position.toJSON() for position in positions]
    
    return jsonify({
        'positions': positions_json,
        'count': len(positions_json)
    }), 200
