#!/usr/bin/env python3
"""
Check batting_stats for the duplicate games
"""

import sqlite3

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

# Check Team 531, Game 6 (Raptors 2025-11-05)
print("Team 531, Game 6 (Raptors 2025-11-05):")
cursor.execute('''
    SELECT b.TeamNumber, b.GameNumber, b.PlayerNumber, p.FirstName, p.LastName, b.PA, b.G
    FROM batting_stats b
    JOIN People p ON b.PlayerNumber = p.PersonNumber
    WHERE b.TeamNumber = 531 AND b.GameNumber = 6
    ORDER BY b.PlayerNumber
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  Player {row[2]:3d}: {row[3]:15s} {row[4]:15s} - PA={row[5]}, G={row[6]}")

print("\nTeam 526, Game 11 (Stars 2025-10-10):")
cursor.execute('''
    SELECT b.TeamNumber, b.GameNumber, b.PlayerNumber, p.FirstName, p.LastName, b.PA, b.G
    FROM batting_stats b
    JOIN People p ON b.PlayerNumber = p.PersonNumber
    WHERE b.TeamNumber = 526 AND b.GameNumber = 11
    ORDER BY b.PlayerNumber
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  Player {row[2]:3d}: {row[3]:15s} {row[4]:15s} - PA={row[5]}, G={row[6]}")

# Check if Brian Brown (478) has records for those games
print("\n\nBrian Brown (478) records for those dates:")
cursor.execute('''
    SELECT b.TeamNumber, b.GameNumber, b.PlayerNumber, g.Date, b.PA, b.G
    FROM batting_stats b
    JOIN game_stats g ON b.TeamNumber = g.TeamNumber AND b.GameNumber = g.GameNumber
    WHERE b.PlayerNumber = 478 AND (g.Date = '2025-11-05' OR g.Date = '2025-10-10')
    ORDER BY g.Date, b.TeamNumber, b.GameNumber
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  Team {row[0]}, Game {row[1]}, Date {row[3]}: PA={row[4]}, G={row[5]}")

conn.close()

