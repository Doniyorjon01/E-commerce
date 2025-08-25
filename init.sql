CREATE DATABASE reports_db;
CREATE DATABASE analytics_db;

CREATE USER report_user WITH PASSWORD 'reportpass';
GRANT ALL PRIVILEGES ON DATABASE reports_db TO report_user;
