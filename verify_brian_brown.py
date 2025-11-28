#!/usr/bin/env python3
"""
Verify Brian Brown's game log - check for duplicates
"""

import sqlite3
from datetime import datetime

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

# Find Brian Brown
cursor.execute("""
    SELECT PersonNumber, FirstName, LastName 
    FROM People 
    WHERE LastName LIKE '%Brown%' AND FirstName LIKE '%Brian%'
""")

person = cursor.fetchone()
if not person:
    print("Brian Brown not found!")
    exit()

person_num, first_name, last_name = person
print(f"Found: {first_name} {last_name} (PID: {person_num})")

# Get his game log from batting_stats joined with game_stats
cursor.execute("""
    SELECT DISTINCT g.Date, g.TeamNumber, g.Opponent, 
           CASE WHEN g.Runs > g.OppRuns THEN 'W'
                WHEN g.Runs < g.OppRuns THEN 'L'
                ELSE 'T' END as Result,
           g.Runs || '-' || g.OppRuns as Score
    FROM batting_stats b
    JOIN game_stats g ON b.TeamNumber = g.TeamNumber AND b.GameNumber = g.GameNumber
    WHERE b.PlayerNumber = ?
    ORDER BY g.Date DESC, g.GameNumber DESC
""", (person_num,))

games = cursor.fetchall()

print(f"\n{'Date':<12} {'Team':<8} {'Opponent':<20} {'W/L':<5} {'Score':<10}")
print("=" * 70)

# Track dates to find duplicates
date_counts = {}
for game in games:
    date, team_num, opponent, result, score = game
    print(f"{date:<12} {team_num:<8} {opponent:<20} {result:<5} {score:<10}")
    
    date_counts[date] = date_counts.get(date, 0) + 1

# Check for duplicate dates
print("\n" + "=" * 70)
duplicates = {date: count for date, count in date_counts.items() if count > 1}
if duplicates:
    print("WARNING - DUPLICATES FOUND:")
    for date, count in duplicates.items():
        print(f"  {date}: {count} games")
else:
    print("[OK] No duplicate dates found!")

conn.close()

