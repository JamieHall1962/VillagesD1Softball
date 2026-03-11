-- ============================================================
-- SBCLAUDE Query Library
-- Reusable SQLite queries for stats and streaks
-- ============================================================

-- ============================================================
-- 1) Last 10 seasons: doubles, triples, and home runs by season
-- ============================================================
WITH season_codes AS (
  SELECT DISTINCT
    TRIM(SUBSTR(t.LongTeamName, LENGTH(t.LongTeamName) - 2, 3)) AS season_code
  FROM Teams t
  WHERE TRIM(SUBSTR(t.LongTeamName, LENGTH(t.LongTeamName) - 2, 3)) GLOB '[FSW][0-9][0-9]'
),
ranked_seasons AS (
  SELECT
    season_code,
    CAST(SUBSTR(season_code, 2, 2) AS INTEGER) AS yy,
    CASE SUBSTR(season_code, 1, 1)
      WHEN 'W' THEN 1
      WHEN 'S' THEN 2
      WHEN 'F' THEN 3
      ELSE 0
    END AS season_order
  FROM season_codes
),
last_10 AS (
  SELECT season_code
  FROM ranked_seasons
  ORDER BY yy DESC, season_order DESC
  LIMIT 10
),
by_season AS (
  SELECT
    l.season_code AS season,
    SUM(b.[2B]) AS doubles,
    SUM(b.[3B]) AS triples,
    SUM(b.HR)   AS homeruns
  FROM last_10 l
  JOIN Teams t
    ON t.LongTeamName LIKE '%' || l.season_code
  JOIN batting_stats b
    ON b.TeamNumber = t.TeamNumber
  GROUP BY l.season_code
)
SELECT *
FROM by_season
ORDER BY CAST(SUBSTR(season, 2, 2) AS INTEGER) DESC,
         CASE SUBSTR(season, 1, 1)
           WHEN 'W' THEN 1
           WHEN 'S' THEN 2
           WHEN 'F' THEN 3
         END DESC;


-- ============================================================
-- 6) BOARD-READY PRINT VIEW: XBH rates per 100 PA (last 10 seasons)
--    Includes one TOTAL row for the full 10-season window
-- ============================================================
WITH season_codes AS (
  SELECT DISTINCT
    TRIM(SUBSTR(t.LongTeamName, LENGTH(t.LongTeamName) - 2, 3)) AS season_code
  FROM Teams t
  WHERE TRIM(SUBSTR(t.LongTeamName, LENGTH(t.LongTeamName) - 2, 3)) GLOB '[FSW][0-9][0-9]'
),
ranked_seasons AS (
  SELECT
    season_code,
    CAST(SUBSTR(season_code, 2, 2) AS INTEGER) AS yy,
    CASE SUBSTR(season_code, 1, 1)
      WHEN 'W' THEN 1
      WHEN 'S' THEN 2
      WHEN 'F' THEN 3
      ELSE 0
    END AS season_order
  FROM season_codes
),
last_10 AS (
  SELECT season_code, yy, season_order
  FROM ranked_seasons
  ORDER BY yy DESC, season_order DESC
  LIMIT 10
),
by_season AS (
  SELECT
    l.season_code AS season,
    l.yy,
    l.season_order,
    SUM(COALESCE(b.PA, 0))   AS pa,
    SUM(COALESCE(b.[2B], 0)) AS doubles,
    SUM(COALESCE(b.[3B], 0)) AS triples,
    SUM(COALESCE(b.HR, 0))   AS hr
  FROM last_10 l
  JOIN Teams t
    ON t.LongTeamName LIKE '%' || l.season_code
  JOIN batting_stats b
    ON b.TeamNumber = t.TeamNumber
  GROUP BY l.season_code, l.yy, l.season_order
),
report_rows AS (
  SELECT
    0 AS sort_bucket,
    yy AS sort_yy,
    season_order AS sort_season_order,
    season AS "Season",
    pa AS "PA",
    doubles AS "2B",
    triples AS "3B",
    hr AS "HR",
    (doubles + triples + hr) AS "XBH",
    ROUND(100.0 * doubles / NULLIF(pa, 0), 2) AS "2B per 100 PA",
    ROUND(100.0 * triples / NULLIF(pa, 0), 2) AS "3B per 100 PA",
    ROUND(100.0 * hr      / NULLIF(pa, 0), 2) AS "HR per 100 PA",
    ROUND(100.0 * (doubles + triples + hr) / NULLIF(pa, 0), 2) AS "XBH per 100 PA"
  FROM by_season

  UNION ALL

  SELECT
    1 AS sort_bucket,
    999 AS sort_yy,
    9 AS sort_season_order,
    'TOTAL (Last 10 Seasons)' AS "Season",
    SUM(pa) AS "PA",
    SUM(doubles) AS "2B",
    SUM(triples) AS "3B",
    SUM(hr) AS "HR",
    SUM(doubles + triples + hr) AS "XBH",
    ROUND(100.0 * SUM(doubles) / NULLIF(SUM(pa), 0), 2) AS "2B per 100 PA",
    ROUND(100.0 * SUM(triples) / NULLIF(SUM(pa), 0), 2) AS "3B per 100 PA",
    ROUND(100.0 * SUM(hr)      / NULLIF(SUM(pa), 0), 2) AS "HR per 100 PA",
    ROUND(100.0 * SUM(doubles + triples + hr) / NULLIF(SUM(pa), 0), 2) AS "XBH per 100 PA"
  FROM by_season
)
SELECT
  "Season",
  "PA",
  "2B",
  "3B",
  "HR",
  "XBH",
  "2B per 100 PA",
  "3B per 100 PA",
  "HR per 100 PA",
  "XBH per 100 PA"
FROM report_rows
ORDER BY sort_bucket, sort_yy, sort_season_order;


-- ============================================================
-- 2) Last 10 seasons: grand total doubles, triples, home runs
-- ============================================================
WITH season_codes AS (
  SELECT DISTINCT
    TRIM(SUBSTR(t.LongTeamName, LENGTH(t.LongTeamName) - 2, 3)) AS season_code
  FROM Teams t
  WHERE TRIM(SUBSTR(t.LongTeamName, LENGTH(t.LongTeamName) - 2, 3)) GLOB '[FSW][0-9][0-9]'
),
ranked_seasons AS (
  SELECT
    season_code,
    CAST(SUBSTR(season_code, 2, 2) AS INTEGER) AS yy,
    CASE SUBSTR(season_code, 1, 1)
      WHEN 'W' THEN 1
      WHEN 'S' THEN 2
      WHEN 'F' THEN 3
      ELSE 0
    END AS season_order
  FROM season_codes
),
last_10 AS (
  SELECT season_code
  FROM ranked_seasons
  ORDER BY yy DESC, season_order DESC
  LIMIT 10
),
by_season AS (
  SELECT
    l.season_code AS season,
    SUM(b.[2B]) AS doubles,
    SUM(b.[3B]) AS triples,
    SUM(b.HR)   AS homeruns
  FROM last_10 l
  JOIN Teams t
    ON t.LongTeamName LIKE '%' || l.season_code
  JOIN batting_stats b
    ON b.TeamNumber = t.TeamNumber
  GROUP BY l.season_code
)
SELECT
  SUM(doubles)  AS total_doubles,
  SUM(triples)  AS total_triples,
  SUM(homeruns) AS total_homeruns
FROM by_season;


-- ============================================================
-- 3) All-time longest ON-BASE streaks (hit OR walk)
-- ============================================================
WITH games_normalized AS (
    SELECT
        b.PlayerNumber,
        p.FirstName,
        p.LastName,
        b.TeamNumber,
        b.GameNumber,
        CASE
            WHEN g.Date LIKE '____-__-__' THEN g.Date
            WHEN substr(g.Date, 7, 2) < '50' THEN
                '20' || substr(g.Date, 7, 2) || '-' ||
                CASE WHEN length(substr(g.Date, 1, 2)) = 1 THEN '0' || substr(g.Date, 1, 2) ELSE substr(g.Date, 1, 2) END || '-' ||
                CASE WHEN length(substr(g.Date, 4, 2)) = 1 THEN '0' || substr(g.Date, 4, 2) ELSE substr(g.Date, 4, 2) END
            ELSE
                '19' || substr(g.Date, 7, 2) || '-' ||
                CASE WHEN length(substr(g.Date, 1, 2)) = 1 THEN '0' || substr(g.Date, 1, 2) ELSE substr(g.Date, 1, 2) END || '-' ||
                CASE WHEN length(substr(g.Date, 4, 2)) = 1 THEN '0' || substr(g.Date, 4, 2) ELSE substr(g.Date, 4, 2) END
        END AS game_date,
        CASE WHEN COALESCE(b.H, 0) > 0 OR COALESCE(b.BB, 0) > 0 THEN 1 ELSE 0 END AS on_base
    FROM batting_stats b
    JOIN game_stats g
      ON b.TeamNumber = g.TeamNumber
     AND b.GameNumber = g.GameNumber
    JOIN People p
      ON p.PersonNumber = b.PlayerNumber
    WHERE b.G = 1
      AND p.LastName != 'Subs'
),
ordered AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY PlayerNumber
            ORDER BY game_date, TeamNumber, GameNumber
        ) AS rn_all,
        ROW_NUMBER() OVER (
            PARTITION BY PlayerNumber, on_base
            ORDER BY game_date, TeamNumber, GameNumber
        ) AS rn_state
    FROM games_normalized
),
ob_runs AS (
    SELECT
        PlayerNumber,
        FirstName,
        LastName,
        (rn_all - rn_state) AS run_id,
        COUNT(*) AS ob_streak,
        MIN(game_date) AS streak_start,
        MAX(game_date) AS streak_end
    FROM ordered
    WHERE on_base = 1
    GROUP BY PlayerNumber, FirstName, LastName, (rn_all - rn_state)
)
SELECT
    FirstName || ' ' || LastName AS player,
    ob_streak AS longest_ob_streak,
    streak_start,
    streak_end
FROM ob_runs
ORDER BY longest_ob_streak DESC, streak_end DESC
LIMIT 50;


-- ============================================================
-- 4) Current active ON-BASE streak leaderboard
-- ============================================================
WITH games_normalized AS (
    SELECT
        b.PlayerNumber,
        p.FirstName,
        p.LastName,
        b.TeamNumber,
        b.GameNumber,
        CASE
            WHEN g.Date LIKE '____-__-__' THEN g.Date
            WHEN substr(g.Date, 7, 2) < '50' THEN
                '20' || substr(g.Date, 7, 2) || '-' ||
                CASE WHEN length(substr(g.Date, 1, 2)) = 1 THEN '0' || substr(g.Date, 1, 2) ELSE substr(g.Date, 1, 2) END || '-' ||
                CASE WHEN length(substr(g.Date, 4, 2)) = 1 THEN '0' || substr(g.Date, 4, 2) ELSE substr(g.Date, 4, 2) END
            ELSE
                '19' || substr(g.Date, 7, 2) || '-' ||
                CASE WHEN length(substr(g.Date, 1, 2)) = 1 THEN '0' || substr(g.Date, 1, 2) ELSE substr(g.Date, 1, 2) END || '-' ||
                CASE WHEN length(substr(g.Date, 4, 2)) = 1 THEN '0' || substr(g.Date, 4, 2) ELSE substr(g.Date, 4, 2) END
        END AS game_date,
        CASE WHEN COALESCE(b.H, 0) > 0 OR COALESCE(b.BB, 0) > 0 THEN 1 ELSE 0 END AS on_base
    FROM batting_stats b
    JOIN game_stats g
      ON b.TeamNumber = g.TeamNumber
     AND b.GameNumber = g.GameNumber
    JOIN People p
      ON p.PersonNumber = b.PlayerNumber
    WHERE b.G = 1
      AND p.LastName != 'Subs'
),
desc_scan AS (
    SELECT
        *,
        SUM(CASE WHEN on_base = 0 THEN 1 ELSE 0 END) OVER (
            PARTITION BY PlayerNumber
            ORDER BY game_date DESC, TeamNumber DESC, GameNumber DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS breaks_seen
    FROM games_normalized
),
current_streaks AS (
    SELECT
        PlayerNumber,
        MAX(FirstName) AS FirstName,
        MAX(LastName) AS LastName,
        SUM(CASE WHEN breaks_seen = 0 AND on_base = 1 THEN 1 ELSE 0 END) AS current_ob_streak,
        MAX(game_date) AS last_game_date
    FROM desc_scan
    GROUP BY PlayerNumber
)
SELECT
    FirstName || ' ' || LastName AS player,
    current_ob_streak,
    last_game_date
FROM current_streaks
WHERE current_ob_streak > 0
ORDER BY current_ob_streak DESC, last_game_date DESC
LIMIT 25;


-- ============================================================
-- 5) Last 10 seasons: extra-base hits per 100 PA
-- ============================================================
WITH season_codes AS (
  SELECT DISTINCT
    TRIM(SUBSTR(t.LongTeamName, LENGTH(t.LongTeamName) - 2, 3)) AS season_code
  FROM Teams t
  WHERE TRIM(SUBSTR(t.LongTeamName, LENGTH(t.LongTeamName) - 2, 3)) GLOB '[FSW][0-9][0-9]'
),
ranked_seasons AS (
  SELECT
    season_code,
    CAST(SUBSTR(season_code, 2, 2) AS INTEGER) AS yy,
    CASE SUBSTR(season_code, 1, 1)
      WHEN 'W' THEN 1
      WHEN 'S' THEN 2
      WHEN 'F' THEN 3
      ELSE 0
    END AS season_order
  FROM season_codes
),
last_10 AS (
  SELECT season_code
  FROM ranked_seasons
  ORDER BY yy DESC, season_order DESC
  LIMIT 10
),
by_season AS (
  SELECT
    l.season_code AS season,
    SUM(COALESCE(b.PA, 0))   AS pa,
    SUM(COALESCE(b.[2B], 0)) AS doubles,
    SUM(COALESCE(b.[3B], 0)) AS triples,
    SUM(COALESCE(b.HR, 0))   AS hr
  FROM last_10 l
  JOIN Teams t
    ON t.LongTeamName LIKE '%' || l.season_code
  JOIN batting_stats b
    ON b.TeamNumber = t.TeamNumber
  GROUP BY l.season_code
)
SELECT
  season,
  pa,
  doubles,
  triples,
  hr,
  (doubles + triples + hr) AS xbh,
  ROUND(100.0 * doubles / NULLIF(pa, 0), 2) AS doubles_per_100_pa,
  ROUND(100.0 * triples / NULLIF(pa, 0), 2) AS triples_per_100_pa,
  ROUND(100.0 * hr      / NULLIF(pa, 0), 2) AS hr_per_100_pa,
  ROUND(100.0 * (doubles + triples + hr) / NULLIF(pa, 0), 2) AS xbh_per_100_pa
FROM by_season
ORDER BY CAST(SUBSTR(season, 2, 2) AS INTEGER) DESC,
         CASE SUBSTR(season, 1, 1)
           WHEN 'W' THEN 1
           WHEN 'S' THEN 2
           WHEN 'F' THEN 3
         END DESC;
