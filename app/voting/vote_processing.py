from flask import render_template, request, redirect, url_for, flash, current_app
from . import voting_bp
from .. import db
from ..models import User, Party, Vote
from ..utils.encryption import encrypt_vote, hash_vote_data, key_to_string
from ..blockchain.web3_integration import get_blockchain_interface
import os

@voting_bp.route('/vote/<int:user_id>')
def vote(user_id):
    """Display voting page for a user."""
    try:
        user = User.query.get_or_404(user_id)
        
        # Check if user has already voted
        existing_vote = Vote.query.filter_by(user_id=user_id).first()
        if existing_vote:
            flash('You have already voted!', 'error')
            return render_template('vote.html', user=user, has_voted=True, vote=existing_vote)
        
        # Get all parties
        parties = Party.query.all()
        
        return render_template('vote.html', user=user, parties=parties, has_voted=False)
        
    except Exception as e:
        current_app.logger.error(f'Error loading voting page: {str(e)}')
        flash('An error occurred while loading the voting page. Please try again.', 'error')
        return redirect(url_for('auth.index'))

@voting_bp.route('/cast_vote/<int:user_id>', methods=['POST'])
def cast_vote(user_id):
    """Process vote submission."""
    try:
        user = User.query.get_or_404(user_id)
        
        # Check if user has already voted
        existing_vote = Vote.query.filter_by(user_id=user_id).first()
        if existing_vote:
            flash('You have already voted!', 'error')
            return redirect(url_for('voting.vote', user_id=user_id))
        
        party_id = request.form.get('party_id')
        
        # Validate input
        validation_error = validate_vote_data(party_id)
        if validation_error:
            flash(validation_error, 'error')
            return redirect(url_for('voting.vote', user_id=user_id))
        
        party = Party.query.get(party_id)
        if not party:
            flash('Invalid party selection', 'error')
            return redirect(url_for('voting.vote', user_id=user_id))
        
        # Prepare vote data
        vote_data = {
            'user_id': user_id,
            'party_id': party_id,
            'timestamp': str(db.func.current_timestamp())
        }
        
        # Create hash of vote data for blockchain
        vote_hash = hash_vote_data(vote_data)
        
        # Encrypt vote data for database storage
        encrypted_vote_data, key = encrypt_vote(vote_data)
        
        # Convert encrypted data to string for storage
        encrypted_vote_str = str(encrypted_vote_data)
        
        # Convert key to string for (hypothetical) secure storage
        # In a real implementation, this key would be stored securely
        key_str = key_to_string(key)
        
        # Create vote record
        vote = Vote(
            user_id=user_id,
            party_id=party_id,
            encrypted_vote=encrypted_vote_str
        )
        
        db.session.add(vote)
        db.session.flush()  # Get the vote ID without committing
        
        # Try to record vote on blockchain
        blockchain_success = False
        try:
            blockchain = get_blockchain_interface()
            
            # Check if user has already voted on blockchain
            if blockchain.check_if_voted(user_id):
                # Blockchain says user already voted, but database doesn't match
                db.session.rollback()
                flash('Vote conflict detected. Please contact administrator.', 'error')
                return redirect(url_for('voting.vote', user_id=user_id))
            
            # Record vote on blockchain
            tx_hash = blockchain.record_vote(vote_hash, user_id, party_id)
            
            # Update vote record with transaction hash
            vote.blockchain_tx_hash = tx_hash
            blockchain_success = True
            
        except Exception as e:
            # Blockchain recording failed, but we'll still store in database
            current_app.logger.warning(f"Failed to record vote on blockchain: {str(e)}")
            flash('Vote recorded locally. Blockchain synchronization will be attempted later.', 'warning')
        
        # Commit to database
        db.session.commit()
        
        if blockchain_success:
            flash('Vote recorded successfully on both local database and blockchain!', 'success')
        else:
            flash('Vote recorded successfully in local database!', 'success')
            
        return render_template('vote.html', user=user, has_voted=True, vote=vote)
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error processing vote: {str(e)}')
        flash(f'An error occurred while recording your vote: {str(e)}', 'error')
        return redirect(url_for('voting.vote', user_id=user_id))

@voting_bp.route('/results')
def results():
    """Display voting results."""
    try:
        # Count votes for each party
        results = db.session.query(
            Party.name,
            Party.description,
            db.func.count(Vote.id).label('vote_count')
        ).outerjoin(Vote, Party.id == Vote.party_id).group_by(
            Party.id, Party.name, Party.description
        ).order_by(db.desc('vote_count')).all()
        
        # Get blockchain vote counts if possible
        blockchain_results = {}
        try:
            blockchain = get_blockchain_interface()
            for party in Party.query.all():
                try:
                    count = blockchain.get_party_vote_count(party.id)
                    blockchain_results[party.id] = count
                except:
                    blockchain_results[party.id] = "N/A"
        except Exception as e:
            current_app.logger.warning(f"Failed to get blockchain results: {str(e)}")
        
        return render_template('results.html', results=results, blockchain_results=blockchain_results)
        
    except Exception as e:
        current_app.logger.error(f'Error loading results: {str(e)}')
        flash('An error occurred while loading results. Please try again.', 'error')
        return redirect(url_for('auth.index'))

def validate_vote_data(party_id):
    """
    Validate vote data.
    
    Args:
        party_id: Selected party ID
        
    Returns:
        Error message string if validation fails, None if valid
    """
    if not party_id:
        return 'Please select a party to vote for'
    
    try:
        party_id_int = int(party_id)
        if party_id_int <= 0:
            return 'Invalid party selection'
    except ValueError:
        return 'Invalid party selection'
    
    return None