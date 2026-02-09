#!/bin/bash

# Universal Startup Script for Cloud Deployments
# Works with Render, Railway, and other platforms

echo "🚀 Starting application deployment..."

# Wait for database to be ready (important for cloud deployments)
echo "⏳ Waiting for database connection..."
sleep 5

# Run database migrations
echo "📦 Running database migrations..."
flask db upgrade

# Check if migration was successful
if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed! Check your DATABASE_URL configuration"
    echo "💡 Make sure you have created a PostgreSQL database and connected it to your service"
    exit 1
fi

# Seed the database (only if empty)
echo "🌱 Seeding database..."
python seed_db.py

# Start the application with Gunicorn
echo "🎯 Starting Gunicorn server on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 app:app
