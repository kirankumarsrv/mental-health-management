# SQLite to MySQL Migration - Complete Guide

## Migration Summary
✅ Migrated from SQLite (`ptsd_simulation.db`) to MySQL

### Changes Made:
1. ✅ Updated `requirements.txt` - Added `pymysql` and `python-dotenv`
2. ✅ Updated `database.py` - Changed connection string to MySQL with environment variables
3. ✅ Created `.env.example` - Configuration template
4. ✅ Created `MYSQL_SETUP.md` - Detailed setup instructions

---

## Quick Start (5 Minutes)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Create MySQL Database
```sql
-- Open MySQL command line or MySQL Workbench and run:
CREATE DATABASE ptsd_simulation_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ptsd_user'@'localhost' IDENTIFIED BY 'ptsd_password_123';
GRANT ALL PRIVILEGES ON ptsd_simulation_db.* TO 'ptsd_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 3: Set Environment Variables (PowerShell)
```powershell
$env:MYSQL_USER = "ptsd_user"
$env:MYSQL_PASSWORD = "ptsd_password_123"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_PORT = "3306"
$env:MYSQL_DATABASE = "ptsd_simulation_db"
```

### Step 4: Seed Database
```powershell
python backend/seed.py
```
Output should show: `Seeding data...`

### Step 5: Start Server
```powershell
uvicorn backend.main:app --reload
```

Visit: http://localhost:8000/docs

---

## Alternative: Using .env File

### Step 1: Create .env file
```bash
cp .env.example .env
```

### Step 2: Edit .env with your MySQL credentials
```
MYSQL_USER=ptsd_user
MYSQL_PASSWORD=ptsd_password_123
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=ptsd_simulation_db
```

### Step 3: Run application
```powershell
uvicorn backend.main:app --reload
```

**Note**: The `.env` file is automatically loaded by `python-dotenv`

---

## Verifying the Connection

### Test 1: Check Tables Created
```sql
mysql -u ptsd_user -p ptsd_simulation_db -e "SHOW TABLES;"
```

Expected output:
```
+---------------------------+
| Tables_in_ptsd_simulation_db |
+---------------------------+
| person                    |
| therapist                 |
| scenario                  |
| reaction                  |
| report                    |
| participates              |
| assigns                   |
| exhibits                  |
| triggers                  |
+---------------------------+
```

### Test 2: Check Sample Data
```sql
mysql -u ptsd_user -p ptsd_simulation_db -e "SELECT COUNT(*) FROM therapist; SELECT COUNT(*) FROM person;"
```

Expected:
```
count(*)
1

count(*)
3
```

### Test 3: API Test
```powershell
# While server is running, open new PowerShell window
Invoke-WebRequest -Uri "http://localhost:8000/simulations/stats"
```

Should return JSON stats.

---

## Troubleshooting

### Error: "Access denied for user 'ptsd_user'@'localhost'"

**Solution**: Verify MySQL user exists
```sql
mysql -u root -p -e "SELECT User, Host FROM mysql.user WHERE User='ptsd_user';"
```

If empty, recreate user:
```sql
CREATE USER 'ptsd_user'@'localhost' IDENTIFIED BY 'ptsd_password_123';
GRANT ALL PRIVILEGES ON ptsd_simulation_db.* TO 'ptsd_user'@'localhost';
FLUSH PRIVILEGES;
```

### Error: "Unknown database 'ptsd_simulation_db'"

**Solution**: Create database
```sql
mysql -u root -p -e "CREATE DATABASE ptsd_simulation_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Error: "No module named 'pymysql'"

**Solution**: Install MySQL driver
```powershell
pip install pymysql
```

### Error: "Connection refused" or "Can't connect to MySQL server"

**Solution**: Ensure MySQL is running
```powershell
# Windows - check if MySQL service is running
Get-Service | grep MySQL

# Or start MySQL if using XAMPP/WAMP/etc
# Or verify connection
mysql -u root -p -e "SELECT 1;"
```

### Error: "Environment variable not found"

**Solution**: Set environment variables before running the app
```powershell
# Option 1: Set in PowerShell session
$env:MYSQL_USER="ptsd_user"
# ... set other variables

# Option 2: Create .env file in project root
# Copy .env.example to .env and edit with your values
```

---

## Migration from SQLite (If You Have Old Data)

### Export SQLite Data
```powershell
# If you still have the old SQLite database
sqlite3 ptsd_simulation.db ".dump" > backup.sql
```

### Import to MySQL (Advanced)
Contact the development team for data migration scripts if needed. SQLite and MySQL have different syntaxes, so direct import requires conversion.

**Recommended**: Start fresh with `python backend/seed.py` to populate with clean data.

---

## Files Changed

```
ptsd_simulation_app/
├── requirements.txt          # ✅ Added pymysql, python-dotenv
├── .env.example             # ✅ NEW - Configuration template
├── MYSQL_SETUP.md           # ✅ NEW - Detailed setup guide
├── backend/
│   └── database.py          # ✅ Updated - MySQL connection + dotenv support
│   └── seed.py              # ✅ No changes needed (SQLAlchemy handles it)
│   └── main.py              # ✅ No changes needed
│   └── models.py            # ✅ No changes needed
│   └── presets.py           # ✅ No changes needed
│   └── routers/
│       └── simulation.py     # ✅ No changes needed
│       └── person.py        # ✅ No changes needed
│       └── scenario.py      # ✅ No changes needed
│       └── therapist.py     # ✅ No changes needed
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_USER` | root | MySQL username |
| `MYSQL_PASSWORD` | (empty) | MySQL password |
| `MYSQL_HOST` | localhost | MySQL server host |
| `MYSQL_PORT` | 3306 | MySQL server port |
| `MYSQL_DATABASE` | ptsd_simulation_db | Database name |

---

## Production Deployment

### Important Security Notes:

1. **Change default credentials**:
   ```sql
   ALTER USER 'ptsd_user'@'localhost' IDENTIFIED BY 'YOUR_STRONG_PASSWORD';
   ```

2. **Use `.env` file** (never commit passwords to git):
   ```
   # Add to .gitignore
   .env
   ```

3. **Restrict user privileges** (production):
   ```sql
   -- Remove dangerous privileges
   REVOKE ALL PRIVILEGES ON ptsd_simulation_db.* FROM 'ptsd_user'@'localhost';
   GRANT SELECT, INSERT, UPDATE, DELETE ON ptsd_simulation_db.* TO 'ptsd_user'@'localhost';
   ```

4. **Enable SSL connections** (if remote database):
   ```python
   # In database.py
   SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?ssl_ca=/path/to/ca.pem"
   ```

5. **Backup database regularly**:
   ```bash
   mysqldump -u ptsd_user -p ptsd_simulation_db > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

---

## Rollback to SQLite (If Needed)

If you need to go back to SQLite:

1. Update `database.py`:
```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./ptsd_simulation.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
```

2. Remove `pymysql` from requirements.txt

3. Run: `pip install -r requirements.txt`

4. Run: `python backend/seed.py`

---

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Create MySQL database and user (see MYSQL_SETUP.md)
3. ✅ Set environment variables
4. ✅ Seed database: `python backend/seed.py`
5. ✅ Start server: `uvicorn backend.main:app --reload`
6. ✅ Test API: http://localhost:8000/docs

**You're done!** The application is now using MySQL instead of SQLite.
