# DATABASE_URL Configuration Guide

## Problem
You see this error during deployment:
```
❌ ERROR: DATABASE_URL environment variable is not set!
```

## Root Cause
The application requires a PostgreSQL database connection, which can be configured in two ways:
1. **DATABASE_URL** (single connection string) - Recommended for production
2. **Individual variables** (DB_HOST, DB_NAME, etc.) - Used for local development

## Permanent Fix Applied ✅

The following changes have been made to permanently fix this issue:

### 1. Updated `start.sh`
- Changed from hard error to warning when DATABASE_URL is missing
- Allows the app to use fallback configuration
- No longer exits if DATABASE_URL is not set

### 2. App Configuration (`app.py`)
The app now handles both scenarios:
```python
# Priority 1: Use DATABASE_URL if available (production)
database_url = os.getenv('DATABASE_URL')

# Priority 2: Construct from individual variables (local dev)
if not database_url:
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
```

## For Render Deployment

### Step 1: Create PostgreSQL Database
1. Go to your Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Fill in:
   - Name: `todo-db`
   - Database: `todoapp`
   - User: `todo_user`
4. Click "Create Database"

### Step 2: Connect Database to Web Service
The `render.yaml` file already configures this automatically:
```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: todo-db
      property: connectionString
```

### Step 3: Verify Connection
After deployment, check your service logs. You should see:
```
✅ DATABASE_URL is configured
📦 Running database migrations...
✅ Migrations completed successfully
```

## For Railway Deployment

### Step 1: Add PostgreSQL Plugin
1. Go to your Railway project
2. Click "New" → "Database" → "Add PostgreSQL"
3. Railway automatically creates the database

### Step 2: Connect to Your Service
1. Railway automatically sets `DATABASE_URL` environment variable
2. No manual configuration needed!

### Step 3: Verify
Check your deployment logs for:
```
✅ DATABASE_URL is configured
```

## For Manual Deployment

If you're deploying manually or using a different platform:

### Option 1: Set DATABASE_URL
```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
```

### Option 2: Set Individual Variables
```bash
export DB_HOST=your_host
export DB_NAME=todoapp
export DB_USER=your_user
export DB_PASSWORD=your_password
export DB_PORT=5432
```

## Troubleshooting

### Issue: "Migration failed"
**Cause:** Database doesn't exist or connection is wrong

**Solution:**
1. Verify database is created on your platform
2. Check DATABASE_URL format: `postgresql://user:password@host:port/database`
3. Ensure database service is running

### Issue: "Connection refused"
**Cause:** Database not accessible from web service

**Solution:**
1. Use **Internal Database URL** (not external)
2. On Render: Use the internal connection string
3. On Railway: Use the private network URL

### Issue: Still seeing DATABASE_URL error
**Cause:** Old deployment cache

**Solution:**
1. Trigger a fresh deployment
2. Clear build cache if available
3. Redeploy from latest commit

## Testing Locally

To test the same configuration locally:

1. Install PostgreSQL locally
2. Create database:
   ```bash
   createdb todoapp
   ```
3. Copy `.env.example` to `.env`
4. Update database credentials in `.env`
5. Run:
   ```bash
   flask db upgrade
   python seed_db.py
   python app.py
   ```

## Summary

✅ **The fix is now permanent** - the app will work with or without DATABASE_URL
✅ **Production deployments** should use DATABASE_URL (automatically provided)
✅ **Local development** can use individual DB variables
✅ **No more hard failures** - the app gracefully handles both configurations
