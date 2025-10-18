from flask import Blueprint, jsonify

test_bp = Blueprint('test', __name__)

@test_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running"})

@test_bp.route('/test-subjects', methods=['GET'])
def test_subjects():
    return jsonify({"subjects": [
        {"id": 1, "name": "Mathematics"},
        {"id": 2, "name": "Chemistry"}, 
        {"id": 3, "name": "Biology"},
        {"id": 4, "name": "Physics"},
        {"id": 5, "name": "English"}
    ]})
