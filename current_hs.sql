WITH player_games AS (
    -- Get all games for all players with hit data, ordered chronologically
    SELECT 
        b.PlayerNumber,
        p.FirstName,
        p.LastName,
        g.Date,
        b.H,
        CASE WHEN b.H > 0 THEN 1 ELSE 0 END as HasHit,
        ROW_NUMBER() OVER (PARTITION BY b.PlayerNumber ORDER BY g.Date) as game_num
    FROM batting_stats b
    JOIN People p ON b.PlayerNumber = p.PersonNumber
    JOIN game_stats g ON b.TeamNumber = g.TeamNumber AND b.GameNumber = g.GameNumber
    WHERE b.G >= 1  -- Only actual game appearances
      AND p.LastName != 'Subs'  -- Exclude subs
),
games_with_groups AS (
    -- Use the difference between row numbers to identify consecutive hitting streaks
    SELECT 
        *,
        game_num - ROW_NUMBER() OVER (PARTITION BY PlayerNumber, HasHit ORDER BY Date) as streak_group
    FROM player_games
),
streak_lengths AS (
    -- Calculate length of each hitting streak
    SELECT 
        PlayerNumber,
        FirstName,
        LastName,
        HasHit,
        streak_group,
        COUNT(*) as streak_length,
        MIN(Date) as streak_start,
        MAX(Date) as streak_end
    FROM games_with_groups
    WHERE HasHit = 1  -- Only count hitting streaks (games with H > 0)
    GROUP BY PlayerNumber, FirstName, LastName, HasHit, streak_group
)
SELECT 
    FirstName || ' ' || LastName as Player,
    streak_length as "Hitting Streak",
    streak_start as "Started",
    streak_end as "Ended"
FROM streak_lengths
ORDER BY streak_length DESC, streak_end DESC
LIMIT 10;