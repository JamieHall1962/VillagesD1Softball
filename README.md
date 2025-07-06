# 🏟️ D1 Softball Management System

A comprehensive system for managing D1 softball league operations, including historical statistics and future scheduling.

## 📁 Project Structure

```
d1softball/
├── apps/
│   ├── drill_down/           # Historical statistics drill-down application
│   │   ├── drill_down_app.py
│   │   ├── setup_database.py
│   │   ├── start_app.py
│   │   ├── requirements.txt
│   │   ├── README_DRILL_DOWN.md
│   │   ├── schema.sql
│   │   ├── import_data.sql
│   │   ├── data/ (71 CSV files)
│   │   └── templates/
│   │       └── index.html
│   └── scheduler/            # Future season scheduling application
│       ├── scheduler.py
│       └── requirements.txt
├── access_to_postgresql_migration_package/  # Professional migration package
├── postgres_migration/       # Original migration files
├── apssb.mdb                # Original All-Pro database
├── apssb_backup.mdb         # Backup of original database
└── README.md                # This file
```

## 🎯 Applications

### 1. Drill-Down Statistics Application
**Location**: `apps/drill_down/`

A comprehensive web application for browsing 18 years of softball statistics with intuitive drill-down navigation.

**Features**:
- **Players Section**: Browse all 600+ players → View seasons → View game-by-game stats
- **Seasons Section**: Browse all seasons → View standings → View team details
- Modern web interface with responsive design
- Complete batting and pitching statistics

**Quick Start**:
```bash
cd apps/drill_down
pip install -r requirements.txt
python setup_database.py
python start_app.py
```

### 2. Schedule Generator Application
**Location**: `apps/scheduler/`

Advanced constraint-based scheduling system for creating balanced league schedules.

**Features**:
- Balanced home/away game distribution
- Holiday and date avoidance
- Multiple export formats (CSV, JSON)
- Team-specific schedule views
- Constraint programming optimization

**Quick Start**:
```bash
cd apps/scheduler
pip install -r requirements.txt
python scheduler.py
```

## 🗄️ Database

The system uses PostgreSQL to store the migrated All-Pro Softball database containing:
- 600+ players
- 18 years of game data
- Complete batting and pitching statistics
- Team standings and rosters

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Migrated All-Pro data (included in `access_to_postgresql_migration_package/`)

### Installation

1. **Clone or download the project**
2. **Set up the database**:
   ```bash
   cd apps/drill_down
   python setup_database.py
   ```
3. **Install application dependencies**:
   ```bash
   # For drill-down app
   cd apps/drill_down
   pip install -r requirements.txt
   
   # For scheduler app
   cd apps/scheduler
   pip install -r requirements.txt
   ```

### Running the Applications

**Drill-Down Statistics**:
```bash
cd apps/drill_down
python start_app.py
# Open http://localhost:5000
```

**Schedule Generator**:
```bash
cd apps/scheduler
python scheduler.py
```

## 📊 Data Overview

The system provides access to:
- **Historical Data**: 18 years of complete game statistics
- **Player Statistics**: Career totals, season breakdowns, game-by-game stats
- **Team Statistics**: Standings, rosters, batting/pitching stats
- **Schedule Management**: Future season planning and optimization

## 🔧 Development

Each application is self-contained with its own:
- Dependencies (`requirements.txt`)
- Documentation (`README.md`)
- Configuration files

## 📞 Support

For issues or questions:
1. Check the individual application README files
2. Verify database connectivity
3. Ensure all dependencies are installed

## 🏆 About the Data

This system provides access to the complete D1 softball league history, migrated from the original All-Pro Softball database (2007-2025) to modern web-accessible formats. 