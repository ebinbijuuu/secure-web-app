# 🔐 Secure Web App with SQLite Database

A modern, secure web application with JWT authentication, password validation, and SQLite database integration.

## 🚀 Features

### **Authentication & Security**
- ✅ **JWT Token Authentication** - Secure login with JSON Web Tokens
- ✅ **Password Hashing** - Passwords stored using bcrypt hashing
- ✅ **Session Management** - Track active login sessions in database
- ✅ **Enhanced Password Requirements** - Real-time validation with visual feedback

### **Database Features**
- ✅ **SQLite Database** - Persistent user storage with SQLAlchemy ORM
- ✅ **User Management** - Register, login, and track user activity
- ✅ **Session Tracking** - Monitor active login sessions
- ✅ **Email Support** - Optional email field for user registration

### **Modern UI**
- ✅ **Responsive Design** - Works on desktop and mobile
- ✅ **Real-time Validation** - Password requirements update as you type
- ✅ **Visual Feedback** - Success/error messages with icons
- ✅ **Tabbed Interface** - Clean separation of login and registration

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Security**: bcrypt password hashing, CORS enabled

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd secure-web-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python create_db.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser to `http://127.0.0.1:5000`
   - API endpoints available at `http://127.0.0.1:5000/api`

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE,
    role VARCHAR(20) DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);
```

### Login Sessions Table
```sql
CREATE TABLE login_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(500) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application UI |
| `/api` | GET | API information |
| `/login` | POST | User authentication |
| `/register` | POST | User registration |
| `/verify` | POST | Token verification |
| `/users` | GET | List all users (admin) |
| `/health` | GET | Health check |

### Example API Usage

**Register a new user:**
```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "password": "SecurePass123!", "email": "user@example.com"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}'
```

**Verify token:**
```bash
curl -X POST http://127.0.0.1:5000/verify \
  -H "Content-Type: application/json" \
  -d '{"token": "your-jwt-token-here"}'
```

## 👑 Admin Access

The application includes role-based access control:

### **Admin Users**
- **admin/Admin123!** - Full admin access

### **Regular Users**
- **user1/password123** - Standard user access

### **Admin Features**
- ✅ **View all users** in the database
- ✅ **Access user statistics** and activity
- ✅ **Monitor login sessions**

### **User Features**
- ✅ **Register new accounts**
- ✅ **Login and logout**
- ✅ **View own JWT tokens**
- ❌ **Cannot access user database**

## 🔐 Password Requirements

- ✅ **Minimum 8 characters**
- ✅ **At least 1 uppercase letter**
- ✅ **At least 1 lowercase letter**
- ✅ **At least 1 number**
- ✅ **At least 1 special character** (`!@#$%^&*()_+-=[]{}|;:,.<>?`)

## 🎯 Learning Outcomes

This project demonstrates:

### **Backend Development**
- Flask web framework
- RESTful API design
- Database integration with SQLAlchemy
- JWT authentication implementation
- Password security with bcrypt
- Role-based access control (RBAC)

### **Database Skills**
- SQLite database setup
- ORM (Object-Relational Mapping)
- Database schema design
- User session management
- Data persistence
- Database migration and versioning

### **Frontend Development**
- Modern CSS with gradients and animations
- JavaScript async/await for API calls
- Real-time form validation
- Responsive design principles
- User experience (UX) design
- Dynamic UI updates based on user roles

### **Security Concepts**
- Password hashing and salting
- JWT token management
- Session tracking
- Input validation and sanitization
- CORS configuration
- Authorization and access control

## 🛡️ Security Features

- **Password Hashing**: All passwords are hashed using bcrypt with salt
- **JWT Tokens**: Secure authentication without server-side sessions
- **Input Validation**: Comprehensive validation on all inputs
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **CORS Enabled**: Safe cross-origin requests
- **Session Management**: Track and expire login sessions
- **Role-Based Access Control**: Admin and user roles with different permissions
- **Password Requirements**: Enforced strong password policies

## 📁 Project Structure

```
secure-web-app/
├── app.py              # Main Flask application
├── models.py           # Database models (User, LoginSession)
├── create_db.py        # Database initialization script
├── view_db.py          # Database viewer utility
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── templates/
│   └── index.html     # Web UI with real-time validation
└── instance/
    └── secure_app.db  # SQLite database
```

## 📊 Database Tools

### View Database Contents
```bash
python view_db.py
```

This will show:
- All registered users with roles
- Active login sessions
- Database schema information

This project showcases:
- **Full-stack development** skills
- **Database design** and implementation
- **Security best practices**
- **Modern web development** techniques
- **API design** and documentation
- **User experience** design
- **Authentication and authorization** systems
- **Real-time form validation** and user feedback

Perfect for demonstrating real-world development skills to potential employers!

## 📝 License

This project is open source and available under the MIT License. 