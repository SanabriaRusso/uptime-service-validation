DROP SCHEMA uptime_reports CASCADE;
CREATE SCHEMA [IF NOT EXISTS] uptime_reports;

DROP TABLE IF EXISTS uptime_reports.register;
CREATE TABLE uptime_reports.register (
	Start_Date TIMESTAMP PRIMARY KEY,
	End_Date TIMESTAMP NOT NULL,
	Done BOOLEAN NOT NULL
);
