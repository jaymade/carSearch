import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Leith Honda Dealership Configuration
LEITH_HONDA_LOCATIONS = {
    'leith_honda_raleigh': {
        'name': 'Leith Honda Raleigh',
        'location': 'Raleigh, NC',
        'new_url': 'https://www.leithhonda.com/new-inventory/index.htm',
        'used_url': 'https://www.leithhonda.com/used-inventory/index.htm'
    },
    'leith_honda_aberdeen': {
        'name': 'Leith Honda Aberdeen',
        'location': 'Aberdeen, NC',
        'new_url': 'https://www.leithhondaaberdeen.com/new-inventory/index.htm',
        'used_url': 'https://www.leithhondaaberdeen.com/used-inventory/index.htm'
    }
}

# Legacy AutoPark Honda (keeping for backward compatibility)
AUTOPARK_HONDA = {
    'name': 'AutoPark Honda',
    'location': 'Cary, NC',
    'new_url': 'https://www.autoparkhonda.com/new-inventory/index.htm',
    'used_url': 'https://www.autoparkhonda.com/used-inventory/index.htm'
}

# Add AutoPark to Leith locations for comprehensive search
LEITH_HONDA_LOCATIONS['autopark_honda'] = AUTOPARK_HONDA

# Legacy URLs for backward compatibility
SEARCH_URL_NEW = AUTOPARK_HONDA['new_url']
SEARCH_URL_USED = AUTOPARK_HONDA['used_url']

# Search year range updated to match URL parameters
CURRENT_YEAR = 2025
MIN_YEAR = 2015  # Specific year from URL
MAX_YEAR = 2026  # Extended to 2026 as per URL

SEARCH_PARAMS = {
    'make': 'Honda',
    'model': ['Civic', 'Civic Sedan'],  # Updated to match URL
    'trim': ['Sport', 'Sport Touring'],  # Specific trims from URL
    'min_year': MIN_YEAR,  # 2015 and newer
    'max_year': MAX_YEAR,  # Up to 2026
    'normalExteriorColor': 'Black',  # Specific color from URL
    'inventory_type': 'used'  # Used vehicles only as per URL
}

# Scheduling Configuration
BUSINESS_HOURS = {
    'start': 9,  # 9 AM
    'end': 17,   # 5 PM
    'days': [0, 1, 2, 3, 4]  # Monday to Friday (0=Monday)
}

SEARCH_TIMES = ['09:00', '13:00', '17:00']  # 9 AM, 1 PM, 5 PM

# Web Dashboard Configuration
WEB_DASHBOARD_ENABLED = True

# File paths
DATA_FILE = 'previous_matches.json'
LOG_FILE = 'search.log'