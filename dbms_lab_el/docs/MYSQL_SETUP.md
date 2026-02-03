# MySQL Setup Instructions

## Prerequisites
- MySQL 5.7+ installed and running
- MySQL command-line client or MySQL Workbench

## Step 1: Create Database and User

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE ptsd_simulation_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (replace 'username' and 'password' with your choices)
CREATE USER 'ptsd_user'@'localhost' IDENTIFIED BY 'ptsd_password_123';

-- Grant all privileges
GRANT ALL PRIVILEGES ON ptsd_simulation_db.* TO 'ptsd_user'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

-- Verify (should show your new database)
SHOW DATABASES;

-- Exit
EXIT;
```

## Step 2: Set Environment Variables

### On Windows (PowerShell):
```powershell
$env:MYSQL_USER = "ptsd_user"
$env:MYSQL_PASSWORD = "ptsd_password_123"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_PORT = "3306"
$env:MYSQL_DATABASE = "ptsd_simulation_db"
```

### On Windows (Command Prompt):
```cmd
set MYSQL_USER=ptsd_user
set MYSQL_PASSWORD=ptsd_password_123
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
set MYSQL_DATABASE=ptsd_simulation_db
```

### On Linux/Mac (Bash):
```bash
export MYSQL_USER="ptsd_user"
export MYSQL_PASSWORD="ptsd_password_123"
export MYSQL_HOST="localhost"
export MYSQL_PORT="3306"
export MYSQL_DATABASE="ptsd_simulation_db"
```

## Step 3: Create Tables and Seed Data

### Option A: Using the Python seed script (Recommended)
```powershell
# Activate virtual environment
& ./.venv/Scripts/Activate.ps1

# Install/upgrade dependencies
pip install -r requirements.txt

# Run seed script to create tables and populate data
python backend/seed.py
```

### Option B: Manual SQL
```sql
-- Connect to the new database
mysql -u ptsd_user -p ptsd_simulation_db

-- Tables will be created automatically by SQLAlchemy when you run the app
-- Just seed the initial data using the Python script
```

## Step 4: Start the Application

```powershell
# With environment variables set
uvicorn backend.main:app --reload

# OR set them inline:
$env:MYSQL_USER="ptsd_user"; $env:MYSQL_PASSWORD="ptsd_password_123"; $env:MYSQL_HOST="localhost"; $env:MYSQL_PORT="3306"; $env:MYSQL_DATABASE="ptsd_simulation_db"; uvicorn backend.main:app --reload
```

## Step 5: Verify Connection

Visit: http://localhost:8000/docs

Test the `/simulations/stats` endpoint to verify the database connection is working.

## Troubleshooting

### "Access denied for user"
- Verify MYSQL_USER and MYSQL_PASSWORD are correct
- Check MySQL user exists: `mysql -u root -p -e "SELECT User, Host FROM mysql.user;"`

### "Unknown database"
- Verify database was created: `mysql -u root -p -e "SHOW DATABASES;"`
- Run Step 1 again if needed

### "pymysql module not found"
```powershell
pip install pymysql
```

### Connection timeout
- Check MySQL is running: `mysql -u root -p -e "SELECT 1;"`
- Verify MYSQL_HOST and MYSQL_PORT are correct

## Reset Database (If Needed)

```sql
-- Connect as root
mysql -u root -p

-- Drop and recreate database
DROP DATABASE ptsd_simulation_db;
CREATE DATABASE ptsd_simulation_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant privileges again
GRANT ALL PRIVILEGES ON ptsd_simulation_db.* TO 'ptsd_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit and run seed.py again
EXIT;
```

## Default Credentials (for testing)
- **User**: ptsd_user
- **Password**: ptsd_password_123
- **Host**: localhost
- **Port**: 3306
- **Database**: ptsd_simulation_db

**Change these in production!**
