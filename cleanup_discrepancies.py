#!/usr/bin/env python3
"""
Cleanup Discrepancies Script
Removes identified erroneous records from the database

IMPORTANT: Review audit_summary.md before running this script!
"""

import sqlite3
import sys

# Batting records to delete (in DB but not in CSV)
BATTING_TO_DELETE = [
    (526, 2, 606),   # Keith Turney - REVIEW THIS ONE!
    (526, 12, 635),  # Unknown player
    (526, 13, 639),  # Unknown player
    (526, 14, 639),  # Unknown player
    (531, 14, 635),  # Unknown player
    (533, 14, 636),  # Unknown player
    (535, 6, 626),   # Unknown player
    (535, 7, 626),   # Unknown player
    (535, 8, 630),   # Unknown player
    (535, 9, 630),   # Unknown player
    (535, 13, 638),  # Unknown player
    (535, 14, 638),  # Unknown player
]

# Pitching records to delete (in DB but not in CSV)
PITCHING_TO_DELETE = [
    (526, 11, 274),  # Stars Subs
    (531, 6, 542),   # Raptors Subs
    (532, 14, 540),  # Lightning Strikes Subs
    (533, 14, 636),  # Unknown player
    (534, 17, 493),  # Buckeyes Subs
    (535, 6, 626),   # Unknown player
    (535, 7, 626),   # Unknown player
    (535, 10, 548),  # Shorebirds Subs
    (535, 13, 638),  # Unknown player
    (535, 14, 638),  # Unknown player
]

def delete_batting_record(conn, team_num, game_num, player_num):
    """Delete a specific batting stats record"""
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM batting_stats 
        WHERE TeamNumber = ? AND GameNumber = ? AND PlayerNumber = ?
    """, (team_num, game_num, player_num))
    return cursor.rowcount

def delete_pitching_record(conn, team_num, game_num, player_num):
    """Delete a specific pitching stats record"""
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM pitching_stats 
        WHERE TeamNumber = ? AND GameNumber = ? AND PlayerNumber = ?
    """, (team_num, game_num, player_num))
    return cursor.rowcount

def get_player_name(conn, player_num):
    """Get player name from database"""
    cursor = conn.cursor()
    cursor.execute("SELECT FirstName, LastName FROM People WHERE PersonNumber = ?", (player_num,))
    result = cursor.fetchone()
    if result:
        return f"{result[0]} {result[1]}"
    return f"Unknown (#{player_num})"

def main():
    print("="*80)
    print("FALL 2025 DISCREPANCY CLEANUP SCRIPT")
    print("="*80)
    print()
    print("This script will DELETE records from your database that don't exist in data.csv")
    print()
    print(f"Records to delete:")
    print(f"  - {len(BATTING_TO_DELETE)} batting records")
    print(f"  - {len(PITCHING_TO_DELETE)} pitching records")
    print()
    print("WARNING: This operation cannot be undone!")
    print("Make sure you have a backup of softball_stats.db before proceeding.")
    print()
    
    # Confirm with user
    response = input("Do you want to proceed? (type 'YES' to continue): ").strip()
    if response != "YES":
        print("\nOperation cancelled by user.")
        sys.exit(0)
    
    # Connect to database
    conn = sqlite3.connect("softball_stats.db")
    
    try:
        # Delete batting records
        print("\n--- DELETING BATTING RECORDS ---")
        batting_deleted = 0
        for team, game, player in BATTING_TO_DELETE:
            player_name = get_player_name(conn, player)
            rows = delete_batting_record(conn, team, game, player)
            if rows > 0:
                print(f"  ✓ Deleted Team {team}, Game {game}, Player {player} ({player_name})")
                batting_deleted += rows
            else:
                print(f"  ! Not found: Team {team}, Game {game}, Player {player} ({player_name})")
        
        # Delete pitching records
        print("\n--- DELETING PITCHING RECORDS ---")
        pitching_deleted = 0
        for team, game, player in PITCHING_TO_DELETE:
            player_name = get_player_name(conn, player)
            rows = delete_pitching_record(conn, team, game, player)
            if rows > 0:
                print(f"  ✓ Deleted Team {team}, Game {game}, Player {player} ({player_name})")
                pitching_deleted += rows
            else:
                print(f"  ! Not found: Team {team}, Game {game}, Player {player} ({player_name})")
        
        # Commit changes
        conn.commit()
        
        print("\n" + "="*80)
        print("CLEANUP COMPLETE")
        print("="*80)
        print(f"\nTotal records deleted:")
        print(f"  - Batting: {batting_deleted}")
        print(f"  - Pitching: {pitching_deleted}")
        print(f"  - Total: {batting_deleted + pitching_deleted}")
        print()
        print("Next steps:")
        print("1. Run audit_f25_stats.py again to verify cleanup")
        print("2. Run data_update.py to sync with data.csv")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        conn.rollback()
        print("No changes were made to the database.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()

