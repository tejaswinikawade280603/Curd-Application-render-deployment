from flask import Flask, request, redirect, render_template, url_for
from functions.models import ToDoModel, db
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# ============ DATABASE CONFIGURATION ============
# Platform services (Render/Railway) provide DATABASE_URL
# Handle both postgres:// and postgresql:// formats
database_url = os.getenv('DATABASE_URL')

if database_url:
    # Convert postgres:// to postgresql:// for SQLAlchemy compatibility
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
else:
    # Fallback for local development when DATABASE_URL is not set
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "todoapp")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_port = os.getenv("DB_PORT", "5432")
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# ============ ROUTES ============

@app.route('/hey') 
def hello():
    return "<h1><b>Hello</b></h1>"

@app.route('/') 
def sql_database():
    results = ToDoModel().list_items()
    return render_template('todo.html', results=results)

@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == 'POST':
        title = request.form['Title']
        des = request.form['Description']
        Date = request.form['DueDate']
        ToDoModel().sql_edit_insert((title, des, Date))
        return redirect(url_for('sql_database'))

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    print("Inside delete")
    if request.method == 'GET':
        ID = request.args.get('ID')
        ToDoModel().sql_delete((ID,))
        return redirect(url_for('sql_database'))

@app.route('/query_edit', methods=['POST', 'GET'])
def editlink():
    if request.method == 'GET':
        ID = request.args.get('ID')
        where = ' and id=' + ID
        eresults = ToDoModel().list_items(where)
        results = ToDoModel().list_items()
        return render_template('todo.html', eresults=eresults, results=results)

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    old_id = request.form['old_ID']
    title = request.form['Title']
    des = request.form['Description']
    date = request.form['DueDate']    
    ToDoModel().sql_edit((title, des, date, old_id))
    return redirect(url_for('sql_database'))

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, port=port, host='0.0.0.0')
