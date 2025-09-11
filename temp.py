#!/usr/bin/env python3
"""
Database Structure Inspector
Shows the actual column names and structure of your database tables
"""

import sqlite3

def inspect_database(db_path='softball_stats.db'):
    print("DATABASE STRUCTURE INSPECTION")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"Database: {db_path}")
        print(f"Tables found: {len(tables)}")
        print()
        
        for table_name in tables:
            table = table_name[0]
            print(f"TABLE: {table}")
            print("-" * 30)
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            print("Columns:")
            for col in columns:
                col_id, name, data_type, not_null, default, pk = col
                pk_marker = " (PRIMARY KEY)" if pk else ""
                print(f"  {name} ({data_type}){pk_marker}")
            
            # Get sample data
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"Total rows: {count}")
            
            if count > 0:
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                sample = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                
                print("Sample data:")
                for i, row in enumerate(sample):
                    print(f"  Row {i+1}: {dict(zip(column_names, row))}")
            
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"Error inspecting database: {e}")

if __name__ == "__main__":
    inspect_database()