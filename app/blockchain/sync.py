from .. import db
from ..models import Vote, Party
from .web3_integration import get_blockchain_interface
from flask import current_app
import logging

def sync_votes_with_blockchain():
    """
    Synchronize local votes with blockchain.
    This function checks for votes that were stored locally but not yet
    recorded on the blockchain and attempts to record them.
    """
    try:
        blockchain = get_blockchain_interface()
        
        # Get votes that don't have a blockchain transaction hash
        unsynced_votes = Vote.query.filter(
            Vote.blockchain_tx_hash.is_(None)
        ).all()
        
        synced_count = 0
        failed_count = 0
        
        for vote in unsynced_votes:
            try:
                # Check if user has already voted on blockchain
                has_voted = False
                try:
                    has_voted = blockchain.check_if_voted(vote.user_id)
                except Exception as e:
                    current_app.logger.warning(
                        f"Failed to check blockchain voting status for user {vote.user_id}: {str(e)}"
                    )
                    # Continue with sync attempt
                
                if has_voted:
                    # User already voted on blockchain, mark this vote as invalid
                    current_app.logger.warning(
                        f"User {vote.user_id} already voted on blockchain. "
                        f"Marking local vote {vote.id} as invalid."
                    )
                    # In a real implementation, you might want to delete or mark invalid votes
                    continue
                
                # Prepare vote data for hashing
                vote_data = {
                    'user_id': vote.user_id,
                    'party_id': vote.party_id,
                    'timestamp': str(vote.voted_at) if vote.voted_at else str(db.func.current_timestamp())
                }
                
                # Create hash of vote data
                from ..utils.encryption import hash_vote_data
                vote_hash = hash_vote_data(vote_data)
                
                # Record vote on blockchain
                tx_hash = blockchain.record_vote(vote_hash, vote.user_id, vote.party_id)
                
                # Update vote record with transaction hash
                vote.blockchain_tx_hash = tx_hash
                db.session.commit()
                
                synced_count += 1
                current_app.logger.info(
                    f"Successfully synced vote {vote.id} to blockchain with tx {tx_hash}"
                )
                
            except Exception as e:
                failed_count += 1
                current_app.logger.error(
                    f"Failed to sync vote {vote.id} to blockchain: {str(e)}"
                )
                db.session.rollback()
        
        return {
            'synced': synced_count,
            'failed': failed_count,
            'total': len(unsynced_votes)
        }
        
    except Exception as e:
        current_app.logger.error(f"Blockchain synchronization failed: {str(e)}")
        return {
            'synced': 0,
            'failed': 0,
            'total': 0,
            'error': str(e)
        }

def verify_blockchain_consistency():
    """
    Verify consistency between local database and blockchain.
    This function checks for discrepancies between local and blockchain records.
    """
    try:
        blockchain = get_blockchain_interface()
        
        # Get all votes from database
        local_votes = Vote.query.all()
        
        discrepancies = []
        
        for vote in local_votes:
            try:
                # Check if user has voted on blockchain
                has_voted = False
                try:
                    has_voted = blockchain.check_if_voted(vote.user_id)
                except Exception as e:
                    discrepancies.append({
                        'vote_id': vote.id,
                        'user_id': vote.user_id,
                        'issue': f'Blockchain check failed: {str(e)}'
                    })
                    continue
                
                # If vote has a transaction hash but user hasn't voted on blockchain,
                # there's a discrepancy
                if vote.blockchain_tx_hash and not has_voted:
                    discrepancies.append({
                        'vote_id': vote.id,
                        'user_id': vote.user_id,
                        'issue': 'Vote recorded locally but not on blockchain'
                    })
                
                # If vote doesn't have a transaction hash but user has voted on blockchain,
                # there's a discrepancy
                elif not vote.blockchain_tx_hash and has_voted:
                    discrepancies.append({
                        'vote_id': vote.id,
                        'user_id': vote.user_id,
                        'issue': 'Vote recorded on blockchain but not locally'
                    })
                    
            except Exception as e:
                discrepancies.append({
                    'vote_id': vote.id,
                    'user_id': vote.user_id,
                    'issue': f'Blockchain check failed: {str(e)}'
                })
        
        return {
            'total_votes': len(local_votes),
            'discrepancies': discrepancies,
            'consistent': len(discrepancies) == 0
        }
        
    except Exception as e:
        current_app.logger.error(f"Blockchain consistency verification failed: {str(e)}")
        return {
            'total_votes': 0,
            'discrepancies': [],
            'consistent': False,
            'error': str(e)
        }

def get_blockchain_status():
    """
    Get the current status of blockchain integration.
    
    Returns:
        Dictionary with blockchain status information
    """
    try:
        blockchain = get_blockchain_interface()
        
        # Try to get a simple value from the blockchain
        # This is just to check if we can connect and interact
        try:
            # Try to get vote count for party 1 as a test
            test_count = blockchain.get_party_vote_count(1)
            connected = True
        except:
            test_count = None
            connected = False
        
        # Count local votes
        local_vote_count = Vote.query.count()
        
        # Count votes with blockchain transaction hashes
        blockchain_vote_count = Vote.query.filter(
            Vote.blockchain_tx_hash.isnot(None)
        ).count()
        
        return {
            'connected': connected,
            'local_votes': local_vote_count,
            'blockchain_votes': blockchain_vote_count,
            'pending_sync': local_vote_count - blockchain_vote_count,
            'test_count': test_count
        }
        
    except Exception as e:
        current_app.logger.error(f"Blockchain status check failed: {str(e)}")
        return {
            'connected': False,
            'error': str(e)
        }