import logging
from flask import Flask, request, jsonify, render_template, redirect
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from metrics import setup_metrics
from kafka_utils import KafkaHandler

# Load API key from .env
load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb.db.svc.cluster.local")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "nasa_db")

# Construct MongoDB URI dynamically
if not MONGO_USER or not MONGO_PASSWORD:
    raise Exception("MongoDB credentials are not set in environment variables.")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/{MONGO_DB_NAME}?authSource={MONGO_DB_NAME}"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NasaApp:
    def __init__(self, db, api_key):
        self.db = db
        self.api_key = api_key

    def get_apod_data(self):
        try:
            response = requests.get("https://api.nasa.gov/planetary/apod", params={'api_key': self.api_key})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Request to NASA API timed out.")
            return {"error": "The request to NASA timed out."}
        except requests.exceptions.ConnectionError:
            logger.error("Connection error occurred while requesting NASA API.")
            return {"error": "Failed to connect to NASA API."}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            return {"error": f"HTTP error: {http_err}"}
        except requests.exceptions.RequestException as err:
            logger.error(f"An error occurred: {err}")
            return {"error": "Failed to fetch APOD data."}

    def save_favorite(self, data):
        try:
            self.db.favorites.insert_one(data)
            logger.info(f"Favorite saved: {data}")
        except Exception as e:
            logger.error(f"Error saving favorite: {e}")
            raise

app = Flask(__name__)

# Setting up Kafka and Prometheus 
metrics, request_counter, db_query_gauge = setup_metrics(app)
kafka_handler = KafkaHandler()

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
nasa_app = NasaApp(db, NASA_API_KEY)

# Home Page Route
@app.route('/')
def home():
    try:
        favs = list(db.favorites.find({}, {'_id': 0, 'url': 1, 'title': 1}))
        return render_template('home.html', favorites=favs)
    except Exception as e:
        logger.error(f"Error retrieving favorites: {e}")
        return jsonify({'error': 'Failed to load favorites. Please try again later.'}), 500

# Request instrumentation
@app.before_request
def before_request():
    # Increment request counter with labels for method and endpoint
    request_counter.labels(request.method, request.endpoint).inc()

# Route to get today's Astronomy Picture
@app.route('/apod', methods=['GET'])
def get_apod():
    db_query_gauge.inc()  # Track active database queries
    data = nasa_app.get_apod_data()
    db_query_gauge.dec()  # After query is done
    if data and 'error' not in data:
        try:
            db.last_seen.insert_one(data)
            return render_template('apod.html', apod=data)
        except Exception as e:
            logger.error(f"Error saving last seen: {e}")
            return jsonify({'error': 'Failed to save picture data.'}), 500
    else:
        logger.error(f"Error fetching APOD data: {data.get('error')}")
        return jsonify({'error': data.get('error', 'Failed to fetch picture')}), 500

# Combined Route for Favorites and Last Seen Pictures
@app.route('/pictures', methods=['GET'])
def get_pictures():
    data_type = request.args.get('type', 'favorites')
    try:
        if data_type == 'favorites':
            pics = list(db.favorites.find({}, {'_id': 0, 'url': 1, 'title': 1}))
        elif data_type == 'last_seen':
            pics = list(db.last_seen.find({}, {'_id': 0}))
        else:
            return jsonify({'error': 'Invalid data type. Use "favorites" or "last_seen".'}), 400
        return render_template(f'{data_type}.html', pictures=pics)
    except Exception as e:
        logger.error(f"Error retrieving {data_type}: {e}")
        return jsonify({'error': f'Failed to load {data_type}. Please try again later.'}), 500

# Route to add a favorite picture
@app.route('/favorites', methods=['POST'])
def add_favorite():
    picture_url = request.form['url']
    title = request.form['title']

    if not picture_url or not title:
        return jsonify({'error': 'No picture data provided'}), 400

    try:
        kafka_handler.create_topic('favorites')  # Create the 'favorites' topic
        nasa_app.save_favorite({'url': picture_url, 'title': title})
        kafka_handler.send_message('favorites', f"Added favorite: {title}")
        logger.info(f"Favorite added: {title}")
        return redirect('/favorites')
    except Exception as e:
        logger.error(f"Error adding favorite: {e}")
        return jsonify({'error': 'Failed to add favorite'}), 500

@app.route('/favorites', methods=['GET'])
def view_favorites():
    try:
        favs = list(db.favorites.find({}, {'_id': 0, 'url': 1, 'title': 1}))
        return render_template('favorites.html', favorites=favs)
    except Exception as e:
        logger.error(f"Error retrieving favorites: {e}")
        return jsonify({'error': 'Failed to load favorites. Please try again later.'}), 500

# Route to delete last seen image
@app.route('/last-seen/delete', methods=['POST'])
def delete_last_seen():
    url = request.form['url']
    try:
        db.last_seen.delete_one({'url': url})
        return redirect('/last-seen')
    except Exception as e:
        logger.error(f"Error deleting last seen: {e}")
        return jsonify({'error': 'Failed to delete last seen image. Please try again later.'}), 500

# Metrics Route
@app.route('/metrics')
def metrics_route():
    return metrics.generate_latest()

if __name__ == '__main__':
    app.run(debug=True)
