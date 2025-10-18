from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

student_bp = Blueprint('student', __name__)

def is_student(app, user_id):
    result = app.supabase.table('users')\
        .select('role')\
        .eq('id', user_id)\
        .execute()
    
    if result.data and result.data[0]['role'] == 'student':
        return True
    return False

@student_bp.route('/available-exams', methods=['GET'])
@jwt_required()
def get_available_exams():
    try:
        current_user = get_jwt_identity()
        
        if not is_student(request.app, current_user['id']):
            return jsonify({'error': 'Student access required'}), 403
        
        # Get student's grade
        user_result = request.app.supabase.table('users')\
            .select('grade')\
            .eq('id', current_user['id'])\
            .execute()
        
        if not user_result.data:
            return jsonify({'error': 'Student not found'}), 404
        
        student_grade = user_result.data[0]['grade']
        
        # Get exams for student's grade that are published
        exams = request.app.supabase.table('exams')\
            .select('*, subjects(name), users(full_name)')\
            .eq('grade', student_grade)\
            .eq('is_published', True)\
            .execute()
        
        return jsonify({'exams': exams.data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/my-results', methods=['GET'])
@jwt_required()
def get_my_results():
    try:
        current_user = get_jwt_identity()
        
        if not is_student(request.app, current_user['id']):
            return jsonify({'error': 'Student access required'}), 403
        
        results = request.app.supabase.table('results')\
            .select('*, exams(title, subjects(name))')\
            .eq('student_id', current_user['id'])\
            .execute()
        
        return jsonify({'results': results.data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/start-exam/<exam_id>', methods=['POST'])
@jwt_required()
def start_exam(exam_id):
    try:
        current_user = get_jwt_identity()
        
        if not is_student(request.app, current_user['id']):
            return jsonify({'error': 'Student access required'}), 403
        
        # Check if student already attempted this exam
        existing_attempt = request.app.supabase.table('student_attempts')\
            .select('*')\
            .eq('student_id', current_user['id'])\
            .eq('exam_id', exam_id)\
            .execute()
        
        if existing_attempt.data:
            return jsonify({'error': 'You have already attempted this exam'}), 400
        
        # Create new attempt
        attempt_data = {
            'student_id': current_user['id'],
            'exam_id': exam_id,
            'start_time': datetime.now().isoformat(),
            'ip_address': request.remote_addr,
            'device_info': request.headers.get('User-Agent')
        }
        
        result = request.app.supabase.table('student_attempts').insert(attempt_data).execute()
        
        if result.data:
            return jsonify({
                'message': 'Exam started successfully',
                'attempt_id': result.data[0]['id']
            }), 201
        else:
            return jsonify({'error': 'Failed to start exam'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
