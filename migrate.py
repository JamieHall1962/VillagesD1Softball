"""
D1 Softball Database Migration
Reads from legacy softball_stats.db -> Creates new d1softball.db

USAGE:
    python migrate.py --old path/to/softball_stats.db --dry-run    # preview only
    python migrate.py --old path/to/softball_stats.db              # do it for real

Preserves all legacy IDs for traceability.
"""
import sqlite3
import re
import argparse
import os
import sys
from collections import defaultdict

# ============================================================
# Team name parsing
# ============================================================

# Known division tags (in parentheses) that are real divisions
# "(D1/2)" is NOT a division — it's a cross-division event marker
DIVISION_BLACKLIST = {'D1/2'}

# Season code pattern: W/S/F followed by 2 digits
SEASON_CODE_RE = re.compile(r'\b([WSF]\d{2})\b')

def parse_team_name(long_name):
    """
    Parse "Wolverines (Ballers) W26" -> {
        'clean_name': 'Wolverines',
        'division': 'Ballers',
        'season_code': 'W26',
        'is_d1d2': False
    }
    """
    original = long_name.strip()

    # Extract season code
    season_match = SEASON_CODE_RE.search(original)
    season_code = season_match.group(1) if season_match else None

    # Extract all parenthetical groups
    parens = re.findall(r'\(([^)]+)\)', original)
    division = None
    is_d1d2 = False
    for p in parens:
        if p.strip() in DIVISION_BLACKLIST:
            is_d1d2 = True
        else:
            division = p.strip()

    # Build clean name: remove season code, remove all parentheticals, strip
    clean = original
    # Remove parentheticals
    clean = re.sub(r'\([^)]*\)', '', clean)
    # Remove season code
    if season_code:
        clean = re.sub(r'\b' + re.escape(season_code) + r'\b', '', clean)
    clean = clean.strip()
    # Remove trailing/leading whitespace and extra spaces
    clean = re.sub(r'\s+', ' ', clean).strip()

    return {
        'clean_name': clean,
        'division': division,
        'season_code': season_code,
        'is_d1d2': is_d1d2,
        'original': original,
    }

# ============================================================
# Season code -> full name
# ============================================================

SEASON_PREFIX = {'W': 'Winter', 'S': 'Summer', 'F': 'Fall'}

def season_code_to_name(code):
    """W26 -> 'Winter 2026', S09 -> 'Summer 2009'"""
    prefix = SEASON_PREFIX.get(code[0], '?')
    yy = int(code[1:])
    year = 2000 + yy
    return f"{prefix} {year}"

def season_code_to_short(code):
    """W26 -> 'Winter 26'"""
    prefix = SEASON_PREFIX.get(code[0], '?')
    return f"{prefix} {code[1:]}"

def season_code_to_year(code):
    return 2000 + int(code[1:])

# ============================================================
# Migration
# ============================================================

def migrate(old_db_path, new_db_path, dry_run=False):
    if not os.path.exists(old_db_path):
        print(f"ERROR: Old database not found: {old_db_path}")
        sys.exit(1)

    old = sqlite3.connect(old_db_path)
    old.row_factory = sqlite3.Row

    print(f"Reading from: {old_db_path}")
    print(f"{'DRY RUN — no changes will be written' if dry_run else f'Writing to: {new_db_path}'}")
    print("=" * 60)

    # --------------------------------------------------------
    # Step 0: Read old data
    # --------------------------------------------------------
    old_seasons = old.execute("SELECT * FROM Seasons ORDER BY FilterNumber").fetchall()
    old_people = old.execute("SELECT * FROM People ORDER BY PersonNumber").fetchall()
    old_teams = old.execute("SELECT * FROM Teams ORDER BY TeamNumber").fetchall()
    old_rosters = old.execute("SELECT * FROM Roster").fetchall()
    old_game_stats = old.execute("SELECT * FROM game_stats ORDER BY Date, TeamNumber").fetchall()
    old_batting = old.execute("SELECT * FROM batting_stats").fetchall()
    old_pitching = old.execute("SELECT * FROM pitching_stats").fetchall()

    print(f"Old data: {len(old_seasons)} seasons, {len(old_people)} players, "
          f"{len(old_teams)} teams, {len(old_rosters)} roster entries")
    print(f"          {len(old_game_stats)} game_stat rows, {len(old_batting)} batting rows, "
          f"{len(old_pitching)} pitching rows")
    print()

    # --------------------------------------------------------
    # Step 1: Seasons
    # --------------------------------------------------------
    # Build from old Seasons table
    print("--- SEASONS ---")
    season_map = {}  # old FilterNumber -> new season id
    seasons_data = []
    for s in old_seasons:
        # short_name holds the actual season code (W11, S25, etc.)
        # FilterNumber is just a sequential integer
        code = s['short_name']
        if not code:
            code = s['FilterNumber']  # fallback
        if not code:
            continue
        code = code.strip()
        seasons_data.append({
            'season_code': code,
            'name': s['season_name'] or season_code_to_name(code),
            'short_name': code,
            'year': season_code_to_year(code) if SEASON_CODE_RE.match(code) else None,
            'champion': s['Champion'],
            'filter_number': s['FilterNumber'],
        })
    print(f"  {len(seasons_data)} seasons to migrate")

    # --------------------------------------------------------
    # Step 2: Parse team names and build team records
    # --------------------------------------------------------
    print("\n--- TEAMS ---")
    teams_data = []
    parse_errors = []
    team_season_codes = set()

    for t in old_teams:
        tn = t['TeamNumber']
        long_name = t['LongTeamName'] or ''
        manager = t['Manager']

        parsed = parse_team_name(long_name)
        if not parsed['season_code']:
            parse_errors.append(f"  NO SEASON CODE: TeamNumber={tn} Name='{long_name}'")
            # Try to infer from game dates
            game = old.execute(
                "SELECT MIN(Date) as d FROM game_stats WHERE TeamNumber=?", (tn,)
            ).fetchone()
            if game and game['d']:
                parse_errors[-1] += f" (first game: {game['d']})"
            continue

        team_season_codes.add(parsed['season_code'])
        teams_data.append({
            'legacy_team_number': tn,
            'legacy_full_name': long_name,
            'clean_name': parsed['clean_name'],
            'division': parsed['division'],
            'season_code': parsed['season_code'],
            'is_d1d2': parsed['is_d1d2'],
            'manager': manager,
        })

    if parse_errors:
        print(f"  PARSE ERRORS ({len(parse_errors)}):")
        for e in parse_errors:
            print(e)

    # Check for season codes in teams not in Seasons table
    known_codes = {s['season_code'] for s in seasons_data}
    missing = team_season_codes - known_codes
    if missing:
        print(f"\n  Season codes found in teams but NOT in Seasons table: {missing}")
        print("  These will be auto-created.")
        for code in sorted(missing):
            seasons_data.append({
                'season_code': code,
                'name': season_code_to_name(code),
                'short_name': season_code_to_short(code),
                'year': season_code_to_year(code),
                'champion': None,
            })

    # Detect which seasons have divisions
    season_divisions = defaultdict(set)
    for td in teams_data:
        if td['division']:
            season_divisions[td['season_code']].add(td['division'])

    print(f"\n  {len(teams_data)} teams parsed successfully")
    print(f"  Seasons with divisions:")
    for code, divs in sorted(season_divisions.items()):
        print(f"    {code}: {', '.join(sorted(divs))}")

    # --------------------------------------------------------
    # Step 3: Players
    # --------------------------------------------------------
    print("\n--- PLAYERS ---")
    players_data = []
    for p in old_people:
        players_data.append({
            'legacy_person_number': p['PersonNumber'],
            'first_name': p['FirstName'],
            'last_name': p['LastName'],
        })
    print(f"  {len(players_data)} players to migrate")

    # --------------------------------------------------------
    # Step 4: Games (merge two rows into one)
    # --------------------------------------------------------
    print("\n--- GAMES ---")
    # Group game_stats by (TeamNumber, GameNumber) for lookup
    gs_lookup = {}
    for gs in old_game_stats:
        key = (gs['TeamNumber'], gs['GameNumber'])
        gs_lookup[key] = gs

    # Also build GStatNumber lookup
    gstat_lookup = {}
    for gs in old_game_stats:
        gstat_lookup[(gs['TeamNumber'], gs['GStatNumber'])] = gs

    # Strategy: iterate game_stats where HomeTeam=1, match to opponent's row
    home_rows = [gs for gs in old_game_stats if gs['HomeTeam'] == 1]
    games_data = []
    game_match_errors = []
    processed_gstats = set()

    for hr in home_rows:
        home_tn = hr['TeamNumber']
        home_gstat = hr['GStatNumber']

        if (home_tn, home_gstat) in processed_gstats:
            continue

        # Find the away team's row
        opp_tn = hr['OpponentTeamNumber']
        try:
            opp_gstat = hr['OpponentGStatNumber']
        except (IndexError, KeyError):
            opp_gstat = None
        away_row = None

        if opp_gstat and opp_tn:
            away_row = gstat_lookup.get((opp_tn, opp_gstat))

        if not away_row and opp_tn:
            # Fallback: find opponent's row for same date where opponent=home_tn
            candidates = [
                gs for gs in old_game_stats
                if gs['TeamNumber'] == opp_tn
                and gs['OpponentTeamNumber'] == home_tn
                and gs['Date'] == hr['Date']
                and gs['HomeTeam'] == 0
            ]
            if len(candidates) == 1:
                away_row = candidates[0]
            elif len(candidates) > 1:
                game_match_errors.append(
                    f"  AMBIGUOUS: home TN={home_tn} GS={home_gstat} date={hr['Date']} "
                    f"found {len(candidates)} opponent rows"
                )

        game_record = {
            'home_team_legacy_tn': home_tn,
            'away_team_legacy_tn': opp_tn,
            'game_date': hr['Date'],
            'innings': hr['Innings'],
            'home_score': hr['Runs'],
            'away_score': hr['OppRuns'],
            'home_inn': [hr[f'RunsInning{i}'] for i in range(1, 10)],
            'away_inn': [hr[f'OppRunsInning{i}'] for i in range(1, 10)],
            'legacy_home_game_number': hr['GameNumber'],
            'legacy_home_gstat': home_gstat,
            'legacy_away_game_number': away_row['GameNumber'] if away_row else None,
            'legacy_away_gstat': away_row['GStatNumber'] if away_row else None,
        }
        games_data.append(game_record)
        processed_gstats.add((home_tn, home_gstat))
        if away_row:
            processed_gstats.add((opp_tn, away_row['GStatNumber']))

    # Also handle games where we only have the away team's perspective
    for gs in old_game_stats:
        if gs['HomeTeam'] == 0:
            key = (gs['TeamNumber'], gs['GStatNumber'])
            if key not in processed_gstats:
                # This away row was never matched to a home row
                # Create game with away team as away, opponent as home
                game_record = {
                    'home_team_legacy_tn': gs['OpponentTeamNumber'],
                    'away_team_legacy_tn': gs['TeamNumber'],
                    'game_date': gs['Date'],
                    'innings': gs['Innings'],
                    'home_score': gs['OppRuns'],
                    'away_score': gs['Runs'],
                    'home_inn': [gs[f'OppRunsInning{i}'] for i in range(1, 10)],
                    'away_inn': [gs[f'RunsInning{i}'] for i in range(1, 10)],
                    'legacy_home_game_number': None,
                    'legacy_home_gstat': None,
                    'legacy_away_game_number': gs['GameNumber'],
                    'legacy_away_gstat': gs['GStatNumber'],
                }
                games_data.append(game_record)
                processed_gstats.add(key)

    unmatched = len(old_game_stats) - len(processed_gstats)
    print(f"  {len(home_rows)} home rows -> {len(games_data)} games")
    if game_match_errors:
        print(f"  MATCH ERRORS ({len(game_match_errors)}):")
        for e in game_match_errors[:10]:
            print(e)
        if len(game_match_errors) > 10:
            print(f"  ... and {len(game_match_errors) - 10} more")
    if unmatched > 0:
        print(f"  WARNING: {unmatched} game_stat rows not accounted for")

    # --------------------------------------------------------
    # Step 5: Batting
    # --------------------------------------------------------
    print(f"\n--- BATTING ---")
    print(f"  {len(old_batting)} rows to migrate (FK mapping at write time)")

    # --------------------------------------------------------
    # Step 6: Pitching
    # --------------------------------------------------------
    print(f"\n--- PITCHING ---")
    print(f"  {len(old_pitching)} rows to migrate (FK mapping at write time)")

    # --------------------------------------------------------
    # Step 7: Rosters
    # --------------------------------------------------------
    print(f"\n--- ROSTERS ---")
    print(f"  {len(old_rosters)} rows to migrate (FK mapping at write time)")

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("MIGRATION SUMMARY")
    print(f"  Seasons:  {len(seasons_data)}")
    print(f"  Players:  {len(players_data)}")
    print(f"  Teams:    {len(teams_data)}")
    print(f"  Games:    {len(games_data)}")
    print(f"  Batting:  {len(old_batting)}")
    print(f"  Pitching: {len(old_pitching)}")
    print(f"  Rosters:  {len(old_rosters)}")

    if dry_run:
        print("\nDRY RUN COMPLETE — no database was created.")
        print("Review the output above. If it looks good, run without --dry-run")
        old.close()
        return

    # ========================================================
    # WRITE TO NEW DATABASE
    # ========================================================
    print(f"\nWriting to {new_db_path}...")
    if os.path.exists(new_db_path):
        backup = new_db_path + '.bak'
        os.rename(new_db_path, backup)
        print(f"  Backed up existing DB to {backup}")

    new = sqlite3.connect(new_db_path)
    cur = new.cursor()

    # Create schema
    cur.executescript("""
        CREATE TABLE seasons (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            season_code     TEXT NOT NULL UNIQUE,
            name            TEXT NOT NULL,
            short_name      TEXT,
            year            INTEGER,
            champion        TEXT,
            has_divisions   INTEGER DEFAULT 0,
            is_current      INTEGER DEFAULT 0
        );

        CREATE TABLE players (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name              TEXT NOT NULL,
            last_name               TEXT NOT NULL,
            phone                   TEXT,
            email                   TEXT,
            active                  INTEGER DEFAULT 1,
            legacy_person_number    INTEGER
        );

        CREATE TABLE teams (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            season_id               INTEGER NOT NULL,
            name                    TEXT NOT NULL,
            division                TEXT,
            manager                 TEXT,
            manager_phone           TEXT,
            manager_email           TEXT,
            legacy_team_number      INTEGER,
            legacy_full_name        TEXT,
            FOREIGN KEY (season_id) REFERENCES seasons(id)
        );

        CREATE TABLE rosters (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id         INTEGER NOT NULL,
            player_id       INTEGER NOT NULL,
            jersey_number   TEXT,
            FOREIGN KEY (team_id)   REFERENCES teams(id),
            FOREIGN KEY (player_id) REFERENCES players(id)
        );

        CREATE TABLE games (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            season_id               INTEGER NOT NULL,
            game_date               TEXT NOT NULL,
            game_time               TEXT,
            field                   TEXT,
            round                   INTEGER,
            innings                 INTEGER DEFAULT 7,
            home_team_id            INTEGER NOT NULL,
            away_team_id            INTEGER NOT NULL,
            home_score              INTEGER,
            away_score              INTEGER,
            home_inn_1 INTEGER, home_inn_2 INTEGER, home_inn_3 INTEGER,
            home_inn_4 INTEGER, home_inn_5 INTEGER, home_inn_6 INTEGER,
            home_inn_7 INTEGER, home_inn_8 INTEGER, home_inn_9 INTEGER,
            away_inn_1 INTEGER, away_inn_2 INTEGER, away_inn_3 INTEGER,
            away_inn_4 INTEGER, away_inn_5 INTEGER, away_inn_6 INTEGER,
            away_inn_7 INTEGER, away_inn_8 INTEGER, away_inn_9 INTEGER,
            status                  TEXT DEFAULT 'completed',
            legacy_home_game_number INTEGER,
            legacy_away_game_number INTEGER,
            legacy_home_gstat       INTEGER,
            legacy_away_gstat       INTEGER,
            FOREIGN KEY (season_id)     REFERENCES seasons(id),
            FOREIGN KEY (home_team_id)  REFERENCES teams(id),
            FOREIGN KEY (away_team_id)  REFERENCES teams(id)
        );

        CREATE TABLE batting (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id         INTEGER NOT NULL,
            player_id       INTEGER NOT NULL,
            team_id         INTEGER NOT NULL,
            home_team       INTEGER,
            pa              INTEGER DEFAULT 0,
            r               INTEGER DEFAULT 0,
            h               INTEGER DEFAULT 0,
            doubles         INTEGER DEFAULT 0,
            triples         INTEGER DEFAULT 0,
            hr              INTEGER DEFAULT 0,
            oe              INTEGER DEFAULT 0,
            bb              INTEGER DEFAULT 0,
            rbi             INTEGER DEFAULT 0,
            sf              INTEGER DEFAULT 0,
            games_played    INTEGER DEFAULT 0,
            FOREIGN KEY (game_id)   REFERENCES games(id),
            FOREIGN KEY (player_id) REFERENCES players(id),
            FOREIGN KEY (team_id)   REFERENCES teams(id)
        );

        CREATE TABLE pitching (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id         INTEGER NOT NULL,
            player_id       INTEGER NOT NULL,
            team_id         INTEGER NOT NULL,
            home_team       INTEGER,
            ip              REAL DEFAULT 0,
            bb              INTEGER DEFAULT 0,
            w               INTEGER DEFAULT 0,
            l               INTEGER DEFAULT 0,
            ibb             INTEGER DEFAULT 0,
            FOREIGN KEY (game_id)   REFERENCES games(id),
            FOREIGN KEY (player_id) REFERENCES players(id),
            FOREIGN KEY (team_id)   REFERENCES teams(id)
        );

        CREATE TABLE news (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            title           TEXT NOT NULL,
            body            TEXT NOT NULL,
            author          TEXT DEFAULT 'Jamie Hall, Commissioner',
            publish_date    TEXT NOT NULL,
            active          INTEGER DEFAULT 1
        );

        CREATE TABLE photos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            filename        TEXT NOT NULL,
            caption         TEXT NOT NULL,
            submitted_by    TEXT,
            submit_date     TEXT NOT NULL,
            approved        INTEGER DEFAULT 0,
            approved_date   TEXT
        );

        CREATE TABLE honor_roll (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            years_active    TEXT,
            description     TEXT,
            sort_order      INTEGER DEFAULT 0
        );
    """)

    # --- Write seasons ---
    season_id_map = {}  # season_code -> new id
    for s in seasons_data:
        has_div = 1 if s['season_code'] in season_divisions else 0
        is_curr = 1 if s['season_code'] == 'S26' else 0
        cur.execute(
            """INSERT INTO seasons (season_code, name, short_name, year, champion,
               has_divisions, is_current)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (s['season_code'], s['name'], s['short_name'], s['year'],
             s['champion'], has_div, is_curr)
        )
        season_id_map[s['season_code']] = cur.lastrowid
    print(f"  Wrote {len(seasons_data)} seasons")

    # --- Write players ---
    player_id_map = {}  # old PersonNumber -> new id
    for p in players_data:
        cur.execute(
            """INSERT INTO players (first_name, last_name, legacy_person_number)
               VALUES (?, ?, ?)""",
            (p['first_name'], p['last_name'], p['legacy_person_number'])
        )
        player_id_map[p['legacy_person_number']] = cur.lastrowid
    print(f"  Wrote {len(players_data)} players")

    # --- Write teams ---
    team_id_map = {}  # old TeamNumber -> new id
    for td in teams_data:
        sid = season_id_map.get(td['season_code'])
        if not sid:
            print(f"  WARNING: No season for team {td['legacy_full_name']}, skipping")
            continue
        cur.execute(
            """INSERT INTO teams (season_id, name, division, manager,
               legacy_team_number, legacy_full_name)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (sid, td['clean_name'], td['division'], td['manager'],
             td['legacy_team_number'], td['legacy_full_name'])
        )
        team_id_map[td['legacy_team_number']] = cur.lastrowid
    print(f"  Wrote {len(team_id_map)} teams")

    # --- Write games ---
    # Build a lookup for (legacy_team_number, legacy_game_number) -> new game_id
    # We need this for batting/pitching FK mapping
    game_id_map = {}  # (old_team_number, old_game_number) -> new game_id
    games_written = 0
    games_skipped = 0
    games_amalgamated = 0

    for gd in games_data:
        home_tn = gd['home_team_legacy_tn']
        away_tn = gd['away_team_legacy_tn']
        home_tid = team_id_map.get(home_tn)
        away_tid = team_id_map.get(away_tn)

        # Amalgamated seasons: OpponentTeamNumber=0, no real opponent
        # Use the real team as both sides, flag as amalgamated
        amalgamated = False
        if home_tid and not away_tid and (away_tn == 0 or away_tn is None):
            away_tid = home_tid
            amalgamated = True
        elif away_tid and not home_tid and (home_tn == 0 or home_tn is None):
            home_tid = away_tid
            amalgamated = True

        if not home_tid or not away_tid:
            games_skipped += 1
            continue

        # Determine season from home team
        home_team_data = next(
            (td for td in teams_data if td['legacy_team_number'] == gd['home_team_legacy_tn']),
            None
        )
        if not home_team_data:
            games_skipped += 1
            continue
        sid = season_id_map.get(home_team_data['season_code'])
        if not sid:
            games_skipped += 1
            continue

        cur.execute(
            """INSERT INTO games (season_id, game_date, innings,
               home_team_id, away_team_id, home_score, away_score,
               home_inn_1, home_inn_2, home_inn_3, home_inn_4, home_inn_5,
               home_inn_6, home_inn_7, home_inn_8, home_inn_9,
               away_inn_1, away_inn_2, away_inn_3, away_inn_4, away_inn_5,
               away_inn_6, away_inn_7, away_inn_8, away_inn_9,
               status,
               legacy_home_game_number, legacy_away_game_number,
               legacy_home_gstat, legacy_away_gstat)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (sid, gd['game_date'], gd['innings'],
             home_tid, away_tid, gd['home_score'], gd['away_score'],
             *gd['home_inn'], *gd['away_inn'],
             'amalgamated' if amalgamated else 'completed',
             gd['legacy_home_game_number'], gd['legacy_away_game_number'],
             gd['legacy_home_gstat'], gd['legacy_away_gstat'])
        )
        new_game_id = cur.lastrowid

        # Map both teams' game numbers to this game
        if gd['legacy_home_game_number'] is not None:
            game_id_map[(gd['home_team_legacy_tn'], gd['legacy_home_game_number'])] = new_game_id
        if gd['legacy_away_game_number'] is not None:
            game_id_map[(gd['away_team_legacy_tn'], gd['legacy_away_game_number'])] = new_game_id

        games_written += 1
        if amalgamated:
            games_amalgamated += 1

    print(f"  Wrote {games_written} games ({games_amalgamated} amalgamated, {games_skipped} skipped)")

    # --- Write batting ---
    batting_written = 0
    batting_skipped = 0
    for b in old_batting:
        tn = b['TeamNumber']
        pn = b['PlayerNumber']
        gn = b['GameNumber']

        new_team = team_id_map.get(tn)
        new_player = player_id_map.get(pn)
        new_game = game_id_map.get((tn, gn))

        if not new_team or not new_player or not new_game:
            batting_skipped += 1
            continue

        cur.execute(
            """INSERT INTO batting (game_id, player_id, team_id, home_team,
               pa, r, h, doubles, triples, hr, oe, bb, rbi, sf, games_played)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (new_game, new_player, new_team, b['HomeTeam'],
             b['PA'], b['R'], b['H'], b['2B'], b['3B'], b['HR'],
             b['OE'], b['BB'], b['RBI'], b['SF'], b['G'])
        )
        batting_written += 1

    print(f"  Wrote {batting_written} batting rows ({batting_skipped} skipped)")

    # --- Write pitching ---
    pitching_written = 0
    pitching_skipped = 0
    for p in old_pitching:
        tn = p['TeamNumber']
        pn = p['PlayerNumber']
        gn = p['GameNumber']

        new_team = team_id_map.get(tn)
        new_player = player_id_map.get(pn)
        new_game = game_id_map.get((tn, gn))

        if not new_team or not new_player or not new_game:
            pitching_skipped += 1
            continue

        cur.execute(
            """INSERT INTO pitching (game_id, player_id, team_id, home_team,
               ip, bb, w, l, ibb)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (new_game, new_player, new_team, p['HomeTeam'],
             p['IP'], p['BB'], p['W'], p['L'], p['IBB'])
        )
        pitching_written += 1

    print(f"  Wrote {pitching_written} pitching rows ({pitching_skipped} skipped)")

    # --- Write rosters ---
    roster_written = 0
    roster_skipped = 0
    for r in old_rosters:
        tn = r['TeamNumber']
        pn = r['PersonNumber']

        new_team = team_id_map.get(tn)
        new_player = player_id_map.get(pn)

        if not new_team or not new_player:
            roster_skipped += 1
            continue

        cur.execute(
            "INSERT INTO rosters (team_id, player_id) VALUES (?, ?)",
            (new_team, new_player)
        )
        roster_written += 1

    print(f"  Wrote {roster_written} roster rows ({roster_skipped} skipped)")

    # --- Create indexes ---
    cur.executescript("""
        CREATE INDEX idx_teams_season ON teams(season_id);
        CREATE INDEX idx_teams_legacy ON teams(legacy_team_number);
        CREATE INDEX idx_players_legacy ON players(legacy_person_number);
        CREATE INDEX idx_games_season ON games(season_id);
        CREATE INDEX idx_games_date ON games(game_date);
        CREATE INDEX idx_games_home ON games(home_team_id);
        CREATE INDEX idx_games_away ON games(away_team_id);
        CREATE INDEX idx_batting_game ON batting(game_id);
        CREATE INDEX idx_batting_player ON batting(player_id);
        CREATE INDEX idx_batting_team ON batting(team_id);
        CREATE INDEX idx_pitching_game ON pitching(game_id);
        CREATE INDEX idx_pitching_player ON pitching(player_id);
        CREATE INDEX idx_rosters_team ON rosters(team_id);
        CREATE INDEX idx_rosters_player ON rosters(player_id);
    """)
    print("  Created indexes")

    new.commit()
    new.close()
    old.close()

    # --- Verification ---
    print("\n" + "=" * 60)
    print("VERIFICATION")
    verify = sqlite3.connect(new_db_path)
    tables = ['seasons', 'players', 'teams', 'rosters', 'games',
              'batting', 'pitching', 'news', 'photos', 'honor_roll']
    for t in tables:
        count = verify.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t:20s} {count:>8,} rows")
    verify.close()
    print("\nMIGRATION COMPLETE.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Migrate D1 softball database')
    parser.add_argument('--old', required=True, help='Path to old softball_stats.db')
    parser.add_argument('--new', default='d1softball.db', help='Path for new database')
    parser.add_argument('--dry-run', action='store_true', help='Preview only, no writes')
    args = parser.parse_args()
    migrate(args.old, args.new, args.dry_run)
