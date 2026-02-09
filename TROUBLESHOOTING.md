# 🔧 Troubleshooting Guide

## 🚨 Common Errors and Solutions

### 1. Migration Errors

#### Error: "Could not locate a Flask application"

**Cause:** Flask can't find your app

**Solution:**
```bash
# Make sure FLASK_APP is set
export FLASK_APP=app.py  # Mac/Linux
set FLASK_APP=app.py     # Windows CMD
$env:FLASK_APP="app.py"  # Windows PowerShell

# Or add to .env file
echo "FLASK_APP=app.py" >> .env
```

#### Error: "Can't locate revision identified by 'xxxxx'"

**Cause:** Migration files not in git or out of sync

**Solution:**
```bash
# Ensure migrations folder is committed
git add migrations/
git commit -m "Add migrations"
git push

# If still broken, recreate migrations
rm -rf migrations/
flask db init
flask db migrate -m "Recreate migrations"
flask db upgrade
```

#### Error: "Target database is not up to date"

**Cause:** Database has migrations that code doesn't know about

**Solution:**
```bash
# Check migration history
flask db history

# Downgrade to a known state
flask db downgrade

# Or start fresh (WARNING: deletes data)
flask db downgrade base
flask db upgrade
```

---

### 2. Database Connection Errors

#### Error: "connection to server at localhost port 5432 failed" (Render/Railway)

**Cause:** `DATABASE_URL` environment variable is not set on your deployment platform

**Solution:**

**On Render:**
1. Go to your web service dashboard
2. Click "Environment" tab
3. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: Copy the "Internal Database URL" from your PostgreSQL database service
4. Click "Save Changes" and redeploy

**On Railway:**
1. Railway automatically sets `DATABASE_URL` when you add PostgreSQL
2. Make sure the database service is linked to your web service
3. Check the "Variables" tab to confirm `DATABASE_URL` exists
4. If missing, reconnect the database to your service

**Verify the fix:**
- After adding `DATABASE_URL`, check deploy logs
- You should see "✅ DATABASE_URL is configured"
- If you still see localhost error, the variable isn't set correctly

**Prevention:**
- The updated `render.yaml` now automatically connects the database
- The `start.sh` script validates `DATABASE_URL` before running migrations

---

#### Error: "could not connect to server: Connection refused" (Local Development)

**Cause:** PostgreSQL is not running

**Solution:**
```bash
# Check if PostgreSQL is running
# Mac:
brew services list
brew services start postgresql

# Linux:
sudo systemctl status postgresql
sudo systemctl start postgresql

# Windows:
# Check Services app for PostgreSQL service

# Docker:
docker-compose up db
```

#### Error: "FATAL: password authentication failed"

**Cause:** Wrong database credentials

**Solution:**
```bash
# Check your .env file
DB_USER=postgres
DB_PASSWORD=your_actual_password
DB_NAME=todoapp
DB_HOST=localhost
DB_PORT=5432

# Test connection manually
psql -U postgres -d todoapp -h localhost
```

#### Error: "FATAL: database 'todoapp' does not exist"

**Cause:** Database not created

**Solution:**
```bash
# Create database manually
psql -U postgres
CREATE DATABASE todoapp;
\q

# Or use createdb command
createdb -U postgres todoapp
```

---

### 3. Railway Deployment Errors

#### Error: "Build failed" on Railway

**Cause:** Various build issues

**Solution:**
```bash
# 1. Check Railway logs for specific error
# 2. Common fixes:

# Ensure Dockerfile is correct
# Ensure requirements.txt has all dependencies
# Ensure start.sh is executable (Dockerfile handles this)

# Test build locally
docker build -t test-app .
docker run -p 5000:5000 test-app
```

#### Error: "Application failed to respond"

**Cause:** App not binding to correct port

**Solution:**
```python
# In app.py, ensure:
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Railway sets PORT
    app.run(host='0.0.0.0', port=port)

# In start.sh, ensure:
gunicorn --bind 0.0.0.0:$PORT app:app
```

#### Error: "No DATABASE_URL found"

**Cause:** PostgreSQL not added to Railway project

**Solution:**
1. Go to Railway project
2. Click "+ New"
3. Select "Database" → "PostgreSQL"
4. Railway auto-creates DATABASE_URL
5. Redeploy your app

#### Error: "postgres:// dialect not found"

**Cause:** Railway uses `postgres://` but SQLAlchemy needs `postgresql://`

**Solution:**
Already handled in `app.py`:
```python
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
```

---

### 4. Seeding Errors

#### Error: "Duplicate key value violates unique constraint"

**Cause:** Trying to seed data that already exists

**Solution:**
Our `seed_db.py` already handles this:
```python
# Check before seeding
if Todo.query.count() > 0:
    print("Data exists, skipping")
    return
```

If you want to force re-seed:
```bash
# Delete all data first
flask shell
>>> from functions.models import Todo, db
>>> Todo.query.delete()
>>> db.session.commit()
>>> exit()

# Now seed
python seed_db.py
```

---

### 5. Docker Errors

#### Error: "port is already allocated"

**Cause:** Port 5000 is in use

**Solution:**
```bash
# Find what's using port 5000
# Mac/Linux:
lsof -i :5000
kill -9 <PID>

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
ports:
  - "5001:5000"  # Use 5001 instead
```

#### Error: "no configuration file provided"

**Cause:** Not in correct directory

**Solution:**
```bash
# Ensure you're in project root
cd /path/to/your/project
ls docker-compose.yml  # Should exist

# Then run
docker-compose up
```

---

### 6. Import Errors

#### Error: "No module named 'flask_sqlalchemy'"

**Cause:** Dependencies not installed

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install Flask-SQLAlchemy Flask-Migrate
```

#### Error: "cannot import name 'db' from 'functions.models'"

**Cause:** Circular import or old code

**Solution:**
Ensure `functions/models.py` has:
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

And `app.py` has:
```python
from functions.models import db
db.init_app(app)
```

---

### 7. Gunicorn Errors

#### Error: "Failed to find application object 'app'"

**Cause:** Gunicorn can't find Flask app

**Solution:**
```bash
# Ensure app.py has:
app = Flask(__name__)

# Run Gunicorn correctly:
gunicorn app:app  # Format: module:variable
```

#### Error: "Address already in use"

**Cause:** Port is occupied

**Solution:**
```bash
# Use different port
gunicorn --bind 0.0.0.0:8000 app:app

# Or kill process on port
lsof -i :5000
kill -9 <PID>
```

---

## 🔍 Debugging Tips

### Check Railway Logs

1. Go to Railway dashboard
2. Click your service
3. Go to "Deployments" tab
4. Click latest deployment
5. View logs for errors

### Test Locally First

```bash
# Test with Docker (closest to Railway)
docker-compose up --build

# If Docker works but Railway doesn't:
# - Check environment variables
# - Check DATABASE_URL format
# - Check port binding
```

### Verify Database Connection

```python
# Test in Flask shell
flask shell

>>> from app import db
>>> db.engine.execute('SELECT 1')
# Should return result without error
```

### Check Migration Status

```bash
# See current migration
flask db current

# See all migrations
flask db history

# See pending migrations
flask db heads
```

---

## 🆘 Still Stuck?

### Checklist

- [ ] PostgreSQL is running (local) or added (Railway)
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Migrations folder exists and committed to git
- [ ] `.env` file has correct credentials (local only)
- [ ] `DATABASE_URL` exists in Railway variables
- [ ] `start.sh` is executable (check Dockerfile)
- [ ] Tested locally with Docker: `docker-compose up`

### Reset Everything (Nuclear Option)

**Local:**
```bash
# Delete database
dropdb todoapp
createdb todoapp

# Delete migrations
rm -rf migrations/

# Start fresh
flask db init
flask db migrate -m "Fresh start"
flask db upgrade
python seed_db.py
```

**Railway:**
1. Delete PostgreSQL database
2. Add new PostgreSQL database
3. Redeploy app (migrations run automatically)

---

## 📞 Getting Help

When asking for help, provide:

1. **Error message** (full text)
2. **What you tried** (commands you ran)
3. **Environment** (local, Docker, Railway)
4. **Logs** (Railway deployment logs or terminal output)

Example:
```
Error: "Could not locate Flask application"
Tried: flask db migrate
Environment: Local development
Logs: [paste error output]
```

---

## ✅ Verification Steps

After fixing issues, verify:

```bash
# 1. Migrations work
flask db upgrade

# 2. Seeding works
python seed_db.py

# 3. App starts
python app.py

# 4. Database has data
flask shell
>>> from functions.models import Todo
>>> Todo.query.all()
>>> exit()

# 5. Routes work
curl http://localhost:5000
```

If all pass, you're good to deploy! 🚀
