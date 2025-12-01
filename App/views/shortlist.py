from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user as jwt_current_user

from App.controllers import get_shortlist_by_student, get_shortlist_by_position
from App.controllers.decorators import login_required
from App.models import Student, Employer, Staff

shortlist_views = Blueprint('shortlist_views', __name__)

# API Endpoints

@shortlist_views.route('/api/shortlist/student/<int:student_id>', methods=['GET'])
@login_required(Staff)
def get_student_shortlist(student_id):
    # Ensure students can only view their own shortlist
    if jwt_current_user.id != student_id:
        return jsonify({"error": "Unauthorized - You can only view your own shortlist"}), 403
    
    shortlists = get_shortlist_by_student(student_id)
    
    return jsonify([s.toJSON() for s in shortlists]), 200

@shortlist_views.route('/api/shortlist/position/<int:position_id>', methods=['GET'])
@login_required(Staff)
def get_position_shortlist(position_id):
    shortlists = get_shortlist_by_position(position_id)
    return jsonify([s.toJSON() for s in shortlists]), 200 
     