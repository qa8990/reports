DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS company_types;
DROP TABLE IF EXISTS datetime_text;
DROP TABLE IF EXISTS report_forms;
DROP TABLE IF EXISTS report_periodicity;
DROP TABLE IF EXISTS report_types;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

CREATE TABLE companies (
	company_id	INTEGER,
	name	TEXT,
	description	TEXT,
	code	INTEGER UNIQUE,
	company_type_id	INTEGER,
	created_at	TEXT,
	status_id	INTEGER,
	FOREIGN KEY(status_id) REFERENCES status(id),
	FOREIGN KEY(company_type_id) REFERENCES company_types(company_type_id),
	PRIMARY KEY(company_id)
);

CREATE TABLE company_types (
	company_type_id	INTEGER,
	code	INTEGER UNIQUE,
	description	TEXT,
	status_id	INTEGER,
	FOREIGN KEY(status_id) REFERENCES status(id),
	PRIMARY KEY(company_type_id)
);

CREATE TABLE datetime_text(
   d1 text, 
   d2 text
);

CREATE TABLE report_forms (
	form_code	TEXT UNIQUE,
	form_name	TEXT,
	form_description	TEXT,
	status_id	INTEGER,
	FOREIGN KEY(status_id) REFERENCES status(id),
	PRIMARY KEY(form_code)
);

CREATE TABLE report_periodicity (
	code	TEXT UNIQUE,
	description	TEXT,
	status_id	INTEGER,
	PRIMARY KEY(code),
	FOREIGN KEY(status_id) REFERENCES status(id)
);

CREATE TABLE report_types (
	report_type_id	INTEGER,
	report_name	TEXT,
	report_description	TEXT,
	report_code	INTEGER UNIQUE,
	status_id	INTEGER,
	FOREIGN KEY(status_id) REFERENCES status(id),
	PRIMARY KEY(report_type_id)
);

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE status (
	id	INTEGER,
	code	TEXT UNIQUE,
	description	INTEGER,
	PRIMARY KEY(id)
);

CREATE TABLE users (
	id	INTEGER,
	username	TEXT NOT NULL UNIQUE,
	password	TEXT NOT NULL,
	status_id	INTEGER,
	PRIMARY KEY(id AUTOINCREMENT),
	FOREIGN KEY(status_id) REFERENCES status(id)
);
