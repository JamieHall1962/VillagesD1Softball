#!/usr/bin/env python3
"""
Quick Start Script for D1 Softball Drill-Down Application
"""

import os
import sys
import subprocess
# import psycopg2  # Removed: not using PostgreSQL
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

# Removed package check for psycopg2 and python-dotenv

def check_database():
    """Stub: Always return True (no DB check needed)"""
    print("✅ Database check skipped (no DB required)")
    return True

def main():
    """Main startup function"""
    print("🏟️  D1 Softball Drill-Down Application")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Removed package check for psycopg2 and python-dotenv
    
    # Remove all DB/password/.env checks
    # if not check_database():
    #     sys.exit(1)
    
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