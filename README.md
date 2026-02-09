# 🚀 Flask Todo Application ..

A production-ready todo application built with Flask, PostgreSQL, Flask-SQLAlchemy, and Flask-Migrate. Fully containerized with Docker and ready for Railway deployment.

## ✨ Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 🔄 Database migrations with Flask-Migrate
- 🌱 Automatic database seeding
- 🐳 Docker containerization
- 🚂 Railway deployment ready
- 🎨 Bootstrap UI
- 🚀 Production-ready with Gunicorn

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment guide with explanations
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Start everything (database + app)
docker-compose up --build

# Visit http://localhost:5000
```

### Option 2: Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up .env file with your database credentials
# See .env.example

# 3. Initialize and run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 4. Seed database
python seed_db.py

# 5. Run app
python app.py
```

### Option 3: Deploy to Railway

```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for Railway"
git push origin main

# 2. Go to railway.app
# 3. New Project → Deploy from GitHub
# 4. Add PostgreSQL database
# 5. Generate domain

# Done! Railway automatically runs migrations and seeds database
```

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for detailed Railway instructions.

## 🗄️ Database Migrations

This app uses **Flask-Migrate** for database version control:

```bash
# Create migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# View migration history
flask db history
```

**Important:** The `migrations/` folder must be committed to git!

## 🌱 Database Seeding

Seed the database with sample data:

```bash
python seed_db.py
```

The seeding script is **safe to run multiple times** - it checks for existing data and won't create duplicates.

## 🐳 Docker Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Access Flask container shell
docker-compose exec web bash

# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d todoapp
```

## 🔧 Environment Variables

### Local Development (.env file)

```env
DB_HOST=localhost
DB_NAME=todoapp
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### Railway (Automatic)

Railway automatically provides:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Application port

No manual configuration needed!

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main todo list page |
| GET | `/hey` | Health check |
| POST | `/insert` | Create new todo |
| GET | `/delete?ID=<id>` | Delete todo (soft delete) |
| GET | `/query_edit?ID=<id>` | Get todo for editing |
| POST | `/edit` | Update existing todo |

## 🗃️ Database Schema

```python
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    _is_deleted = db.Column(db.Boolean, default=False)
    CreatedOn = db.Column(db.Date, default=datetime.utcnow().date)
    DueDate = db.Column(db.Date, nullable=True)
```

## 🏗️ Project Structure

```
.
├── app.py                  # Main Flask application
├── functions/
│   ├── models.py          # SQLAlchemy models
│   └── __init__.py
├── templates/
│   └── todo.html          # Frontend template
├── migrations/            # Database migrations (commit to git!)
├── seed_db.py            # Database seeding script
├── start.sh              # Railway startup script
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
├── .env                  # Local environment variables (not in git)
├── DEPLOYMENT_GUIDE.md   # Detailed deployment guide
├── QUICK_START.md        # Quick reference
└── TROUBLESHOOTING.md    # Common issues and solutions
```

## 🚂 Railway Deployment

This app is **Railway-ready** with:

✅ Automatic database migrations on deployment  
✅ Automatic database seeding (if empty)  
✅ Gunicorn production server  
✅ PostgreSQL DATABASE_URL support  
✅ Proper port binding  
✅ Health checks  

**Deploy in 3 steps:**

1. Push to GitHub
2. Connect to Railway
3. Add PostgreSQL database

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for complete instructions.

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Could not locate Flask application" | Run `flask db init` |
| "Can't locate revision" | Commit `migrations/` to git |
| Port 5000 in use | Change port in docker-compose.yml |
| Database connection error | Check .env credentials |
| Railway deployment fails | Check logs in Railway dashboard |

See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for detailed solutions.

## 🧪 Testing

```bash
# Test database connection
flask shell
>>> from app import db
>>> db.engine.execute('SELECT 1')

# Test migrations
flask db upgrade

# Test seeding
python seed_db.py

# Test app
python app.py
# Visit http://localhost:5000
```

## 📦 Dependencies

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-Migrate** - Database migrations
- **psycopg2-binary** - PostgreSQL adapter
- **python-dotenv** - Environment variable management
- **gunicorn** - Production WSGI server

## 🎯 What's New?

This version includes major improvements:

- ✅ Migrated from raw SQL to SQLAlchemy ORM
- ✅ Added Flask-Migrate for database version control
- ✅ Implemented safe database seeding
- ✅ Railway deployment configuration
- ✅ Gunicorn production server
- ✅ Automatic migrations on deployment
- ✅ Comprehensive documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run migrations: `flask db migrate -m "Your changes"`
5. Test locally with Docker
6. Submit a pull request

## 📄 License

MIT License

## 🆘 Need Help?

1. Check **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**
2. Review **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**
3. Check Railway deployment logs
4. Verify environment variables

---

**Made with ❤️ using Flask, PostgreSQL, and Railway**
