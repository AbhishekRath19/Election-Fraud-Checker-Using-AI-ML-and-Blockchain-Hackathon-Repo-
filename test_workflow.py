#!/usr/bin/env python3
"""
Test script for the complete voting workflow.
This script tests the entire voting process from registration to voting to results.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

class TestVotingWorkflow(unittest.TestCase):
    """Test the complete voting workflow."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Set up Flask app for testing
        from app import create_app
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['UPLOAD_FOLDER'] = os.path.join(self.test_dir, 'uploads')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        # Create upload folder
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        self.client = self.app.test_client()
        
        # Create application context
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        # Create database tables
        from app import db
        db.create_all()
        
        # Add test parties
        from app.models import Party
        party1 = Party(name='Party A', description='First political party')
        party2 = Party(name='Party B', description='Second political party')
        db.session.add(party1)
        db.session.add(party2)
        db.session.commit()
    
    def tearDown(self):
        """Clean up test environment."""
        from app import db
        db.session.remove()
        db.drop_all()
        
        self.ctx.pop()
        
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_image(self):
        """Create a simple test image file."""
        from PIL import Image
        import io
        
        # Create a simple 100x100 red image
        image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Create a file-like object
        class MockFile:
            def __init__(self, data, filename):
                self.data = data
                self.filename = filename
                self.content_type = 'image/jpeg'
            
            def seek(self, pos, whence=0):
                if pos == 0 and whence == 0:
                    return 0
                elif pos == 0 and whence == 2:  # SEEK_END
                    return len(self.data)
                return pos
            
            def tell(self):
                return len(self.data)
            
            def read(self, size=-1):
                if size == -1:
                    return self.data
                # This is a simplified implementation
                return self.data[:size]
            
            @property
            def stream(self):
                return io.BytesIO(self.data)
        
        return MockFile(img_byte_arr.getvalue(), 'test_id.jpg')
    
    @patch('app.blockchain.web3_integration.get_blockchain_interface')
    def test_complete_voting_workflow(self, mock_get_blockchain):
        """Test the complete voting workflow."""
        # Mock blockchain interface
        mock_blockchain = MagicMock()
        mock_blockchain.check_if_voted.return_value = False
        mock_blockchain.record_vote.return_value = '0x123456789abcdef'
        mock_get_blockchain.return_value = mock_blockchain
        
        # Step 1: Register a user
        test_image = self.create_test_image()
        
        response = self.client.post('/register', data={
            'name': 'Test User',
            'id_image': test_image
        }, content_type='multipart/form-data')
        
        # Check that registration was successful
        self.assertEqual(response.status_code, 302)  # Redirect to vote page
        
        # Step 2: Cast a vote
        # Get the user ID from the database
        from app.models import User
        user = User.query.first()
        self.assertIsNotNone(user)
        
        # Cast vote
        response = self.client.post(f'/cast_vote/{user.id}', data={
            'party_id': '1'
        })
        
        # Check that vote was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Vote recorded successfully', response.data)
        
        # Step 3: Check results
        response = self.client.get('/results')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Party A', response.data)
        
        # Verify blockchain interaction
        mock_blockchain.check_if_voted.assert_called()
        mock_blockchain.record_vote.assert_called()
    
    def test_user_registration_validation(self):
        """Test user registration validation."""
        # Test missing name
        test_image = self.create_test_image()
        response = self.client.post('/register', data={
            'name': '',
            'id_image': test_image
        }, content_type='multipart/form-data')
        
        self.assertIn(b'Name is required', response.data)
        
        # Test missing image
        response = self.client.post('/register', data={
            'name': 'Test User',
            'id_image': (None, '')
        }, content_type='multipart/form-data')
        
        self.assertIn(b'ID image is required', response.data)
    
    def test_vote_validation(self):
        """Test vote validation."""
        # Create a test user
        from app.models import User
        from app import db
        user = User(name='Test User', id_image_path='test_path')
        db.session.add(user)
        db.session.commit()
        
        # Test missing party selection
        response = self.client.post(f'/cast_vote/{user.id}', data={
            'party_id': ''
        })
        
        self.assertIn(b'Please select a party to vote for', response.data)

def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == '__main__':
    run_tests()