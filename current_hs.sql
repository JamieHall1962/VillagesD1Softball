WITH player_games_desc AS (
    -- Get all games ordered from newest to oldest for each player
    SELECT 
        b.PlayerNumber,
        p.FirstName,
        p.LastName,
        g.Date,
        b.H,
        ROW_NUMBER() OVER (PARTITION BY b.PlayerNumber ORDER BY g.Date DESC) as games_back
    FROM batting_stats b
    JOIN People p ON b.PlayerNumber = p.PersonNumber
    JOIN game_stats g ON b.TeamNumber = g.TeamNumber AND b.GameNumber = g.GameNumber
    WHERE b.G >= 1
      AND p.LastName != 'Subs'
),
streak_breaks AS (
    -- Find the first hitless game counting back from most recent
    SELECT 
        PlayerNumber,
        FirstName,
        LastName,
        MIN(CASE WHEN H = 0 THEN games_back ELSE NULL END) as first_hitless_game_num,
        MAX(Date) as most_recent_game
    FROM player_games_desc
    GROUP BY PlayerNumber, FirstName, LastName
),
current_streaks AS (
    -- Count consecutive hits from most recent game until hitless game (or all games)
    SELECT 
        pg.PlayerNumber,
        pg.FirstName,
        pg.LastName,
        COUNT(*) as current_streak,
        MIN(pg.Date) as streak_started,
        MAX(pg.Date) as last_game
    FROM player_games_desc pg
    JOIN streak_breaks sb ON pg.PlayerNumber = sb.PlayerNumber
    WHERE pg.H > 0
      AND (sb.first_hitless_game_num IS NULL OR pg.games_back < sb.first_hitless_game_num)
    GROUP BY pg.PlayerNumber, pg.FirstName, pg.LastName
)
SELECT 
    FirstName || ' ' || LastName as Player,
    current_streak as "Current Streak",
    streak_started as "Started",
    last_game as "Last Game"
FROM current_streaks
WHERE current_streak > 0
ORDER BY current_streak DESC, last_game DESC
LIMIT 10;