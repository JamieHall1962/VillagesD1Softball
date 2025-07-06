-- ----------------------------------------------------------
-- MDB Tools - A library for reading MS Access database files
-- Copyright (C) 2000-2011 Brian Bruns and others.
-- Files in libmdb are licensed under LGPL and the utilities under
-- the GPL, see COPYING.LIB and COPYING files respectively.
-- Check out http://mdbtools.sourceforge.net
-- ----------------------------------------------------------

SET client_encoding = 'UTF-8';

CREATE TABLE IF NOT EXISTS "battingrptcats"
 (
	"reportnumber"			INTEGER, 
	"reportorder"			SMALLINT, 
	"categorynumber"			SMALLINT
);
COMMENT ON COLUMN "battingrptcats"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "battingrptcats"."reportorder" IS 'Report Order';
COMMENT ON COLUMN "battingrptcats"."categorynumber" IS 'Category Number';

-- CREATE INDEXES ...
ALTER TABLE "battingrptcats" ADD CONSTRAINT "battingrptcats_pkey" PRIMARY KEY ("reportnumber", "reportorder");

CREATE TABLE IF NOT EXISTS "battingrptformat"
 (
	"reportnumber"			INTEGER, 
	"reportdescription"			VARCHAR (25), 
	"sortcategory"			SMALLINT, 
	"sortdirection"			VARCHAR (1)
);
COMMENT ON COLUMN "battingrptformat"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "battingrptformat"."reportdescription" IS 'Report Description';
COMMENT ON COLUMN "battingrptformat"."sortcategory" IS 'Sort Category';
COMMENT ON COLUMN "battingrptformat"."sortdirection" IS 'Sort Direction';

-- CREATE INDEXES ...
ALTER TABLE "battingrptformat" ADD CONSTRAINT "battingrptformat_pkey" PRIMARY KEY ("reportnumber");
CREATE UNIQUE INDEX "battingrptformat_reportnumber_idx" ON "battingrptformat" ("reportnumber");

CREATE TABLE IF NOT EXISTS "catindex"
 (
	"stattype"			INTEGER, 
	"stat"			VARCHAR (10), 
	"categorynumber"			INTEGER, 
	"format"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "compactcount"
 (
	"compactcounter"			INTEGER
);
COMMENT ON COLUMN "compactcount"."compactcounter" IS 'Compact Counter';

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "crboxscores"
 (
	"reportidnumber"			INTEGER, 
	"reporttitle"			VARCHAR (100), 
	"teamtitle"			VARCHAR (100), 
	"reportdate"			VARCHAR (25), 
	"headingbatting"			VARCHAR (10), 
	"headingbatpa"			VARCHAR (3), 
	"headingbatab"			VARCHAR (3), 
	"headingbatr"			VARCHAR (3), 
	"headingbath"			VARCHAR (3), 
	"headingbat2b"			VARCHAR (3), 
	"headingbat3b"			VARCHAR (3), 
	"headingbathr"			VARCHAR (3), 
	"headingbattb"			VARCHAR (3), 
	"headingbatoe"			VARCHAR (3), 
	"headingbatfc"			VARCHAR (3), 
	"headingbatbb"			VARCHAR (3), 
	"headingbathp"			VARCHAR (3), 
	"headingbatso"			VARCHAR (3), 
	"headingbatsh"			VARCHAR (3), 
	"headingbatsf"			VARCHAR (3), 
	"headingbatdp"			VARCHAR (3), 
	"headingbatsb"			VARCHAR (3), 
	"headingbatcs"			VARCHAR (3), 
	"headingbatrbi"			VARCHAR (3), 
	"headingbatobp"			VARCHAR (3), 
	"headingbatslg"			VARCHAR (3), 
	"headingbatba"			VARCHAR (3), 
	"headingpitching"			VARCHAR (10), 
	"headingpitchip"			VARCHAR (3), 
	"headingpitchr"			VARCHAR (3), 
	"headingpitcher"			VARCHAR (3), 
	"headingpitchbf"			VARCHAR (3), 
	"headingpitchab"			VARCHAR (3), 
	"headingpitchh"			VARCHAR (3), 
	"headingpitch2b"			VARCHAR (3), 
	"headingpitch3b"			VARCHAR (3), 
	"headingpitchhr"			VARCHAR (3), 
	"headingpitchbb"			VARCHAR (3), 
	"headingpitchhb"			VARCHAR (3), 
	"headingpitchso"			VARCHAR (3), 
	"headingpitchwp"			VARCHAR (3), 
	"headingpitchbk"			VARCHAR (3), 
	"headingpitchpo"			VARCHAR (3), 
	"headingpitchb"			VARCHAR (3), 
	"headingpitchs"			VARCHAR (3), 
	"headingpitchtp"			VARCHAR (3), 
	"headingpitchobp"			VARCHAR (3), 
	"headingpitchslg"			VARCHAR (3), 
	"headingpitchba"			VARCHAR (3), 
	"headingpitchera"			VARCHAR (3)
);

-- CREATE INDEXES ...
ALTER TABLE "crboxscores" ADD CONSTRAINT "crboxscores_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crboxscoresdetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"battingplayer"			VARCHAR (50), 
	"batpa"			VARCHAR (7), 
	"batab"			VARCHAR (7), 
	"batr"			VARCHAR (7), 
	"bath"			VARCHAR (7), 
	"bat2b"			VARCHAR (7), 
	"bat3b"			VARCHAR (7), 
	"bathr"			VARCHAR (7), 
	"battb"			VARCHAR (7), 
	"batoe"			VARCHAR (7), 
	"batfc"			VARCHAR (7), 
	"batbb"			VARCHAR (7), 
	"bathp"			VARCHAR (7), 
	"batso"			VARCHAR (7), 
	"batsh"			VARCHAR (7), 
	"batsf"			VARCHAR (7), 
	"batdp"			VARCHAR (7), 
	"batsb"			VARCHAR (7), 
	"batcs"			VARCHAR (7), 
	"batrbi"			VARCHAR (7), 
	"batobp"			VARCHAR (7), 
	"batslg"			VARCHAR (7), 
	"batba"			VARCHAR (7), 
	"pitchingplayer"			VARCHAR (50), 
	"pitchip"			VARCHAR (9), 
	"pitchr"			VARCHAR (7), 
	"pitcher"			VARCHAR (7), 
	"pitchbf"			VARCHAR (7), 
	"pitchab"			VARCHAR (7), 
	"pitchh"			VARCHAR (7), 
	"pitch2b"			VARCHAR (7), 
	"pitch3b"			VARCHAR (7), 
	"pitchhr"			VARCHAR (7), 
	"pitchbb"			VARCHAR (7), 
	"pitchhb"			VARCHAR (7), 
	"pitchso"			VARCHAR (7), 
	"pitchwp"			VARCHAR (7), 
	"pitchbk"			VARCHAR (7), 
	"pitchpo"			VARCHAR (7), 
	"pitchb"			VARCHAR (7), 
	"pitchs"			VARCHAR (7), 
	"pitchtp"			VARCHAR (7), 
	"pitchobp"			VARCHAR (7), 
	"pitchslg"			VARCHAR (7), 
	"pitchba"			VARCHAR (7), 
	"pitchera"			VARCHAR (7)
);

-- CREATE INDEXES ...
ALTER TABLE "crboxscoresdetail" ADD CONSTRAINT "crboxscoresdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crbpfstatsdetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"playername"			VARCHAR (50), 
	"teamname"			VARCHAR (50), 
	"centertext"			VARCHAR (50), 
	"g"			VARCHAR (7), 
	"pa"			VARCHAR (7), 
	"bf"			VARCHAR (7), 
	"ab"			VARCHAR (7), 
	"r"			VARCHAR (7), 
	"h"			VARCHAR (7), 
	"s"			VARCHAR (7), 
	"d"			VARCHAR (7), 
	"t"			VARCHAR (7), 
	"hr"			VARCHAR (7), 
	"tb"			VARCHAR (7), 
	"oe"			VARCHAR (7), 
	"fc"			VARCHAR (7), 
	"bb"			VARCHAR (7), 
	"hp"			VARCHAR (7), 
	"hb"			VARCHAR (7), 
	"co"			VARCHAR (7), 
	"so"			VARCHAR (7), 
	"sh"			VARCHAR (7), 
	"sf"			VARCHAR (7), 
	"dp"			VARCHAR (7), 
	"sb"			VARCHAR (7), 
	"cs"			VARCHAR (7), 
	"rbi"			VARCHAR (7), 
	"chs"			VARCHAR (7), 
	"lhs"			VARCHAR (7), 
	"c"			VARCHAR (7), 
	"a"			VARCHAR (7), 
	"e"			VARCHAR (7), 
	"pb"			VARCHAR (7), 
	"ip"			VARCHAR (9), 
	"er"			VARCHAR (7), 
	"wp"			VARCHAR (7), 
	"bk"			VARCHAR (7), 
	"po"			VARCHAR (7), 
	"pickoff"			VARCHAR (7), 
	"ball"			VARCHAR (7), 
	"strike"			VARCHAR (7), 
	"tp"			VARCHAR (7), 
	"gs"			VARCHAR (7), 
	"gf"			VARCHAR (7), 
	"cg"			VARCHAR (7), 
	"w"			VARCHAR (7), 
	"l"			VARCHAR (7), 
	"sv"			VARCHAR (7), 
	"sho"			VARCHAR (7), 
	"ba"			VARCHAR (7), 
	"fa"			VARCHAR (7), 
	"obp"			VARCHAR (7), 
	"slg"			VARCHAR (7), 
	"pp"			VARCHAR (7), 
	"rc"			VARCHAR (7), 
	"ta"			VARCHAR (7), 
	"sba"			VARCHAR (7), 
	"csa"			VARCHAR (7), 
	"rng"			VARCHAR (7), 
	"era"			VARCHAR (7), 
	"sog"			VARCHAR (7), 
	"whip"			VARCHAR (7), 
	"spct"			VARCHAR (7), 
	"user1"			VARCHAR (7), 
	"user2"			VARCHAR (7), 
	"user3"			VARCHAR (7), 
	"user4"			VARCHAR (7), 
	"user5"			VARCHAR (7), 
	"users1"			VARCHAR (7), 
	"users2"			VARCHAR (7), 
	"users3"			VARCHAR (7), 
	"users4"			VARCHAR (7), 
	"users5"			VARCHAR (7)
);

-- CREATE INDEXES ...
ALTER TABLE "crbpfstatsdetail" ADD CONSTRAINT "crbpfstatsdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crgamescores"
 (
	"reportidnumber"			INTEGER, 
	"reporttitle"			VARCHAR (100), 
	"teamtitle"			VARCHAR (100), 
	"reportdate"			VARCHAR (25)
);

-- CREATE INDEXES ...
ALTER TABLE "crgamescores" ADD CONSTRAINT "crgamescores_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crgamescoresdetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"gamenumber"			VARCHAR (5), 
	"gamedescription"			TEXT, 
	"team"			VARCHAR (50), 
	"runs"			VARCHAR (10), 
	"decision"			VARCHAR (5)
);

-- CREATE INDEXES ...
ALTER TABLE "crgamescoresdetail" ADD CONSTRAINT "crgamescoresdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crleaderstats"
 (
	"reportid"			INTEGER, 
	"reporttitle"			VARCHAR (30), 
	"teamtitle"			VARCHAR (30), 
	"reportdate"			TIMESTAMP WITHOUT TIME ZONE, 
	"topxrecords"			INTEGER, 
	"minimumtype"			VARCHAR (1), 
	"minimumnumber"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "crlineupdetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"lineuporder"			VARCHAR (3), 
	"playername"			VARCHAR (50), 
	"inn1"			VARCHAR (5), 
	"inn2"			VARCHAR (5), 
	"inn3"			VARCHAR (5), 
	"inn4"			VARCHAR (5), 
	"inn5"			VARCHAR (5), 
	"inn6"			VARCHAR (5), 
	"inn7"			VARCHAR (5), 
	"inn8"			VARCHAR (5), 
	"inn9"			VARCHAR (5)
);

-- CREATE INDEXES ...
ALTER TABLE "crlineupdetail" ADD CONSTRAINT "crlineupdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crplayerheadingindex"
 (
	"playernumber"			INTEGER, 
	"categorynumber"			INTEGER, 
	"sortorder"			INTEGER, 
	"stattype"			INTEGER
);

-- CREATE INDEXES ...
ALTER TABLE "crplayerheadingindex" ADD CONSTRAINT "crplayerheadingindex_pkey" PRIMARY KEY ("playernumber", "categorynumber", "stattype");

CREATE TABLE IF NOT EXISTS "crplayerheadingstats"
 (
	"playernumber"			INTEGER, 
	"sh1"			VARCHAR (20), 
	"sh2"			VARCHAR (20), 
	"sh3"			VARCHAR (20), 
	"sh4"			VARCHAR (20), 
	"stat1"			VARCHAR (20), 
	"stat2"			VARCHAR (20), 
	"stat3"			VARCHAR (20), 
	"stat4"			VARCHAR (20)
);

-- CREATE INDEXES ...
ALTER TABLE "crplayerheadingstats" ADD CONSTRAINT "crplayerheadingstats_pkey" PRIMARY KEY ("playernumber");

CREATE TABLE IF NOT EXISTS "crplayerstatsdetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"stattype"			INTEGER, 
	"playername"			VARCHAR (50), 
	"playernumber"			INTEGER, 
	"teamname"			VARCHAR (50), 
	"teamnumber"			INTEGER, 
	"opponent"			VARCHAR (50), 
	"gamedate"			VARCHAR (50), 
	"gamenumber"			INTEGER, 
	"g"			VARCHAR (7), 
	"pa"			VARCHAR (7), 
	"bf"			VARCHAR (7), 
	"ab"			VARCHAR (7), 
	"r"			VARCHAR (7), 
	"h"			VARCHAR (7), 
	"s"			VARCHAR (7), 
	"d"			VARCHAR (7), 
	"t"			VARCHAR (7), 
	"hr"			VARCHAR (7), 
	"tb"			VARCHAR (7), 
	"oe"			VARCHAR (7), 
	"fc"			VARCHAR (7), 
	"bb"			VARCHAR (7), 
	"hp"			VARCHAR (7), 
	"hb"			VARCHAR (7), 
	"co"			VARCHAR (7), 
	"so"			VARCHAR (7), 
	"sh"			VARCHAR (7), 
	"sf"			VARCHAR (7), 
	"dp"			VARCHAR (7), 
	"sb"			VARCHAR (7), 
	"cs"			VARCHAR (7), 
	"rbi"			VARCHAR (7), 
	"chs"			VARCHAR (7), 
	"lhs"			VARCHAR (7), 
	"c"			VARCHAR (7), 
	"a"			VARCHAR (7), 
	"e"			VARCHAR (7), 
	"pb"			VARCHAR (7), 
	"ip"			VARCHAR (9), 
	"ip13"			VARCHAR (7), 
	"er"			VARCHAR (7), 
	"wp"			VARCHAR (7), 
	"bk"			VARCHAR (7), 
	"po"			VARCHAR (7), 
	"b"			VARCHAR (7), 
	"tp"			VARCHAR (7), 
	"gs"			VARCHAR (7), 
	"gf"			VARCHAR (7), 
	"cg"			VARCHAR (7), 
	"w"			VARCHAR (7), 
	"l"			VARCHAR (7), 
	"sv"			VARCHAR (7), 
	"sho"			VARCHAR (7), 
	"ba"			VARCHAR (7), 
	"fa"			VARCHAR (7), 
	"obp"			VARCHAR (7), 
	"slg"			VARCHAR (7), 
	"pp"			VARCHAR (7), 
	"rc"			VARCHAR (7), 
	"ta"			VARCHAR (7), 
	"sba"			VARCHAR (7), 
	"csa"			VARCHAR (7), 
	"rng"			VARCHAR (7), 
	"era"			VARCHAR (7), 
	"sog"			VARCHAR (7), 
	"whip"			VARCHAR (7), 
	"spct"			VARCHAR (7), 
	"u1"			VARCHAR (7), 
	"u2"			VARCHAR (7), 
	"u3"			VARCHAR (7), 
	"u4"			VARCHAR (7), 
	"u5"			VARCHAR (7), 
	"us1"			VARCHAR (7), 
	"us2"			VARCHAR (7), 
	"us3"			VARCHAR (7), 
	"us4"			VARCHAR (7), 
	"us5"			VARCHAR (7)
);

-- CREATE INDEXES ...
CREATE INDEX "crplayerstatsdetail_playernumber_idx" ON "crplayerstatsdetail" ("playernumber");
ALTER TABLE "crplayerstatsdetail" ADD CONSTRAINT "crplayerstatsdetail_pkey" PRIMARY KEY ("playernumber", "stattype", "gamenumber", "detaillinenumber");
CREATE INDEX "crplayerstatsdetail_teamnumber_idx" ON "crplayerstatsdetail" ("teamnumber");

CREATE TABLE IF NOT EXISTS "crrecord"
 (
	"reportidnumber"			INTEGER, 
	"reporttitle"			VARCHAR (100), 
	"teamtitle"			VARCHAR (100), 
	"reportdate"			VARCHAR (25), 
	"headingties"			VARCHAR (10), 
	"headingrf"			VARCHAR (20), 
	"headingra"			VARCHAR (20)
);

-- CREATE INDEXES ...
ALTER TABLE "crrecord" ADD CONSTRAINT "crrecord_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crroster"
 (
	"reportidnumber"			INTEGER, 
	"reporttitle"			VARCHAR (100), 
	"teamtitle"			VARCHAR (100), 
	"reportdate"			VARCHAR (25)
);

-- CREATE INDEXES ...
ALTER TABLE "crroster" ADD CONSTRAINT "crroster_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crrosterdetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"playername"			VARCHAR (50), 
	"playernumber"			VARCHAR (3), 
	"addressline1"			VARCHAR (40), 
	"addressline2"			VARCHAR (40), 
	"city"			VARCHAR (20), 
	"state"			VARCHAR (20), 
	"zip"			VARCHAR (20), 
	"homephone"			VARCHAR (20), 
	"workphone"			VARCHAR (20), 
	"email"			VARCHAR (50), 
	"birthdate"			VARCHAR (25), 
	"notes"			TEXT
);

-- CREATE INDEXES ...
ALTER TABLE "crrosterdetail" ADD CONSTRAINT "crrosterdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crscorebyinnings"
 (
	"reportidnumber"			INTEGER, 
	"reporttitle"			VARCHAR (100), 
	"teamtitle"			VARCHAR (100), 
	"reportdate"			VARCHAR (25), 
	"headinginn1"			VARCHAR (3), 
	"headinginn2"			VARCHAR (3), 
	"headinginn3"			VARCHAR (3), 
	"headinginn4"			VARCHAR (3), 
	"headinginn5"			VARCHAR (3), 
	"headinginn6"			VARCHAR (3), 
	"headinginn7"			VARCHAR (3), 
	"headinginn8"			VARCHAR (3), 
	"headinginn9"			VARCHAR (3), 
	"headinginn10"			VARCHAR (3)
);

-- CREATE INDEXES ...
ALTER TABLE "crscorebyinnings" ADD CONSTRAINT "crscorebyinnings_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crscorebyinningsdetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"teamordate"			VARCHAR (50), 
	"inn1"			VARCHAR (6), 
	"inn2"			VARCHAR (6), 
	"inn3"			VARCHAR (6), 
	"inn4"			VARCHAR (6), 
	"inn5"			VARCHAR (6), 
	"inn6"			VARCHAR (6), 
	"inn7"			VARCHAR (6), 
	"inn8"			VARCHAR (6), 
	"inn9"			VARCHAR (6), 
	"inn10"			VARCHAR (6), 
	"finalscore"			VARCHAR (6)
);

-- CREATE INDEXES ...
ALTER TABLE "crscorebyinningsdetail" ADD CONSTRAINT "crscorebyinningsdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crstandingsdetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"team"			VARCHAR (50), 
	"gameswon"			VARCHAR (10), 
	"gameslost"			VARCHAR (10), 
	"gamestied"			VARCHAR (10), 
	"streak"			VARCHAR (10), 
	"winpct"			VARCHAR (10), 
	"runsfor"			VARCHAR (10), 
	"runsagainst"			VARCHAR (10), 
	"gamesbehind"			VARCHAR (10)
);

-- CREATE INDEXES ...
ALTER TABLE "crstandingsdetail" ADD CONSTRAINT "crstandingsdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "fieldingrptcats"
 (
	"reportnumber"			INTEGER, 
	"reportorder"			SMALLINT, 
	"categorynumber"			SMALLINT
);
COMMENT ON COLUMN "fieldingrptcats"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "fieldingrptcats"."reportorder" IS 'Report Order';
COMMENT ON COLUMN "fieldingrptcats"."categorynumber" IS 'Category Number';

-- CREATE INDEXES ...
ALTER TABLE "fieldingrptcats" ADD CONSTRAINT "fieldingrptcats_pkey" PRIMARY KEY ("reportnumber", "reportorder");

CREATE TABLE IF NOT EXISTS "fieldingrptformat"
 (
	"reportnumber"			INTEGER, 
	"reportdescription"			VARCHAR (25), 
	"sortcategory"			SMALLINT, 
	"sortdirection"			VARCHAR (1)
);
COMMENT ON COLUMN "fieldingrptformat"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "fieldingrptformat"."reportdescription" IS 'Report Description';
COMMENT ON COLUMN "fieldingrptformat"."sortcategory" IS 'Sort Category';
COMMENT ON COLUMN "fieldingrptformat"."sortdirection" IS 'Sort Direction';

-- CREATE INDEXES ...
ALTER TABLE "fieldingrptformat" ADD CONSTRAINT "fieldingrptformat_pkey" PRIMARY KEY ("reportnumber", "reportdescription");
CREATE UNIQUE INDEX "fieldingrptformat_reportnumber_idx" ON "fieldingrptformat" ("reportnumber");

CREATE TABLE IF NOT EXISTS "fieldingstats"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"eventnumber"			SMALLINT, 
	"gametype"			INTEGER, 
	"hometeam"			BOOLEAN, 
	"starter"			BOOLEAN, 
	"fieldingposition"			SMALLINT, 
	"po"			INTEGER, 
	"a"			INTEGER, 
	"e"			INTEGER, 
	"dp"			INTEGER, 
	"pb"			INTEGER, 
	"sb"			INTEGER, 
	"cs"			INTEGER, 
	"u1"			INTEGER, 
	"u2"			INTEGER, 
	"u3"			INTEGER, 
	"u4"			INTEGER, 
	"u5"			INTEGER, 
	"u6"			INTEGER, 
	"u7"			INTEGER, 
	"u8"			INTEGER, 
	"u9"			INTEGER, 
	"u10"			INTEGER, 
	"notes"			TEXT
);
COMMENT ON COLUMN "fieldingstats"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "fieldingstats"."gamenumber" IS 'Game Number';
COMMENT ON COLUMN "fieldingstats"."playernumber" IS 'Player Number';
COMMENT ON COLUMN "fieldingstats"."eventnumber" IS 'Event Number';
COMMENT ON COLUMN "fieldingstats"."gametype" IS 'Game Type';
COMMENT ON COLUMN "fieldingstats"."hometeam" IS 'Home Team';
COMMENT ON COLUMN "fieldingstats"."starter" IS 'Starter';
COMMENT ON COLUMN "fieldingstats"."fieldingposition" IS 'Primary Fielding Position';
COMMENT ON COLUMN "fieldingstats"."po" IS 'Put Outs';
COMMENT ON COLUMN "fieldingstats"."a" IS 'Assists';
COMMENT ON COLUMN "fieldingstats"."e" IS 'Errors';
COMMENT ON COLUMN "fieldingstats"."dp" IS 'Double Plays';
COMMENT ON COLUMN "fieldingstats"."pb" IS 'Pass Balls';
COMMENT ON COLUMN "fieldingstats"."sb" IS 'Stolen Bases';
COMMENT ON COLUMN "fieldingstats"."cs" IS 'Caught Stealing';
COMMENT ON COLUMN "fieldingstats"."u1" IS 'User Defined 1';
COMMENT ON COLUMN "fieldingstats"."u2" IS 'User Defined 2';
COMMENT ON COLUMN "fieldingstats"."u3" IS 'User Defined 3';
COMMENT ON COLUMN "fieldingstats"."u4" IS 'User Defined 4';
COMMENT ON COLUMN "fieldingstats"."u5" IS 'User Defined 5';
COMMENT ON COLUMN "fieldingstats"."u6" IS 'User Defined 6';
COMMENT ON COLUMN "fieldingstats"."u7" IS 'User Defined 7';
COMMENT ON COLUMN "fieldingstats"."u8" IS 'User Defined 8';
COMMENT ON COLUMN "fieldingstats"."u9" IS 'User Defined 9';
COMMENT ON COLUMN "fieldingstats"."u10" IS 'User Defined 10';
COMMENT ON COLUMN "fieldingstats"."notes" IS 'Notes';

-- CREATE INDEXES ...
CREATE INDEX "fieldingstats_eventnumber_idx" ON "fieldingstats" ("eventnumber");
CREATE INDEX "fieldingstats_gamenumber_idx" ON "fieldingstats" ("gamenumber");
CREATE INDEX "fieldingstats_playernumber_idx" ON "fieldingstats" ("playernumber");
ALTER TABLE "fieldingstats" ADD CONSTRAINT "fieldingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber", "eventnumber");
CREATE INDEX "fieldingstats_teamnumber_idx" ON "fieldingstats" ("teamnumber");

CREATE TABLE IF NOT EXISTS "gamelineup"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"lineupnumber"			INTEGER, 
	"starter"			BOOLEAN, 
	"fieldingposition"			SMALLINT, 
	"fieldingposition2"			SMALLINT, 
	"fieldingposition3"			SMALLINT, 
	"fieldingposition4"			SMALLINT, 
	"batting"			BOOLEAN, 
	"pitchingorder"			INTEGER
);
COMMENT ON COLUMN "gamelineup"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "gamelineup"."gamenumber" IS 'Game Number';
COMMENT ON COLUMN "gamelineup"."playernumber" IS 'Player Number';
COMMENT ON COLUMN "gamelineup"."lineupnumber" IS 'Lineup Number';
COMMENT ON COLUMN "gamelineup"."starter" IS 'Starter';
COMMENT ON COLUMN "gamelineup"."fieldingposition" IS 'Primary Fielding Position';
COMMENT ON COLUMN "gamelineup"."fieldingposition2" IS '2nd Fielding Position';
COMMENT ON COLUMN "gamelineup"."fieldingposition3" IS '3rd Fielding Position';
COMMENT ON COLUMN "gamelineup"."fieldingposition4" IS '4th Fielding Position';

-- CREATE INDEXES ...
CREATE INDEX "gamelineup_gamenumber_idx" ON "gamelineup" ("gamenumber");
CREATE INDEX "gamelineup_pitchingorder_idx" ON "gamelineup" ("pitchingorder");
ALTER TABLE "gamelineup" ADD CONSTRAINT "gamelineup_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber");
CREATE INDEX "gamelineup_teamnumber_idx" ON "gamelineup" ("teamnumber");

CREATE TABLE IF NOT EXISTS "gamestats"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"gstatnumber"			INTEGER, 
	"gamedate"			TIMESTAMP WITHOUT TIME ZONE, 
	"gametype"			INTEGER, 
	"location"			VARCHAR (30), 
	"innings"			SMALLINT, 
	"hometeam"			BOOLEAN, 
	"opponent"			VARCHAR (50), 
	"opponentteamnumber"			INTEGER, 
	"opponentgstatnumber"			INTEGER, 
	"dp"			INTEGER, 
	"runs"			INTEGER, 
	"runsinning1"			SMALLINT, 
	"runsinning2"			SMALLINT, 
	"runsinning3"			SMALLINT, 
	"runsinning4"			SMALLINT, 
	"runsinning5"			SMALLINT, 
	"runsinning6"			SMALLINT, 
	"runsinning7"			SMALLINT, 
	"runsinning8"			SMALLINT, 
	"runsinning9"			SMALLINT, 
	"runsinningx"			SMALLINT, 
	"oppruns"			INTEGER, 
	"opprunsinning1"			SMALLINT, 
	"opprunsinning2"			SMALLINT, 
	"opprunsinning3"			SMALLINT, 
	"opprunsinning4"			SMALLINT, 
	"opprunsinning5"			SMALLINT, 
	"opprunsinning6"			SMALLINT, 
	"opprunsinning7"			SMALLINT, 
	"opprunsinning8"			SMALLINT, 
	"opprunsinning9"			SMALLINT, 
	"opprunsinningx"			SMALLINT, 
	"notes"			TEXT
);
COMMENT ON COLUMN "gamestats"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "gamestats"."gamenumber" IS 'Game Number';
COMMENT ON COLUMN "gamestats"."gstatnumber" IS 'GStat Number';
COMMENT ON COLUMN "gamestats"."gamedate" IS 'Game Date';
COMMENT ON COLUMN "gamestats"."gametype" IS 'Game Type';
COMMENT ON COLUMN "gamestats"."location" IS 'Location';
COMMENT ON COLUMN "gamestats"."innings" IS 'Innings Played';
COMMENT ON COLUMN "gamestats"."hometeam" IS 'Home Team';
COMMENT ON COLUMN "gamestats"."opponent" IS 'Opponents';
COMMENT ON COLUMN "gamestats"."opponentteamnumber" IS 'Opponent Team Number';
COMMENT ON COLUMN "gamestats"."opponentgstatnumber" IS 'Opponent GStat Number';
COMMENT ON COLUMN "gamestats"."dp" IS 'Double Plays';
COMMENT ON COLUMN "gamestats"."runs" IS 'Runs';
COMMENT ON COLUMN "gamestats"."runsinning1" IS 'Runs Inning 1';
COMMENT ON COLUMN "gamestats"."runsinning2" IS 'Runs Inning 2';
COMMENT ON COLUMN "gamestats"."runsinning3" IS 'Runs Inning 3';
COMMENT ON COLUMN "gamestats"."runsinning4" IS 'Runs Inning 4';
COMMENT ON COLUMN "gamestats"."runsinning5" IS 'Runs Inning 5';
COMMENT ON COLUMN "gamestats"."runsinning6" IS 'Runs Inning 6';
COMMENT ON COLUMN "gamestats"."runsinning7" IS 'Runs Inning 7';
COMMENT ON COLUMN "gamestats"."runsinning8" IS 'Runs Inning 8';
COMMENT ON COLUMN "gamestats"."runsinning9" IS 'Runs Inning 9';
COMMENT ON COLUMN "gamestats"."runsinningx" IS 'Runs Inning X';
COMMENT ON COLUMN "gamestats"."oppruns" IS 'Opponents Runs';
COMMENT ON COLUMN "gamestats"."opprunsinning1" IS 'Opponents Runs Inning 1';
COMMENT ON COLUMN "gamestats"."opprunsinning2" IS 'Opponents Runs Inning 2';
COMMENT ON COLUMN "gamestats"."opprunsinning3" IS 'Opponents Runs Inning 3';
COMMENT ON COLUMN "gamestats"."opprunsinning4" IS 'Opponents Runs Inning 4';
COMMENT ON COLUMN "gamestats"."opprunsinning5" IS 'Opponents Runs Inning 5';
COMMENT ON COLUMN "gamestats"."opprunsinning6" IS 'Opponents Runs Inning 6';
COMMENT ON COLUMN "gamestats"."opprunsinning7" IS 'Opponents Runs Inning 7';
COMMENT ON COLUMN "gamestats"."opprunsinning8" IS 'Opponents Runs Inning 8';
COMMENT ON COLUMN "gamestats"."opprunsinning9" IS 'Opponents Runs Inning 9';
COMMENT ON COLUMN "gamestats"."opprunsinningx" IS 'Opponents Runs Inning X';
COMMENT ON COLUMN "gamestats"."notes" IS 'Notes';

-- CREATE INDEXES ...
CREATE INDEX "gamestats_gamenumber_idx" ON "gamestats" ("gamenumber");
ALTER TABLE "gamestats" ADD CONSTRAINT "gamestats_pkey" PRIMARY KEY ("teamnumber", "gamenumber");
CREATE INDEX "gamestats_teamnumber_idx" ON "gamestats" ("teamnumber");

CREATE TABLE IF NOT EXISTS "gametypes"
 (
	"gametypenumber"			INTEGER, 
	"gametypedescription"			VARCHAR (25)
);
COMMENT ON COLUMN "gametypes"."gametypedescription" IS 'GameTypeDescription';

-- CREATE INDEXES ...
ALTER TABLE "gametypes" ADD CONSTRAINT "gametypes_pkey" PRIMARY KEY ("gametypenumber");

CREATE TABLE IF NOT EXISTS "inputorder"
 (
	"categorytype"			VARCHAR (1), 
	"ordernumber"			INTEGER, 
	"categorynumber"			SMALLINT
);
COMMENT ON COLUMN "inputorder"."categorytype" IS 'Category Type';
COMMENT ON COLUMN "inputorder"."ordernumber" IS 'Input Order Number';
COMMENT ON COLUMN "inputorder"."categorynumber" IS 'Category Number';

-- CREATE INDEXES ...
ALTER TABLE "inputorder" ADD CONSTRAINT "inputorder_pkey" PRIMARY KEY ("categorytype", "ordernumber");

CREATE TABLE IF NOT EXISTS "internetoptions"
 (
	"homepagetitle"			TEXT, 
	"homepagegreeting"			TEXT, 
	"linkpagegreeting"			TEXT, 
	"linkpagelinks"			TEXT, 
	"news"			TEXT, 
	"ftpexport"			BOOLEAN, 
	"ftpwarnoverwrite"			BOOLEAN, 
	"ftpurl"			TEXT, 
	"ftpdirectory"			TEXT, 
	"ftpuserid"			VARCHAR (255), 
	"ftppassword"			VARCHAR (255), 
	"fileexport"			BOOLEAN, 
	"filedirectory"			TEXT, 
	"websitename"			TEXT, 
	"apwebexport"			BOOLEAN, 
	"apwebid"			VARCHAR (255), 
	"apwebuserurl"			VARCHAR (255), 
	"apwebftpuser"			VARCHAR (255), 
	"apwebftppass"			VARCHAR (255), 
	"apwebhttpurl"			VARCHAR (255), 
	"apwebftpurl"			VARCHAR (255), 
	"apwebftpdirectory"			VARCHAR (255), 
	"apwebserverurl"			VARCHAR (255), 
	"shownews"			BOOLEAN, 
	"showlinks"			BOOLEAN, 
	"showbatting"			BOOLEAN, 
	"showpitching"			BOOLEAN, 
	"showfielding"			BOOLEAN, 
	"showroster"			BOOLEAN, 
	"showrecord"			BOOLEAN, 
	"showgamescores"			BOOLEAN, 
	"showboxscores"			BOOLEAN, 
	"showscoresbyinning"			BOOLEAN, 
	"showstandings"			BOOLEAN, 
	"includecontact"			BOOLEAN, 
	"includenotes"			BOOLEAN, 
	"showpicturegallery"			BOOLEAN, 
	"showplayer"			BOOLEAN
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "internetteams"
 (
	"teamnumber"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "leadercats"
 (
	"stattype"			INTEGER, 
	"reportorder"			INTEGER, 
	"categorynumber"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "leaderstats"
 (
	"personnumber"			INTEGER, 
	"teamnumber"			INTEGER, 
	"stattype"			INTEGER, 
	"statheading"			VARCHAR (20), 
	"stat"			VARCHAR (20), 
	"reportorder"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "lineupplayer"
 (
	"teamnumber"			INTEGER, 
	"lineupnumber"			INTEGER, 
	"sequencenumber"			INTEGER, 
	"lineuporder"			VARCHAR (3), 
	"playername"			VARCHAR (25), 
	"inn1pos"			VARCHAR (5), 
	"inn2pos"			VARCHAR (5), 
	"inn3pos"			VARCHAR (5), 
	"inn4pos"			VARCHAR (5), 
	"inn5pos"			VARCHAR (5), 
	"inn6pos"			VARCHAR (5), 
	"inn7pos"			VARCHAR (5), 
	"inn8pos"			VARCHAR (5), 
	"inn9pos"			VARCHAR (5)
);
COMMENT ON COLUMN "lineupplayer"."teamnumber" IS 'Team  Number';
COMMENT ON COLUMN "lineupplayer"."lineupnumber" IS 'Lineup Number';
COMMENT ON COLUMN "lineupplayer"."sequencenumber" IS 'Sequence Number';
COMMENT ON COLUMN "lineupplayer"."lineuporder" IS 'LineupOrder';
COMMENT ON COLUMN "lineupplayer"."playername" IS 'Player Name';
COMMENT ON COLUMN "lineupplayer"."inn1pos" IS 'Inning 1 Position';
COMMENT ON COLUMN "lineupplayer"."inn2pos" IS 'Inning 2 Position';
COMMENT ON COLUMN "lineupplayer"."inn3pos" IS 'Inning 3 Position';
COMMENT ON COLUMN "lineupplayer"."inn4pos" IS 'Inning 4 Position';
COMMENT ON COLUMN "lineupplayer"."inn5pos" IS 'Inning 5 Position';
COMMENT ON COLUMN "lineupplayer"."inn6pos" IS 'Inning 6 Position';
COMMENT ON COLUMN "lineupplayer"."inn7pos" IS 'Inning 7 Position';
COMMENT ON COLUMN "lineupplayer"."inn8pos" IS 'Inning 8 Position';
COMMENT ON COLUMN "lineupplayer"."inn9pos" IS 'Inning 9 Position';

-- CREATE INDEXES ...
CREATE INDEX "lineupplayer_lineupnumber_idx" ON "lineupplayer" ("teamnumber");
CREATE INDEX "lineupplayer_lineupsequence_idx" ON "lineupplayer" ("sequencenumber");
ALTER TABLE "lineupplayer" ADD CONSTRAINT "lineupplayer_pkey" PRIMARY KEY ("teamnumber", "lineupnumber", "sequencenumber");
CREATE INDEX "lineupplayer_teamnumber_idx" ON "lineupplayer" ("lineupnumber");

CREATE TABLE IF NOT EXISTS "memooptions"
 (
	"optionnumber"			INTEGER, 
	"option"			TEXT
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "nameyourowncats"
 (
	"categorytype"			VARCHAR (3), 
	"categorynumber"			INTEGER, 
	"categorydescription"			VARCHAR (5)
);
COMMENT ON COLUMN "nameyourowncats"."categorytype" IS 'Category Type';
COMMENT ON COLUMN "nameyourowncats"."categorynumber" IS 'Category Number';
COMMENT ON COLUMN "nameyourowncats"."categorydescription" IS 'Category Description';

-- CREATE INDEXES ...
ALTER TABLE "nameyourowncats" ADD CONSTRAINT "nameyourowncats_pkey" PRIMARY KEY ("categorytype", "categorynumber");

CREATE TABLE IF NOT EXISTS "nameyourownstats"
 (
	"categorytype"			VARCHAR (3), 
	"categorynumber"			INTEGER, 
	"categorydescription"			VARCHAR (5), 
	"decimals"			SMALLINT, 
	"teamtotal"			BOOLEAN, 
	"cat1"			REAL, 
	"cat2"			REAL, 
	"cat3"			REAL, 
	"cat4"			REAL, 
	"cat5"			REAL, 
	"cat6"			REAL, 
	"cat7"			REAL, 
	"cat8"			REAL, 
	"cat9"			REAL, 
	"cat10"			REAL, 
	"cat11"			REAL, 
	"cat12"			REAL, 
	"op1"			SMALLINT, 
	"op2"			SMALLINT, 
	"op3"			SMALLINT, 
	"op4"			SMALLINT, 
	"op5"			SMALLINT, 
	"op6"			SMALLINT, 
	"op7"			SMALLINT, 
	"op8"			SMALLINT, 
	"op9"			SMALLINT, 
	"op10"			SMALLINT, 
	"midop"			SMALLINT
);

-- CREATE INDEXES ...
ALTER TABLE "nameyourownstats" ADD CONSTRAINT "nameyourownstats_pkey" PRIMARY KEY ("categorytype", "categorynumber");

CREATE TABLE IF NOT EXISTS "numberoptions"
 (
	"optionnumber"			INTEGER, 
	"option"			REAL, 
	"optiondescription"			VARCHAR (50)
);
COMMENT ON COLUMN "numberoptions"."optionnumber" IS 'Option Number';
COMMENT ON COLUMN "numberoptions"."option" IS 'Option';
COMMENT ON COLUMN "numberoptions"."optiondescription" IS 'Option Description';

-- CREATE INDEXES ...
CREATE UNIQUE INDEX "numberoptions_optionnumber_idx" ON "numberoptions" ("optionnumber");
ALTER TABLE "numberoptions" ADD CONSTRAINT "numberoptions_pkey" PRIMARY KEY ("optionnumber");

CREATE TABLE IF NOT EXISTS "people"
 (
	"personnumber"			INTEGER, 
	"firstname"			VARCHAR (20), 
	"lastname"			VARCHAR (20), 
	"address1"			VARCHAR (40), 
	"address2"			VARCHAR (40), 
	"city"			VARCHAR (20), 
	"state"			VARCHAR (20), 
	"zip"			VARCHAR (20), 
	"country"			VARCHAR (20), 
	"homephone"			VARCHAR (20), 
	"workphone"			VARCHAR (20), 
	"faxnumber"			VARCHAR (20), 
	"emailaddress"			VARCHAR (50), 
	"birthdate"			DATE, 
	"notes"			TEXT
);
COMMENT ON COLUMN "people"."personnumber" IS 'Person Number';
COMMENT ON COLUMN "people"."firstname" IS 'First Name';
COMMENT ON COLUMN "people"."lastname" IS 'Last Name';
COMMENT ON COLUMN "people"."address1" IS 'Address';
COMMENT ON COLUMN "people"."city" IS 'City';
COMMENT ON COLUMN "people"."state" IS 'State/Province';
COMMENT ON COLUMN "people"."zip" IS 'Zip/Postal';
COMMENT ON COLUMN "people"."country" IS 'Country';
COMMENT ON COLUMN "people"."homephone" IS 'Home Phone';
COMMENT ON COLUMN "people"."workphone" IS 'Work Phone';
COMMENT ON COLUMN "people"."faxnumber" IS 'Fax Number';
COMMENT ON COLUMN "people"."emailaddress" IS 'Email Address';
COMMENT ON COLUMN "people"."birthdate" IS 'Birth Date';
COMMENT ON COLUMN "people"."notes" IS 'Notes';

-- CREATE INDEXES ...
ALTER TABLE "people" ADD CONSTRAINT "people_pkey" PRIMARY KEY ("personnumber");

CREATE TABLE IF NOT EXISTS "picturegallery"
 (
	"picturename"			TEXT, 
	"caption"			TEXT, 
	"publishtoweb"			BOOLEAN, 
	"sortorder"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "pitchingrptformat"
 (
	"reportnumber"			INTEGER, 
	"reportdescription"			VARCHAR (25), 
	"sortcategory"			SMALLINT, 
	"sortdirection"			VARCHAR (1)
);
COMMENT ON COLUMN "pitchingrptformat"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "pitchingrptformat"."reportdescription" IS 'Report Description';
COMMENT ON COLUMN "pitchingrptformat"."sortcategory" IS 'Sort Category';
COMMENT ON COLUMN "pitchingrptformat"."sortdirection" IS 'Sort Direction';

-- CREATE INDEXES ...
ALTER TABLE "pitchingrptformat" ADD CONSTRAINT "pitchingrptformat_pkey" PRIMARY KEY ("reportnumber");
CREATE UNIQUE INDEX "pitchingrptformat_reportnumber_idx" ON "pitchingrptformat" ("reportnumber");

CREATE TABLE IF NOT EXISTS "pitchingstats"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"eventnumber"			SMALLINT, 
	"gametype"			INTEGER, 
	"hometeam"			BOOLEAN, 
	"starter"			BOOLEAN, 
	"ip"			INTEGER, 
	"ip13"			SMALLINT, 
	"bf"			INTEGER, 
	"r"			INTEGER, 
	"er"			INTEGER, 
	"h"			INTEGER, 
	"d"			INTEGER, 
	"t"			INTEGER, 
	"hr"			INTEGER, 
	"bb"			INTEGER, 
	"hb"			INTEGER, 
	"co"			INTEGER, 
	"so"			INTEGER, 
	"sh"			INTEGER, 
	"sf"			INTEGER, 
	"wp"			INTEGER, 
	"bk"			INTEGER, 
	"po"			INTEGER, 
	"b"			INTEGER, 
	"s"			INTEGER, 
	"gs"			INTEGER, 
	"gf"			INTEGER, 
	"cg"			INTEGER, 
	"w"			INTEGER, 
	"l"			INTEGER, 
	"sv"			INTEGER, 
	"sho"			INTEGER, 
	"u1"			INTEGER, 
	"u2"			INTEGER, 
	"u3"			INTEGER, 
	"u4"			INTEGER, 
	"u5"			INTEGER, 
	"u6"			INTEGER, 
	"u7"			INTEGER, 
	"u8"			INTEGER, 
	"u9"			INTEGER, 
	"u10"			INTEGER, 
	"notes"			TEXT
);
COMMENT ON COLUMN "pitchingstats"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "pitchingstats"."gamenumber" IS 'Game Number';
COMMENT ON COLUMN "pitchingstats"."playernumber" IS 'Player Number';
COMMENT ON COLUMN "pitchingstats"."eventnumber" IS 'Event Number';
COMMENT ON COLUMN "pitchingstats"."gametype" IS 'Game Type';
COMMENT ON COLUMN "pitchingstats"."hometeam" IS 'Home Team';
COMMENT ON COLUMN "pitchingstats"."starter" IS 'Starter';
COMMENT ON COLUMN "pitchingstats"."ip" IS 'Innings Pitched';
COMMENT ON COLUMN "pitchingstats"."ip13" IS 'Third Innings';
COMMENT ON COLUMN "pitchingstats"."bf" IS 'Batters Faced';
COMMENT ON COLUMN "pitchingstats"."r" IS 'Runs';
COMMENT ON COLUMN "pitchingstats"."er" IS 'Earned Runs';
COMMENT ON COLUMN "pitchingstats"."h" IS 'Hits';
COMMENT ON COLUMN "pitchingstats"."d" IS 'Doubles';
COMMENT ON COLUMN "pitchingstats"."t" IS 'Triples';
COMMENT ON COLUMN "pitchingstats"."hr" IS 'Home Runs';
COMMENT ON COLUMN "pitchingstats"."bb" IS 'Walks';
COMMENT ON COLUMN "pitchingstats"."hb" IS 'Hit Batters';
COMMENT ON COLUMN "pitchingstats"."co" IS 'Catcher''s Obstruction';
COMMENT ON COLUMN "pitchingstats"."so" IS 'Strike Outs';
COMMENT ON COLUMN "pitchingstats"."sh" IS 'Sac Hits';
COMMENT ON COLUMN "pitchingstats"."sf" IS 'Sac Flys';
COMMENT ON COLUMN "pitchingstats"."wp" IS 'Wild Pitch';
COMMENT ON COLUMN "pitchingstats"."bk" IS 'Balks';
COMMENT ON COLUMN "pitchingstats"."po" IS 'Pick Offs';
COMMENT ON COLUMN "pitchingstats"."b" IS 'Balls';
COMMENT ON COLUMN "pitchingstats"."s" IS 'Strikes';
COMMENT ON COLUMN "pitchingstats"."gs" IS 'Games Started';
COMMENT ON COLUMN "pitchingstats"."gf" IS 'Games Finished';
COMMENT ON COLUMN "pitchingstats"."cg" IS 'Complete Game';
COMMENT ON COLUMN "pitchingstats"."w" IS 'Games Won';
COMMENT ON COLUMN "pitchingstats"."l" IS 'Games Lost';
COMMENT ON COLUMN "pitchingstats"."sv" IS 'Games Saved';
COMMENT ON COLUMN "pitchingstats"."sho" IS 'Shut Outs';
COMMENT ON COLUMN "pitchingstats"."u1" IS 'User Defined 1';
COMMENT ON COLUMN "pitchingstats"."u2" IS 'User Defined 2';
COMMENT ON COLUMN "pitchingstats"."u3" IS 'User Defined 3';
COMMENT ON COLUMN "pitchingstats"."u4" IS 'User Defined 4';
COMMENT ON COLUMN "pitchingstats"."u5" IS 'User Defined 5';
COMMENT ON COLUMN "pitchingstats"."u6" IS 'User Defined 6';
COMMENT ON COLUMN "pitchingstats"."u7" IS 'User Defined 7';
COMMENT ON COLUMN "pitchingstats"."u8" IS 'User Defined 8';
COMMENT ON COLUMN "pitchingstats"."u9" IS 'User Defined 9';
COMMENT ON COLUMN "pitchingstats"."u10" IS 'User Defined 10';
COMMENT ON COLUMN "pitchingstats"."notes" IS 'Notes';

-- CREATE INDEXES ...
CREATE INDEX "pitchingstats_eventnumber_idx" ON "pitchingstats" ("eventnumber");
CREATE INDEX "pitchingstats_gamenumber_idx" ON "pitchingstats" ("gamenumber");
CREATE INDEX "pitchingstats_pitchingstatsteamnumber_idx" ON "pitchingstats" ("teamnumber");
CREATE INDEX "pitchingstats_playernumber_idx" ON "pitchingstats" ("playernumber");
ALTER TABLE "pitchingstats" ADD CONSTRAINT "pitchingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber", "eventnumber");

CREATE TABLE IF NOT EXISTS "programversion"
 (
	"programversion"			REAL, 
	"versiondate"			DATE
);
COMMENT ON COLUMN "programversion"."programversion" IS 'Program Version';
COMMENT ON COLUMN "programversion"."versiondate" IS 'Version Date';

-- CREATE INDEXES ...
ALTER TABLE "programversion" ADD CONSTRAINT "programversion_pkey" PRIMARY KEY ("programversion");

CREATE TABLE IF NOT EXISTS "reportnumber"
 (
	"reporttype"			VARCHAR (1), 
	"reportnumber"			INTEGER
);
COMMENT ON COLUMN "reportnumber"."reporttype" IS 'Report Type';
COMMENT ON COLUMN "reportnumber"."reportnumber" IS 'Report Number';

-- CREATE INDEXES ...
ALTER TABLE "reportnumber" ADD CONSTRAINT "reportnumber_pkey" PRIMARY KEY ("reporttype");

CREATE TABLE IF NOT EXISTS "rptbatting"
 (
	"sortkey"			INTEGER, 
	"teamnumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"opponent"			VARCHAR (25), 
	"g"			VARCHAR (7), 
	"pa"			VARCHAR (7), 
	"ab"			VARCHAR (7), 
	"r"			VARCHAR (7), 
	"h"			VARCHAR (7), 
	"s"			VARCHAR (7), 
	"d"			VARCHAR (7), 
	"t"			VARCHAR (7), 
	"hr"			VARCHAR (7), 
	"tb"			VARCHAR (7), 
	"oe"			VARCHAR (7), 
	"fc"			VARCHAR (7), 
	"bb"			VARCHAR (7), 
	"hp"			VARCHAR (7), 
	"co"			VARCHAR (7), 
	"so"			VARCHAR (7), 
	"sh"			VARCHAR (7), 
	"sf"			VARCHAR (7), 
	"dp"			VARCHAR (7), 
	"sb"			VARCHAR (7), 
	"cs"			VARCHAR (7), 
	"rbi"			VARCHAR (7), 
	"ba"			VARCHAR (5), 
	"obp"			VARCHAR (5), 
	"slg"			VARCHAR (5), 
	"pp"			VARCHAR (5), 
	"rc"			VARCHAR (7), 
	"ta"			VARCHAR (6), 
	"sba"			VARCHAR (5), 
	"user1"			VARCHAR (7), 
	"user2"			VARCHAR (7), 
	"user3"			VARCHAR (7), 
	"user4"			VARCHAR (7), 
	"user5"			VARCHAR (7), 
	"users1"			VARCHAR (7), 
	"users2"			VARCHAR (7), 
	"users3"			VARCHAR (7), 
	"users4"			VARCHAR (7), 
	"users5"			VARCHAR (7), 
	"chs"			VARCHAR (5), 
	"lhs"			VARCHAR (5), 
	"playername"			VARCHAR (50), 
	"teamname"			VARCHAR (50)
);
COMMENT ON COLUMN "rptbatting"."sortkey" IS 'Sort Key';
COMMENT ON COLUMN "rptbatting"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "rptbatting"."playernumber" IS 'Player Number';
COMMENT ON COLUMN "rptbatting"."opponent" IS 'Opponent';
COMMENT ON COLUMN "rptbatting"."g" IS 'Games';
COMMENT ON COLUMN "rptbatting"."pa" IS 'Plate Appearances';
COMMENT ON COLUMN "rptbatting"."ab" IS 'At Bats';
COMMENT ON COLUMN "rptbatting"."r" IS 'Runs';
COMMENT ON COLUMN "rptbatting"."h" IS 'Hits';
COMMENT ON COLUMN "rptbatting"."s" IS 'Singles';
COMMENT ON COLUMN "rptbatting"."d" IS 'Doubles';
COMMENT ON COLUMN "rptbatting"."t" IS 'Triples';
COMMENT ON COLUMN "rptbatting"."hr" IS 'Home Runs';
COMMENT ON COLUMN "rptbatting"."tb" IS 'Total Bases';
COMMENT ON COLUMN "rptbatting"."oe" IS 'On-Error';
COMMENT ON COLUMN "rptbatting"."fc" IS 'Fielder''s Choice';
COMMENT ON COLUMN "rptbatting"."bb" IS 'Walks';
COMMENT ON COLUMN "rptbatting"."hp" IS 'Hit By Pitch';
COMMENT ON COLUMN "rptbatting"."co" IS 'Catcher''s Obstruction';
COMMENT ON COLUMN "rptbatting"."so" IS 'Strike Outs';
COMMENT ON COLUMN "rptbatting"."sh" IS 'Sac Bunts';
COMMENT ON COLUMN "rptbatting"."sf" IS 'Sac Flys';
COMMENT ON COLUMN "rptbatting"."dp" IS 'Double Plays Hit Into';
COMMENT ON COLUMN "rptbatting"."sb" IS 'Stolen Bases';
COMMENT ON COLUMN "rptbatting"."cs" IS 'Caught Stealing';
COMMENT ON COLUMN "rptbatting"."rbi" IS 'Runs Batted In';
COMMENT ON COLUMN "rptbatting"."ba" IS 'Batting Average';
COMMENT ON COLUMN "rptbatting"."obp" IS 'On-Base Percentage';
COMMENT ON COLUMN "rptbatting"."slg" IS 'Slugging Percentage';
COMMENT ON COLUMN "rptbatting"."pp" IS 'Pure Power';
COMMENT ON COLUMN "rptbatting"."rc" IS 'Runs Created';
COMMENT ON COLUMN "rptbatting"."ta" IS 'Total Average';
COMMENT ON COLUMN "rptbatting"."sba" IS 'Stolen Base Average';
COMMENT ON COLUMN "rptbatting"."user1" IS 'User Defined 1';
COMMENT ON COLUMN "rptbatting"."user2" IS 'User Defined 2';
COMMENT ON COLUMN "rptbatting"."user3" IS 'User Defined 3';
COMMENT ON COLUMN "rptbatting"."user4" IS 'User Defined 4';
COMMENT ON COLUMN "rptbatting"."user5" IS 'User Defined 5';

-- CREATE INDEXES ...
ALTER TABLE "rptbatting" ADD CONSTRAINT "rptbatting_pkey" PRIMARY KEY ("sortkey");

CREATE TABLE IF NOT EXISTS "rptboxscores"
 (
	"sortkey"			INTEGER, 
	"batter"			VARCHAR (50), 
	"b_ab"			VARCHAR (5), 
	"b_r"			VARCHAR (5), 
	"b_h"			VARCHAR (5), 
	"b_hr"			VARCHAR (5), 
	"b_bb"			VARCHAR (5), 
	"b_so"			VARCHAR (5), 
	"b_rbi"			VARCHAR (5), 
	"separator"			VARCHAR (1), 
	"pitcher"			VARCHAR (50), 
	"p_ip"			VARCHAR (5), 
	"p_r"			VARCHAR (5), 
	"p_er"			VARCHAR (5), 
	"p_h"			VARCHAR (5), 
	"p_hr"			VARCHAR (5), 
	"p_bb"			VARCHAR (5), 
	"p_so"			VARCHAR (5), 
	"b_pa"			VARCHAR (5), 
	"b_2b"			VARCHAR (5), 
	"b_3b"			VARCHAR (5), 
	"b_tb"			VARCHAR (5), 
	"b_oe"			VARCHAR (5), 
	"b_fc"			VARCHAR (5), 
	"b_hp"			VARCHAR (5), 
	"b_sh"			VARCHAR (5), 
	"b_sf"			VARCHAR (5), 
	"b_dp"			VARCHAR (5), 
	"b_sb"			VARCHAR (5), 
	"b_cs"			VARCHAR (5), 
	"b_obp"			VARCHAR (5), 
	"b_slg"			VARCHAR (5), 
	"b_ba"			VARCHAR (5), 
	"p_bf"			VARCHAR (5), 
	"p_ab"			VARCHAR (5), 
	"p_2b"			VARCHAR (5), 
	"p_3b"			VARCHAR (5), 
	"p_hb"			VARCHAR (5), 
	"p_wp"			VARCHAR (5), 
	"p_bk"			VARCHAR (5), 
	"p_po"			VARCHAR (5), 
	"p_b"			VARCHAR (5), 
	"p_s"			VARCHAR (5), 
	"p_tp"			VARCHAR (5), 
	"p_obp"			VARCHAR (5), 
	"p_slg"			VARCHAR (5), 
	"p_ba"			VARCHAR (5), 
	"p_era"			VARCHAR (5)
);
COMMENT ON COLUMN "rptboxscores"."sortkey" IS 'Sort Key';
COMMENT ON COLUMN "rptboxscores"."batter" IS 'Batter';
COMMENT ON COLUMN "rptboxscores"."b_ab" IS 'AB';
COMMENT ON COLUMN "rptboxscores"."b_r" IS 'R';
COMMENT ON COLUMN "rptboxscores"."b_h" IS 'H';
COMMENT ON COLUMN "rptboxscores"."b_hr" IS 'HR';
COMMENT ON COLUMN "rptboxscores"."b_bb" IS 'BB';
COMMENT ON COLUMN "rptboxscores"."b_so" IS 'SO';
COMMENT ON COLUMN "rptboxscores"."b_rbi" IS 'RBI';
COMMENT ON COLUMN "rptboxscores"."separator" IS 'Separator';
COMMENT ON COLUMN "rptboxscores"."pitcher" IS 'Pitcher';
COMMENT ON COLUMN "rptboxscores"."p_ip" IS 'IP';
COMMENT ON COLUMN "rptboxscores"."p_r" IS 'R';
COMMENT ON COLUMN "rptboxscores"."p_er" IS 'ER';
COMMENT ON COLUMN "rptboxscores"."p_h" IS 'H';
COMMENT ON COLUMN "rptboxscores"."p_hr" IS 'HR';
COMMENT ON COLUMN "rptboxscores"."p_bb" IS 'BB';
COMMENT ON COLUMN "rptboxscores"."p_so" IS 'SO';

-- CREATE INDEXES ...
ALTER TABLE "rptboxscores" ADD CONSTRAINT "rptboxscores_pkey" PRIMARY KEY ("sortkey");
CREATE UNIQUE INDEX "rptboxscores_sortykey_idx" ON "rptboxscores" ("sortkey");

CREATE TABLE IF NOT EXISTS "rptfielding"
 (
	"sortkey"			INTEGER, 
	"teamnumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"opponent"			VARCHAR (25), 
	"g"			VARCHAR (7), 
	"po"			VARCHAR (7), 
	"a"			VARCHAR (7), 
	"e"			VARCHAR (7), 
	"c"			VARCHAR (7), 
	"dp"			VARCHAR (7), 
	"pb"			VARCHAR (7), 
	"sb"			VARCHAR (7), 
	"cs"			VARCHAR (7), 
	"csa"			VARCHAR (5), 
	"fa"			VARCHAR (5), 
	"rng"			VARCHAR (7), 
	"user1"			VARCHAR (7), 
	"user2"			VARCHAR (7), 
	"user3"			VARCHAR (7), 
	"user4"			VARCHAR (7), 
	"user5"			VARCHAR (7), 
	"users1"			VARCHAR (7), 
	"users2"			VARCHAR (7), 
	"users3"			VARCHAR (7), 
	"users4"			VARCHAR (7), 
	"users5"			VARCHAR (7), 
	"playername"			VARCHAR (50), 
	"teamname"			VARCHAR (50)
);
COMMENT ON COLUMN "rptfielding"."sortkey" IS 'Sort Key';
COMMENT ON COLUMN "rptfielding"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "rptfielding"."playernumber" IS 'Player Number';
COMMENT ON COLUMN "rptfielding"."opponent" IS 'Opponent';
COMMENT ON COLUMN "rptfielding"."g" IS 'Games';
COMMENT ON COLUMN "rptfielding"."po" IS 'Putouts';
COMMENT ON COLUMN "rptfielding"."a" IS 'Assists';
COMMENT ON COLUMN "rptfielding"."e" IS 'Errors';
COMMENT ON COLUMN "rptfielding"."c" IS 'Chances';
COMMENT ON COLUMN "rptfielding"."dp" IS 'Double Plays';
COMMENT ON COLUMN "rptfielding"."pb" IS 'Pass Balls (C)';
COMMENT ON COLUMN "rptfielding"."sb" IS 'Stolen Bases (C)';
COMMENT ON COLUMN "rptfielding"."cs" IS 'Caught Stealing (C)';
COMMENT ON COLUMN "rptfielding"."csa" IS 'Caught Stealing Average (C)';
COMMENT ON COLUMN "rptfielding"."fa" IS 'Fielding Average';
COMMENT ON COLUMN "rptfielding"."rng" IS 'Range Factor';
COMMENT ON COLUMN "rptfielding"."user1" IS 'User Defined 1';
COMMENT ON COLUMN "rptfielding"."user2" IS 'User Defined 2';
COMMENT ON COLUMN "rptfielding"."user3" IS 'User Defined 3';
COMMENT ON COLUMN "rptfielding"."user4" IS 'User Defined 4';
COMMENT ON COLUMN "rptfielding"."user5" IS 'User Defined 5';

-- CREATE INDEXES ...
ALTER TABLE "rptfielding" ADD CONSTRAINT "rptfielding_pkey" PRIMARY KEY ("sortkey");
CREATE UNIQUE INDEX "rptfielding_sortkey_idx" ON "rptfielding" ("sortkey");

CREATE TABLE IF NOT EXISTS "rptinnings"
 (
	"sortkey"			INTEGER, 
	"teamname"			VARCHAR (100), 
	"inn1score"			VARCHAR (7), 
	"inn2score"			VARCHAR (7), 
	"inn3score"			VARCHAR (7), 
	"inn4score"			VARCHAR (7), 
	"inn5score"			VARCHAR (7), 
	"inn6score"			VARCHAR (7), 
	"inn7score"			VARCHAR (7), 
	"inn8score"			VARCHAR (7), 
	"inn9score"			VARCHAR (7), 
	"innxscore"			VARCHAR (7), 
	"finalscore"			VARCHAR (9)
);

-- CREATE INDEXES ...
ALTER TABLE "rptinnings" ADD CONSTRAINT "rptinnings_pkey" PRIMARY KEY ("sortkey");

CREATE TABLE IF NOT EXISTS "rptpitching"
 (
	"sortkey"			INTEGER, 
	"teamnumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"opponent"			VARCHAR (25), 
	"g"			VARCHAR (7), 
	"ip"			VARCHAR (9), 
	"r"			VARCHAR (7), 
	"er"			VARCHAR (7), 
	"bf"			VARCHAR (7), 
	"ab"			VARCHAR (7), 
	"h"			VARCHAR (7), 
	"d"			VARCHAR (7), 
	"t"			VARCHAR (7), 
	"hr"			VARCHAR (7), 
	"tb"			VARCHAR (7), 
	"bb"			VARCHAR (7), 
	"hb"			VARCHAR (7), 
	"co"			VARCHAR (7), 
	"so"			VARCHAR (7), 
	"sh"			VARCHAR (7), 
	"sf"			VARCHAR (7), 
	"wp"			VARCHAR (7), 
	"bk"			VARCHAR (7), 
	"po"			VARCHAR (7), 
	"b"			VARCHAR (7), 
	"s"			VARCHAR (7), 
	"tp"			VARCHAR (7), 
	"gs"			VARCHAR (7), 
	"gf"			VARCHAR (7), 
	"cg"			VARCHAR (7), 
	"w"			VARCHAR (7), 
	"l"			VARCHAR (7), 
	"sv"			VARCHAR (7), 
	"sho"			VARCHAR (7), 
	"ba"			VARCHAR (5), 
	"obp"			VARCHAR (5), 
	"slg"			VARCHAR (5), 
	"sog"			VARCHAR (5), 
	"era"			VARCHAR (7), 
	"spct"			VARCHAR (5), 
	"whip"			VARCHAR (5), 
	"user1"			VARCHAR (7), 
	"user2"			VARCHAR (7), 
	"user3"			VARCHAR (7), 
	"user4"			VARCHAR (7), 
	"user5"			VARCHAR (7), 
	"users1"			VARCHAR (7), 
	"users2"			VARCHAR (7), 
	"users3"			VARCHAR (7), 
	"users4"			VARCHAR (7), 
	"users5"			VARCHAR (7), 
	"playername"			VARCHAR (50), 
	"teamname"			VARCHAR (50)
);
COMMENT ON COLUMN "rptpitching"."sortkey" IS 'Sort Key';
COMMENT ON COLUMN "rptpitching"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "rptpitching"."playernumber" IS 'Player Number';
COMMENT ON COLUMN "rptpitching"."opponent" IS 'Opponent';
COMMENT ON COLUMN "rptpitching"."g" IS 'Games';
COMMENT ON COLUMN "rptpitching"."ip" IS 'Innings Pitched';
COMMENT ON COLUMN "rptpitching"."r" IS 'Runs';
COMMENT ON COLUMN "rptpitching"."er" IS 'Earned-Runs';
COMMENT ON COLUMN "rptpitching"."bf" IS 'Batters Faced';
COMMENT ON COLUMN "rptpitching"."ab" IS 'At Bats';
COMMENT ON COLUMN "rptpitching"."h" IS 'Hits';
COMMENT ON COLUMN "rptpitching"."d" IS 'Doubles';
COMMENT ON COLUMN "rptpitching"."t" IS 'Triples';
COMMENT ON COLUMN "rptpitching"."hr" IS 'Home Runs';
COMMENT ON COLUMN "rptpitching"."tb" IS 'Total Bases';
COMMENT ON COLUMN "rptpitching"."bb" IS 'Walks';
COMMENT ON COLUMN "rptpitching"."hb" IS 'Hit Batters';
COMMENT ON COLUMN "rptpitching"."co" IS 'Catcher''s Obstruction';
COMMENT ON COLUMN "rptpitching"."so" IS 'Strike Outs';
COMMENT ON COLUMN "rptpitching"."sh" IS 'Sac Hits';
COMMENT ON COLUMN "rptpitching"."sf" IS 'Sac Flys';
COMMENT ON COLUMN "rptpitching"."wp" IS 'Wild Pitch';
COMMENT ON COLUMN "rptpitching"."bk" IS 'Balks';
COMMENT ON COLUMN "rptpitching"."po" IS 'Pick Offs';
COMMENT ON COLUMN "rptpitching"."b" IS 'Balls';
COMMENT ON COLUMN "rptpitching"."s" IS 'Strikes';
COMMENT ON COLUMN "rptpitching"."tp" IS 'Total Pitches';
COMMENT ON COLUMN "rptpitching"."gs" IS 'Games Started';
COMMENT ON COLUMN "rptpitching"."gf" IS 'Games Finished';
COMMENT ON COLUMN "rptpitching"."cg" IS 'Complete Games';
COMMENT ON COLUMN "rptpitching"."w" IS 'Wins';
COMMENT ON COLUMN "rptpitching"."l" IS 'Losses';
COMMENT ON COLUMN "rptpitching"."sv" IS 'Saves';
COMMENT ON COLUMN "rptpitching"."sho" IS 'Shutouts';
COMMENT ON COLUMN "rptpitching"."ba" IS 'Opponents Average';
COMMENT ON COLUMN "rptpitching"."obp" IS 'Opponents OBP';
COMMENT ON COLUMN "rptpitching"."slg" IS 'Opponents SLG';
COMMENT ON COLUMN "rptpitching"."sog" IS 'Strike Outs per Game';
COMMENT ON COLUMN "rptpitching"."era" IS 'Earned-Run Average';
COMMENT ON COLUMN "rptpitching"."spct" IS 'Strike Percent';
COMMENT ON COLUMN "rptpitching"."whip" IS 'WHIP Calculation';
COMMENT ON COLUMN "rptpitching"."user1" IS 'User Defined 1';
COMMENT ON COLUMN "rptpitching"."user2" IS 'User Defined 2';
COMMENT ON COLUMN "rptpitching"."user3" IS 'User Defined 3';
COMMENT ON COLUMN "rptpitching"."user4" IS 'User Defined 4';
COMMENT ON COLUMN "rptpitching"."user5" IS 'User Defined 5';

-- CREATE INDEXES ...
ALTER TABLE "rptpitching" ADD CONSTRAINT "rptpitching_pkey" PRIMARY KEY ("sortkey");
CREATE UNIQUE INDEX "rptpitching_sortkey_idx" ON "rptpitching" ("sortkey");

CREATE TABLE IF NOT EXISTS "rptrecord"
 (
	"sortkey"			INTEGER, 
	"teamnumber"			INTEGER, 
	"gametype"			INTEGER, 
	"gametypedescription"			VARCHAR (25), 
	"gameswon"			VARCHAR (7), 
	"gameslost"			VARCHAR (7), 
	"gamestied"			VARCHAR (7), 
	"winpct"			VARCHAR (5), 
	"runsfor"			VARCHAR (7), 
	"runsagainst"			VARCHAR (7)
);
COMMENT ON COLUMN "rptrecord"."sortkey" IS 'Sort Key';
COMMENT ON COLUMN "rptrecord"."teamnumber" IS 'TeamNumber';
COMMENT ON COLUMN "rptrecord"."gametype" IS 'Game Type Number';
COMMENT ON COLUMN "rptrecord"."gametypedescription" IS 'Game Type Description';
COMMENT ON COLUMN "rptrecord"."gameswon" IS 'Games Won';
COMMENT ON COLUMN "rptrecord"."gameslost" IS 'Games Lost';
COMMENT ON COLUMN "rptrecord"."gamestied" IS 'Games Tied';
COMMENT ON COLUMN "rptrecord"."winpct" IS 'Win Percentage';
COMMENT ON COLUMN "rptrecord"."runsfor" IS 'Runs For';
COMMENT ON COLUMN "rptrecord"."runsagainst" IS 'Runs Against';

-- CREATE INDEXES ...
ALTER TABLE "rptrecord" ADD CONSTRAINT "rptrecord_pkey" PRIMARY KEY ("sortkey");
CREATE INDEX "rptrecord_sortkey_idx" ON "rptrecord" ("sortkey");

CREATE TABLE IF NOT EXISTS "rptroster"
 (
	"sortkey"			INTEGER, 
	"text"			VARCHAR (50)
);

-- CREATE INDEXES ...
ALTER TABLE "rptroster" ADD CONSTRAINT "rptroster_pkey" PRIMARY KEY ("sortkey");

CREATE TABLE IF NOT EXISTS "rptstandings"
 (
	"sortkey"			INTEGER, 
	"teamnumber"			INTEGER, 
	"teamname"			VARCHAR (50), 
	"gameswon"			VARCHAR (7), 
	"gameslost"			VARCHAR (7), 
	"gamestied"			VARCHAR (7), 
	"streak"			VARCHAR (15), 
	"winpct"			VARCHAR (50), 
	"runsfor"			VARCHAR (7), 
	"runsagainst"			VARCHAR (7), 
	"gamesbehind"			VARCHAR (7)
);
COMMENT ON COLUMN "rptstandings"."sortkey" IS 'Sort Key';
COMMENT ON COLUMN "rptstandings"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "rptstandings"."teamname" IS 'Team Name';
COMMENT ON COLUMN "rptstandings"."gameswon" IS 'Games Won';
COMMENT ON COLUMN "rptstandings"."gameslost" IS 'Games Lost';
COMMENT ON COLUMN "rptstandings"."gamestied" IS 'Games Tied';
COMMENT ON COLUMN "rptstandings"."streak" IS 'Streak';
COMMENT ON COLUMN "rptstandings"."winpct" IS 'Win Percentage';
COMMENT ON COLUMN "rptstandings"."runsfor" IS 'Runs For';
COMMENT ON COLUMN "rptstandings"."runsagainst" IS 'Runs Against';
COMMENT ON COLUMN "rptstandings"."gamesbehind" IS 'Games Behind';

-- CREATE INDEXES ...
ALTER TABLE "rptstandings" ADD CONSTRAINT "rptstandings_pkey" PRIMARY KEY ("sortkey");
CREATE INDEX "rptstandings_sortkey_idx" ON "rptstandings" ("sortkey");
CREATE UNIQUE INDEX "rptstandings_teamnumber_idx" ON "rptstandings" ("teamnumber");

CREATE TABLE IF NOT EXISTS "rtbattingstats"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"inning"			SMALLINT, 
	"inningab"			SMALLINT, 
	"lineupnumber"			SMALLINT, 
	"pitcher"			INTEGER, 
	"outonbasespitcher"			INTEGER, 
	"abtype"			SMALLINT, 
	"sb"			SMALLINT, 
	"cs"			SMALLINT, 
	"rbi"			SMALLINT, 
	"batting"			BOOLEAN, 
	"out"			BOOLEAN, 
	"outonbases"			BOOLEAN, 
	"leftforpr"			BOOLEAN, 
	"earnedrun"			BOOLEAN, 
	"basenumber"			SMALLINT, 
	"balls"			SMALLINT, 
	"strikes"			SMALLINT, 
	"twostrikefouls"			SMALLINT
);

-- CREATE INDEXES ...
ALTER TABLE "rtbattingstats" ADD CONSTRAINT "rtbattingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber", "inning", "inningab");

CREATE TABLE IF NOT EXISTS "rtfieldingstats"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"po"			INTEGER, 
	"a"			INTEGER, 
	"e"			INTEGER, 
	"dp"			INTEGER, 
	"pb"			INTEGER, 
	"sb"			INTEGER, 
	"cs"			INTEGER
);

-- CREATE INDEXES ...
ALTER TABLE "rtfieldingstats" ADD CONSTRAINT "rtfieldingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber");

CREATE TABLE IF NOT EXISTS "rtgamestats"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"innings"			SMALLINT, 
	"pitching"			BOOLEAN, 
	"fielding"			BOOLEAN, 
	"runsinning1"			INTEGER, 
	"opprunsinning1"			INTEGER, 
	"runsinning2"			INTEGER, 
	"opprunsinning2"			INTEGER, 
	"runsinning3"			INTEGER, 
	"opprunsinning3"			INTEGER, 
	"runsinning4"			INTEGER, 
	"opprunsinning4"			INTEGER, 
	"runsinning5"			INTEGER, 
	"opprunsinning5"			INTEGER, 
	"runsinning6"			INTEGER, 
	"opprunsinning6"			INTEGER, 
	"runsinning7"			INTEGER, 
	"opprunsinning7"			INTEGER, 
	"runsinning8"			INTEGER, 
	"opprunsinning8"			INTEGER, 
	"runsinning9"			INTEGER, 
	"opprunsinning9"			INTEGER
);

-- CREATE INDEXES ...
ALTER TABLE "rtgamestats" ADD CONSTRAINT "rtgamestats_pkey" PRIMARY KEY ("teamnumber", "gamenumber");

CREATE TABLE IF NOT EXISTS "rtpitchingstats"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"wp"			INTEGER, 
	"bk"			INTEGER, 
	"po"			INTEGER, 
	"gs"			BOOLEAN, 
	"gf"			BOOLEAN, 
	"w"			BOOLEAN, 
	"l"			BOOLEAN, 
	"sv"			BOOLEAN
);

-- CREATE INDEXES ...
ALTER TABLE "rtpitchingstats" ADD CONSTRAINT "rtpitchingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber");

CREATE TABLE IF NOT EXISTS "spray"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"eventnumber"			SMALLINT, 
	"sequencenumber"			INTEGER, 
	"gametype"			INTEGER, 
	"hometeam"			BOOLEAN, 
	"starter"			BOOLEAN, 
	"type1"			SMALLINT, 
	"x1"			INTEGER, 
	"y1"			INTEGER, 
	"type2"			SMALLINT, 
	"x2"			INTEGER, 
	"y2"			INTEGER, 
	"type3"			SMALLINT, 
	"x3"			INTEGER, 
	"y3"			INTEGER, 
	"type4"			SMALLINT, 
	"x4"			INTEGER, 
	"y4"			INTEGER, 
	"type5"			SMALLINT, 
	"x5"			INTEGER, 
	"y5"			INTEGER
);

-- CREATE INDEXES ...
ALTER TABLE "spray" ADD CONSTRAINT "spray_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber", "eventnumber", "sequencenumber");

CREATE TABLE IF NOT EXISTS "stringoptions"
 (
	"optionnumber"			INTEGER, 
	"option"			VARCHAR (100), 
	"optiondescription"			VARCHAR (25)
);

-- CREATE INDEXES ...
ALTER TABLE "stringoptions" ADD CONSTRAINT "stringoptions_pkey" PRIMARY KEY ("optionnumber");

CREATE TABLE IF NOT EXISTS "teamfilters"
 (
	"filternumber"			INTEGER, 
	"teamnumber"			INTEGER
);
COMMENT ON COLUMN "teamfilters"."filternumber" IS 'Filter Number';
COMMENT ON COLUMN "teamfilters"."teamnumber" IS 'Team Number';

-- CREATE INDEXES ...
CREATE INDEX "teamfilters_filternumber_idx" ON "teamfilters" ("filternumber");
ALTER TABLE "teamfilters" ADD CONSTRAINT "teamfilters_pkey" PRIMARY KEY ("filternumber", "teamnumber");
CREATE INDEX "teamfilters_teamnumber_idx" ON "teamfilters" ("teamnumber");

CREATE TABLE IF NOT EXISTS "battingstats"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"playernumber"			INTEGER, 
	"eventnumber"			SMALLINT, 
	"gametype"			INTEGER, 
	"hometeam"			BOOLEAN, 
	"starter"			BOOLEAN, 
	"fieldingposition"			SMALLINT, 
	"pa"			INTEGER, 
	"r"			INTEGER, 
	"h"			INTEGER, 
	"d"			INTEGER, 
	"t"			INTEGER, 
	"hr"			INTEGER, 
	"oe"			INTEGER, 
	"bb"			INTEGER, 
	"hp"			INTEGER, 
	"co"			INTEGER, 
	"fc"			INTEGER, 
	"so"			INTEGER, 
	"sh"			INTEGER, 
	"sf"			INTEGER, 
	"sb"			INTEGER, 
	"cs"			INTEGER, 
	"dp"			INTEGER, 
	"rbi"			INTEGER, 
	"lob"			INTEGER, 
	"u1"			INTEGER, 
	"u2"			INTEGER, 
	"u3"			INTEGER, 
	"u4"			INTEGER, 
	"u5"			INTEGER, 
	"u6"			INTEGER, 
	"u7"			INTEGER, 
	"u8"			INTEGER, 
	"u9"			INTEGER, 
	"u10"			INTEGER, 
	"notes"			TEXT
);
COMMENT ON COLUMN "battingstats"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "battingstats"."gamenumber" IS 'Game Number';
COMMENT ON COLUMN "battingstats"."playernumber" IS 'Player Number';
COMMENT ON COLUMN "battingstats"."eventnumber" IS 'Event Number';
COMMENT ON COLUMN "battingstats"."gametype" IS 'Game Type';
COMMENT ON COLUMN "battingstats"."hometeam" IS 'Home Team';
COMMENT ON COLUMN "battingstats"."starter" IS 'Starter';
COMMENT ON COLUMN "battingstats"."fieldingposition" IS 'Fielding Position';
COMMENT ON COLUMN "battingstats"."pa" IS 'Plate Appearances';
COMMENT ON COLUMN "battingstats"."r" IS 'Runs';
COMMENT ON COLUMN "battingstats"."h" IS 'Hits';
COMMENT ON COLUMN "battingstats"."d" IS 'Doubles';
COMMENT ON COLUMN "battingstats"."t" IS 'Triples';
COMMENT ON COLUMN "battingstats"."hr" IS 'Home Runs';
COMMENT ON COLUMN "battingstats"."oe" IS 'On Error';
COMMENT ON COLUMN "battingstats"."bb" IS 'Walks';
COMMENT ON COLUMN "battingstats"."hp" IS 'Hit By Pitch';
COMMENT ON COLUMN "battingstats"."co" IS 'Catcher''s Obstruction';
COMMENT ON COLUMN "battingstats"."fc" IS 'Fielders Choice';
COMMENT ON COLUMN "battingstats"."so" IS 'Strike Outs';
COMMENT ON COLUMN "battingstats"."sh" IS 'Sacrifice Hits';
COMMENT ON COLUMN "battingstats"."sf" IS 'Sacrifice Flys';
COMMENT ON COLUMN "battingstats"."sb" IS 'Stolen Bases';
COMMENT ON COLUMN "battingstats"."cs" IS 'Caught Stealing';
COMMENT ON COLUMN "battingstats"."dp" IS 'Double Plays Hit Into';
COMMENT ON COLUMN "battingstats"."rbi" IS 'Runs Batted In';
COMMENT ON COLUMN "battingstats"."lob" IS 'Left On Base';
COMMENT ON COLUMN "battingstats"."u1" IS 'User Defined 1';
COMMENT ON COLUMN "battingstats"."u2" IS 'User Defined 2';
COMMENT ON COLUMN "battingstats"."u3" IS 'User Defined 3';
COMMENT ON COLUMN "battingstats"."u4" IS 'User Defined 4';
COMMENT ON COLUMN "battingstats"."u5" IS 'User Defined 5';
COMMENT ON COLUMN "battingstats"."u6" IS 'User Defined 6';
COMMENT ON COLUMN "battingstats"."u7" IS 'User Defined 7';
COMMENT ON COLUMN "battingstats"."u8" IS 'User Defined 8';
COMMENT ON COLUMN "battingstats"."u9" IS 'User Defined 9';
COMMENT ON COLUMN "battingstats"."u10" IS 'Useer Defined 10';
COMMENT ON COLUMN "battingstats"."notes" IS 'Notes';

-- CREATE INDEXES ...
CREATE INDEX "battingstats_eventnumber_idx" ON "battingstats" ("eventnumber");
CREATE INDEX "battingstats_gamenumber_idx" ON "battingstats" ("gamenumber");
CREATE INDEX "battingstats_playernumber_idx" ON "battingstats" ("playernumber");
ALTER TABLE "battingstats" ADD CONSTRAINT "battingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber", "eventnumber");
CREATE INDEX "battingstats_teamnumber_idx" ON "battingstats" ("teamnumber");

CREATE TABLE IF NOT EXISTS "crbpfstats"
 (
	"reportidnumber"			INTEGER, 
	"reporttitle"			VARCHAR (100), 
	"teamtitle"			VARCHAR (100), 
	"reportdate"			VARCHAR (25), 
	"headingplayer"			VARCHAR (50), 
	"headingteam"			VARCHAR (50), 
	"headingg"			VARCHAR (3), 
	"headingpa"			VARCHAR (3), 
	"headingbf"			VARCHAR (3), 
	"headingab"			VARCHAR (3), 
	"headingr"			VARCHAR (3), 
	"headingh"			VARCHAR (3), 
	"heading1b"			VARCHAR (3), 
	"heading2b"			VARCHAR (3), 
	"heading3b"			VARCHAR (3), 
	"headinghr"			VARCHAR (3), 
	"headingtb"			VARCHAR (3), 
	"headingoe"			VARCHAR (3), 
	"headingfc"			VARCHAR (3), 
	"headingbb"			VARCHAR (3), 
	"headinghp"			VARCHAR (3), 
	"headinghb"			VARCHAR (3), 
	"headingco"			VARCHAR (3), 
	"headingso"			VARCHAR (3), 
	"headingsh"			VARCHAR (3), 
	"headingsf"			VARCHAR (3), 
	"headingdp"			VARCHAR (3), 
	"headingsb"			VARCHAR (3), 
	"headingcs"			VARCHAR (3), 
	"headingrbi"			VARCHAR (3), 
	"headingchs"			VARCHAR (3), 
	"headinglhs"			VARCHAR (3), 
	"headingc"			VARCHAR (3), 
	"headinga"			VARCHAR (3), 
	"headinge"			VARCHAR (3), 
	"headingpb"			VARCHAR (3), 
	"headingip"			VARCHAR (3), 
	"headinger"			VARCHAR (3), 
	"headingwp"			VARCHAR (3), 
	"headingbk"			VARCHAR (3), 
	"headingpo"			VARCHAR (3), 
	"headingpickoff"			VARCHAR (3), 
	"headingball"			VARCHAR (3), 
	"headingstrike"			VARCHAR (3), 
	"headingtp"			VARCHAR (3), 
	"headinggs"			VARCHAR (3), 
	"headinggf"			VARCHAR (3), 
	"headingcg"			VARCHAR (3), 
	"headingw"			VARCHAR (3), 
	"headingl"			VARCHAR (3), 
	"headingsv"			VARCHAR (3), 
	"headingsho"			VARCHAR (3), 
	"headingba"			VARCHAR (3), 
	"headingfa"			VARCHAR (3), 
	"headingobp"			VARCHAR (3), 
	"headingslg"			VARCHAR (3), 
	"headingpp"			VARCHAR (3), 
	"headingrc"			VARCHAR (3), 
	"headingta"			VARCHAR (3), 
	"headingsba"			VARCHAR (3), 
	"headingcsa"			VARCHAR (3), 
	"headingrng"			VARCHAR (3), 
	"headingera"			VARCHAR (3), 
	"headingsog"			VARCHAR (3), 
	"headingwhip"			VARCHAR (4), 
	"headingspct"			VARCHAR (4), 
	"headinguser1"			VARCHAR (3), 
	"headinguser2"			VARCHAR (3), 
	"headinguser3"			VARCHAR (3), 
	"headinguser4"			VARCHAR (3), 
	"headinguser5"			VARCHAR (3), 
	"headingusers1"			VARCHAR (3), 
	"headingusers2"			VARCHAR (3), 
	"headingusers3"			VARCHAR (3), 
	"headingusers4"			VARCHAR (3), 
	"headingusers5"			VARCHAR (3)
);

-- CREATE INDEXES ...
ALTER TABLE "crbpfstats" ADD CONSTRAINT "crbpfstats_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crlineup"
 (
	"reportidnumber"			INTEGER, 
	"reporttitle"			VARCHAR (100), 
	"teamtitle"			VARCHAR (100), 
	"reportdate"			VARCHAR (25), 
	"headinginn1"			VARCHAR (3), 
	"headinginn2"			VARCHAR (3), 
	"headinginn3"			VARCHAR (3), 
	"headinginn4"			VARCHAR (3), 
	"headinginn5"			VARCHAR (3), 
	"headinginn6"			VARCHAR (3), 
	"headinginn7"			VARCHAR (3), 
	"headinginn8"			VARCHAR (3), 
	"headinginn9"			VARCHAR (3), 
	"lineupnotes"			TEXT
);

-- CREATE INDEXES ...
ALTER TABLE "crlineup" ADD CONSTRAINT "crlineup_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crrecorddetail"
 (
	"reportidnumber"			INTEGER, 
	"detaillinenumber"			INTEGER, 
	"gametype"			VARCHAR (50), 
	"gameswon"			VARCHAR (10), 
	"gameslost"			VARCHAR (10), 
	"gamestied"			VARCHAR (10), 
	"runsfor"			VARCHAR (10), 
	"runsagainst"			VARCHAR (10), 
	"winpct"			VARCHAR (10)
);

-- CREATE INDEXES ...
ALTER TABLE "crrecorddetail" ADD CONSTRAINT "crrecorddetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crstandings"
 (
	"reportidnumber"			INTEGER, 
	"reporttitle"			VARCHAR (100), 
	"reportsubtitle"			VARCHAR (100), 
	"reportdate"			VARCHAR (25), 
	"headingties"			VARCHAR (10), 
	"headingstreak"			VARCHAR (10), 
	"headingrf"			VARCHAR (20), 
	"headingra"			VARCHAR (20)
);

-- CREATE INDEXES ...
ALTER TABLE "crstandings" ADD CONSTRAINT "crstandings_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "filters"
 (
	"filternumber"			INTEGER, 
	"filtername"			VARCHAR (50)
);
COMMENT ON COLUMN "filters"."filternumber" IS 'Filter Number';
COMMENT ON COLUMN "filters"."filtername" IS 'Filter Name';

-- CREATE INDEXES ...
ALTER TABLE "filters" ADD CONSTRAINT "filters_pkey" PRIMARY KEY ("filternumber");

CREATE TABLE IF NOT EXISTS "internetdocuments"
 (
	"key"			SERIAL, 
	"description"			VARCHAR (255), 
	"path"			TEXT, 
	"lastpublishdate"			TIMESTAMP WITHOUT TIME ZONE
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "lineup"
 (
	"teamnumber"			INTEGER, 
	"lineupnumber"			INTEGER, 
	"description"			VARCHAR (50), 
	"innings"			INTEGER, 
	"lineupnotes"			TEXT
);
COMMENT ON COLUMN "lineup"."teamnumber" IS 'TeamNumber';
COMMENT ON COLUMN "lineup"."lineupnumber" IS 'LineupNumber';
COMMENT ON COLUMN "lineup"."description" IS 'LineupDescription';

-- CREATE INDEXES ...
CREATE INDEX "lineup_lineupnumber_idx" ON "lineup" ("teamnumber");
ALTER TABLE "lineup" ADD CONSTRAINT "lineup_pkey" PRIMARY KEY ("teamnumber", "lineupnumber");
CREATE INDEX "lineup_teamnumber_idx" ON "lineup" ("lineupnumber");

CREATE TABLE IF NOT EXISTS "pitchingrptcats"
 (
	"reportnumber"			INTEGER, 
	"reportorder"			SMALLINT, 
	"categorynumber"			SMALLINT
);
COMMENT ON COLUMN "pitchingrptcats"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "pitchingrptcats"."reportorder" IS 'Report Order';
COMMENT ON COLUMN "pitchingrptcats"."categorynumber" IS 'Category Number';

-- CREATE INDEXES ...
ALTER TABLE "pitchingrptcats" ADD CONSTRAINT "pitchingrptcats_pkey" PRIMARY KEY ("reportnumber", "reportorder");

CREATE TABLE IF NOT EXISTS "roster"
 (
	"teamnumber"			INTEGER, 
	"personnumber"			INTEGER, 
	"playerindicator"			BOOLEAN, 
	"uniformnumber"			VARCHAR (3), 
	"notes"			TEXT
);
COMMENT ON COLUMN "roster"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "roster"."personnumber" IS 'Person Number';
COMMENT ON COLUMN "roster"."playerindicator" IS 'Player Indicator';
COMMENT ON COLUMN "roster"."uniformnumber" IS 'Uniform Number';
COMMENT ON COLUMN "roster"."notes" IS 'Notes';

-- CREATE INDEXES ...
CREATE INDEX "roster_personnumber_idx" ON "roster" ("personnumber");
ALTER TABLE "roster" ADD CONSTRAINT "roster_pkey" PRIMARY KEY ("teamnumber", "personnumber");
CREATE INDEX "roster_teamnumber_idx" ON "roster" ("teamnumber");

CREATE TABLE IF NOT EXISTS "rptlineup"
 (
	"lineuporder"			VARCHAR (3), 
	"playername"			VARCHAR (25), 
	"inn1pos"			VARCHAR (5), 
	"inn2pos"			VARCHAR (5), 
	"inn3pos"			VARCHAR (5), 
	"inn4pos"			VARCHAR (5), 
	"inn5pos"			VARCHAR (5), 
	"inn6pos"			VARCHAR (5), 
	"inn7pos"			VARCHAR (5), 
	"inn8pos"			VARCHAR (5), 
	"inn9pos"			VARCHAR (5)
);
COMMENT ON COLUMN "rptlineup"."lineuporder" IS 'Lineup Order';
COMMENT ON COLUMN "rptlineup"."playername" IS 'Player Name';
COMMENT ON COLUMN "rptlineup"."inn1pos" IS 'Inning 1 Position';
COMMENT ON COLUMN "rptlineup"."inn2pos" IS 'Inning 2 Position';
COMMENT ON COLUMN "rptlineup"."inn3pos" IS 'Inning 3 Position';
COMMENT ON COLUMN "rptlineup"."inn4pos" IS 'Inning 4 Position';
COMMENT ON COLUMN "rptlineup"."inn5pos" IS 'Inning 5 Position';
COMMENT ON COLUMN "rptlineup"."inn6pos" IS 'Inning 6 Position';
COMMENT ON COLUMN "rptlineup"."inn7pos" IS 'Inning 7 Position';
COMMENT ON COLUMN "rptlineup"."inn8pos" IS 'Inning 8 Position';
COMMENT ON COLUMN "rptlineup"."inn9pos" IS 'Inning 9 Position';

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "rptscores"
 (
	"sortkey"			INTEGER, 
	"col1"			VARCHAR (5), 
	"col2"			VARCHAR (100), 
	"col3"			VARCHAR (50), 
	"col4"			VARCHAR (50), 
	"col5"			VARCHAR (10), 
	"col6"			VARCHAR (10)
);
COMMENT ON COLUMN "rptscores"."sortkey" IS 'Sort Key';
COMMENT ON COLUMN "rptscores"."col1" IS 'Column 1';
COMMENT ON COLUMN "rptscores"."col2" IS 'Column 2';
COMMENT ON COLUMN "rptscores"."col3" IS 'Column 3';
COMMENT ON COLUMN "rptscores"."col4" IS 'Column 4';
COMMENT ON COLUMN "rptscores"."col5" IS 'Column 5';
COMMENT ON COLUMN "rptscores"."col6" IS 'Column 6';

-- CREATE INDEXES ...
ALTER TABLE "rptscores" ADD CONSTRAINT "rptscores_pkey" PRIMARY KEY ("sortkey");
CREATE UNIQUE INDEX "rptscores_sortkey_idx" ON "rptscores" ("sortkey");

CREATE TABLE IF NOT EXISTS "rtgamestatsxinnings"
 (
	"teamnumber"			INTEGER, 
	"gamenumber"			INTEGER, 
	"inning"			SMALLINT, 
	"runsinning"			INTEGER, 
	"opprunsinning"			INTEGER
);

-- CREATE INDEXES ...
ALTER TABLE "rtgamestatsxinnings" ADD CONSTRAINT "rtgamestatsxinnings_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "inning");

CREATE TABLE IF NOT EXISTS "teams"
 (
	"teamnumber"			INTEGER, 
	"longteamname"			VARCHAR (50), 
	"shortteamname"			VARCHAR (20), 
	"contactperson"			VARCHAR (50), 
	"phonenumber"			VARCHAR (30), 
	"email"			VARCHAR (70), 
	"notes"			TEXT
);
COMMENT ON COLUMN "teams"."teamnumber" IS 'Team Number';
COMMENT ON COLUMN "teams"."longteamname" IS 'Long Team Name';
COMMENT ON COLUMN "teams"."shortteamname" IS 'Short Team Name';
COMMENT ON COLUMN "teams"."contactperson" IS 'Contact Person';
COMMENT ON COLUMN "teams"."phonenumber" IS 'Phone Number';
COMMENT ON COLUMN "teams"."email" IS 'Email Address';
COMMENT ON COLUMN "teams"."notes" IS 'Notes';

-- CREATE INDEXES ...
ALTER TABLE "teams" ADD CONSTRAINT "teams_pkey" PRIMARY KEY ("teamnumber");


-- All constraints removed for import
