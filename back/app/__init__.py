from flask import Flask
from flask_cors import CORS
from .routes import api_blueprint
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    
    app = Flask(__name__)

    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-fallback'),
        JSON_SORT_KEYS=False
    )
    
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('CORS_ORIGINS', 'http://localhost:3000')       # Change when making frontend
        }
    })
    
    # Register API blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Health check
    @app.route('/')
    def health_check():
        return "Meteo-API OK"

    return app




