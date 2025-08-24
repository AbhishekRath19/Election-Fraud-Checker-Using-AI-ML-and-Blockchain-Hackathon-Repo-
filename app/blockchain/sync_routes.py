from flask import render_template, request, jsonify, current_app
from . import blockchain_bp
from .sync import sync_votes_with_blockchain, verify_blockchain_consistency, get_blockchain_status
from .. import db
from ..models import Vote, Party

@blockchain_bp.route('/blockchain/status')
def blockchain_status():
    """Get blockchain integration status."""
    try:
        status = get_blockchain_status()
        return jsonify(status)
    except Exception as e:
        current_app.logger.error(f"Error getting blockchain status: {str(e)}")
        return jsonify({
            'connected': False,
            'error': 'Failed to get blockchain status'
        }), 500

@blockchain_bp.route('/blockchain/sync')
def blockchain_sync():
    """Manually trigger blockchain synchronization."""
    try:
        result = sync_votes_with_blockchain()
        if 'error' in result:
            return jsonify({
                'success': False,
                'message': f'Synchronization failed: {result["error"]}'
            }), 500
        
        return jsonify({
            'success': True,
            'message': f'Synchronization complete. {result["synced"]} votes synced, {result["failed"]} failed.',
            'details': result
        })
    except Exception as e:
        current_app.logger.error(f"Synchronization error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Synchronization failed: {str(e)}'
        }), 500

@blockchain_bp.route('/blockchain/verify')
def blockchain_verify():
    """Verify consistency between local database and blockchain."""
    try:
        result = verify_blockchain_consistency()
        if 'error' in result:
            return jsonify({
                'success': False,
                'message': f'Verification failed: {result["error"]}'
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'Verification complete',
            'details': result
        })
    except Exception as e:
        current_app.logger.error(f"Verification error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Verification failed: {str(e)}'
        }), 500

@blockchain_bp.route('/blockchain/dashboard')
def blockchain_dashboard():
    """Display blockchain dashboard."""
    try:
        status = get_blockchain_status()
        
        # Get recent votes
        recent_votes = Vote.query.order_by(Vote.voted_at.desc()).limit(10).all()
        
        # Get party information
        parties = Party.query.all()
        
        return render_template('blockchain_dashboard.html', 
                             status=status, 
                             recent_votes=recent_votes, 
                             parties=parties)
    except Exception as e:
        current_app.logger.error(f"Error loading blockchain dashboard: {str(e)}")
        flash('Failed to load blockchain dashboard', 'error')
        return redirect(url_for('auth.index'))