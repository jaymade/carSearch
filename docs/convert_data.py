#!/usr/bin/env python3
"""
Convert previous_matches.json to web-friendly format
"""

import json
import sys
import os
import re
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from config import SEARCH_URL_NEW, SEARCH_URL_USED

def convert_data_for_web():
    """Convert the previous_matches.json to web dashboard format"""
    
    # Read the original data
    try:
        with open('../previous_matches.json', 'r') as f:
            original_data = json.load(f)
    except FileNotFoundError:
        print("previous_matches.json not found")
        return
    
    # Extract statistics from the actual data structure
    previous_matches = original_data.get('previous_matches', [])
    last_search = original_data.get('last_search', '')
    total_searches = original_data.get('total_searches', 0)
    notifications_sent = original_data.get('notifications_sent', 0)
    
    # Convert to web format
    web_data = {
        'last_updated': datetime.now().isoformat(),
        'last_search': last_search,
        'total_searches': total_searches,
        'vehicles_tracked': len(previous_matches),
        'notifications_sent': notifications_sent,
        'matches': []
    }
    
    # Process vehicle matches
    for vehicle in previous_matches:
        # Get basic vehicle information
        title = vehicle.get('title', 'Honda Vehicle')
        url = vehicle.get('url', '')
        first_seen = vehicle.get('first_seen', '')
        
        # Try to extract year from title or URL
        year = 'Unknown'
        year_match = re.search(r'20\d{2}', title)
        if year_match:
            year = year_match.group()
        elif url:
            year_match = re.search(r'20\d{2}', url)
            if year_match:
                year = year_match.group()
        
        # Determine vehicle type based on year or URL
        vehicle_type = 'unknown'
        current_year = datetime.now().year
        if year != 'Unknown':
            year_int = int(year)
            vehicle_type = 'new' if year_int >= current_year else 'used'
        elif 'new-inventory' in url:
            vehicle_type = 'new'
        elif 'used-inventory' in url:
            vehicle_type = 'used'
        
        # Extract dealership info from URL
        dealership = 'Honda Dealership'
        if 'leithhonda.com' in url:
            dealership = 'Leith Honda Raleigh'
        elif 'leithhondaaberdeen.com' in url:
            dealership = 'Leith Honda Aberdeen'
        elif 'autoparkhonda.com' in url:
            dealership = 'AutoPark Honda'
        
        # Enhance title if it's too basic
        enhanced_title = title
        if title == 'Hybrid' or len(title) < 10:
            trim = extract_trim_from_title(title)
            enhanced_title = f"Honda Civic {trim}"
            if year != 'Unknown':
                enhanced_title = f"{year} {enhanced_title}"
        
        # Format found date to be JavaScript-friendly
        found_date = first_seen
        if found_date:
            try:
                # Keep the original ISO format for JavaScript Date parsing
                dt = datetime.fromisoformat(found_date.replace('Z', '+00:00'))
                found_date = dt.isoformat()
            except:
                # If parsing fails, use current time
                found_date = datetime.now().isoformat()
        
        # Create vehicle entry
        vehicle_entry = {
            'title': enhanced_title,
            'year': year,
            'make': 'Honda',
            'model': 'Civic',
            'trim': extract_trim_from_title(title),
            'type': vehicle_type,
            'price': vehicle.get('price', 'Not available'),
            'found_date': found_date or 'Unknown',
            'dealership': dealership,
            'link': url or determine_search_link(title),
            'dealer_link': url
        }
        
        web_data['matches'].append(vehicle_entry)
    
    # Sort matches by found_date (newest first)
    web_data['matches'].sort(key=lambda x: x['found_date'], reverse=True)
    
    # Write to web data file
    with open('data.json', 'w') as f:
        json.dump(web_data, f, indent=2)
    
    print(f"✅ Converted {len(web_data['matches'])} vehicles to web format")
    print(f"📊 Statistics: {web_data['total_searches']} searches, {web_data['notifications_sent']} notifications")
    
    return web_data

def extract_trim_from_title(title):
    """Extract trim level from vehicle title"""
    title_lower = title.lower()
    
    if 'hybrid' in title_lower:
        return 'Hybrid'
    elif 'sport' in title_lower:
        return 'Sport'
    elif 'touring' in title_lower:
        return 'Touring'
    elif 'ex' in title_lower:
        return 'EX'
    elif 'lx' in title_lower:
        return 'LX'
    else:
        return 'Base'

def determine_search_link(title):
    """Determine appropriate search link based on vehicle title"""
    if 'hybrid' in title.lower():
        return f"{SEARCH_URL_NEW}?make=Honda&model=Civic%20Hybrid"
    else:
        return f"{SEARCH_URL_NEW}?make=Honda&model=Civic"

def create_sample_data():
    """Create sample data file for demo purposes"""
    sample_data = {
        'last_updated': datetime.now().isoformat(),
        'last_search': "2025-10-09T19:03:13.087245",
        'total_searches': 14,
        'vehicles_tracked': 3,
        'notifications_sent': 2,
        'matches': [
            {
                'title': "2024 Honda Civic Hybrid",
                'year': "2024",
                'make': "Honda", 
                'model': "Civic",
                'trim': "Hybrid",
                'type': "new",
                'price': "$28,500",
                'found_date': "2025-10-09T19:03:12.600085",
                'link': "https://www.autoparkhonda.com/new-inventory/index.htm?make=Honda&model=Civic%20Hybrid",
                'dealer_link': "https://www.autoparkhonda.com/VehicleDetails/new-2024-Honda-Civic-Hybrid-4dr_Sedan-Cary-NC/5438262784"
            },
            {
                'title': "2023 Honda Civic Sport",
                'year': "2023",
                'make': "Honda",
                'model': "Civic", 
                'trim': "Sport",
                'type': "used",
                'price': "$24,995",
                'mileage': "15,420",
                'found_date': "2025-10-09T18:33:08.951741",
                'link': "https://www.autoparkhonda.com/used-inventory/index.htm?make=Honda&model=Civic",
                'dealer_link': "https://www.autoparkhonda.com/VehicleDetails/used-2023-Honda-Civic-Sport-4dr_Sedan-Cary-NC/5441238791"
            }
        ]
    }
    
    with open('data.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print("📝 Created sample data file")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if len(sys.argv) > 1 and sys.argv[1] == '--sample':
        create_sample_data()
    else:
        convert_data_for_web()