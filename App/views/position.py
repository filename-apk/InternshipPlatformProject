from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from App.controllers import (get_positions_by_employer_json, get_all_positions_json)
from App.controllers.decorators import login_required
from App.models import Staff

position_views = Blueprint('position_views', __name__)

# Get All Positions
@position_views.route('/api/positions/all', methods = ['GET'])
@login_required(Staff)
def get_all_positions():
    position_list = get_all_positions_json()
    return jsonify(position_list), 200
  
# Get All Positions For A Given Employer
@position_views.route('/api/employer/positions', methods=['GET'])
@login_required(Staff)
def get_employer_positions():
    return jsonify(get_positions_by_employer_json(current_user.id)), 200