#!/usr/bin/env python3
"""
D1 Softball Stats App Launcher
Automatically navigates to the correct directory and starts the Flask app
"""

import os
import sys
import subprocess
import time

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the drill_down app directory
    app_dir = os.path.join(script_dir, 'apps', 'drill_down')
    
    if not os.path.exists(app_dir):
        print(f"Error: App directory not found at {app_dir}")
        print("Please make sure you're running this from the d1softball root directory")
        return
    
    # Check if the Flask app file exists
    app_file = os.path.join(app_dir, 'simple_csv_app.py')
    if not os.path.exists(app_file):
        print(f"Error: Flask app not found at {app_file}")
        return
    
    print("=" * 60)
    print("D1 Softball Stats App Launcher")
    print("=" * 60)
    print(f"Starting app from: {app_dir}")
    print(f"App file: {app_file}")
    print()
    print("The app will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        # Change to the app directory
        os.chdir(app_dir)
        
        # Start the Flask app
        print("Starting Flask app...")
        subprocess.run([sys.executable, 'simple_csv_app.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\nError starting app: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main() 