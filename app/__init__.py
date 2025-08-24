from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Create upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Register blueprints
    from .auth import auth_bp
    from .voting import voting_bp
    from .blockchain import blockchain_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(voting_bp)
    app.register_blueprint(blockchain_bp)
    
    # Register error handlers
    from .errors import register_error_handlers
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app