# D1 Softball Stats App - Clean Backup

This is a clean backup of the D1 Softball Stats Application with all essential files.

## What's Included

- **Flask Web Application** (`apps/drill_down/simple_csv_app.py`) - Complete stats app with all features
- **All CSV Data Files** (`apps/drill_down/data/`) - 18 years of softball statistics
- **HTML Templates** (`apps/drill_down/templates/`) - All web pages and styling
- **Requirements** (`apps/drill_down/requirements.txt`) - Python dependencies
- **Launcher Scripts** (`start_app.py`, `start_app.bat`) - Easy startup

## Features

- **Players Page** - Complete player stats with sorting and search
- **Player Detail Pages** - Individual player career breakdowns
- **Seasons Page** - All seasons with standings
- **Team Detail Pages** - Team rosters and stats
- **Game Logs** - Individual player and team game results
- **Easter Eggs** - Konami code for lineups, 'record' for W/L records
- **Responsive Design** - Works on desktop and mobile

## Quick Start

1. **Install Python dependencies:**
   ```bash
   cd apps/drill_down
   pip install -r requirements.txt
   ```

2. **Start the app:**
   ```bash
   # From root directory:
   python start_app.py
   
   # Or from drill_down directory:
   python simple_csv_app.py
   ```

3. **Open in browser:** `http://localhost:5000`

## Data Structure

The app reads directly from CSV files:
- `People.csv` - Player information
- `BattingStats.csv` - Batting statistics
- `GameStats.csv` - Game results
- `Teams.csv` - Team information
- `Filters.csv` - Season information

## Deployment

This app is ready for deployment to:
- **Render** (recommended)
- **Heroku**
- **Railway**
- Any Python web hosting service

## Backup Information

- **Created:** July 6, 2025
- **Branch:** `clean-backup-20250706`
- **Status:** All features working, ready for deployment

## Notes

- All 18 years of D1 Softball data included
- U2 correction implemented for accurate games played
- Season ordering: Winter, Summer, Fall
- Proper formatting for averages (.563 instead of 0.563)
- Sticky headers and responsive design 