PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- CREATE TABLE alembic_version (
--         version_num VARCHAR(32) NOT NULL, 
--         CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
-- );
-- INSERT INTO alembic_version VALUES('1584d836f365');

CREATE TABLE citizen (
        citizen_id VARCHAR(12) NOT NULL, 
        name VARCHAR(64), 
        password_hash VARCHAR(128), permission VARCHAR(20), score FLOAT, 
        PRIMARY KEY (citizen_id)
);
-- CREATE INDEX ix_citizen_name ON citizen (name);
-- CREATE INDEX ix_citizen_permission ON citizen (permission);

CREATE TABLE report (
        reporter_id VARCHAR(12), 
        reported_id VARCHAR(12), 
        report_id INTEGER NOT NULL, 
        time DATETIME, 
        report_category VARCHAR(64), 
        body VARCHAR(140), 
        PRIMARY KEY (report_id), 
        FOREIGN KEY(reported_id) REFERENCES citizen (citizen_id), 
        FOREIGN KEY(reporter_id) REFERENCES citizen (citizen_id)
);
-- CREATE INDEX ix_report_time ON report (time);

CREATE TABLE status (
        citizen_id VARCHAR(12), 
        status_id INTEGER NOT NULL, 
        timestamp DATETIME, 
        status_category VARCHAR(64), 
        body VARCHAR(140), 
        PRIMARY KEY (status_id), 
        FOREIGN KEY(citizen_id) REFERENCES citizen (citizen_id)
);
-- CREATE INDEX ix_status_timestamp ON status (timestamp);

COMMIT;