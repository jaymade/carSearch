#!/usr/bin/env python3
"""
Web Dashboard Updater - Call this from main.py after each search
"""

import os
import sys
import json
import subprocess
from datetime import datetime

def update_web_dashboard():
    """Update the web dashboard data after a search"""
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(project_root, 'docs')
    
    if not os.path.exists(docs_dir):
        print("📱 Web dashboard not set up yet")
        return
    
    try:
        # Run the data conversion script
        result = subprocess.run(
            ['python3', 'convert_data.py'],
            cwd=docs_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("📱 Web dashboard updated successfully")
            print(result.stdout.strip())
        else:
            print("❌ Failed to update web dashboard:")
            print(result.stderr.strip())
            
    except Exception as e:
        print(f"❌ Error updating web dashboard: {e}")

def update_dashboard_stats(search_stats):
    """Update dashboard with search statistics"""
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(project_root, 'docs', 'data.json')
    
    if not os.path.exists(data_file):
        return
    
    try:
        # Read current data
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Update statistics
        data['last_updated'] = datetime.now().isoformat()
        data['total_searches'] = search_stats.get('total_searches', data.get('total_searches', 0))
        data['vehicles_tracked'] = search_stats.get('vehicles_tracked', data.get('vehicles_tracked', 0))
        data['notifications_sent'] = search_stats.get('notifications_sent', data.get('notifications_sent', 0))
        data['last_search'] = search_stats.get('last_search', data.get('last_search', ''))
        
        # Write back
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)
            
        print("📊 Dashboard statistics updated")
        
    except Exception as e:
        print(f"❌ Error updating dashboard stats: {e}")

if __name__ == "__main__":
    update_web_dashboard()