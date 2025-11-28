#!/usr/bin/env python3
"""
Check Team 536 (Sandlot - Brian Brown's team) for duplicate player records
"""

import sqlite3

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

# Check Team 536, Game 11 (2025-10-10 vs Stars)
print("Team 536, Game 11 (2025-10-10 vs Stars):")
cursor.execute('''
    SELECT b.TeamNumber, b.GameNumber, b.PlayerNumber, p.FirstName, p.LastName, b.PA, b.G
    FROM batting_stats b
    JOIN People p ON b.PlayerNumber = p.PersonNumber
    WHERE b.TeamNumber = 536 AND b.GameNumber = 11
    ORDER BY b.PlayerNumber
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  Player {row[2]:3d}: {row[3]:15s} {row[4]:15s} - PA={row[5]}, G={row[6]}")

print("\n\nTeam 536, Game 17 (2025-11-05 vs Raptors):")
cursor.execute('''
    SELECT b.TeamNumber, b.GameNumber, b.PlayerNumber, p.FirstName, p.LastName, b.PA, b.G
    FROM batting_stats b
    JOIN People p ON b.PlayerNumber = p.PersonNumber
    WHERE b.TeamNumber = 536 AND b.GameNumber = 17
    ORDER BY b.PlayerNumber
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  Player {row[2]:3d}: {row[3]:15s} {row[4]:15s} - PA={row[5]}, G={row[6]}")

# Check if there are duplicate PlayerNumbers with G=1
print("\n\nChecking for players in Team 536 who appear in multiple games with same GameNumber...")
cursor.execute('''
    SELECT TeamNumber, GameNumber, PlayerNumber, COUNT(*) as cnt
    FROM batting_stats
    WHERE TeamNumber = 536
    GROUP BY TeamNumber, GameNumber, PlayerNumber
    HAVING COUNT(*) > 1
''')
rows = cursor.fetchall()
if rows:
    print("DUPLICATES FOUND:")
    for row in rows:
        print(f"  Team {row[0]}, Game {row[1]}, Player {row[2]}: {row[3]} records")
else:
    print("No duplicates found in batting_stats for Team 536")

conn.close()

