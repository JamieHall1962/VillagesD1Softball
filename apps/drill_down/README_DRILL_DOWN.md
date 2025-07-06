# 🏟️ D1 Softball Drill-Down Statistics Application

A comprehensive web application for browsing 18 years of softball statistics with intuitive drill-down navigation.

## 🎯 Features

### **Players Section**
- **Level 1**: All 600+ players with career totals
- **Level 2**: Individual player → Season totals  
- **Level 3**: Season → Game-by-game statistics

### **Seasons Section**
- **Level 1**: All seasons listed
- **Level 2**: Season → Final standings with clickable teams
- **Level 3**: Team → Rosters, batting stats, pitching stats, game scores

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- PostgreSQL database with the migrated All-Pro data
- The `apssb_postgres_migration.tar.gz` data should be imported

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python setup_database.py
```
This will prompt you for your PostgreSQL connection details and create a `.env` file.

### 4. Run the Application
```bash
python drill_down_app.py
```

### 5. Access the Application
Open your browser and go to: `http://localhost:5000`

## 📊 Data Structure

The application connects to these key PostgreSQL tables:

- **`people`** - Player information (600+ players)
- **`battingstats`** - Individual game batting statistics
- **`pitchingstats`** - Individual game pitching statistics  
- **`teams`** - Team information
- **`gamestats`** - Game results and metadata

## 🎨 User Interface

### Modern Design
- Responsive Bootstrap 5 interface
- Beautiful gradient backgrounds
- Smooth hover animations
- Intuitive breadcrumb navigation

### Drill-Down Navigation
- **Players**: Browse all players → Select player → View seasons → View games
- **Seasons**: Browse all seasons → Select season → View standings → Select team → View details

### Statistics Display
- Career totals for players
- Season-by-season breakdowns
- Game-by-game statistics
- Team standings and rosters
- Batting and pitching statistics

## 🔧 Configuration

The application uses environment variables for database configuration. Create a `.env` file:

```env
DB_HOST=localhost
DB_NAME=apssb_db
DB_USER=postgres
DB_PASSWORD=your_password
```

## 📈 Sample Data Views

### Player Career View
- Games played, batting average, home runs, RBI
- Sortable by any statistic
- Click to drill down to seasons

### Season Standings
- Win/loss records
- Win percentage
- Games played
- Click teams to see detailed statistics

### Team Details
- Complete roster with games played
- Batting statistics for all players
- Pitching statistics for all players
- Recent game results

## 🛠️ Development

### Project Structure
```
d1softball/
├── drill_down_app.py          # Main Flask application
├── setup_database.py          # Database setup script
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Main web interface
├── postgres_migration/        # Database schema and data
└── README_DRILL_DOWN.md      # This file
```

### API Endpoints
- `GET /api/players` - Get all players with career totals
- `GET /api/players/<id>/seasons` - Get seasons for a player
- `GET /api/players/<id>/seasons/<year>/games` - Get games for a player in a season
- `GET /api/seasons` - Get all seasons
- `GET /api/seasons/<year>/standings` - Get standings for a season
- `GET /api/teams/<id>/season/<year>` - Get team details for a season

## 🎯 Key Statistics Available

### Batting Statistics
- Plate appearances, at bats, runs, hits
- Doubles, triples, home runs, RBI
- Walks, strikeouts, stolen bases
- Batting average, on-base percentage

### Pitching Statistics  
- Innings pitched, batters faced
- Runs, earned runs, hits, walks
- Strikeouts, wins, losses, saves
- ERA, WHIP

### Team Statistics
- Win/loss records and percentages
- Games played
- Team rosters
- Game-by-game results

## 🔍 Search and Filter

The interface provides:
- Easy navigation through breadcrumbs
- Sortable statistics tables
- Responsive design for all devices
- Quick access to detailed information

## 🚀 Future Enhancements

### Advanced Filtering Options (Planned)
- **Season range filters** - "Show players from 2010-2015"
- **Minimum thresholds** - "Show players with 50+ games played" or "Batting average > .400"
- **Team filters** - "Show only Avalanche players"
- **Career vs. Active** - Filter out retired players
- **Stat combinations** - "Show players with 10+ HR AND .300+ average"
- **Export functionality** - Download filtered results as CSV/Excel

### Statistical Calculations (Pending Decision)
- **On-Base Percentage (OBP)** - Currently calculated as (H + BB) / PA
  - **Question**: Should OE (Reached on Error) be included in OBP calculation?
  - **Current**: OE is tracked but not included in OBP (baseball standard)
  - **League Discussion**: Board meeting pending to determine if OE should count for OBP
  - **Impact**: Would change OBP = (H + BB + OE) / PA if approved

### Other Potential Additions
- Statistical comparisons between players
- Season-over-season trends
- Mobile app version
- Advanced search with multiple criteria

## 📞 Support

If you encounter any issues:
1. Check that PostgreSQL is running
2. Verify the database contains the migrated data
3. Ensure all dependencies are installed
4. Check the `.env` file configuration

## 🏆 About the Data

This application provides access to 18 years of D1 softball statistics from the original All-Pro Softball database, containing:
- 600+ players
- Thousands of games
- Complete batting and pitching records
- Team standings and rosters

The data has been migrated from the legacy Microsoft Access format to PostgreSQL for modern web access. 