#!/usr/bin/env python3
"""
Quick Start Script for D1 Softball Drill-Down Application
"""

import os
import sys
import subprocess
import psycopg2
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'psycopg2', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_database():
    """Check if database is accessible"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'apssb_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        if not db_config['password']:
            print("❌ Database password not found in .env file")
            print("   Run: python setup_database.py")
            return False
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if key tables exist
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('people', 'battingstats', 'teams')
        """)
        
        table_count = cursor.fetchone()[0]
        
        if table_count >= 3:
            # Count some records
            cursor.execute("SELECT COUNT(*) FROM people")
            player_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM battingstats")
            batting_count = cursor.fetchone()[0]
            
            print(f"✅ Database connected successfully")
            print(f"   Players: {player_count:,}")
            print(f"   Batting records: {batting_count:,}")
            
            cursor.close()
            conn.close()
            return True
        else:
            print("❌ Required database tables not found")
            print("   Please import the PostgreSQL migration data")
            return False
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Run: python setup_database.py")
        return False

def main():
    """Main startup function"""
    print("🏟️  D1 Softball Drill-Down Application")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_database():
        sys.exit(1)
    
    print("\n🚀 Starting application...")
    print("   Open your browser to: http://localhost:5000")
    print("   Press Ctrl+C to stop the application")
    print("-" * 50)
    
    # Start the Flask application
    try:
        from drill_down_app import app
        app.run(debug=True, port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

if __name__ == "__main__":
    main() 