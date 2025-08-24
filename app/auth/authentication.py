from flask import render_template, request, redirect, url_for, flash, current_app
from . import auth_bp
from .. import db
from ..models import User
from ..utils.image_compression import compress_image, get_image_info
import os
import time
from werkzeug.utils import secure_filename
from PIL import Image

@auth_bp.route('/')
def index():
    """Home page route."""
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if request.method == 'POST':
        name = request.form.get('name')
        id_image = request.files.get('id_image')
        
        # Validate input
        validation_error = validate_registration_data(name, id_image)
        if validation_error:
            flash(validation_error, 'error')
            return render_template('login.html')
        
        try:
            # Process the image
            compressed_image = compress_image(id_image)
            
            # Validate compressed image
            image_info = get_image_info(id_image)
            if image_info['width'] < 100 or image_info['height'] < 100:
                flash('ID image is too small. Please upload a clearer image.', 'error')
                return render_template('login.html')
            
            # Generate secure filename
            filename = secure_filename(f"{name.replace(' ', '_')}_{int(time.time() * 1000)}_{id_image.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            # Save compressed image
            compressed_image.save(filepath)
            
            # Create user record
            user = User(name=name, id_image_path=filepath)
            db.session.add(user)
            db.session.commit()
            
            flash(f'Registration successful! Your user ID is {user.id}', 'success')
            return redirect(url_for('voting.vote', user_id=user.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Registration error: {str(e)}')
            flash(f'An error occurred during registration: {str(e)}', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

def validate_registration_data(name, id_image):
    """
    Validate registration data.
    
    Args:
        name: User's name
        id_image: Uploaded ID image file
        
    Returns:
        Error message string if validation fails, None if valid
    """
    if not name:
        return 'Name is required'
    
    if len(name.strip()) < 2:
        return 'Name must be at least 2 characters long'
    
    if len(name.strip()) > 100:
        return 'Name must be less than 100 characters long'
    
    if not id_image:
        return 'ID image is required'
    
    if id_image.filename == '':
        return 'Please select an ID image'
    
    # Check if file is allowed
    if not allowed_file(id_image.filename):
        return 'Invalid file type. Please upload an image file (png, jpg, jpeg, gif)'
    
    # Check file size (max 5MB)
    id_image.seek(0, os.SEEK_END)
    file_size = id_image.tell()
    id_image.seek(0)
    
    if file_size > 5 * 1024 * 1024:
        return 'File size exceeds 5MB limit. Please upload a smaller file.'
    
    return None

def allowed_file(filename):
    """Check if file extension is allowed."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions