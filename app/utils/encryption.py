from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json
import hashlib

def encrypt_vote(vote_data, key=None):
    """
    Encrypt vote data using AES encryption.
    
    Args:
        vote_data: Dictionary containing vote information
        key: Optional encryption key (if None, a random key will be generated)
        
    Returns:
        Tuple of (encrypted_data_dict, key)
    """
    # Convert vote data to JSON string
    json_data = json.dumps(vote_data)
    
    # Generate a random key if not provided
    if key is None:
        key = get_random_bytes(32)  # 256-bit key
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_EAX)
    
    # Encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(json_data.encode('utf-8'))
    
    # Prepare encrypted data for storage
    encrypted_data = {
        'nonce': base64.b64encode(cipher.nonce).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8')
    }
    
    return encrypted_data, key

def decrypt_vote(encrypted_data, key):
    """
    Decrypt vote data using AES decryption.
    
    Args:
        encrypted_data: Dictionary containing encrypted vote data
        key: Decryption key
        
    Returns:
        Decrypted vote data as dictionary
    """
    try:
        # Decode base64 encoded data
        nonce = base64.b64decode(encrypted_data['nonce'])
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        tag = base64.b64decode(encrypted_data['tag'])
        
        # Create cipher
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        
        # Decrypt the data
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        # Convert JSON string back to dictionary
        vote_data = json.loads(plaintext.decode('utf-8'))
        
        return vote_data
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

def hash_vote_data(vote_data):
    """
    Create a hash of vote data for blockchain storage.
    
    Args:
        vote_data: Dictionary containing vote information
        
    Returns:
        SHA256 hash of the vote data
    """
    json_data = json.dumps(vote_data, sort_keys=True)
    return hashlib.sha256(json_data.encode('utf-8')).hexdigest()

def generate_key():
    """
    Generate a random 256-bit encryption key.
    
    Returns:
        Random encryption key
    """
    return get_random_bytes(32)

def key_to_string(key):
    """
    Convert encryption key to base64 string for storage.
    
    Args:
        key: Encryption key
        
    Returns:
        Base64 encoded key string
    """
    return base64.b64encode(key).decode('utf-8')

def string_to_key(key_string):
    """
    Convert base64 string back to encryption key.
    
    Args:
        key_string: Base64 encoded key string
        
    Returns:
        Encryption key
    """
    return base64.b64decode(key_string.encode('utf-8'))