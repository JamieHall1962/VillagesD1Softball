-- PostgreSQL Data Import Script
-- Imports all data from CSV files
-- Generated for Access to PostgreSQL Migration

\set ON_ERROR_STOP off
SET client_encoding = 'UTF8';
SET datestyle = 'MDY';

-- Change to data directory
\cd data

\echo 'Starting data import...'
\echo 'This may take several minutes depending on data size.'
\echo ''

-- Import all tables
\echo 'Importing battingrptcats...'
\COPY "battingrptcats" FROM 'battingrptcats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing battingrptformat...'
\COPY "battingrptformat" FROM 'battingrptformat.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing battingstats (79,104 rows)...'
\COPY "battingstats" FROM 'battingstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crbpfstats...'
\COPY "crbpfstats" FROM 'crbpfstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crbpfstatsdetail...'
\COPY "crbpfstatsdetail" FROM 'crbpfstatsdetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crboxscores...'
\COPY "crboxscores" FROM 'crboxscores.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crboxscoresdetail...'
\COPY "crboxscoresdetail" FROM 'crboxscoresdetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crgamescores...'
\COPY "crgamescores" FROM 'crgamescores.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crgamescoresdetail...'
\COPY "crgamescoresdetail" FROM 'crgamescoresdetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crleaderstats...'
\COPY "crleaderstats" FROM 'crleaderstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crlineup...'
\COPY "crlineup" FROM 'crlineup.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crlineupdetail...'
\COPY "crlineupdetail" FROM 'crlineupdetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crplayerheadingindex...'
\COPY "crplayerheadingindex" FROM 'crplayerheadingindex.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crplayerheadingstats...'
\COPY "crplayerheadingstats" FROM 'crplayerheadingstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crplayerstatsdetail...'
\COPY "crplayerstatsdetail" FROM 'crplayerstatsdetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crrecord...'
\COPY "crrecord" FROM 'crrecord.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crrecorddetail...'
\COPY "crrecorddetail" FROM 'crrecorddetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crroster...'
\COPY "crroster" FROM 'crroster.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crrosterdetail...'
\COPY "crrosterdetail" FROM 'crrosterdetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crscorebyinnings...'
\COPY "crscorebyinnings" FROM 'crscorebyinnings.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crscorebyinningsdetail...'
\COPY "crscorebyinningsdetail" FROM 'crscorebyinningsdetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crstandings...'
\COPY "crstandings" FROM 'crstandings.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing crstandingsdetail...'
\COPY "crstandingsdetail" FROM 'crstandingsdetail.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing catindex...'
\COPY "catindex" FROM 'catindex.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing compactcount...'
\COPY "compactcount" FROM 'compactcount.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing fieldingrptcats...'
\COPY "fieldingrptcats" FROM 'fieldingrptcats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing fieldingrptformat...'
\COPY "fieldingrptformat" FROM 'fieldingrptformat.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing fieldingstats (3,223 rows)...'
\COPY "fieldingstats" FROM 'fieldingstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing filters...'
\COPY "filters" FROM 'filters.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing gamelineup...'
\COPY "gamelineup" FROM 'gamelineup.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing gamestats (7,686 rows)...'
\COPY "gamestats" FROM 'gamestats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing gametypes...'
\COPY "gametypes" FROM 'gametypes.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing inputorder...'
\COPY "inputorder" FROM 'inputorder.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing internetdocuments...'
\COPY "internetdocuments" FROM 'internetdocuments.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing internetoptions...'
\COPY "internetoptions" FROM 'internetoptions.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing internetteams...'
\COPY "internetteams" FROM 'internetteams.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing leadercats...'
\COPY "leadercats" FROM 'leadercats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing leaderstats...'
\COPY "leaderstats" FROM 'leaderstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing lineup...'
\COPY "lineup" FROM 'lineup.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing lineupplayer...'
\COPY "lineupplayer" FROM 'lineupplayer.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing memooptions...'
\COPY "memooptions" FROM 'memooptions.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing nameyourowncats...'
\COPY "nameyourowncats" FROM 'nameyourowncats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing nameyourownstats...'
\COPY "nameyourownstats" FROM 'nameyourownstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing numberoptions...'
\COPY "numberoptions" FROM 'numberoptions.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing people...'
\COPY "people" FROM 'people.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing picturegallery...'
\COPY "picturegallery" FROM 'picturegallery.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing pitchingrptcats...'
\COPY "pitchingrptcats" FROM 'pitchingrptcats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing pitchingrptformat...'
\COPY "pitchingrptformat" FROM 'pitchingrptformat.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing pitchingstats (7,763 rows)...'
\COPY "pitchingstats" FROM 'pitchingstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing programversion...'
\COPY "programversion" FROM 'programversion.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rtbattingstats...'
\COPY "rtbattingstats" FROM 'rtbattingstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rtfieldingstats...'
\COPY "rtfieldingstats" FROM 'rtfieldingstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rtgamestats...'
\COPY "rtgamestats" FROM 'rtgamestats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rtgamestatsxinnings...'
\COPY "rtgamestatsxinnings" FROM 'rtgamestatsxinnings.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rtpitchingstats...'
\COPY "rtpitchingstats" FROM 'rtpitchingstats.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing reportnumber...'
\COPY "reportnumber" FROM 'reportnumber.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing roster (5,688 rows)...'
\COPY "roster" FROM 'roster.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptbatting...'
\COPY "rptbatting" FROM 'rptbatting.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptboxscores...'
\COPY "rptboxscores" FROM 'rptboxscores.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptfielding...'
\COPY "rptfielding" FROM 'rptfielding.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptinnings...'
\COPY "rptinnings" FROM 'rptinnings.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptlineup...'
\COPY "rptlineup" FROM 'rptlineup.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptpitching...'
\COPY "rptpitching" FROM 'rptpitching.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptrecord...'
\COPY "rptrecord" FROM 'rptrecord.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptroster...'
\COPY "rptroster" FROM 'rptroster.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptscores...'
\COPY "rptscores" FROM 'rptscores.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing rptstandings...'
\COPY "rptstandings" FROM 'rptstandings.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing spray...'
\COPY "spray" FROM 'spray.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing stringoptions...'
\COPY "stringoptions" FROM 'stringoptions.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing teamfilters...'
\COPY "teamfilters" FROM 'teamfilters.csv' WITH (FORMAT CSV, HEADER true);

\echo 'Importing teams...'
\COPY "teams" FROM 'teams.csv' WITH (FORMAT CSV, HEADER true);

-- Return to original directory
\cd ..

-- Update statistics
ANALYZE;

\echo ''
\echo 'Data import completed!'
\echo ''