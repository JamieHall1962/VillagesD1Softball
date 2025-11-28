#!/usr/bin/env python3
"""
Delete all playoff games from November 26, 2025
"""

import sqlite3
from datetime import datetime
import shutil

# Create backup
backup_file = f"softball_stats.db.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
print(f"Creating backup: {backup_file}")
shutil.copy('softball_stats.db', backup_file)

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

target_date = '2025-11-26'

print(f"\nDeleting all games from {target_date}...")

# Count records first
cursor.execute('SELECT COUNT(*) FROM batting_stats WHERE TeamNumber IN (SELECT TeamNumber FROM game_stats WHERE Date = ?) AND GameNumber IN (SELECT GameNumber FROM game_stats WHERE Date = ?)', (target_date, target_date))
batting_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM pitching_stats WHERE TeamNumber IN (SELECT TeamNumber FROM game_stats WHERE Date = ?) AND GameNumber IN (SELECT GameNumber FROM game_stats WHERE Date = ?)', (target_date, target_date))
pitching_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM game_stats WHERE Date = ?', (target_date,))
game_count = cursor.fetchone()[0]

print(f"  Found {batting_count} batting records")
print(f"  Found {pitching_count} pitching records")
print(f"  Found {game_count} game records")

# Delete batting_stats
cursor.execute('''
    DELETE FROM batting_stats 
    WHERE TeamNumber IN (SELECT TeamNumber FROM game_stats WHERE Date = ?)
      AND GameNumber IN (SELECT GameNumber FROM game_stats WHERE Date = ?)
''', (target_date, target_date))
print(f"  Deleted {cursor.rowcount} batting_stats records")

# Delete pitching_stats
cursor.execute('''
    DELETE FROM pitching_stats 
    WHERE TeamNumber IN (SELECT TeamNumber FROM game_stats WHERE Date = ?)
      AND GameNumber IN (SELECT GameNumber FROM game_stats WHERE Date = ?)
''', (target_date, target_date))
print(f"  Deleted {cursor.rowcount} pitching_stats records")

# Delete game_stats
cursor.execute('DELETE FROM game_stats WHERE Date = ?', (target_date,))
print(f"  Deleted {cursor.rowcount} game_stats records")

conn.commit()

# Verify
cursor.execute('SELECT COUNT(*) FROM game_stats WHERE Date = ?', (target_date,))
remaining = cursor.fetchone()[0]

print(f"\n[DONE]")
print(f"Backup: {backup_file}")

if remaining == 0:
    print(f"[OK] All games from {target_date} have been deleted")
else:
    print(f"[WARNING] {remaining} games from {target_date} still remain")

conn.close()

