#!/usr/bin/env python3
"""
Main entry point for the voting application.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, Party, Vote
from config import config

def create_default_parties():
    """Create default political parties if they don't exist."""
    # Check if parties already exist
    if Party.query.count() == 0:
        # Create default parties
        party1 = Party(name='Democratic Party', description='The Democratic Party')
        party2 = Party(name='Republican Party', description='The Republican Party')
        party3 = Party(name='Libertarian Party', description='The Libertarian Party')
        party4 = Party(name='Green Party', description='The Green Party')
        
        db.session.add_all([party1, party2, party3, party4])
        db.session.commit()
        print("Default parties created.")
    else:
        print("Parties already exist.")

def initialize_database():
    """Initialize the database with default data."""
    with app.app_context():
        # Create tables
        db.create_all()
        print("Database tables created.")
        
        # Create default parties
        create_default_parties()

def main():
    """Main function to run the application."""
    global app
    
    # Create the Flask app
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    # Initialize database
    initialize_database()
    
    # Run the application
    app.run(
        host=os.getenv('FLASK_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )

if __name__ == '__main__':
    main()