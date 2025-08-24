from flask import render_template, current_app
from . import db

def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors."""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server Error."""
        db.session.rollback()
        current_app.logger.error(f"Internal server error: {str(error)}")
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unhandled exceptions."""
        # Pass through HTTP errors
        if hasattr(e, 'code'):
            return render_template(f'errors/{e.code}.html'), e.code
        
        # Handle non-HTTP exceptions
        db.session.rollback()
        current_app.logger.error(f"Unhandled exception: {str(e)}")
        return render_template('errors/500.html'), 500