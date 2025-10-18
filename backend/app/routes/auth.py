from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'role', 'full_name', 'grade']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        existing_user = request.app.supabase.table('users')\
            .select('*')\
            .or_(f"username.eq.{data['username']},email.eq.{data['email']}")\
            .execute()
        
        if existing_user.data:
            return jsonify({'error': 'Username or email already exists'}), 400
        
        # Hash password
        hashed_password = hash_password(data['password'])
        
        # Create user
        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password_hash': hashed_password,
            'role': data['role'],
            'full_name': data['full_name'],
            'grade': data['grade'],
            'school_id': data.get('school_id'),
            'is_approved': data['role'] == 'student'  # Students auto-approved, teachers need admin approval
        }
        
        result = request.app.supabase.table('users').insert(user_data).execute()
        
        if result.data:
            return jsonify({
                'message': 'Registration successful. Please wait for admin approval.',
                'user_id': result.data[0]['id']
            }), 201
        else:
            return jsonify({'error': 'Registration failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Get user from database
        result = request.app.supabase.table('users')\
            .select('*')\
            .eq('username', data['username'])\
            .execute()
        
        if not result.data:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        user_data = result.data[0]
        
        # Check password
        if not check_password(data['password'], user_data['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if user is approved
        if not user_data['is_approved']:
            return jsonify({'error': 'Account pending admin approval'}), 403
        
        # Check if user is active
        if not user_data.get('is_active', True):
            return jsonify({'error': 'Account deactivated'}), 403
        
        # Create access token
        access_token = create_access_token(identity={
            'id': user_data['id'],
            'username': user_data['username'],
            'role': user_data['role']
        })
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'role': user_data['role'],
                'full_name': user_data['full_name'],
                'grade': user_data['grade'],
                'profile_picture_url': user_data.get('profile_picture_url')
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user = get_jwt_identity()
        
        result = request.app.supabase.table('users')\
            .select('*')\
            .eq('id', current_user['id'])\
            .execute()
        
        if not result.data:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = result.data[0]
        
        return jsonify({
            'user': {
                'id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'role': user_data['role'],
                'full_name': user_data['full_name'],
                'grade': user_data['grade'],
                'profile_picture_url': user_data.get('profile_picture_url'),
                'school_id': user_data.get('school_id')
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500