import os
import logging
import json
from flask import Flask, render_template, jsonify, request

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "maycol-personal-website-secret")

# Visit counter file path
COUNTER_FILE = "visit_counter.json"

# Initialize visit counter if it doesn't exist
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, 'w') as f:
        json.dump({"visits": 0}, f)

def get_visit_count():
    try:
        with open(COUNTER_FILE, 'r') as f:
            data = json.load(f)
            return data.get("visits", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def increment_visit_count():
    try:
        count = get_visit_count()
        with open(COUNTER_FILE, 'w') as f:
            json.dump({"visits": count + 1}, f)
        return count + 1
    except Exception as e:
        logging.error(f"Error incrementing visit count: {e}")
        return 0

@app.route('/')
def index():
    visit_count = increment_visit_count()
    return render_template('index.html', visit_count=visit_count)

@app.route('/projects')
def projects():
    visit_count = get_visit_count()
    return render_template('projects.html', visit_count=visit_count)

@app.route('/contact')
def contact():
    visit_count = get_visit_count()
    return render_template('contact.html', visit_count=visit_count)

@app.route('/api/visits')
def get_visits():
    return jsonify({"visits": get_visit_count()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
