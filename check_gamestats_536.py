#!/usr/bin/env python3
"""
Check game_stats for Team 536 to see what the Opponent field contains
"""

import sqlite3

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

# Check Team 536 games for those dates
print("Team 536 game_stats for 2025-11-05 and 2025-10-10:")
cursor.execute('''
    SELECT Date, TeamNumber, GameNumber, Opponent, Runs, OppRuns
    FROM game_stats
    WHERE TeamNumber = 536 AND (Date = '2025-11-05' OR Date = '2025-10-10')
    ORDER BY Date DESC
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  {row[0]}: Team {row[1]}, Game {row[2]}, Opponent='{row[3]}', Score {row[4]}-{row[5]}")

# Check if there are multiple game_stats records for same team/date
print("\n\nChecking for duplicate game_stats records on same date...")
cursor.execute('''
    SELECT Date, TeamNumber, COUNT(*) as cnt
    FROM game_stats
    WHERE TeamNumber = 536
    GROUP BY Date, TeamNumber
    HAVING COUNT(*) > 1
''')
rows = cursor.fetchall()
if rows:
    print("DUPLICATES FOUND:")
    for row in rows:
        print(f"  {row[0]}: {row[2]} game_stats records for Team {row[1]}")
else:
    print("No duplicate game_stats records")

conn.close()

