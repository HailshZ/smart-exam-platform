from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__)

def is_admin(app, user_id):
    result = app.supabase.table('users')\
        .select('role')\
        .eq('id', user_id)\
        .execute()
    
    if result.data and result.data[0]['role'] == 'admin':
        return True
    return False

@admin_bp.route('/pending-users', methods=['GET'])
@jwt_required()
def get_pending_users():
    try:
        current_user = get_jwt_identity()
        
        if not is_admin(request.app, current_user['id']):
            return jsonify({'error': 'Admin access required'}), 403
        
        result = request.app.supabase.table('users')\
            .select('*')\
            .eq('is_approved', False)\
            .execute()
        
        return jsonify({'pending_users': result.data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/approve-user/<user_id>', methods=['POST'])
@jwt_required()
def approve_user(user_id):
    try:
        current_user = get_jwt_identity()
        
        if not is_admin(request.app, current_user['id']):
            return jsonify({'error': 'Admin access required'}), 403
        
        result = request.app.supabase.table('users')\
            .update({'is_approved': True})\
            .eq('id', user_id)\
            .execute()
        
        if result.data:
            return jsonify({'message': 'User approved successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        current_user = get_jwt_identity()
        
        if not is_admin(request.app, current_user['id']):
            return jsonify({'error': 'Admin access required'}), 403
        
        result = request.app.supabase.table('users')\
            .select('*')\
            .execute()
        
        return jsonify({'users': result.data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        current_user = get_jwt_identity()
        
        if not is_admin(request.app, current_user['id']):
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get counts
        users_count = request.app.supabase.table('users').select('*', count='exact').execute()
        exams_count = request.app.supabase.table('exams').select('*', count='exact').execute()
        pending_count = request.app.supabase.table('users').select('*', count='exact').eq('is_approved', False).execute()
        
        return jsonify({
            'total_users': users_count.count,
            'total_exams': exams_count.count,
            'pending_approvals': pending_count.count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
