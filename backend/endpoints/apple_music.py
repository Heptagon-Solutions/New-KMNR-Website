"""Apple Music API endpoints for generating developer tokens."""

import os
import time
import jwt
from flask import Blueprint, jsonify
from dotenv import dotenv_values

# Load environment variables
secrets = dotenv_values(".env")

# Apple Music credentials from environment
APPLE_TEAM_ID = secrets.get('APPLE_TEAM_ID')
APPLE_KEY_ID = secrets.get('APPLE_KEY_ID')
APPLE_PRIVATE_KEY_FILE = secrets.get('APPLE_PRIVATE_KEY_FILE', 'AuthKey.p8')

# Create blueprint
apple_music_bp = Blueprint('apple_music', __name__, url_prefix='/api/apple-music')

def generate_developer_token():
    """Generates a Developer Token for the Apple Music API."""
    
    # Read the private key
    try:
        with open(APPLE_PRIVATE_KEY_FILE, 'r') as f:
            private_key = f.read()
    except FileNotFoundError:
        raise RuntimeError(f"Private key file not found at {APPLE_PRIVATE_KEY_FILE}")
    
    # Token is valid for 6 months (max allowed)
    issue_time = time.time()
    expiration_time = issue_time + 15777000  # 6 months in seconds
    
    # Header
    headers = {
        "alg": "ES256",
        "kid": APPLE_KEY_ID
    }
    
    # Payload
    payload = {
        "iss": APPLE_TEAM_ID,      # Issuer: Your Team ID
        "iat": int(issue_time),    # Issued At: Current time
        "exp": int(expiration_time) # Expiration Time
    }
    
    # Generate the token
    token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
    
    return token

@apple_music_bp.route('/get-developer-token', methods=['GET'])
def get_developer_token():
    """
    Generates and returns a new developer token.
    """
    try:
        # Check if required credentials are available
        if not all([APPLE_TEAM_ID, APPLE_KEY_ID]):
            return jsonify({
                'error': 'Apple Music credentials not configured. Please set APPLE_TEAM_ID and APPLE_KEY_ID in .env file'
            }), 500
        
        token = generate_developer_token()
        return jsonify({'token': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@apple_music_bp.route('/test', methods=['GET'])
def test_apple_music():
    """Test endpoint to verify Apple Music integration is working."""
    return jsonify({
        'status': 'Apple Music integration ready',
        'has_team_id': bool(APPLE_TEAM_ID),
        'has_key_id': bool(APPLE_KEY_ID),
        'private_key_file': APPLE_PRIVATE_KEY_FILE
    })