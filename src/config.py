import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
TARGET_PHONE_NUMBER = os.getenv('TARGET_PHONE_NUMBER')

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

# Current year for calculating 10 years old or newer
CURRENT_YEAR = 2025
MIN_YEAR = CURRENT_YEAR - 10  # 2015 and newer

SEARCH_PARAMS = {
    'make': 'Honda',
    'model': ['Civic Hybrid', 'Civic'],
    'trim': ['Sport', 'Sport Touring', 'EX', 'LX'],  # Expanded trims
    'min_year': MIN_YEAR,  # 2015 and newer
    'normalExteriorColor': 'Black',
    'normalBodyStyle': 'Sedan'
}

# Scheduling Configuration
BUSINESS_HOURS = {
    'start': 9,  # 9 AM
    'end': 17,   # 5 PM
    'days': [0, 1, 2, 3, 4]  # Monday to Friday (0=Monday)
}

SEARCH_TIMES = ['09:00', '13:00', '17:00']  # 9 AM, 1 PM, 5 PM

# Notification Configuration
SEND_NO_MATCHES_NOTIFICATION = True  # Send SMS when no vehicles match criteria
NO_MATCHES_NOTIFICATION_FREQUENCY = 'daily'  # 'always', 'daily', 'weekly', 'never'

# File paths
DATA_FILE = 'previous_matches.json'
LOG_FILE = 'search.log'