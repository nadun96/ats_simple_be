# Scripts Directory

This directory contains utility scripts for database setup, management, and troubleshooting.

## 🔧 Setup Scripts

### `setup-databases.sh` (Linux/Mac)
**Purpose**: One-click setup for the entire system  
**Usage**: 
```bash
chmod +x setup-databases.sh
./setup-databases.sh
```

### `setup-databases.bat` (Windows)
**Purpose**: One-click setup for Windows systems  
**Usage**: 
```cmd
setup-databases.bat
```

**What these scripts do**:
- Check for `.env` file, create if missing
- Make scripts executable (Linux/Mac)
- Stop any existing containers
- Start all services with `docker-compose up --build`
- Display service URLs and connection info

## 🗄️ Database Scripts

### `init-db.sh`
**Purpose**: Initialize PostgreSQL databases for all services  
**Usage**: Automatically called by Docker Compose during PostgreSQL startup  
**Creates**:
- `auth_db` - Authentication service database
- `ats_db` - Application service database  
- `email_db` - Email service database
- `notification_db` - Notification service database

### `wait-for-db.sh`
**Purpose**: Ensure database readiness before service startup  
**Usage**: Called by each service before running migrations  
**Parameters**: `host port user password database`

Example:
```bash
./wait-for-db.sh postgres 5432 ats_user ats_password auth_db
```

## 🔍 Utility Scripts

### `check-databases.sh`
**Purpose**: Verify database connectivity and status  
**Usage**:
```bash
chmod +x check-databases.sh
./check-databases.sh
```

**Checks**:
- PostgreSQL container status
- Database connectivity for each service
- Table counts and migration status
- Service container status

### `reset-databases.sh`
**Purpose**: Reset all databases and volumes (⚠️ DESTRUCTIVE)  
**Usage**:
```bash
chmod +x reset-databases.sh
./reset-databases.sh
```

**Actions**:
- Stops all services
- Removes all data volumes
- Rebuilds and restarts services
- **WARNING**: This destroys all data!

## 📁 Script Locations in Docker

When services run, scripts are mounted to:
- `init-db.sh` → `/docker-entrypoint-initdb.d/init-db.sh` (PostgreSQL)
- `wait-for-db.sh` → `/app/wait-for-db.sh` (All services)

## 🔒 Permissions

Linux/Mac users need to make scripts executable:
```bash
chmod +x scripts/*.sh
```

Or individually:
```bash
chmod +x scripts/setup-databases.sh
chmod +x scripts/check-databases.sh
chmod +x scripts/reset-databases.sh
```

## 🚨 Important Notes

1. **Always run setup scripts from the project root directory**
2. **Scripts automatically navigate to parent directory if needed**  
3. **Windows users should use `.bat` files, Linux/Mac use `.sh` files**
4. **Reset script is destructive - use with caution**
5. **Check scripts help diagnose issues without making changes**

## 🔗 Related Documentation

- [Database Setup Guide](../docs/DATABASE_SETUP.md)
- [Setup Summary](../docs/SETUP_SUMMARY.md)
- [Troubleshooting](../docs/TROUBLESHOOTING.md)
