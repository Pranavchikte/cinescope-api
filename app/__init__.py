# In app/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from config import Config
import os # Import os

cors = CORS()
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- REPLACEMENT CODE STARTS HERE ---
    frontend_url = os.environ.get('FRONTEND_URL')
    if frontend_url:
        # Handle both the main domain and Vercel's preview domains
        origins = [frontend_url, f"https://cinescope-client-git-main-{os.environ.get('GITHUB_USER', 'your-username')}.vercel.app"]
        cors.init_app(app, resources={r"/api/*": {"origins": origins}})
    else:
        # Default for local development
        cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    # --- REPLACEMENT CODE ENDS HERE ---

    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})

    from app.api.v1.movies import movies_bp
    app.register_blueprint(movies_bp, url_prefix='/api/v1/movies')

    return app