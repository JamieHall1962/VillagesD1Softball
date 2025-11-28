#!/usr/bin/env python3
"""
Check pitching_stats for the opposing teams in Brian Brown's games
"""

import sqlite3

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

# Team 531 (Raptors), Game 6 (2025-11-05 vs Sandlot)
print("Team 531 (Raptors), Game 6 - Pitching Stats:")
cursor.execute('''
    SELECT ps.PlayerNumber, p.FirstName, p.LastName, ps.IP, ps.W, ps.L
    FROM pitching_stats ps
    JOIN People p ON ps.PlayerNumber = p.PersonNumber
    WHERE ps.TeamNumber = 531 AND ps.GameNumber = 6
    ORDER BY ps.PlayerNumber
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  Player {row[0]:3d}: {row[1]:15s} {row[2]:15s} - IP={row[3]}, W={row[4]}, L={row[5]}")

print("\nTeam 526 (Stars), Game 11 - Pitching Stats:")
cursor.execute('''
    SELECT ps.PlayerNumber, p.FirstName, p.LastName, ps.IP, ps.W, ps.L
    FROM pitching_stats ps
    JOIN People p ON ps.PlayerNumber = p.PersonNumber
    WHERE ps.TeamNumber = 526 AND ps.GameNumber = 11
    ORDER BY ps.PlayerNumber
''')
rows = cursor.fetchall()
for row in rows:
    print(f"  Player {row[0]:3d}: {row[1]:15s} {row[2]:15s} - IP={row[3]}, W={row[4]}, L={row[5]}")

conn.close()

