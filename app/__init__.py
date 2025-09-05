from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from config import Config

cors = CORS()
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})
    
    from app.api.v1.movies import movies_bp
    app.register_blueprint(movies_bp, url_prefix='/api/v1/movies')
    
    return app