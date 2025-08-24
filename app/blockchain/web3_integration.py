from flask import current_app
from web3 import Web3
import json
import os

class BlockchainInterface:
    def __init__(self, provider_url=None):
        """
        Initialize blockchain interface.
        
        Args:
            provider_url: URL of the Ethereum node (defaults to config value)
        """
        if provider_url is None:
            provider_url = current_app.config.get('BLOCKCHAIN_PROVIDER_URL', 'http://127.0.0.1:7545')
        
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = None
        self.account = None
        
        # Check connection
        if not self.w3.is_connected():
            raise Exception(f"Failed to connect to Ethereum node at {provider_url}")
    
    def connect_account(self, private_key):
        """
        Connect to an Ethereum account.
        
        Args:
            private_key: Private key of the account
            
        Returns:
            Account address
        """
        self.account = self.w3.eth.account.from_key(private_key)
        return self.account.address
        
    def load_contract(self, contract_address, abi=None):
        """
        Load deployed smart contract.
        
        Args:
            contract_address: Address of deployed contract
            abi: Contract ABI (if None, will try to load from file)
        """
        try:
            # If ABI is not provided, try to load from contract_info.json
            if abi is None:
                contract_info_path = os.path.join('contracts', 'contract_info.json')
                if os.path.exists(contract_info_path):
                    with open(contract_info_path, 'r') as f:
                        contract_info = json.load(f)
                        abi = contract_info['abi']
                else:
                    # Fallback to simplified ABI
                    abi = [
                        {
                            "inputs": [
                                {"name": "voteHash", "type": "bytes32"},
                                {"name": "userId", "type": "uint256"},
                                {"name": "partyId", "type": "uint256"}
                            ],
                            "name": "recordVote",
                            "outputs": [],
                            "stateMutability": "nonpayable",
                            "type": "function"
                        },
                        {
                            "inputs": [{"name": "userId", "type": "uint256"}],
                            "name": "hasVoted",
                            "outputs": [{"name": "", "type": "bool"}],
                            "stateMutability": "view",
                            "type": "function"
                        },
                        {
                            "inputs": [{"name": "partyId", "type": "uint256"}],
                            "name": "getPartyVoteCount",
                            "outputs": [{"name": "", "type": "uint256"}],
                            "stateMutability": "view",
                            "type": "function"
                        }
                    ]
            
            self.contract = self.w3.eth.contract(
                address=contract_address,
                abi=abi
            )
            
            return True
        except Exception as e:
            raise Exception(f"Failed to load contract: {str(e)}")
    
    def record_vote(self, vote_hash, user_id, party_id, gas_price_gwei=40):
        """
        Record vote on blockchain.
        
        Args:
            vote_hash: Hash of the vote data
            user_id: User ID
            party_id: Party ID
            gas_price_gwei: Gas price in Gwei
            
        Returns:
            Transaction hash
        """
        if not self.contract:
            raise Exception("Contract not loaded")
            
        if not self.account:
            raise Exception("Account not connected")
        
        # Convert hex string to bytes32 if needed
        if isinstance(vote_hash, str) and vote_hash.startswith('0x'):
            vote_hash_bytes = Web3.to_bytes(hexstr=vote_hash)
        elif isinstance(vote_hash, str):
            vote_hash_bytes = Web3.to_bytes(hexstr='0x' + vote_hash)
        else:
            vote_hash_bytes = vote_hash
        
        try:
            # Build transaction
            transaction = self.contract.functions.recordVote(
                vote_hash_bytes, user_id, party_id
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.to_wei(gas_price_gwei, 'gwei')
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.account.key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            raise Exception(f"Failed to record vote on blockchain: {str(e)}")
    
    def check_if_voted(self, user_id):
        """
        Check if user has already voted.
        
        Args:
            user_id: User ID
            
        Returns:
            Boolean indicating if user has voted
        """
        if not self.contract:
            raise Exception("Contract not loaded")
            
        try:
            return self.contract.functions.hasVoted(user_id).call()
        except Exception as e:
            raise Exception(f"Failed to check voting status: {str(e)}")
    
    def get_party_vote_count(self, party_id):
        """
        Get vote count for a party.
        
        Args:
            party_id: Party ID
            
        Returns:
            Number of votes for the party
        """
        if not self.contract:
            raise Exception("Contract not loaded")
            
        try:
            return self.contract.functions.getPartyVoteCount(party_id).call()
        except Exception as e:
            raise Exception(f"Failed to get party vote count: {str(e)}")

# Global blockchain interface instance
blockchain_interface = None

def get_blockchain_interface():
    """
    Get singleton blockchain interface instance.
    
    Returns:
        BlockchainInterface instance
    """
    global blockchain_interface
    
    if blockchain_interface is None:
        blockchain_interface = BlockchainInterface()
        
    return blockchain_interface

def initialize_blockchain(contract_address=None):
    """
    Initialize blockchain interface with contract.
    
    Args:
        contract_address: Address of deployed contract (optional)
        
    Returns:
        BlockchainInterface instance
    """
    global blockchain_interface
    
    if blockchain_interface is None:
        blockchain_interface = BlockchainInterface()
    
    # Load contract if address is provided
    if contract_address:
        blockchain_interface.load_contract(contract_address)
    
    return blockchain_interface