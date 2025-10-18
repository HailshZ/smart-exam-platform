from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

teacher_bp = Blueprint('teacher', __name__)

def is_teacher(app, user_id):
    result = app.supabase.table('users')\
        .select('role')\
        .eq('id', user_id)\
        .execute()
    
    if result.data and result.data[0]['role'] == 'teacher':
        return True
    return False

@teacher_bp.route('/exams', methods=['GET'])
@jwt_required()
def get_teacher_exams():
    try:
        current_user = get_jwt_identity()
        
        if not is_teacher(request.app, current_user['id']):
            return jsonify({'error': 'Teacher access required'}), 403
        
        result = request.app.supabase.table('exams')\
            .select('*, subjects(name)')\
            .eq('teacher_id', current_user['id'])\
            .execute()
        
        return jsonify({'exams': result.data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teacher_bp.route('/create-exam', methods=['POST'])
@jwt_required()
def create_exam():
    try:
        current_user = get_jwt_identity()
        
        if not is_teacher(request.app, current_user['id']):
            return jsonify({'error': 'Teacher access required'}), 403
        
        data = request.get_json()
        
        required_fields = ['title', 'subject_id', 'grade', 'duration_minutes', 'total_marks']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        exam_data = {
            'title': data['title'],
            'subject_id': data['subject_id'],
            'teacher_id': current_user['id'],
            'grade': data['grade'],
            'duration_minutes': data['duration_minutes'],
            'total_marks': data['total_marks'],
            'instructions': data.get('instructions', ''),
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time')
        }
        
        result = request.app.supabase.table('exams').insert(exam_data).execute()
        
        if result.data:
            return jsonify({
                'message': 'Exam created successfully',
                'exam_id': result.data[0]['id']
            }), 201
        else:
            return jsonify({'error': 'Failed to create exam'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teacher_bp.route('/add-question/<exam_id>', methods=['POST'])
@jwt_required()
def add_question(exam_id):
    try:
        current_user = get_jwt_identity()
        
        if not is_teacher(request.app, current_user['id']):
            return jsonify({'error': 'Teacher access required'}), 403
        
        # Verify exam belongs to teacher
        exam_result = request.app.supabase.table('exams')\
            .select('*')\
            .eq('id', exam_id)\
            .eq('teacher_id', current_user['id'])\
            .execute()
        
        if not exam_result.data:
            return jsonify({'error': 'Exam not found or access denied'}), 404
        
        data = request.get_json()
        
        required_fields = ['question_type', 'marks']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        question_data = {
            'exam_id': exam_id,
            'question_type': data['question_type'],
            'question_text': data.get('question_text'),
            'image_url': data.get('image_url'),
            'option_a': data.get('option_a'),
            'option_b': data.get('option_b'),
            'option_c': data.get('option_c'),
            'option_d': data.get('option_d'),
            'correct_answer': data.get('correct_answer'),
            'matching_pairs': json.dumps(data.get('matching_pairs')) if data.get('matching_pairs') else None,
            'marks': data['marks'],
            'sequence_number': data.get('sequence_number', 0)
        }
        
        result = request.app.supabase.table('questions').insert(question_data).execute()
        
        if result.data:
            return jsonify({
                'message': 'Question added successfully',
                'question_id': result.data[0]['id']
            }), 201
        else:
            return jsonify({'error': 'Failed to add question'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teacher_bp.route('/exam-results/<exam_id>', methods=['GET'])
@jwt_required()
def get_exam_results(exam_id):
    try:
        current_user = get_jwt_identity()
        
        if not is_teacher(request.app, current_user['id']):
            return jsonify({'error': 'Teacher access required'}), 403
        
        # Verify exam belongs to teacher
        exam_result = request.app.supabase.table('exams')\
            .select('*')\
            .eq('id', exam_id)\
            .eq('teacher_id', current_user['id'])\
            .execute()
        
        if not exam_result.data:
            return jsonify({'error': 'Exam not found or access denied'}), 404
        
        # Get results with student information
        results = request.app.supabase.table('results')\
            .select('*, users(full_name, username, grade), student_attempts(start_time, end_time)')\
            .eq('exam_id', exam_id)\
            .execute()
        
        return jsonify({'results': results.data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
