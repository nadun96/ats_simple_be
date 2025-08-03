#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create databases for each service
    CREATE DATABASE auth_db;
    CREATE DATABASE ats_db;
    CREATE DATABASE email_db;
    CREATE DATABASE notification_db;
    
    -- Grant all privileges to the user for all databases
    GRANT ALL PRIVILEGES ON DATABASE auth_db TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE ats_db TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE email_db TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE notification_db TO $POSTGRES_USER;
    
    -- Connect to each database and grant schema privileges
    \c auth_db;
    GRANT ALL ON SCHEMA public TO $POSTGRES_USER;
    
    \c ats_db;
    GRANT ALL ON SCHEMA public TO $POSTGRES_USER;
    
    \c email_db;
    GRANT ALL ON SCHEMA public TO $POSTGRES_USER;
    
    \c notification_db;
    GRANT ALL ON SCHEMA public TO $POSTGRES_USER;
EOSQL

echo "All databases created successfully!"
