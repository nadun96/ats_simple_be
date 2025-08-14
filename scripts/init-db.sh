#!/bin/bash
set -e

echo "Creating databases for ATS services..."

# Create databases for each service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE auth_db;
    CREATE DATABASE ats_db;
    CREATE DATABASE email_db;
    CREATE DATABASE notification_db;
EOSQL

echo "Granting privileges to user $POSTGRES_USER..."

# Grant privileges for each database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "auth_db" <<-EOSQL
    GRANT ALL ON SCHEMA public TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $POSTGRES_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "ats_db" <<-EOSQL
    GRANT ALL ON SCHEMA public TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $POSTGRES_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "email_db" <<-EOSQL
    GRANT ALL ON SCHEMA public TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $POSTGRES_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "notification_db" <<-EOSQL
    GRANT ALL ON SCHEMA public TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $POSTGRES_USER;
EOSQL

echo "All databases created and privileges granted successfully!"
