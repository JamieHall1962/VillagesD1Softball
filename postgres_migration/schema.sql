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
	"reportnumber"			INTEGER NOT NULL, 
	"reportorder"			SMALLINT NOT NULL, 
	"categorynumber"			SMALLINT NOT NULL
);
COMMENT ON COLUMN "battingrptcats"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "battingrptcats"."reportorder" IS 'Report Order';
COMMENT ON COLUMN "battingrptcats"."categorynumber" IS 'Category Number';

-- CREATE INDEXES ...
ALTER TABLE "battingrptcats" ADD CONSTRAINT "battingrptcats_pkey" PRIMARY KEY ("reportnumber", "reportorder");

CREATE TABLE IF NOT EXISTS "battingrptformat"
 (
	"reportnumber"			INTEGER NOT NULL, 
	"reportdescription"			VARCHAR (25) NOT NULL, 
	"sortcategory"			SMALLINT NOT NULL, 
	"sortdirection"			VARCHAR (1) NOT NULL
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
	"reportidnumber"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (100) NOT NULL, 
	"teamtitle"			VARCHAR (100) NOT NULL, 
	"reportdate"			VARCHAR (25) NOT NULL, 
	"headingbatting"			VARCHAR (10) NOT NULL, 
	"headingbatpa"			VARCHAR (3) NOT NULL, 
	"headingbatab"			VARCHAR (3) NOT NULL, 
	"headingbatr"			VARCHAR (3) NOT NULL, 
	"headingbath"			VARCHAR (3) NOT NULL, 
	"headingbat2b"			VARCHAR (3) NOT NULL, 
	"headingbat3b"			VARCHAR (3) NOT NULL, 
	"headingbathr"			VARCHAR (3) NOT NULL, 
	"headingbattb"			VARCHAR (3) NOT NULL, 
	"headingbatoe"			VARCHAR (3) NOT NULL, 
	"headingbatfc"			VARCHAR (3) NOT NULL, 
	"headingbatbb"			VARCHAR (3) NOT NULL, 
	"headingbathp"			VARCHAR (3) NOT NULL, 
	"headingbatso"			VARCHAR (3) NOT NULL, 
	"headingbatsh"			VARCHAR (3) NOT NULL, 
	"headingbatsf"			VARCHAR (3) NOT NULL, 
	"headingbatdp"			VARCHAR (3) NOT NULL, 
	"headingbatsb"			VARCHAR (3) NOT NULL, 
	"headingbatcs"			VARCHAR (3) NOT NULL, 
	"headingbatrbi"			VARCHAR (3) NOT NULL, 
	"headingbatobp"			VARCHAR (3) NOT NULL, 
	"headingbatslg"			VARCHAR (3) NOT NULL, 
	"headingbatba"			VARCHAR (3) NOT NULL, 
	"headingpitching"			VARCHAR (10) NOT NULL, 
	"headingpitchip"			VARCHAR (3) NOT NULL, 
	"headingpitchr"			VARCHAR (3) NOT NULL, 
	"headingpitcher"			VARCHAR (3) NOT NULL, 
	"headingpitchbf"			VARCHAR (3) NOT NULL, 
	"headingpitchab"			VARCHAR (3) NOT NULL, 
	"headingpitchh"			VARCHAR (3) NOT NULL, 
	"headingpitch2b"			VARCHAR (3) NOT NULL, 
	"headingpitch3b"			VARCHAR (3) NOT NULL, 
	"headingpitchhr"			VARCHAR (3) NOT NULL, 
	"headingpitchbb"			VARCHAR (3) NOT NULL, 
	"headingpitchhb"			VARCHAR (3) NOT NULL, 
	"headingpitchso"			VARCHAR (3) NOT NULL, 
	"headingpitchwp"			VARCHAR (3) NOT NULL, 
	"headingpitchbk"			VARCHAR (3) NOT NULL, 
	"headingpitchpo"			VARCHAR (3) NOT NULL, 
	"headingpitchb"			VARCHAR (3) NOT NULL, 
	"headingpitchs"			VARCHAR (3) NOT NULL, 
	"headingpitchtp"			VARCHAR (3) NOT NULL, 
	"headingpitchobp"			VARCHAR (3) NOT NULL, 
	"headingpitchslg"			VARCHAR (3) NOT NULL, 
	"headingpitchba"			VARCHAR (3) NOT NULL, 
	"headingpitchera"			VARCHAR (3) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crboxscores" ADD CONSTRAINT "crboxscores_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crboxscoresdetail"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"detaillinenumber"			INTEGER NOT NULL, 
	"battingplayer"			VARCHAR (50) NOT NULL, 
	"batpa"			VARCHAR (7) NOT NULL, 
	"batab"			VARCHAR (7) NOT NULL, 
	"batr"			VARCHAR (7) NOT NULL, 
	"bath"			VARCHAR (7) NOT NULL, 
	"bat2b"			VARCHAR (7) NOT NULL, 
	"bat3b"			VARCHAR (7) NOT NULL, 
	"bathr"			VARCHAR (7) NOT NULL, 
	"battb"			VARCHAR (7) NOT NULL, 
	"batoe"			VARCHAR (7) NOT NULL, 
	"batfc"			VARCHAR (7) NOT NULL, 
	"batbb"			VARCHAR (7) NOT NULL, 
	"bathp"			VARCHAR (7) NOT NULL, 
	"batso"			VARCHAR (7) NOT NULL, 
	"batsh"			VARCHAR (7) NOT NULL, 
	"batsf"			VARCHAR (7) NOT NULL, 
	"batdp"			VARCHAR (7) NOT NULL, 
	"batsb"			VARCHAR (7) NOT NULL, 
	"batcs"			VARCHAR (7) NOT NULL, 
	"batrbi"			VARCHAR (7) NOT NULL, 
	"batobp"			VARCHAR (7) NOT NULL, 
	"batslg"			VARCHAR (7) NOT NULL, 
	"batba"			VARCHAR (7) NOT NULL, 
	"pitchingplayer"			VARCHAR (50) NOT NULL, 
	"pitchip"			VARCHAR (9) NOT NULL, 
	"pitchr"			VARCHAR (7) NOT NULL, 
	"pitcher"			VARCHAR (7) NOT NULL, 
	"pitchbf"			VARCHAR (7) NOT NULL, 
	"pitchab"			VARCHAR (7) NOT NULL, 
	"pitchh"			VARCHAR (7) NOT NULL, 
	"pitch2b"			VARCHAR (7) NOT NULL, 
	"pitch3b"			VARCHAR (7) NOT NULL, 
	"pitchhr"			VARCHAR (7) NOT NULL, 
	"pitchbb"			VARCHAR (7) NOT NULL, 
	"pitchhb"			VARCHAR (7) NOT NULL, 
	"pitchso"			VARCHAR (7) NOT NULL, 
	"pitchwp"			VARCHAR (7) NOT NULL, 
	"pitchbk"			VARCHAR (7) NOT NULL, 
	"pitchpo"			VARCHAR (7) NOT NULL, 
	"pitchb"			VARCHAR (7) NOT NULL, 
	"pitchs"			VARCHAR (7) NOT NULL, 
	"pitchtp"			VARCHAR (7) NOT NULL, 
	"pitchobp"			VARCHAR (7) NOT NULL, 
	"pitchslg"			VARCHAR (7) NOT NULL, 
	"pitchba"			VARCHAR (7) NOT NULL, 
	"pitchera"			VARCHAR (7) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crboxscoresdetail" ADD CONSTRAINT "crboxscoresdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crbpfstatsdetail"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"detaillinenumber"			INTEGER NOT NULL, 
	"playername"			VARCHAR (50) NOT NULL, 
	"teamname"			VARCHAR (50) NOT NULL, 
	"centertext"			VARCHAR (50) NOT NULL, 
	"g"			VARCHAR (7) NOT NULL, 
	"pa"			VARCHAR (7) NOT NULL, 
	"bf"			VARCHAR (7) NOT NULL, 
	"ab"			VARCHAR (7) NOT NULL, 
	"r"			VARCHAR (7) NOT NULL, 
	"h"			VARCHAR (7) NOT NULL, 
	"s"			VARCHAR (7) NOT NULL, 
	"d"			VARCHAR (7) NOT NULL, 
	"t"			VARCHAR (7) NOT NULL, 
	"hr"			VARCHAR (7) NOT NULL, 
	"tb"			VARCHAR (7) NOT NULL, 
	"oe"			VARCHAR (7) NOT NULL, 
	"fc"			VARCHAR (7) NOT NULL, 
	"bb"			VARCHAR (7) NOT NULL, 
	"hp"			VARCHAR (7) NOT NULL, 
	"hb"			VARCHAR (7) NOT NULL, 
	"co"			VARCHAR (7) NOT NULL, 
	"so"			VARCHAR (7) NOT NULL, 
	"sh"			VARCHAR (7) NOT NULL, 
	"sf"			VARCHAR (7) NOT NULL, 
	"dp"			VARCHAR (7) NOT NULL, 
	"sb"			VARCHAR (7) NOT NULL, 
	"cs"			VARCHAR (7) NOT NULL, 
	"rbi"			VARCHAR (7) NOT NULL, 
	"chs"			VARCHAR (7) NOT NULL, 
	"lhs"			VARCHAR (7) NOT NULL, 
	"c"			VARCHAR (7) NOT NULL, 
	"a"			VARCHAR (7) NOT NULL, 
	"e"			VARCHAR (7) NOT NULL, 
	"pb"			VARCHAR (7) NOT NULL, 
	"ip"			VARCHAR (9) NOT NULL, 
	"er"			VARCHAR (7) NOT NULL, 
	"wp"			VARCHAR (7) NOT NULL, 
	"bk"			VARCHAR (7) NOT NULL, 
	"po"			VARCHAR (7) NOT NULL, 
	"pickoff"			VARCHAR (7) NOT NULL, 
	"ball"			VARCHAR (7) NOT NULL, 
	"strike"			VARCHAR (7) NOT NULL, 
	"tp"			VARCHAR (7) NOT NULL, 
	"gs"			VARCHAR (7) NOT NULL, 
	"gf"			VARCHAR (7) NOT NULL, 
	"cg"			VARCHAR (7) NOT NULL, 
	"w"			VARCHAR (7) NOT NULL, 
	"l"			VARCHAR (7) NOT NULL, 
	"sv"			VARCHAR (7) NOT NULL, 
	"sho"			VARCHAR (7) NOT NULL, 
	"ba"			VARCHAR (7) NOT NULL, 
	"fa"			VARCHAR (7) NOT NULL, 
	"obp"			VARCHAR (7) NOT NULL, 
	"slg"			VARCHAR (7) NOT NULL, 
	"pp"			VARCHAR (7) NOT NULL, 
	"rc"			VARCHAR (7) NOT NULL, 
	"ta"			VARCHAR (7) NOT NULL, 
	"sba"			VARCHAR (7) NOT NULL, 
	"csa"			VARCHAR (7) NOT NULL, 
	"rng"			VARCHAR (7) NOT NULL, 
	"era"			VARCHAR (7) NOT NULL, 
	"sog"			VARCHAR (7) NOT NULL, 
	"whip"			VARCHAR (7) NOT NULL, 
	"spct"			VARCHAR (7) NOT NULL, 
	"user1"			VARCHAR (7) NOT NULL, 
	"user2"			VARCHAR (7) NOT NULL, 
	"user3"			VARCHAR (7) NOT NULL, 
	"user4"			VARCHAR (7) NOT NULL, 
	"user5"			VARCHAR (7) NOT NULL, 
	"users1"			VARCHAR (7) NOT NULL, 
	"users2"			VARCHAR (7) NOT NULL, 
	"users3"			VARCHAR (7) NOT NULL, 
	"users4"			VARCHAR (7) NOT NULL, 
	"users5"			VARCHAR (7) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crbpfstatsdetail" ADD CONSTRAINT "crbpfstatsdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crgamescores"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (100) NOT NULL, 
	"teamtitle"			VARCHAR (100) NOT NULL, 
	"reportdate"			VARCHAR (25) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crgamescores" ADD CONSTRAINT "crgamescores_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crgamescoresdetail"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"detaillinenumber"			INTEGER NOT NULL, 
	"gamenumber"			VARCHAR (5) NOT NULL, 
	"gamedescription"			TEXT NOT NULL, 
	"team"			VARCHAR (50) NOT NULL, 
	"runs"			VARCHAR (10) NOT NULL, 
	"decision"			VARCHAR (5) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crgamescoresdetail" ADD CONSTRAINT "crgamescoresdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crleaderstats"
 (
	"reportid"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (30) NOT NULL, 
	"teamtitle"			VARCHAR (30), 
	"reportdate"			TIMESTAMP WITHOUT TIME ZONE, 
	"topxrecords"			INTEGER, 
	"minimumtype"			VARCHAR (1), 
	"minimumnumber"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "crlineupdetail"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"detaillinenumber"			INTEGER NOT NULL, 
	"lineuporder"			VARCHAR (3) NOT NULL, 
	"playername"			VARCHAR (50) NOT NULL, 
	"inn1"			VARCHAR (5) NOT NULL, 
	"inn2"			VARCHAR (5) NOT NULL, 
	"inn3"			VARCHAR (5) NOT NULL, 
	"inn4"			VARCHAR (5) NOT NULL, 
	"inn5"			VARCHAR (5) NOT NULL, 
	"inn6"			VARCHAR (5) NOT NULL, 
	"inn7"			VARCHAR (5) NOT NULL, 
	"inn8"			VARCHAR (5) NOT NULL, 
	"inn9"			VARCHAR (5) NOT NULL
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
	"reportidnumber"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (100) NOT NULL, 
	"teamtitle"			VARCHAR (100) NOT NULL, 
	"reportdate"			VARCHAR (25) NOT NULL, 
	"headingties"			VARCHAR (10) NOT NULL, 
	"headingrf"			VARCHAR (20) NOT NULL, 
	"headingra"			VARCHAR (20) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crrecord" ADD CONSTRAINT "crrecord_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crroster"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (100) NOT NULL, 
	"teamtitle"			VARCHAR (100) NOT NULL, 
	"reportdate"			VARCHAR (25) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crroster" ADD CONSTRAINT "crroster_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crrosterdetail"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"detaillinenumber"			INTEGER NOT NULL, 
	"playername"			VARCHAR (50) NOT NULL, 
	"playernumber"			VARCHAR (3) NOT NULL, 
	"addressline1"			VARCHAR (40) NOT NULL, 
	"addressline2"			VARCHAR (40) NOT NULL, 
	"city"			VARCHAR (20) NOT NULL, 
	"state"			VARCHAR (20) NOT NULL, 
	"zip"			VARCHAR (20) NOT NULL, 
	"homephone"			VARCHAR (20) NOT NULL, 
	"workphone"			VARCHAR (20) NOT NULL, 
	"email"			VARCHAR (50) NOT NULL, 
	"birthdate"			VARCHAR (25) NOT NULL, 
	"notes"			TEXT NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crrosterdetail" ADD CONSTRAINT "crrosterdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crscorebyinnings"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (100) NOT NULL, 
	"teamtitle"			VARCHAR (100) NOT NULL, 
	"reportdate"			VARCHAR (25) NOT NULL, 
	"headinginn1"			VARCHAR (3) NOT NULL, 
	"headinginn2"			VARCHAR (3) NOT NULL, 
	"headinginn3"			VARCHAR (3) NOT NULL, 
	"headinginn4"			VARCHAR (3) NOT NULL, 
	"headinginn5"			VARCHAR (3) NOT NULL, 
	"headinginn6"			VARCHAR (3) NOT NULL, 
	"headinginn7"			VARCHAR (3) NOT NULL, 
	"headinginn8"			VARCHAR (3) NOT NULL, 
	"headinginn9"			VARCHAR (3) NOT NULL, 
	"headinginn10"			VARCHAR (3) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crscorebyinnings" ADD CONSTRAINT "crscorebyinnings_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crscorebyinningsdetail"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"detaillinenumber"			INTEGER NOT NULL, 
	"teamordate"			VARCHAR (50) NOT NULL, 
	"inn1"			VARCHAR (6) NOT NULL, 
	"inn2"			VARCHAR (6) NOT NULL, 
	"inn3"			VARCHAR (6) NOT NULL, 
	"inn4"			VARCHAR (6) NOT NULL, 
	"inn5"			VARCHAR (6) NOT NULL, 
	"inn6"			VARCHAR (6) NOT NULL, 
	"inn7"			VARCHAR (6) NOT NULL, 
	"inn8"			VARCHAR (6) NOT NULL, 
	"inn9"			VARCHAR (6) NOT NULL, 
	"inn10"			VARCHAR (6) NOT NULL, 
	"finalscore"			VARCHAR (6) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crscorebyinningsdetail" ADD CONSTRAINT "crscorebyinningsdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crstandingsdetail"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"detaillinenumber"			INTEGER NOT NULL, 
	"team"			VARCHAR (50) NOT NULL, 
	"gameswon"			VARCHAR (10) NOT NULL, 
	"gameslost"			VARCHAR (10) NOT NULL, 
	"gamestied"			VARCHAR (10) NOT NULL, 
	"streak"			VARCHAR (10) NOT NULL, 
	"winpct"			VARCHAR (10) NOT NULL, 
	"runsfor"			VARCHAR (10) NOT NULL, 
	"runsagainst"			VARCHAR (10) NOT NULL, 
	"gamesbehind"			VARCHAR (10) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crstandingsdetail" ADD CONSTRAINT "crstandingsdetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "fieldingrptcats"
 (
	"reportnumber"			INTEGER NOT NULL, 
	"reportorder"			SMALLINT NOT NULL, 
	"categorynumber"			SMALLINT NOT NULL
);
COMMENT ON COLUMN "fieldingrptcats"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "fieldingrptcats"."reportorder" IS 'Report Order';
COMMENT ON COLUMN "fieldingrptcats"."categorynumber" IS 'Category Number';

-- CREATE INDEXES ...
ALTER TABLE "fieldingrptcats" ADD CONSTRAINT "fieldingrptcats_pkey" PRIMARY KEY ("reportnumber", "reportorder");

CREATE TABLE IF NOT EXISTS "fieldingrptformat"
 (
	"reportnumber"			INTEGER NOT NULL, 
	"reportdescription"			VARCHAR (25) NOT NULL, 
	"sortcategory"			SMALLINT NOT NULL, 
	"sortdirection"			VARCHAR (1) NOT NULL
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
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"eventnumber"			SMALLINT NOT NULL, 
	"gametype"			INTEGER NOT NULL, 
	"hometeam"			BOOLEAN NOT NULL, 
	"starter"			BOOLEAN NOT NULL, 
	"fieldingposition"			SMALLINT NOT NULL, 
	"po"			INTEGER NOT NULL, 
	"a"			INTEGER NOT NULL, 
	"e"			INTEGER NOT NULL, 
	"dp"			INTEGER NOT NULL, 
	"pb"			INTEGER NOT NULL, 
	"sb"			INTEGER NOT NULL, 
	"cs"			INTEGER NOT NULL, 
	"u1"			INTEGER NOT NULL, 
	"u2"			INTEGER NOT NULL, 
	"u3"			INTEGER NOT NULL, 
	"u4"			INTEGER NOT NULL, 
	"u5"			INTEGER NOT NULL, 
	"u6"			INTEGER NOT NULL, 
	"u7"			INTEGER NOT NULL, 
	"u8"			INTEGER NOT NULL, 
	"u9"			INTEGER NOT NULL, 
	"u10"			INTEGER NOT NULL, 
	"notes"			TEXT NOT NULL
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
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"lineupnumber"			INTEGER NOT NULL, 
	"starter"			BOOLEAN NOT NULL, 
	"fieldingposition"			SMALLINT NOT NULL, 
	"fieldingposition2"			SMALLINT NOT NULL, 
	"fieldingposition3"			SMALLINT NOT NULL, 
	"fieldingposition4"			SMALLINT NOT NULL, 
	"batting"			BOOLEAN NOT NULL, 
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
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"gstatnumber"			INTEGER NOT NULL, 
	"gamedate"			TIMESTAMP WITHOUT TIME ZONE, 
	"gametype"			INTEGER NOT NULL, 
	"location"			VARCHAR (30) NOT NULL, 
	"innings"			SMALLINT NOT NULL, 
	"hometeam"			BOOLEAN NOT NULL, 
	"opponent"			VARCHAR (50) NOT NULL, 
	"opponentteamnumber"			INTEGER NOT NULL, 
	"opponentgstatnumber"			INTEGER NOT NULL, 
	"dp"			INTEGER NOT NULL, 
	"runs"			INTEGER NOT NULL, 
	"runsinning1"			SMALLINT NOT NULL, 
	"runsinning2"			SMALLINT NOT NULL, 
	"runsinning3"			SMALLINT NOT NULL, 
	"runsinning4"			SMALLINT NOT NULL, 
	"runsinning5"			SMALLINT NOT NULL, 
	"runsinning6"			SMALLINT NOT NULL, 
	"runsinning7"			SMALLINT NOT NULL, 
	"runsinning8"			SMALLINT NOT NULL, 
	"runsinning9"			SMALLINT NOT NULL, 
	"runsinningx"			SMALLINT NOT NULL, 
	"oppruns"			INTEGER NOT NULL, 
	"opprunsinning1"			SMALLINT NOT NULL, 
	"opprunsinning2"			SMALLINT NOT NULL, 
	"opprunsinning3"			SMALLINT NOT NULL, 
	"opprunsinning4"			SMALLINT NOT NULL, 
	"opprunsinning5"			SMALLINT NOT NULL, 
	"opprunsinning6"			SMALLINT NOT NULL, 
	"opprunsinning7"			SMALLINT NOT NULL, 
	"opprunsinning8"			SMALLINT NOT NULL, 
	"opprunsinning9"			SMALLINT NOT NULL, 
	"opprunsinningx"			SMALLINT NOT NULL, 
	"notes"			TEXT NOT NULL
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
	"gametypenumber"			INTEGER NOT NULL, 
	"gametypedescription"			VARCHAR (25) NOT NULL
);
COMMENT ON COLUMN "gametypes"."gametypedescription" IS 'GameTypeDescription';

-- CREATE INDEXES ...
ALTER TABLE "gametypes" ADD CONSTRAINT "gametypes_pkey" PRIMARY KEY ("gametypenumber");

CREATE TABLE IF NOT EXISTS "inputorder"
 (
	"categorytype"			VARCHAR (1) NOT NULL, 
	"ordernumber"			INTEGER NOT NULL, 
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
	"ftpexport"			BOOLEAN NOT NULL, 
	"ftpwarnoverwrite"			BOOLEAN NOT NULL, 
	"ftpurl"			TEXT, 
	"ftpdirectory"			TEXT, 
	"ftpuserid"			VARCHAR (255), 
	"ftppassword"			VARCHAR (255), 
	"fileexport"			BOOLEAN NOT NULL, 
	"filedirectory"			TEXT, 
	"websitename"			TEXT, 
	"apwebexport"			BOOLEAN NOT NULL, 
	"apwebid"			VARCHAR (255), 
	"apwebuserurl"			VARCHAR (255), 
	"apwebftpuser"			VARCHAR (255), 
	"apwebftppass"			VARCHAR (255), 
	"apwebhttpurl"			VARCHAR (255), 
	"apwebftpurl"			VARCHAR (255), 
	"apwebftpdirectory"			VARCHAR (255), 
	"apwebserverurl"			VARCHAR (255), 
	"shownews"			BOOLEAN NOT NULL, 
	"showlinks"			BOOLEAN NOT NULL, 
	"showbatting"			BOOLEAN NOT NULL, 
	"showpitching"			BOOLEAN NOT NULL, 
	"showfielding"			BOOLEAN NOT NULL, 
	"showroster"			BOOLEAN NOT NULL, 
	"showrecord"			BOOLEAN NOT NULL, 
	"showgamescores"			BOOLEAN NOT NULL, 
	"showboxscores"			BOOLEAN NOT NULL, 
	"showscoresbyinning"			BOOLEAN NOT NULL, 
	"showstandings"			BOOLEAN NOT NULL, 
	"includecontact"			BOOLEAN NOT NULL, 
	"includenotes"			BOOLEAN NOT NULL, 
	"showpicturegallery"			BOOLEAN NOT NULL, 
	"showplayer"			BOOLEAN NOT NULL
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "internetteams"
 (
	"teamnumber"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "leadercats"
 (
	"stattype"			INTEGER NOT NULL, 
	"reportorder"			INTEGER NOT NULL, 
	"categorynumber"			INTEGER NOT NULL
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "leaderstats"
 (
	"personnumber"			INTEGER NOT NULL, 
	"teamnumber"			INTEGER NOT NULL, 
	"stattype"			INTEGER NOT NULL, 
	"statheading"			VARCHAR (20) NOT NULL, 
	"stat"			VARCHAR (20) NOT NULL, 
	"reportorder"			INTEGER NOT NULL
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "lineupplayer"
 (
	"teamnumber"			INTEGER NOT NULL, 
	"lineupnumber"			INTEGER NOT NULL, 
	"sequencenumber"			INTEGER NOT NULL, 
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
	"categorytype"			VARCHAR (3) NOT NULL, 
	"categorynumber"			INTEGER NOT NULL, 
	"categorydescription"			VARCHAR (5) NOT NULL
);
COMMENT ON COLUMN "nameyourowncats"."categorytype" IS 'Category Type';
COMMENT ON COLUMN "nameyourowncats"."categorynumber" IS 'Category Number';
COMMENT ON COLUMN "nameyourowncats"."categorydescription" IS 'Category Description';

-- CREATE INDEXES ...
ALTER TABLE "nameyourowncats" ADD CONSTRAINT "nameyourowncats_pkey" PRIMARY KEY ("categorytype", "categorynumber");

CREATE TABLE IF NOT EXISTS "nameyourownstats"
 (
	"categorytype"			VARCHAR (3) NOT NULL, 
	"categorynumber"			INTEGER NOT NULL, 
	"categorydescription"			VARCHAR (5) NOT NULL, 
	"decimals"			SMALLINT NOT NULL, 
	"teamtotal"			BOOLEAN NOT NULL, 
	"cat1"			REAL NOT NULL, 
	"cat2"			REAL NOT NULL, 
	"cat3"			REAL NOT NULL, 
	"cat4"			REAL NOT NULL, 
	"cat5"			REAL NOT NULL, 
	"cat6"			REAL NOT NULL, 
	"cat7"			REAL NOT NULL, 
	"cat8"			REAL NOT NULL, 
	"cat9"			REAL NOT NULL, 
	"cat10"			REAL NOT NULL, 
	"cat11"			REAL NOT NULL, 
	"cat12"			REAL NOT NULL, 
	"op1"			SMALLINT NOT NULL, 
	"op2"			SMALLINT NOT NULL, 
	"op3"			SMALLINT NOT NULL, 
	"op4"			SMALLINT NOT NULL, 
	"op5"			SMALLINT NOT NULL, 
	"op6"			SMALLINT NOT NULL, 
	"op7"			SMALLINT NOT NULL, 
	"op8"			SMALLINT NOT NULL, 
	"op9"			SMALLINT NOT NULL, 
	"op10"			SMALLINT NOT NULL, 
	"midop"			SMALLINT NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "nameyourownstats" ADD CONSTRAINT "nameyourownstats_pkey" PRIMARY KEY ("categorytype", "categorynumber");

CREATE TABLE IF NOT EXISTS "numberoptions"
 (
	"optionnumber"			INTEGER NOT NULL, 
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
	"personnumber"			INTEGER NOT NULL, 
	"firstname"			VARCHAR (20) NOT NULL, 
	"lastname"			VARCHAR (20) NOT NULL, 
	"address1"			VARCHAR (40) NOT NULL, 
	"address2"			VARCHAR (40) NOT NULL, 
	"city"			VARCHAR (20) NOT NULL, 
	"state"			VARCHAR (20) NOT NULL, 
	"zip"			VARCHAR (20) NOT NULL, 
	"country"			VARCHAR (20) NOT NULL, 
	"homephone"			VARCHAR (20) NOT NULL, 
	"workphone"			VARCHAR (20) NOT NULL, 
	"faxnumber"			VARCHAR (20) NOT NULL, 
	"emailaddress"			VARCHAR (50) NOT NULL, 
	"birthdate"			DATE, 
	"notes"			TEXT NOT NULL
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
	"publishtoweb"			BOOLEAN NOT NULL, 
	"sortorder"			INTEGER
);

-- CREATE INDEXES ...

CREATE TABLE IF NOT EXISTS "pitchingrptformat"
 (
	"reportnumber"			INTEGER NOT NULL, 
	"reportdescription"			VARCHAR (25) NOT NULL, 
	"sortcategory"			SMALLINT NOT NULL, 
	"sortdirection"			VARCHAR (1) NOT NULL
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
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"eventnumber"			SMALLINT NOT NULL, 
	"gametype"			INTEGER NOT NULL, 
	"hometeam"			BOOLEAN NOT NULL, 
	"starter"			BOOLEAN NOT NULL, 
	"ip"			INTEGER NOT NULL, 
	"ip13"			SMALLINT NOT NULL, 
	"bf"			INTEGER NOT NULL, 
	"r"			INTEGER NOT NULL, 
	"er"			INTEGER NOT NULL, 
	"h"			INTEGER NOT NULL, 
	"d"			INTEGER NOT NULL, 
	"t"			INTEGER NOT NULL, 
	"hr"			INTEGER NOT NULL, 
	"bb"			INTEGER NOT NULL, 
	"hb"			INTEGER NOT NULL, 
	"co"			INTEGER NOT NULL, 
	"so"			INTEGER NOT NULL, 
	"sh"			INTEGER NOT NULL, 
	"sf"			INTEGER NOT NULL, 
	"wp"			INTEGER NOT NULL, 
	"bk"			INTEGER NOT NULL, 
	"po"			INTEGER NOT NULL, 
	"b"			INTEGER NOT NULL, 
	"s"			INTEGER NOT NULL, 
	"gs"			INTEGER NOT NULL, 
	"gf"			INTEGER NOT NULL, 
	"cg"			INTEGER NOT NULL, 
	"w"			INTEGER NOT NULL, 
	"l"			INTEGER NOT NULL, 
	"sv"			INTEGER NOT NULL, 
	"sho"			INTEGER NOT NULL, 
	"u1"			INTEGER NOT NULL, 
	"u2"			INTEGER NOT NULL, 
	"u3"			INTEGER NOT NULL, 
	"u4"			INTEGER NOT NULL, 
	"u5"			INTEGER NOT NULL, 
	"u6"			INTEGER NOT NULL, 
	"u7"			INTEGER NOT NULL, 
	"u8"			INTEGER NOT NULL, 
	"u9"			INTEGER NOT NULL, 
	"u10"			INTEGER NOT NULL, 
	"notes"			TEXT NOT NULL
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
	"programversion"			REAL NOT NULL, 
	"versiondate"			DATE NOT NULL
);
COMMENT ON COLUMN "programversion"."programversion" IS 'Program Version';
COMMENT ON COLUMN "programversion"."versiondate" IS 'Version Date';

-- CREATE INDEXES ...
ALTER TABLE "programversion" ADD CONSTRAINT "programversion_pkey" PRIMARY KEY ("programversion");

CREATE TABLE IF NOT EXISTS "reportnumber"
 (
	"reporttype"			VARCHAR (1) NOT NULL, 
	"reportnumber"			INTEGER NOT NULL
);
COMMENT ON COLUMN "reportnumber"."reporttype" IS 'Report Type';
COMMENT ON COLUMN "reportnumber"."reportnumber" IS 'Report Number';

-- CREATE INDEXES ...
ALTER TABLE "reportnumber" ADD CONSTRAINT "reportnumber_pkey" PRIMARY KEY ("reporttype");

CREATE TABLE IF NOT EXISTS "rptbatting"
 (
	"sortkey"			INTEGER NOT NULL, 
	"teamnumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"opponent"			VARCHAR (25) NOT NULL, 
	"g"			VARCHAR (7) NOT NULL, 
	"pa"			VARCHAR (7) NOT NULL, 
	"ab"			VARCHAR (7) NOT NULL, 
	"r"			VARCHAR (7) NOT NULL, 
	"h"			VARCHAR (7) NOT NULL, 
	"s"			VARCHAR (7) NOT NULL, 
	"d"			VARCHAR (7) NOT NULL, 
	"t"			VARCHAR (7) NOT NULL, 
	"hr"			VARCHAR (7) NOT NULL, 
	"tb"			VARCHAR (7) NOT NULL, 
	"oe"			VARCHAR (7) NOT NULL, 
	"fc"			VARCHAR (7) NOT NULL, 
	"bb"			VARCHAR (7) NOT NULL, 
	"hp"			VARCHAR (7) NOT NULL, 
	"co"			VARCHAR (7) NOT NULL, 
	"so"			VARCHAR (7) NOT NULL, 
	"sh"			VARCHAR (7) NOT NULL, 
	"sf"			VARCHAR (7) NOT NULL, 
	"dp"			VARCHAR (7) NOT NULL, 
	"sb"			VARCHAR (7) NOT NULL, 
	"cs"			VARCHAR (7) NOT NULL, 
	"rbi"			VARCHAR (7) NOT NULL, 
	"ba"			VARCHAR (5) NOT NULL, 
	"obp"			VARCHAR (5) NOT NULL, 
	"slg"			VARCHAR (5) NOT NULL, 
	"pp"			VARCHAR (5) NOT NULL, 
	"rc"			VARCHAR (7) NOT NULL, 
	"ta"			VARCHAR (6) NOT NULL, 
	"sba"			VARCHAR (5) NOT NULL, 
	"user1"			VARCHAR (7) NOT NULL, 
	"user2"			VARCHAR (7) NOT NULL, 
	"user3"			VARCHAR (7) NOT NULL, 
	"user4"			VARCHAR (7) NOT NULL, 
	"user5"			VARCHAR (7) NOT NULL, 
	"users1"			VARCHAR (7) NOT NULL, 
	"users2"			VARCHAR (7) NOT NULL, 
	"users3"			VARCHAR (7) NOT NULL, 
	"users4"			VARCHAR (7) NOT NULL, 
	"users5"			VARCHAR (7) NOT NULL, 
	"chs"			VARCHAR (5) NOT NULL, 
	"lhs"			VARCHAR (5) NOT NULL, 
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
	"sortkey"			INTEGER NOT NULL, 
	"batter"			VARCHAR (50) NOT NULL, 
	"b_ab"			VARCHAR (5) NOT NULL, 
	"b_r"			VARCHAR (5) NOT NULL, 
	"b_h"			VARCHAR (5) NOT NULL, 
	"b_hr"			VARCHAR (5) NOT NULL, 
	"b_bb"			VARCHAR (5) NOT NULL, 
	"b_so"			VARCHAR (5) NOT NULL, 
	"b_rbi"			VARCHAR (5) NOT NULL, 
	"separator"			VARCHAR (1) NOT NULL, 
	"pitcher"			VARCHAR (50) NOT NULL, 
	"p_ip"			VARCHAR (5) NOT NULL, 
	"p_r"			VARCHAR (5) NOT NULL, 
	"p_er"			VARCHAR (5) NOT NULL, 
	"p_h"			VARCHAR (5) NOT NULL, 
	"p_hr"			VARCHAR (5) NOT NULL, 
	"p_bb"			VARCHAR (5) NOT NULL, 
	"p_so"			VARCHAR (5) NOT NULL, 
	"b_pa"			VARCHAR (5) NOT NULL, 
	"b_2b"			VARCHAR (5) NOT NULL, 
	"b_3b"			VARCHAR (5) NOT NULL, 
	"b_tb"			VARCHAR (5) NOT NULL, 
	"b_oe"			VARCHAR (5) NOT NULL, 
	"b_fc"			VARCHAR (5) NOT NULL, 
	"b_hp"			VARCHAR (5) NOT NULL, 
	"b_sh"			VARCHAR (5) NOT NULL, 
	"b_sf"			VARCHAR (5) NOT NULL, 
	"b_dp"			VARCHAR (5) NOT NULL, 
	"b_sb"			VARCHAR (5) NOT NULL, 
	"b_cs"			VARCHAR (5) NOT NULL, 
	"b_obp"			VARCHAR (5) NOT NULL, 
	"b_slg"			VARCHAR (5) NOT NULL, 
	"b_ba"			VARCHAR (5) NOT NULL, 
	"p_bf"			VARCHAR (5) NOT NULL, 
	"p_ab"			VARCHAR (5) NOT NULL, 
	"p_2b"			VARCHAR (5) NOT NULL, 
	"p_3b"			VARCHAR (5) NOT NULL, 
	"p_hb"			VARCHAR (5) NOT NULL, 
	"p_wp"			VARCHAR (5) NOT NULL, 
	"p_bk"			VARCHAR (5) NOT NULL, 
	"p_po"			VARCHAR (5) NOT NULL, 
	"p_b"			VARCHAR (5) NOT NULL, 
	"p_s"			VARCHAR (5) NOT NULL, 
	"p_tp"			VARCHAR (5) NOT NULL, 
	"p_obp"			VARCHAR (5) NOT NULL, 
	"p_slg"			VARCHAR (5) NOT NULL, 
	"p_ba"			VARCHAR (5) NOT NULL, 
	"p_era"			VARCHAR (5) NOT NULL
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
	"sortkey"			INTEGER NOT NULL, 
	"teamnumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"opponent"			VARCHAR (25) NOT NULL, 
	"g"			VARCHAR (7) NOT NULL, 
	"po"			VARCHAR (7) NOT NULL, 
	"a"			VARCHAR (7) NOT NULL, 
	"e"			VARCHAR (7) NOT NULL, 
	"c"			VARCHAR (7) NOT NULL, 
	"dp"			VARCHAR (7) NOT NULL, 
	"pb"			VARCHAR (7) NOT NULL, 
	"sb"			VARCHAR (7) NOT NULL, 
	"cs"			VARCHAR (7) NOT NULL, 
	"csa"			VARCHAR (5) NOT NULL, 
	"fa"			VARCHAR (5) NOT NULL, 
	"rng"			VARCHAR (7) NOT NULL, 
	"user1"			VARCHAR (7) NOT NULL, 
	"user2"			VARCHAR (7) NOT NULL, 
	"user3"			VARCHAR (7) NOT NULL, 
	"user4"			VARCHAR (7) NOT NULL, 
	"user5"			VARCHAR (7) NOT NULL, 
	"users1"			VARCHAR (7) NOT NULL, 
	"users2"			VARCHAR (7) NOT NULL, 
	"users3"			VARCHAR (7) NOT NULL, 
	"users4"			VARCHAR (7) NOT NULL, 
	"users5"			VARCHAR (7) NOT NULL, 
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
	"sortkey"			INTEGER NOT NULL, 
	"teamname"			VARCHAR (100) NOT NULL, 
	"inn1score"			VARCHAR (7) NOT NULL, 
	"inn2score"			VARCHAR (7) NOT NULL, 
	"inn3score"			VARCHAR (7) NOT NULL, 
	"inn4score"			VARCHAR (7) NOT NULL, 
	"inn5score"			VARCHAR (7) NOT NULL, 
	"inn6score"			VARCHAR (7) NOT NULL, 
	"inn7score"			VARCHAR (7) NOT NULL, 
	"inn8score"			VARCHAR (7) NOT NULL, 
	"inn9score"			VARCHAR (7) NOT NULL, 
	"innxscore"			VARCHAR (7) NOT NULL, 
	"finalscore"			VARCHAR (9) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "rptinnings" ADD CONSTRAINT "rptinnings_pkey" PRIMARY KEY ("sortkey");

CREATE TABLE IF NOT EXISTS "rptpitching"
 (
	"sortkey"			INTEGER NOT NULL, 
	"teamnumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"opponent"			VARCHAR (25) NOT NULL, 
	"g"			VARCHAR (7) NOT NULL, 
	"ip"			VARCHAR (9) NOT NULL, 
	"r"			VARCHAR (7) NOT NULL, 
	"er"			VARCHAR (7) NOT NULL, 
	"bf"			VARCHAR (7) NOT NULL, 
	"ab"			VARCHAR (7) NOT NULL, 
	"h"			VARCHAR (7) NOT NULL, 
	"d"			VARCHAR (7) NOT NULL, 
	"t"			VARCHAR (7) NOT NULL, 
	"hr"			VARCHAR (7) NOT NULL, 
	"tb"			VARCHAR (7) NOT NULL, 
	"bb"			VARCHAR (7) NOT NULL, 
	"hb"			VARCHAR (7) NOT NULL, 
	"co"			VARCHAR (7) NOT NULL, 
	"so"			VARCHAR (7) NOT NULL, 
	"sh"			VARCHAR (7) NOT NULL, 
	"sf"			VARCHAR (7) NOT NULL, 
	"wp"			VARCHAR (7) NOT NULL, 
	"bk"			VARCHAR (7) NOT NULL, 
	"po"			VARCHAR (7) NOT NULL, 
	"b"			VARCHAR (7) NOT NULL, 
	"s"			VARCHAR (7) NOT NULL, 
	"tp"			VARCHAR (7) NOT NULL, 
	"gs"			VARCHAR (7) NOT NULL, 
	"gf"			VARCHAR (7) NOT NULL, 
	"cg"			VARCHAR (7) NOT NULL, 
	"w"			VARCHAR (7) NOT NULL, 
	"l"			VARCHAR (7) NOT NULL, 
	"sv"			VARCHAR (7) NOT NULL, 
	"sho"			VARCHAR (7) NOT NULL, 
	"ba"			VARCHAR (5) NOT NULL, 
	"obp"			VARCHAR (5) NOT NULL, 
	"slg"			VARCHAR (5) NOT NULL, 
	"sog"			VARCHAR (5) NOT NULL, 
	"era"			VARCHAR (7) NOT NULL, 
	"spct"			VARCHAR (5) NOT NULL, 
	"whip"			VARCHAR (5) NOT NULL, 
	"user1"			VARCHAR (7) NOT NULL, 
	"user2"			VARCHAR (7) NOT NULL, 
	"user3"			VARCHAR (7) NOT NULL, 
	"user4"			VARCHAR (7) NOT NULL, 
	"user5"			VARCHAR (7) NOT NULL, 
	"users1"			VARCHAR (7) NOT NULL, 
	"users2"			VARCHAR (7) NOT NULL, 
	"users3"			VARCHAR (7) NOT NULL, 
	"users4"			VARCHAR (7) NOT NULL, 
	"users5"			VARCHAR (7) NOT NULL, 
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
	"sortkey"			INTEGER NOT NULL, 
	"teamnumber"			INTEGER NOT NULL, 
	"gametype"			INTEGER NOT NULL, 
	"gametypedescription"			VARCHAR (25) NOT NULL, 
	"gameswon"			VARCHAR (7) NOT NULL, 
	"gameslost"			VARCHAR (7) NOT NULL, 
	"gamestied"			VARCHAR (7) NOT NULL, 
	"winpct"			VARCHAR (5) NOT NULL, 
	"runsfor"			VARCHAR (7) NOT NULL, 
	"runsagainst"			VARCHAR (7) NOT NULL
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
	"sortkey"			INTEGER NOT NULL, 
	"text"			VARCHAR (50) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "rptroster" ADD CONSTRAINT "rptroster_pkey" PRIMARY KEY ("sortkey");

CREATE TABLE IF NOT EXISTS "rptstandings"
 (
	"sortkey"			INTEGER NOT NULL, 
	"teamnumber"			INTEGER NOT NULL, 
	"teamname"			VARCHAR (50) NOT NULL, 
	"gameswon"			VARCHAR (7) NOT NULL, 
	"gameslost"			VARCHAR (7) NOT NULL, 
	"gamestied"			VARCHAR (7) NOT NULL, 
	"streak"			VARCHAR (15) NOT NULL, 
	"winpct"			VARCHAR (50) NOT NULL, 
	"runsfor"			VARCHAR (7) NOT NULL, 
	"runsagainst"			VARCHAR (7) NOT NULL, 
	"gamesbehind"			VARCHAR (7) NOT NULL
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
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"inning"			SMALLINT NOT NULL, 
	"inningab"			SMALLINT NOT NULL, 
	"lineupnumber"			SMALLINT NOT NULL, 
	"pitcher"			INTEGER NOT NULL, 
	"outonbasespitcher"			INTEGER NOT NULL, 
	"abtype"			SMALLINT NOT NULL, 
	"sb"			SMALLINT NOT NULL, 
	"cs"			SMALLINT NOT NULL, 
	"rbi"			SMALLINT NOT NULL, 
	"batting"			BOOLEAN NOT NULL, 
	"out"			BOOLEAN NOT NULL, 
	"outonbases"			BOOLEAN NOT NULL, 
	"leftforpr"			BOOLEAN NOT NULL, 
	"earnedrun"			BOOLEAN NOT NULL, 
	"basenumber"			SMALLINT NOT NULL, 
	"balls"			SMALLINT NOT NULL, 
	"strikes"			SMALLINT NOT NULL, 
	"twostrikefouls"			SMALLINT NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "rtbattingstats" ADD CONSTRAINT "rtbattingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber", "inning", "inningab");

CREATE TABLE IF NOT EXISTS "rtfieldingstats"
 (
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"po"			INTEGER NOT NULL, 
	"a"			INTEGER NOT NULL, 
	"e"			INTEGER NOT NULL, 
	"dp"			INTEGER NOT NULL, 
	"pb"			INTEGER NOT NULL, 
	"sb"			INTEGER NOT NULL, 
	"cs"			INTEGER NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "rtfieldingstats" ADD CONSTRAINT "rtfieldingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber");

CREATE TABLE IF NOT EXISTS "rtgamestats"
 (
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"innings"			SMALLINT NOT NULL, 
	"pitching"			BOOLEAN NOT NULL, 
	"fielding"			BOOLEAN NOT NULL, 
	"runsinning1"			INTEGER NOT NULL, 
	"opprunsinning1"			INTEGER NOT NULL, 
	"runsinning2"			INTEGER NOT NULL, 
	"opprunsinning2"			INTEGER NOT NULL, 
	"runsinning3"			INTEGER NOT NULL, 
	"opprunsinning3"			INTEGER NOT NULL, 
	"runsinning4"			INTEGER NOT NULL, 
	"opprunsinning4"			INTEGER NOT NULL, 
	"runsinning5"			INTEGER NOT NULL, 
	"opprunsinning5"			INTEGER NOT NULL, 
	"runsinning6"			INTEGER NOT NULL, 
	"opprunsinning6"			INTEGER NOT NULL, 
	"runsinning7"			INTEGER NOT NULL, 
	"opprunsinning7"			INTEGER NOT NULL, 
	"runsinning8"			INTEGER NOT NULL, 
	"opprunsinning8"			INTEGER NOT NULL, 
	"runsinning9"			INTEGER NOT NULL, 
	"opprunsinning9"			INTEGER NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "rtgamestats" ADD CONSTRAINT "rtgamestats_pkey" PRIMARY KEY ("teamnumber", "gamenumber");

CREATE TABLE IF NOT EXISTS "rtpitchingstats"
 (
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"wp"			INTEGER NOT NULL, 
	"bk"			INTEGER NOT NULL, 
	"po"			INTEGER NOT NULL, 
	"gs"			BOOLEAN NOT NULL, 
	"gf"			BOOLEAN NOT NULL, 
	"w"			BOOLEAN NOT NULL, 
	"l"			BOOLEAN NOT NULL, 
	"sv"			BOOLEAN NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "rtpitchingstats" ADD CONSTRAINT "rtpitchingstats_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber");

CREATE TABLE IF NOT EXISTS "spray"
 (
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"eventnumber"			SMALLINT NOT NULL, 
	"sequencenumber"			INTEGER NOT NULL, 
	"gametype"			INTEGER NOT NULL, 
	"hometeam"			BOOLEAN NOT NULL, 
	"starter"			BOOLEAN NOT NULL, 
	"type1"			SMALLINT NOT NULL, 
	"x1"			INTEGER NOT NULL, 
	"y1"			INTEGER NOT NULL, 
	"type2"			SMALLINT NOT NULL, 
	"x2"			INTEGER NOT NULL, 
	"y2"			INTEGER NOT NULL, 
	"type3"			SMALLINT NOT NULL, 
	"x3"			INTEGER NOT NULL, 
	"y3"			INTEGER NOT NULL, 
	"type4"			SMALLINT NOT NULL, 
	"x4"			INTEGER NOT NULL, 
	"y4"			INTEGER NOT NULL, 
	"type5"			SMALLINT NOT NULL, 
	"x5"			INTEGER NOT NULL, 
	"y5"			INTEGER NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "spray" ADD CONSTRAINT "spray_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "playernumber", "eventnumber", "sequencenumber");

CREATE TABLE IF NOT EXISTS "stringoptions"
 (
	"optionnumber"			INTEGER NOT NULL, 
	"option"			VARCHAR (100) NOT NULL, 
	"optiondescription"			VARCHAR (25) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "stringoptions" ADD CONSTRAINT "stringoptions_pkey" PRIMARY KEY ("optionnumber");

CREATE TABLE IF NOT EXISTS "teamfilters"
 (
	"filternumber"			INTEGER NOT NULL, 
	"teamnumber"			INTEGER NOT NULL
);
COMMENT ON COLUMN "teamfilters"."filternumber" IS 'Filter Number';
COMMENT ON COLUMN "teamfilters"."teamnumber" IS 'Team Number';

-- CREATE INDEXES ...
CREATE INDEX "teamfilters_filternumber_idx" ON "teamfilters" ("filternumber");
ALTER TABLE "teamfilters" ADD CONSTRAINT "teamfilters_pkey" PRIMARY KEY ("filternumber", "teamnumber");
CREATE INDEX "teamfilters_teamnumber_idx" ON "teamfilters" ("teamnumber");

CREATE TABLE IF NOT EXISTS "battingstats"
 (
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"playernumber"			INTEGER NOT NULL, 
	"eventnumber"			SMALLINT NOT NULL, 
	"gametype"			INTEGER NOT NULL, 
	"hometeam"			BOOLEAN NOT NULL, 
	"starter"			BOOLEAN NOT NULL, 
	"fieldingposition"			SMALLINT NOT NULL, 
	"pa"			INTEGER NOT NULL, 
	"r"			INTEGER NOT NULL, 
	"h"			INTEGER NOT NULL, 
	"d"			INTEGER NOT NULL, 
	"t"			INTEGER NOT NULL, 
	"hr"			INTEGER NOT NULL, 
	"oe"			INTEGER NOT NULL, 
	"bb"			INTEGER NOT NULL, 
	"hp"			INTEGER NOT NULL, 
	"co"			INTEGER NOT NULL, 
	"fc"			INTEGER NOT NULL, 
	"so"			INTEGER NOT NULL, 
	"sh"			INTEGER NOT NULL, 
	"sf"			INTEGER NOT NULL, 
	"sb"			INTEGER NOT NULL, 
	"cs"			INTEGER NOT NULL, 
	"dp"			INTEGER NOT NULL, 
	"rbi"			INTEGER NOT NULL, 
	"lob"			INTEGER NOT NULL, 
	"u1"			INTEGER NOT NULL, 
	"u2"			INTEGER NOT NULL, 
	"u3"			INTEGER NOT NULL, 
	"u4"			INTEGER NOT NULL, 
	"u5"			INTEGER NOT NULL, 
	"u6"			INTEGER NOT NULL, 
	"u7"			INTEGER NOT NULL, 
	"u8"			INTEGER NOT NULL, 
	"u9"			INTEGER NOT NULL, 
	"u10"			INTEGER NOT NULL, 
	"notes"			TEXT NOT NULL
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
	"reportidnumber"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (100) NOT NULL, 
	"teamtitle"			VARCHAR (100) NOT NULL, 
	"reportdate"			VARCHAR (25) NOT NULL, 
	"headingplayer"			VARCHAR (50) NOT NULL, 
	"headingteam"			VARCHAR (50) NOT NULL, 
	"headingg"			VARCHAR (3) NOT NULL, 
	"headingpa"			VARCHAR (3) NOT NULL, 
	"headingbf"			VARCHAR (3) NOT NULL, 
	"headingab"			VARCHAR (3) NOT NULL, 
	"headingr"			VARCHAR (3) NOT NULL, 
	"headingh"			VARCHAR (3) NOT NULL, 
	"heading1b"			VARCHAR (3) NOT NULL, 
	"heading2b"			VARCHAR (3) NOT NULL, 
	"heading3b"			VARCHAR (3) NOT NULL, 
	"headinghr"			VARCHAR (3) NOT NULL, 
	"headingtb"			VARCHAR (3) NOT NULL, 
	"headingoe"			VARCHAR (3) NOT NULL, 
	"headingfc"			VARCHAR (3) NOT NULL, 
	"headingbb"			VARCHAR (3) NOT NULL, 
	"headinghp"			VARCHAR (3) NOT NULL, 
	"headinghb"			VARCHAR (3) NOT NULL, 
	"headingco"			VARCHAR (3) NOT NULL, 
	"headingso"			VARCHAR (3) NOT NULL, 
	"headingsh"			VARCHAR (3) NOT NULL, 
	"headingsf"			VARCHAR (3) NOT NULL, 
	"headingdp"			VARCHAR (3) NOT NULL, 
	"headingsb"			VARCHAR (3) NOT NULL, 
	"headingcs"			VARCHAR (3) NOT NULL, 
	"headingrbi"			VARCHAR (3) NOT NULL, 
	"headingchs"			VARCHAR (3) NOT NULL, 
	"headinglhs"			VARCHAR (3) NOT NULL, 
	"headingc"			VARCHAR (3) NOT NULL, 
	"headinga"			VARCHAR (3) NOT NULL, 
	"headinge"			VARCHAR (3) NOT NULL, 
	"headingpb"			VARCHAR (3) NOT NULL, 
	"headingip"			VARCHAR (3) NOT NULL, 
	"headinger"			VARCHAR (3) NOT NULL, 
	"headingwp"			VARCHAR (3) NOT NULL, 
	"headingbk"			VARCHAR (3) NOT NULL, 
	"headingpo"			VARCHAR (3) NOT NULL, 
	"headingpickoff"			VARCHAR (3) NOT NULL, 
	"headingball"			VARCHAR (3) NOT NULL, 
	"headingstrike"			VARCHAR (3) NOT NULL, 
	"headingtp"			VARCHAR (3) NOT NULL, 
	"headinggs"			VARCHAR (3) NOT NULL, 
	"headinggf"			VARCHAR (3) NOT NULL, 
	"headingcg"			VARCHAR (3) NOT NULL, 
	"headingw"			VARCHAR (3) NOT NULL, 
	"headingl"			VARCHAR (3) NOT NULL, 
	"headingsv"			VARCHAR (3) NOT NULL, 
	"headingsho"			VARCHAR (3) NOT NULL, 
	"headingba"			VARCHAR (3) NOT NULL, 
	"headingfa"			VARCHAR (3) NOT NULL, 
	"headingobp"			VARCHAR (3) NOT NULL, 
	"headingslg"			VARCHAR (3) NOT NULL, 
	"headingpp"			VARCHAR (3) NOT NULL, 
	"headingrc"			VARCHAR (3) NOT NULL, 
	"headingta"			VARCHAR (3) NOT NULL, 
	"headingsba"			VARCHAR (3) NOT NULL, 
	"headingcsa"			VARCHAR (3) NOT NULL, 
	"headingrng"			VARCHAR (3) NOT NULL, 
	"headingera"			VARCHAR (3) NOT NULL, 
	"headingsog"			VARCHAR (3) NOT NULL, 
	"headingwhip"			VARCHAR (4) NOT NULL, 
	"headingspct"			VARCHAR (4) NOT NULL, 
	"headinguser1"			VARCHAR (3) NOT NULL, 
	"headinguser2"			VARCHAR (3) NOT NULL, 
	"headinguser3"			VARCHAR (3) NOT NULL, 
	"headinguser4"			VARCHAR (3) NOT NULL, 
	"headinguser5"			VARCHAR (3) NOT NULL, 
	"headingusers1"			VARCHAR (3) NOT NULL, 
	"headingusers2"			VARCHAR (3) NOT NULL, 
	"headingusers3"			VARCHAR (3) NOT NULL, 
	"headingusers4"			VARCHAR (3) NOT NULL, 
	"headingusers5"			VARCHAR (3) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crbpfstats" ADD CONSTRAINT "crbpfstats_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crlineup"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (100) NOT NULL, 
	"teamtitle"			VARCHAR (100) NOT NULL, 
	"reportdate"			VARCHAR (25) NOT NULL, 
	"headinginn1"			VARCHAR (3) NOT NULL, 
	"headinginn2"			VARCHAR (3) NOT NULL, 
	"headinginn3"			VARCHAR (3) NOT NULL, 
	"headinginn4"			VARCHAR (3) NOT NULL, 
	"headinginn5"			VARCHAR (3) NOT NULL, 
	"headinginn6"			VARCHAR (3) NOT NULL, 
	"headinginn7"			VARCHAR (3) NOT NULL, 
	"headinginn8"			VARCHAR (3) NOT NULL, 
	"headinginn9"			VARCHAR (3) NOT NULL, 
	"lineupnotes"			TEXT NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crlineup" ADD CONSTRAINT "crlineup_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "crrecorddetail"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"detaillinenumber"			INTEGER NOT NULL, 
	"gametype"			VARCHAR (50) NOT NULL, 
	"gameswon"			VARCHAR (10) NOT NULL, 
	"gameslost"			VARCHAR (10) NOT NULL, 
	"gamestied"			VARCHAR (10) NOT NULL, 
	"runsfor"			VARCHAR (10) NOT NULL, 
	"runsagainst"			VARCHAR (10) NOT NULL, 
	"winpct"			VARCHAR (10) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crrecorddetail" ADD CONSTRAINT "crrecorddetail_pkey" PRIMARY KEY ("reportidnumber", "detaillinenumber");

CREATE TABLE IF NOT EXISTS "crstandings"
 (
	"reportidnumber"			INTEGER NOT NULL, 
	"reporttitle"			VARCHAR (100) NOT NULL, 
	"reportsubtitle"			VARCHAR (100) NOT NULL, 
	"reportdate"			VARCHAR (25) NOT NULL, 
	"headingties"			VARCHAR (10) NOT NULL, 
	"headingstreak"			VARCHAR (10) NOT NULL, 
	"headingrf"			VARCHAR (20) NOT NULL, 
	"headingra"			VARCHAR (20) NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "crstandings" ADD CONSTRAINT "crstandings_pkey" PRIMARY KEY ("reportidnumber");

CREATE TABLE IF NOT EXISTS "filters"
 (
	"filternumber"			INTEGER NOT NULL, 
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
	"teamnumber"			INTEGER NOT NULL, 
	"lineupnumber"			INTEGER NOT NULL, 
	"description"			VARCHAR (50) NOT NULL, 
	"innings"			INTEGER NOT NULL, 
	"lineupnotes"			TEXT NOT NULL
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
	"reportnumber"			INTEGER NOT NULL, 
	"reportorder"			SMALLINT NOT NULL, 
	"categorynumber"			SMALLINT NOT NULL
);
COMMENT ON COLUMN "pitchingrptcats"."reportnumber" IS 'Report Number';
COMMENT ON COLUMN "pitchingrptcats"."reportorder" IS 'Report Order';
COMMENT ON COLUMN "pitchingrptcats"."categorynumber" IS 'Category Number';

-- CREATE INDEXES ...
ALTER TABLE "pitchingrptcats" ADD CONSTRAINT "pitchingrptcats_pkey" PRIMARY KEY ("reportnumber", "reportorder");

CREATE TABLE IF NOT EXISTS "roster"
 (
	"teamnumber"			INTEGER NOT NULL, 
	"personnumber"			INTEGER NOT NULL, 
	"playerindicator"			BOOLEAN NOT NULL, 
	"uniformnumber"			VARCHAR (3) NOT NULL, 
	"notes"			TEXT NOT NULL
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
	"sortkey"			INTEGER NOT NULL, 
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
	"teamnumber"			INTEGER NOT NULL, 
	"gamenumber"			INTEGER NOT NULL, 
	"inning"			SMALLINT NOT NULL, 
	"runsinning"			INTEGER NOT NULL, 
	"opprunsinning"			INTEGER NOT NULL
);

-- CREATE INDEXES ...
ALTER TABLE "rtgamestatsxinnings" ADD CONSTRAINT "rtgamestatsxinnings_pkey" PRIMARY KEY ("teamnumber", "gamenumber", "inning");

CREATE TABLE IF NOT EXISTS "teams"
 (
	"teamnumber"			INTEGER NOT NULL, 
	"longteamname"			VARCHAR (50) NOT NULL, 
	"shortteamname"			VARCHAR (20) NOT NULL, 
	"contactperson"			VARCHAR (50) NOT NULL, 
	"phonenumber"			VARCHAR (30) NOT NULL, 
	"email"			VARCHAR (70) NOT NULL, 
	"notes"			TEXT NOT NULL
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


-- CREATE Relationships ...
ALTER TABLE "BattingRptCats" ADD CONSTRAINT "battingrptcats_reportnumber_fk" FOREIGN KEY ("reportnumber") REFERENCES "BattingRptFormat"("reportnumber") ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "CRBoxScoresDetail" ADD CONSTRAINT "crboxscoresdetail_reportidnumber_fk" FOREIGN KEY ("reportidnumber") REFERENCES "CRBoxScores"("reportidnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "CRBPFStatsDetail" ADD CONSTRAINT "crbpfstatsdetail_reportidnumber_fk" FOREIGN KEY ("reportidnumber") REFERENCES "CRBPFStats"("reportidnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "CRGameScoresDetail" ADD CONSTRAINT "crgamescoresdetail_reportidnumber_fk" FOREIGN KEY ("reportidnumber") REFERENCES "CRGameScores"("reportidnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "CRLineupDetail" ADD CONSTRAINT "crlineupdetail_reportidnumber_fk" FOREIGN KEY ("reportidnumber") REFERENCES "CRLineup"("reportidnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "CRRecordDetail" ADD CONSTRAINT "crrecorddetail_reportidnumber_fk" FOREIGN KEY ("reportidnumber") REFERENCES "CRRecord"("reportidnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "CRRosterDetail" ADD CONSTRAINT "crrosterdetail_reportidnumber_fk" FOREIGN KEY ("reportidnumber") REFERENCES "CRRoster"("reportidnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "CRScoreByInningsDetail" ADD CONSTRAINT "crscorebyinningsdetail_reportidnumber_fk" FOREIGN KEY ("reportidnumber") REFERENCES "CRScoreByInnings"("reportidnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "CRStandingsDetail" ADD CONSTRAINT "crstandingsdetail_reportidnumber_fk" FOREIGN KEY ("reportidnumber") REFERENCES "CRStandings"("reportidnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "FieldingRptCats" ADD CONSTRAINT "fieldingrptcats_reportnumber_fk" FOREIGN KEY ("reportnumber") REFERENCES "FieldingRptFormat"("reportnumber") ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "TeamFilters" ADD CONSTRAINT "teamfilters_filternumber_fk" FOREIGN KEY ("filternumber") REFERENCES "Filters"("filternumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "BattingStats" ADD CONSTRAINT "battingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "GameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "BattingStats" ADD CONSTRAINT "battingstats_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "GameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "FieldingStats" ADD CONSTRAINT "fieldingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "GameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "FieldingStats" ADD CONSTRAINT "fieldingstats_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "GameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "GameLineup" ADD CONSTRAINT "gamelineup_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "GameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "GameLineup" ADD CONSTRAINT "gamelineup_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "GameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "PitchingStats" ADD CONSTRAINT "pitchingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "GameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "PitchingStats" ADD CONSTRAINT "pitchingstats_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "GameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTGameStats" ADD CONSTRAINT "rtgamestats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "GameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTGameStats" ADD CONSTRAINT "rtgamestats_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "GameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "Spray" ADD CONSTRAINT "spray_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "GameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "Spray" ADD CONSTRAINT "spray_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "GameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "LineupPlayer" ADD CONSTRAINT "lineupplayer_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Lineup"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "LineupPlayer" ADD CONSTRAINT "lineupplayer_lineupnumber_fk" FOREIGN KEY ("lineupnumber") REFERENCES "Lineup"("lineupnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "BattingStats" ADD CONSTRAINT "battingstats_playernumber_fk" FOREIGN KEY ("playernumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "FieldingStats" ADD CONSTRAINT "fieldingstats_playernumber_fk" FOREIGN KEY ("playernumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "GameLineup" ADD CONSTRAINT "gamelineup_playernumber_fk" FOREIGN KEY ("playernumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "PitchingStats" ADD CONSTRAINT "pitchingstats_playernumber_fk" FOREIGN KEY ("playernumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "Roster" ADD CONSTRAINT "roster_personnumber_fk" FOREIGN KEY ("personnumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTBattingStats" ADD CONSTRAINT "rtbattingstats_playernumber_fk" FOREIGN KEY ("playernumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTFieldingStats" ADD CONSTRAINT "rtfieldingstats_playernumber_fk" FOREIGN KEY ("playernumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTPitchingStats" ADD CONSTRAINT "rtpitchingstats_playernumber_fk" FOREIGN KEY ("playernumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "Spray" ADD CONSTRAINT "spray_playernumber_fk" FOREIGN KEY ("playernumber") REFERENCES "People"("personnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "PitchingRptCats" ADD CONSTRAINT "pitchingrptcats_reportnumber_fk" FOREIGN KEY ("reportnumber") REFERENCES "PitchingRptFormat"("reportnumber") ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTBattingStats" ADD CONSTRAINT "rtbattingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "RTGameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTBattingStats" ADD CONSTRAINT "rtbattingstats_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "RTGameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTFieldingStats" ADD CONSTRAINT "rtfieldingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "RTGameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTFieldingStats" ADD CONSTRAINT "rtfieldingstats_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "RTGameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTGameStatsXInnings" ADD CONSTRAINT "rtgamestatsxinnings_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "RTGameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTGameStatsXInnings" ADD CONSTRAINT "rtgamestatsxinnings_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "RTGameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTPitchingStats" ADD CONSTRAINT "rtpitchingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "RTGameStats"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "RTPitchingStats" ADD CONSTRAINT "rtpitchingstats_gamenumber_fk" FOREIGN KEY ("gamenumber") REFERENCES "RTGameStats"("gamenumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "BattingStats" ADD CONSTRAINT "battingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Teams"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "FieldingStats" ADD CONSTRAINT "fieldingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Teams"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "GameLineup" ADD CONSTRAINT "gamelineup_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Teams"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "GameStats" ADD CONSTRAINT "gamestats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Teams"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "Lineup" ADD CONSTRAINT "lineup_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Teams"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "PitchingStats" ADD CONSTRAINT "pitchingstats_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Teams"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "Spray" ADD CONSTRAINT "spray_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Teams"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "Roster" ADD CONSTRAINT "roster_teamnumber_fk" FOREIGN KEY ("teamnumber") REFERENCES "Teams"("teamnumber") ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
