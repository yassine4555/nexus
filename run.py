"""
Run script for Nexus API.
This script ensures proper Python path configuration before starting the app.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import and run the app
from app import app

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST', '127.0.0.1'),
        port=app.config.get('PORT', 5001),
        debug=app.config.get('DEBUG', True)
    )
