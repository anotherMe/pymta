BEGIN TRANSACTION;

CREATE TABLE "DAT_symbol" (

	`code`	TEXT NOT NULL,
	`descr`	TEXT NOT NULL,
	PRIMARY KEY(code)
);

-- link index --> symbol
CREATE TABLE "DAT_index_symbol" (

	`index`	TEXT NOT NULL,
	`symbol`	TEXT NOT NULL
);

-- table for Yahoo indexes ( like FTSEMIB.MI )
CREATE TABLE "DAT_index" (

	`code`	TEXT NOT NULL,
	`descr`	TEXT,
	PRIMARY KEY(code)
);

CREATE TABLE "DAT_EoD" (

	`symbol`	TEXT NOT NULL,
	`date`	INTEGER,
	`date_STR`	TEXT NOT NULL,
	`open`	REAL,
	`high`	REAL,
	`low`	REAL,
	`close`	REAL,
	`volume`	INTEGER,
	`adj_close`	REAL,
	UNIQUE(`symbol`, `date`)
);

COMMIT;
