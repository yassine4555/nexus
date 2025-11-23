"""
Nexus API - Employee Management System
Main application file that initializes and runs the Flask server.
"""

import sys
import os

# Ensure project root is in Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import get_config
from models import db
#from routes import users_bp, invites_bp


def create_app(config_name=None):
    """
    Application factory pattern.
    
    Args:
        config_name (str): Configuration name (development, production, testing)
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # Register blueprints
    # Register blueprints
    #app.register_blueprint(users_bp)
    #app.register_blueprint(invites_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/')
    def index():
        return jsonify(
            status=200,
            message='Nexus API is running',
            version='2.0'
        ), 200
    
    @app.route('/health')
    def health():
        return jsonify(status=200, message='OK'), 200
    
    return app


def register_error_handlers(app):
    """Register custom error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(status=404, message='Resource not found'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(status=500, message='Internal server error'), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(status=405, message='Method not allowed'), 405


# Create the application instance
app = create_app()


if __name__ == '__main__':
    # Run the development server
    app.run(host='0.0.0.0' ,port=5001, debug=True)
    
