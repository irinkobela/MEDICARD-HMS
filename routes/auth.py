from flask import Blueprint, request, jsonify # type: ignore
from models.models import User # type: ignore
from extensions import db
import jwt # type: ignore
from datetime import datetime, timedelta
from functools import wraps
import os
from schemas import UserSchema
from marshmallow import ValidationError # type: ignore

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()

def get_token_expiry():
    return datetime.utcnow() + timedelta(days=1)

def create_token(user):
    return jwt.encode({
        'user_id': user.id,
        'exp': get_token_expiry(),
        'role': user.role
    }, os.environ.get('SECRET_KEY'))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            if not token.startswith('Bearer '):
                raise jwt.InvalidTokenError('Invalid token format')
            token = token.split('Bearer ')[1]
            data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                raise jwt.InvalidTokenError('User not found')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'message': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
           
        # Validate and deserialize input
        user = user_schema.load(json_data)
        
        # Check for existing username/email
        if User.query.filter_by(username=user.username).first():
            return jsonify({'message': 'Username already exists'}), 409
           
        if User.query.filter_by(email=user.email).first():
            return jsonify({'message': 'Email already exists'}), 409
       
        # Set password (this will hash it)
        user.set_password(json_data['password'])
        user.role = json_data.get('role', 'user')  # Default role
       
        db.session.add(user)
        db.session.commit()
        
        # Create response without password hash
        result = user_schema.dump(user)
        return jsonify({
            'message': 'User created successfully',
            'user': result
        }), 201
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        json_data = request.get_json()
        if not all(k in json_data for k in ('username', 'password')):
            return jsonify({'message': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=json_data['username']).first()
        
        if not user or not user.check_password(json_data['password']):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        token = create_token(user)
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 200
    except Exception as e:
        return jsonify({'message': 'Error logging in', 'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role
    }), 200
