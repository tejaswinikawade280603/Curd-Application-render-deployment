# 🔗 Render Database Connection Guide

## The Problem

If you see this error on Render:
```
connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
```

It means your web service can't find the PostgreSQL database because `DATABASE_URL` is not configured.

---

## The Solution (3 Steps)

### Step 1: Get Your Database URL

1. Go to your Render dashboard
2. Click on your **PostgreSQL database** (named `todo-db`)
3. Scroll down to find the **Internal Database URL**
4. Copy the entire URL (it looks like: `postgresql://user:password@host/database`)

### Step 2: Add DATABASE_URL to Your Web Service

1. Go back to your **web service** (named `python-application-deploy-using-railway-1`)
2. Click the **Environment** tab
3. Click **Add Environment Variable**
4. Enter:
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the Internal Database URL you copied
5. Click **Save Changes**

### Step 3: Redeploy

1. Go to the **Manual Deploy** dropdown
2. Click **Deploy latest commit**
3. Watch the logs - you should now see:
   ```
   ✅ DATABASE_URL is configured
   📦 Running database migrations...
   ✅ Migrations completed successfully
   ```

---

## Alternative: Use render.yaml (Automatic)

If you deploy using the `render.yaml` file (Infrastructure as Code), the database connection is now configured automatically.

The updated `render.yaml` includes:
```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: todo-db
      property: connectionString
```

To use this:
1. Commit and push the updated `render.yaml`
2. Render will automatically connect the database
3. No manual environment variable setup needed

---

## Verification

After deployment, check the logs for these success messages:

✅ **Good logs:**
```
✅ DATABASE_URL is configured
⏳ Waiting for database connection...
📦 Running database migrations...
✅ Migrations completed successfully
🌱 Seeding database...
🎯 Starting Gunicorn server...
```

❌ **Bad logs:**
```
connection to server at "localhost" port 5432 failed
```
→ This means `DATABASE_URL` is still not set. Go back to Step 2.

---

## Why This Happens

- Your app code checks for `DATABASE_URL` first (for production)
- If not found, it falls back to `.env` file settings (for local development)
- The `.env` file has `DB_HOST=localhost`, which doesn't exist on Render
- Render's PostgreSQL runs on a different host, accessible via `DATABASE_URL`

---

## Quick Troubleshooting

**Q: I added DATABASE_URL but still getting the error**
- Make sure you clicked "Save Changes"
- Trigger a new deployment (don't just restart)
- Check the Environment tab to confirm the variable is there

**Q: Which database URL should I use - Internal or External?**
- Use **Internal Database URL** (faster, more secure)
- External is only for connecting from your local machine

**Q: Do I need to set DB_HOST, DB_NAME, etc. on Render?**
- No! `DATABASE_URL` contains everything
- Those individual variables are only for local development

---

## Success!

Once configured correctly, your app will:
- ✅ Connect to PostgreSQL automatically
- ✅ Run migrations on every deployment
- ✅ Seed the database with sample data
- ✅ Start serving requests

Your todo app should now be live! 🎉
