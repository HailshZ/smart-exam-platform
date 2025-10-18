from datetime import datetime
import uuid

class User:
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.role = user_data.get('role')
        self.full_name = user_data.get('full_name')
        self.grade = user_data.get('grade')
        self.school_id = user_data.get('school_id')
        self.profile_picture_url = user_data.get('profile_picture_url')
        self.is_approved = user_data.get('is_approved', False)
        self.is_active = user_data.get('is_active', True)
        self.created_at = user_data.get('created_at')

class Exam:
    def __init__(self, exam_data):
        self.id = exam_data.get('id')
        self.title = exam_data.get('title')
        self.subject_id = exam_data.get('subject_id')
        self.teacher_id = exam_data.get('teacher_id')
        self.grade = exam_data.get('grade')
        self.duration_minutes = exam_data.get('duration_minutes')
        self.total_marks = exam_data.get('total_marks')
        self.instructions = exam_data.get('instructions')
        self.start_time = exam_data.get('start_time')
        self.end_time = exam_data.get('end_time')
        self.is_published = exam_data.get('is_published', False)
        self.created_at = exam_data.get('created_at')

class Question:
    def __init__(self, question_data):
        self.id = question_data.get('id')
        self.exam_id = question_data.get('exam_id')
        self.question_type = question_data.get('question_type')
        self.question_text = question_data.get('question_text')
        self.image_url = question_data.get('image_url')
        self.option_a = question_data.get('option_a')
        self.option_b = question_data.get('option_b')
        self.option_c = question_data.get('option_c')
        self.option_d = question_data.get('option_d')
        self.correct_answer = question_data.get('correct_answer')
        self.matching_pairs = question_data.get('matching_pairs')
        self.marks = question_data.get('marks', 1)
        self.sequence_number = question_data.get('sequence_number')
