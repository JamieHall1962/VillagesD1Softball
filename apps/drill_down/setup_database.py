"""
Database Setup Script for D1 Softball Drill-Down Application
Updated to use the professional migration package
"""

import psycopg2
import os
import subprocess
import sys
from pathlib import Path

def setup_database():
    """Set up the PostgreSQL database using the professional migration package"""
    
    print("🏟️  D1 Softball Database Setup")
    print("=" * 50)
    print("Using professional migration package")
    print()
    
    # Check if we have the migration files
    schema_file = Path("schema.sql")
    import_file = Path("import_data.sql")
    data_dir = Path("data")
    
    if not schema_file.exists():
        print("❌ Schema file not found!")
        print("   Make sure schema.sql is in the current directory")
        return False
        
    if not import_file.exists():
        print("❌ Import file not found!")
        print("   Make sure import_data.sql is in the current directory")
        return False
        
    if not data_dir.exists():
        print("❌ Data directory not found!")
        print("   Make sure the data/ directory exists with CSV files")
        return False
    
    print("✅ Migration files found")
    
    # Database configuration
    db_config = {
        'host': input("Database host (default: localhost): ").strip() or 'localhost',
        'database': input("Database name (default: apssb_db): ").strip() or 'apssb_db',
        'user': input("Database user (default: postgres): ").strip() or 'postgres',
        'password': input("Database password: ").strip()
    }
    
    if not db_config['password']:
        print("❌ Database password is required!")
        return False
    
    print(f"\n📊 Setting up database: {db_config['database']} on {db_config['host']}")
    
    try:
        # Test connection to PostgreSQL server
        test_conn = psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database='postgres'  # Connect to default database first
        )
        test_conn.close()
        print("✅ PostgreSQL connection successful")
        
        # Create database if it doesn't exist
        try:
            conn = psycopg2.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database']
            )
            conn.close()
            print(f"✅ Database '{db_config['database']}' already exists")
            
            # Check if it has data
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM people")
            player_count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            if player_count > 0:
                print(f"✅ Database contains {player_count} players - migration already complete!")
                create_config_file(db_config)
                return True
            else:
                print("⚠️  Database exists but appears empty - proceeding with migration")
                
        except psycopg2.OperationalError:
            # Database doesn't exist, create it
            print(f"📝 Creating database '{db_config['database']}'...")
            conn = psycopg2.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database='postgres'
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_config['database']}")
            cursor.close()
            conn.close()
            print("✅ Database created successfully")
        
        # Run the migration
        print("\n🔄 Running database migration...")
        print("   This may take a few minutes...")
        
        # Import schema
        print("   Step 1: Creating database structure...")
        result = subprocess.run([
            'psql', '-h', db_config['host'], '-U', db_config['user'], 
            '-d', db_config['database'], '-f', 'schema.sql'
        ], input=db_config['password'].encode(), capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Schema import failed: {result.stderr}")
            return False
        
        print("   Step 2: Importing data...")
        # Change to data directory for import
        original_dir = os.getcwd()
        os.chdir('data')
        
        result = subprocess.run([
            'psql', '-h', db_config['host'], '-U', db_config['user'], 
            '-d', db_config['database'], '-f', '../import_data.sql'
        ], input=db_config['password'].encode(), capture_output=True, text=True)
        
        os.chdir(original_dir)
        
        if result.returncode != 0:
            print(f"❌ Data import failed: {result.stderr}")
            return False
        
        print("✅ Migration completed successfully!")
        
        # Verify the migration
        print("\n🔍 Verifying migration...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Check key tables
        cursor.execute("SELECT COUNT(*) FROM people")
        player_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM battingstats")
        batting_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM gamestats")
        game_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM teams")
        team_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"✅ Migration verification complete:")
        print(f"   Players: {player_count:,}")
        print(f"   Batting records: {batting_count:,}")
        print(f"   Games: {game_count:,}")
        print(f"   Teams: {team_count:,}")
        
        # Create configuration file
        create_config_file(db_config)
        
        print("\n🎉 Database setup complete!")
        print("\n🚀 You can now run the application:")
        print("   python start_app.py")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        print("\n💡 Make sure PostgreSQL is running and accessible")
        return False
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def create_config_file(db_config):
    """Create .env configuration file"""
    config_content = f"""# Database Configuration for D1 Softball App
DB_HOST={db_config['host']}
DB_NAME={db_config['database']}
DB_USER={db_config['user']}
DB_PASSWORD={db_config['password']}
"""
    
    with open('.env', 'w') as f:
        f.write(config_content)
    
    print("✅ Database configuration saved to .env file")

if __name__ == "__main__":
    setup_database() 