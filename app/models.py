from . import db
from datetime import datetime

class User(db.Model):
    """User model for storing voter information."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_image_path = db.Column(db.String(200), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with votes
    votes = db.relationship('Vote', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name}>'

class Party(db.Model):
    """Party model for storing political party information."""
    __tablename__ = 'parties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relationship with votes
    votes = db.relationship('Vote', backref='party', lazy=True)
    
    def __repr__(self):
        return f'<Party {self.name}>'

class Vote(db.Model):
    """Vote model for storing encrypted vote information."""
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False)
    encrypted_vote = db.Column(db.Text, nullable=False)
    blockchain_tx_hash = db.Column(db.String(66))  # Ethereum transaction hash
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Vote {self.id} by User {self.user_id}>'