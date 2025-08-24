#!/usr/bin/env python3
"""
Script to deploy the Voting smart contract to Ethereum blockchain.
"""

import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc
import argparse

def compile_contract():
    """
    Compile the Voting.sol smart contract.
    
    Returns:
        Compiled contract interface
    """
    # Install Solidity compiler if needed
    install_solc('0.8.0')
    
    # Read contract source code
    with open('contracts/Voting.sol', 'r') as file:
        contract_source = file.read()
    
    # Compile contract
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "Voting.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode.object"]
                }
            }
        }
    }, solc_version="0.8.0")
    
    # Get contract interface
    contract_interface = compiled_sol['contracts']['Voting.sol']['Voting']
    
    return contract_interface

def deploy_contract(provider_url, private_key):
    """
    Deploy the Voting contract to the blockchain.
    
    Args:
        provider_url: URL of the Ethereum node
        private_key: Private key of the deployer account
        
    Returns:
        Tuple of (contract_address, contract_abi)
    """
    # Connect to Ethereum node
    w3 = Web3(Web3.HTTPProvider(provider_url))
    
    if not w3.is_connected():
        raise Exception(f"Failed to connect to Ethereum node at {provider_url}")
    
    # Get account from private key
    account = w3.eth.account.from_key(private_key)
    print(f"Deploying from account: {account.address}")
    
    # Compile contract
    contract_interface = compile_contract()
    
    # Create contract instance
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['evm']['bytecode']['object']
    )
    
    # Build transaction
    transaction = contract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.to_wei('40', 'gwei')
    })
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction hash: {tx_hash.hex()}")
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    print(f"Contract deployed at address: {contract_address}")
    
    return contract_address, contract_interface['abi']

def save_contract_info(contract_address, contract_abi, output_file='contract_info.json'):
    """
    Save contract information to a file.
    
    Args:
        contract_address: Address of deployed contract
        contract_abi: ABI of the contract
        output_file: File to save information to
    """
    contract_info = {
        'address': contract_address,
        'abi': contract_abi
    }
    
    with open(output_file, 'w') as f:
        json.dump(contract_info, f, indent=2)
    
    print(f"Contract information saved to {output_file}")

def main():
    """Main function to deploy contract."""
    parser = argparse.ArgumentParser(description='Deploy Voting smart contract')
    parser.add_argument('--provider-url', default='http://127.0.0.1:7545',
                        help='Ethereum node provider URL')
    parser.add_argument('--private-key', required=True,
                        help='Private key of deployer account')
    parser.add_argument('--output-file', default='contract_info.json',
                        help='Output file for contract information')
    
    args = parser.parse_args()
    
    try:
        # Deploy contract
        contract_address, contract_abi = deploy_contract(
            args.provider_url, args.private_key
        )
        
        # Save contract information
        save_contract_info(contract_address, contract_abi, args.output_file)
        
        print("Deployment successful!")
        
    except Exception as e:
        print(f"Deployment failed: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())