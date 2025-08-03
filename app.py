from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, LoginSession

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Use environment variable for secret key, fallback to a default for development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Enable CORS for cross-origin requests
CORS(app)

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    # Add some default users if they don't exist
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', password_hash=generate_password_hash('Admin123!'), role='admin')
        db.session.add(admin_user)
    
    if not User.query.filter_by(username='Ebinbijuu').first():
        ebinbijuu_user = User(username='Ebinbijuu', password_hash=generate_password_hash('Lopmop12@'), role='admin')
        db.session.add(ebinbijuu_user)
    
    if not User.query.filter_by(username='user1').first():
        user1 = User(username='user1', password_hash=generate_password_hash('password123'), role='user')
        db.session.add(user1)
    
    db.session.commit()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        'message': 'Secure Web API is running',
        'endpoints': {
            'login': '/login (POST)',
            'register': '/register (POST)', 
            'verify': '/verify (POST)',
            'health': '/health (GET)',
            'users': '/users (GET) - Admin only'
        }
    }), 200

@app.route('/login', methods=['POST'])
def login():
    try:
        # Check if request has JSON content
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Validate input
        if not username or not password:
            return jsonify({'error': 'Username and password cannot be empty'}), 400
        
        # Check if user exists and password is correct
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Check password using bcrypt
        if not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Update last login time
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        payload = {
            'user': username,
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # 24 hours
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Store session in database
        session = LoginSession(
            user_id=user.id,
            token=token,
            expires_at=datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        )
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'token': token,
            'user': username,
            'user_id': user.id,
            'role': user.role,
            'expires_in': 86400  # 24 hours in seconds
        }), 200
        
    except jwt.PyJWTError as e:
        return jsonify({'error': 'Token generation failed'}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/register', methods=['POST'])
def register():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username'].strip()
        password = data['password']
        email = data.get('email', '').strip() if data.get('email') else None
        
        if not username or not password:
            return jsonify({'error': 'Username and password cannot be empty'}), 400
        
        # Enhanced password validation
        errors = []
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        
        if not any(c.isupper() for c in password):
            errors.append('Password must contain at least 1 uppercase letter')
        
        if not any(c.islower() for c in password):
            errors.append('Password must contain at least 1 lowercase letter')
        
        if not any(c.isdigit() for c in password):
            errors.append('Password must contain at least 1 number')
        
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            errors.append('Password must contain at least 1 special character (!@#$%^&*()_+-=[]{}|;:,.<>?)')
        
        if errors:
            return jsonify({'error': 'Password requirements not met', 'details': errors}), 400
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        # Check if email already exists (if provided)
        if email and User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create new user
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            email=email
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/verify', methods=['POST'])
def verify_token():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({'error': 'Token is required'}), 400
        
        token = data['token']
        
        # Verify and decode token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Check if session exists in database
        session = LoginSession.query.filter_by(
            token=token,
            is_active=True
        ).first()
        
        if not session:
            return jsonify({'error': 'Session not found or inactive'}), 401
        
        # Check if session has expired
        if session.expires_at < datetime.datetime.utcnow():
            session.is_active = False
            db.session.commit()
            return jsonify({'error': 'Session has expired'}), 401
        
        return jsonify({
            'valid': True,
            'user': payload['user'],
            'user_id': payload['user_id'],
            'expires_at': payload['exp']
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/users', methods=['GET'])
def get_users():
    """Admin endpoint to get all users (for demonstration)"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization header required'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Verify token and get user
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        
        if not user or not user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        users = User.query.all()
        user_list = []
        
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
            user_list.append(user_data)
        
        return jsonify({
            'users': user_list,
            'total_users': len(user_list)
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200

if __name__ == '__main__':
    # In production, set debug=False
    app.run(debug=True, host='0.0.0.0', port=5000)