from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from datetime import datetime

exams_bp = Blueprint('exams', __name__)

@exams_bp.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        result = current_app.supabase.table('subjects').select('*').execute()
        return jsonify({'subjects': result.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exams_bp.route('/questions/<exam_id>', methods=['GET'])
@jwt_required()
def get_exam_questions(exam_id):
    try:
        current_user = get_jwt_identity()
        
        # Verify the user has access to this exam
        if current_user['role'] == 'student':
            # Check if student has started this exam
            attempt_result = current_app.supabase.table('student_attempts')\
                .select('*')\
                .eq('student_id', current_user['id'])\
                .eq('exam_id', exam_id)\
                .execute()
            
            if not attempt_result.data:
                return jsonify({'error': 'Exam not started or access denied'}), 403
        
        # Get questions
        questions_result = current_app.supabase.table('questions')\
            .select('*')\
            .eq('exam_id', exam_id)\
            .order('sequence_number')\
            .execute()
        
        # Parse matching pairs from JSON string
        questions = []
        for question in questions_result.data:
            if question.get('matching_pairs'):
                try:
                    question['matching_pairs'] = json.loads(question['matching_pairs'])
                except:
                    question['matching_pairs'] = None
            questions.append(question)
        
        return jsonify({'questions': questions}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exams_bp.route('/submit-answer', methods=['POST'])
@jwt_required()
def submit_answer():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['attempt_id', 'question_id', 'answer_text']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Verify the attempt belongs to the student
        if current_user['role'] == 'student':
            attempt_result = current_app.supabase.table('student_attempts')\
                .select('*')\
                .eq('id', data['attempt_id'])\
                .eq('student_id', current_user['id'])\
                .execute()
            
            if not attempt_result.data:
                return jsonify({'error': 'Invalid attempt'}), 403
        
        answer_data = {
            'attempt_id': data['attempt_id'],
            'question_id': data['question_id'],
            'answer_text': data['answer_text'],
            'is_flagged': data.get('is_flagged', False)
        }
        
        # Check if answer already exists
        existing_answer = current_app.supabase.table('student_answers')\
            .select('*')\
            .eq('attempt_id', data['attempt_id'])\
            .eq('question_id', data['question_id'])\
            .execute()
        
        if existing_answer.data:
            # Update existing answer
            result = current_app.supabase.table('student_answers')\
                .update(answer_data)\
                .eq('id', existing_answer.data[0]['id'])\
                .execute()
        else:
            # Create new answer
            result = current_app.supabase.table('student_answers').insert(answer_data).execute()
        
        if result.data:
            return jsonify({'message': 'Answer submitted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to submit answer'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exams_bp.route('/submit-exam', methods=['POST'])
@jwt_required()
def submit_exam():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if 'attempt_id' not in data:
            return jsonify({'error': 'Missing attempt_id'}), 400
        
        # Verify the attempt belongs to the student
        attempt_result = current_app.supabase.table('student_attempts')\
            .select('*')\
            .eq('id', data['attempt_id'])\
            .eq('student_id', current_user['id'])\
            .execute()
        
        if not attempt_result.data:
            return jsonify({'error': 'Invalid attempt'}), 403
        
        # Calculate score (this is a simplified version)
        answers_result = current_app.supabase.table('student_answers')\
            .select('*, questions(correct_answer, marks)')\
            .eq('attempt_id', data['attempt_id'])\
            .execute()
        
        total_score = 0
        total_marks = 0
        
        for answer in answers_result.data:
            question_data = answer.get('questions', {})
            if answer['answer_text'] == question_data.get('correct_answer'):
                marks = question_data.get('marks', 1)
                total_score += marks
                
                # Update answer with correctness
                current_app.supabase.table('student_answers')\
                    .update({'is_correct': True, 'marks_obtained': marks})\
                    .eq('id', answer['id'])\
                    .execute()
            
            total_marks += question_data.get('marks', 1)
        
        percentage = (total_score / total_marks * 100) if total_marks > 0 else 0
        
        # Update attempt
        current_app.supabase.table('student_attempts')\
            .update({
                'is_submitted': True,
                'end_time': datetime.now().isoformat(),
                'total_score': total_score
            })\
            .eq('id', data['attempt_id'])\
            .execute()
        
        # Create result record
        attempt_data = attempt_result.data[0]
        result_data = {
            'attempt_id': data['attempt_id'],
            'student_id': current_user['id'],
            'exam_id': attempt_data['exam_id'],
            'total_marks_obtained': total_score,
            'percentage': percentage,
            'grade': calculate_grade(percentage),
            'submitted_at': datetime.now().isoformat()
        }
        
        result = current_app.supabase.table('results').insert(result_data).execute()
        
        if result.data:
            return jsonify({
                'message': 'Exam submitted successfully',
                'score': total_score,
                'percentage': percentage,
                'grade': calculate_grade(percentage)
            }), 200
        else:
            return jsonify({'error': 'Failed to submit exam'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'
