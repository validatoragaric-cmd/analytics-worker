import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize database
db = SQLAlchemy(app)

# Import models and tasks
from analytics_worker.models import *
from analytics_worker.tasks import *

# Import API routes
from analytics_worker.routes import *

# Create a scheduler instance
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

# Load environment variables from .env file
load_dotenv()

# Register tasks with the scheduler
def schedule_tasks():
    scheduler.add_job(tasks.send_report, 'cron', day('*'), hour='0')
    scheduler.start()

# Run the scheduler as a background thread
import threading
threading.Thread(target=scheduler._run).start()

# Initialize the database
with app.app_context():
    db.create_all()

# URL prefix
app.url_prefix = '/api'

# API endpoint to trigger report generation
@app.route('/report', methods=['POST'])
def generate_report():
    # Process the request data
    data = request.get_json()
    # Call the report generation function
    tasks.send_report(data)
    return jsonify({'message': 'Report generated successfully'})

if __name__ == '__main__':
    app.run(debug=True)