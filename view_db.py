#!/usr/bin/env python3
"""
Simple database viewer for the Secure Web App
Run this to see what's stored in the database
"""

import sqlite3
from datetime import datetime

def view_database():
    """View the contents of the SQLite database"""
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/secure_app.db')
        cursor = conn.cursor()
        
        print("🔐 Secure Web App Database Viewer")
        print("=" * 50)
        
        # View users table
        print("\n📋 USERS TABLE:")
        print("-" * 30)
        cursor.execute("SELECT id, username, email, role, created_at, last_login FROM users")
        users = cursor.fetchall()
        
        if users:
            print(f"{'ID':<3} {'Username':<15} {'Email':<25} {'Role':<8} {'Created':<12} {'Last Login':<12}")
            print("-" * 90)
            for user in users:
                user_id, username, email, role, created_at, last_login = user
                created_str = created_at[:10] if created_at else 'N/A'
                login_str = last_login[:10] if last_login else 'Never'
                email_str = email if email else 'N/A'
                role_str = role if role else 'user'
                print(f"{user_id:<3} {username:<15} {email_str:<25} {role_str:<8} {created_str:<12} {login_str:<12}")
        else:
            print("No users found")
        
        # View login sessions table
        print("\n🔑 LOGIN SESSIONS TABLE:")
        print("-" * 30)
        cursor.execute("""
            SELECT ls.id, u.username, ls.created_at, ls.expires_at, ls.is_active 
            FROM login_sessions ls 
            JOIN users u ON ls.user_id = u.id
        """)
        sessions = cursor.fetchall()
        
        if sessions:
            print(f"{'ID':<3} {'User':<15} {'Created':<12} {'Expires':<12} {'Active':<6}")
            print("-" * 60)
            for session in sessions:
                session_id, username, created_at, expires_at, is_active = session
                created_str = created_at[:10] if created_at else 'N/A'
                expires_str = expires_at[:10] if expires_at else 'N/A'
                active_str = 'Yes' if is_active else 'No'
                print(f"{session_id:<3} {username:<15} {created_str:<12} {expires_str:<12} {active_str:<6}")
        else:
            print("No login sessions found")
        
        # Show table schemas
        print("\n📊 DATABASE SCHEMA:")
        print("-" * 30)
        
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            print(table[0])
            print()
        
        conn.close()
        print("✅ Database viewer completed successfully!")
        
    except sqlite3.OperationalError as e:
        print(f"❌ Database error: {e}")
        print("Make sure you've run the Flask app at least once to create the database.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    view_database() 