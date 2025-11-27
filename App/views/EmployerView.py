from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user as jwt_current_user

from App.controllers import create_employer, createPosition, viewApplicants, makeDecision, editPosition
from App.controllers.decorators import login_required
from App.models import Employer
from App.database import db

employer_views = Blueprint('employer_views', __name__)

# API Endpoints

@employer_views.route('/api/employer', methods=['POST'])
def create_employer_endpoint():
    data = request.json
    
    # Validate required fields
    if not data.get('username') or not data.get('password') or not data.get('name') or not data.get('company'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    employer = create_employer(data['username'], data['password'], data['name'], data['company'])
    return jsonify({'message': f"Employer {employer.username} created with ID {employer.id}"}), 201

@employer_views.route('/api/position', methods=['POST'])
@login_required(Employer)
def create_position_endpoint():
    data = request.json
    
    # Validate required fields
    if not data.get('title') or not data.get('description') or not data.get('numberOfPositions'):
        return jsonify({'error': 'Missing required fields: title, description, numberOfPositions'}), 400
    
    # Validate numberOfPositions is a positive integer
    try:
        num_positions = int(data['numberOfPositions'])
        if num_positions <= 0:
            return jsonify({'error': 'numberOfPositions must be a positive integer'}), 400
    except ValueError:
        return jsonify({'error': 'numberOfPositions must be a valid integer'}), 400
    
    # Create position with the current employer
    position = createPosition(
        title=data['title'],
        employer=jwt_current_user,  # Use the authenticated employer
        description=data['description'],
        numberOfPositions=num_positions
    )
    
    return jsonify({
        'message': f"Position '{position.title}' created with ID {position.positionID}",
        'position': {
            'id': position.positionID,
            'title': position.title,
            'description': position.description,
            'numberOfPositions': position.numberOfPositions
        }
    }), 201

@employer_views.route('/api/position/<int:position_id>/applicants', methods=['GET'])
@login_required(Employer)
def view_applicants_endpoint(position_id):
    # Get applicants for this position
    applicants = viewApplicants(jwt_current_user.id, position_id)
    
    if applicants is None:
        return jsonify({'error': 'Position not found or you do not have permission to view it'}), 404
    
    # Convert applicants to JSON
    applicants_json = [applicant.toJSON() for applicant in applicants]
    
    return jsonify({
        'position_id': position_id,
        'applicants': applicants_json,
        'count': len(applicants_json)
    }), 200

@employer_views.route('/api/shortlist/<int:shortlist_id>/decision', methods=['PUT'])
@login_required(Employer)
def make_decision_endpoint(shortlist_id):
    data = request.json
    
    # Validate decision field
    if not data.get('decision'):
        return jsonify({'error': 'Missing required field: decision'}), 400
    
    decision = data['decision']
    
    # Validate decision value
    if decision not in ['Accepted', 'Rejected', 'accepted', 'rejected']:
        return jsonify({'error': 'Invalid decision. Must be "Accepted" or "Rejected"'}), 400
    
    # Make the decision
    result = makeDecision(jwt_current_user.id, shortlist_id, decision)
    
    if result is None:
        return jsonify({'error': 'Shortlist entry not found or you do not have permission to make this decision'}), 404
    
    return jsonify({
        'message': f'Decision "{decision.capitalize()}" recorded for shortlist ID {shortlist_id}'
    }), 200

@employer_views.route('/api/position/<int:position_id>', methods=['PUT'])
@login_required(Employer)
def edit_position_endpoint(position_id):
    data = request.json
    
    # Validate at least one field is provided
    if not any([data.get('title'), data.get('description'), data.get('numberOfPositions'), data.get('status')]):
        return jsonify({'error': 'At least one field must be provided to update'}), 400
    
    # Validate numberOfPositions if provided
    num_positions = None
    if data.get('numberOfPositions'):
        try:
            num_positions = int(data['numberOfPositions'])
            if num_positions <= 0:
                return jsonify({'error': 'numberOfPositions must be a positive integer'}), 400
        except ValueError:
            return jsonify({'error': 'numberOfPositions must be a valid integer'}), 400
    
    # Validate status if provided
    status = data.get('status')
    if status and status not in ['Open', 'Closed']:
        return jsonify({'error': 'Invalid status. Must be "Open" or "Closed"'}), 400
    
    # Edit the position
    updated_position = editPosition(
        employerID=jwt_current_user.id,
        positionID=position_id,
        title=data.get('title'),
        description=data.get('description'),
        numberOfPositions=num_positions,
        status=status
    )
    
    if not updated_position:
        return jsonify({'error': 'Position not found or you do not have permission to edit it'}), 404
    
    return jsonify({
        'message': f'Position {position_id} updated successfully',
        'position': {
            'id': updated_position.positionID,
            'title': updated_position.title,
            'description': updated_position.description,
            'numberOfPositions': updated_position.numberOfPositions,
            'status': updated_position.status.value
        }
    }), 200