#!/bin/bash
# wait-for-db.sh - Wait for database to be ready and check if specific database exists

set -e

host="$1"
port="$2"
user="$3"
password="$4"
database="$5"

until PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - checking if database $database exists"

# Check if the specific database exists, if not create it
PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "postgres" -tc "SELECT 1 FROM pg_database WHERE datname = '$database'" | grep -q 1 || {
    >&2 echo "Database $database does not exist, creating it..."
    PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "postgres" -c "CREATE DATABASE $database;"
    PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "$database" -c "GRANT ALL ON SCHEMA public TO $user;"
}

>&2 echo "Database $database is ready"
