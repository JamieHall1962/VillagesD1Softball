#!/usr/bin/env python3
"""
Run the exact query that app.py uses for Brian Brown's game log
"""

import sqlite3

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

# Brian Brown's player ID
player_id = 478

# This is the EXACT query from app.py lines 507-559
games_query = '''
    SELECT 
        g.Date,
        g.Opponent,
        g.Runs,
        g.OppRuns,
        g.OpponentTeamNumber,
        g.GameNumber,
        CASE 
            WHEN g.Runs > g.OppRuns THEN 'W'
            WHEN g.Runs < g.OppRuns THEN 'L'
            ELSE 'T'
        END as Result,
        b.PA,
        b.R,
        b.H,
        b."2B" as Doubles,
        b."3B" as Triples,
        b.HR,
        b.BB,
        b.RBI,
        b.SF,
        b.OE,
        -- Get opposing pitcher who got the decision
        opp_pitcher.FirstName as OppPitcherFirst,
        opp_pitcher.LastName as OppPitcherLast,
        opp_pitcher.PlayerNumber as OppPitcherNumber
    FROM batting_stats b
    JOIN game_stats g ON b.TeamNumber = g.TeamNumber AND b.GameNumber = g.GameNumber
    LEFT JOIN (
        -- Find opposing pitcher using OpponentGStatNumber - SIMPLE AND RELIABLE
        SELECT 
            ps.PlayerNumber,
            opp_game.GStatNumber,
            p.FirstName,
            p.LastName
        FROM pitching_stats ps
        JOIN People p ON ps.PlayerNumber = p.PersonNumber
        JOIN game_stats opp_game ON ps.TeamNumber = opp_game.TeamNumber AND ps.GameNumber = opp_game.GameNumber
        WHERE (ps.W > 0 OR ps.L > 0)
    ) opp_pitcher ON g.OpponentGStatNumber = opp_pitcher.GStatNumber
    WHERE b.PlayerNumber = ? AND b.G = 1
    ORDER BY g.Date DESC
    LIMIT 5
'''

print(f"Query for Player {player_id} (Brian Brown):\n")
cursor.execute(games_query, (player_id,))
rows = cursor.fetchall()

print(f"{'Date':<12} {'Opponent':<20} {'Result':<6} {'Score':<8} {'PA':<4}")
print("=" * 65)
for row in rows:
    date, opponent, runs, oppruns, oppteamnum, gamenum, result, pa = row[:8]
    score = f"{runs}-{oppruns}"
    print(f"{date:<12} {opponent:<20} {result:<6} {score:<8} {pa:<4}")

print(f"\nTotal rows returned: {len(rows)}")

conn.close()

