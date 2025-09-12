"""
WSGI Entry Point for InfluBerry v2
Production and Development server entry point
"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create Flask application
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Development server configuration
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', '1').lower() in ['1', 'true', 'on']
    
    print(f"Starting InfluBerry v2 server...")
    print(f"Environment: {config_name}")
    print(f"Debug mode: {debug}")
    print(f"Port: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
