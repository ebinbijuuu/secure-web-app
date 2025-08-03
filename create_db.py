#!/usr/bin/env python3
"""
Simple database creation script
"""

import sqlite3
from werkzeug.security import generate_password_hash

def create_database():
    """Create the database with the new schema"""
    try:
        # Connect to database (this will create it if it doesn't exist)
        conn = sqlite3.connect('instance/secure_app.db')
        cursor = conn.cursor()
        
        # Create users table with role column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(120) UNIQUE,
                role VARCHAR(20) DEFAULT 'user',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        ''')
        
        # Create login_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_sessions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                token VARCHAR(500) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Clear existing users first
        cursor.execute('DELETE FROM users')
        
        # Insert admin users
        admin_users = [
            ('admin', generate_password_hash('Admin123!'), None, 'admin'),
            ('Ebinbijuu', generate_password_hash('Lopmop12@'), None, 'admin'),
            ('user1', generate_password_hash('password123'), None, 'user')
        ]
        
        for username, password_hash, email, role in admin_users:
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, role)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, email, role))
        
        conn.commit()
        conn.close()
        
        print("✅ Database created successfully!")
        print("📋 Admin users created:")
        print("   - admin/Admin123!")
        print("   - Ebinbijuu/Lopmop12@")
        print("   - user1/password123 (regular user)")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")

if __name__ == "__main__":
    create_database() 