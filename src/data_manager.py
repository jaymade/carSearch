import json
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Set
from config import DATA_FILE

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self):
        self.data_file = DATA_FILE
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load previous search data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Loaded data from {self.data_file}")
                    return data
            else:
                logger.info(f"No existing data file found, starting fresh")
                return {
                    'previous_matches': [],
                    'last_search': None,
                    'total_searches': 0,
                    'notifications_sent': 0
                }
        except Exception as e:
            logger.error(f"Error loading data file: {e}")
            return {
                'previous_matches': [],
                'last_search': None,
                'total_searches': 0,
                'notifications_sent': 0
            }
    
    def save_data(self) -> bool:
        """Save current data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
            logger.info(f"Data saved to {self.data_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving data file: {e}")
            return False
    
    def generate_vehicle_id(self, vehicle: Dict) -> str:
        """Generate unique identifier for a vehicle"""
        # Use VIN if available, otherwise use combination of other fields
        if 'vin' in vehicle and vehicle['vin']:
            return f"vin_{vehicle['vin']}"
        
        # Fallback to URL-based ID
        if 'url' in vehicle and vehicle['url']:
            # Extract vehicle ID from URL if possible
            url_parts = vehicle['url'].split('/')
            if len(url_parts) > 2:
                return f"url_{url_parts[-1]}"
        
        # Last resort: use title and price
        title = vehicle.get('title', 'unknown')
        price = vehicle.get('price', 'unknown')
        return f"title_{hash(f'{title}_{price}')}"
    
    def is_duplicate(self, vehicle: Dict) -> bool:
        """Check if vehicle has been seen before"""
        vehicle_id = self.generate_vehicle_id(vehicle)
        
        for previous_vehicle in self.data['previous_matches']:
            if previous_vehicle.get('id') == vehicle_id:
                return True
        
        return False
    
    def get_new_vehicles(self, current_vehicles: List[Dict]) -> List[Dict]:
        """Filter out vehicles that have been seen before"""
        new_vehicles = []
        
        for vehicle in current_vehicles:
            if not self.is_duplicate(vehicle):
                # Add timestamp and ID
                vehicle['id'] = self.generate_vehicle_id(vehicle)
                vehicle['first_seen'] = datetime.now().isoformat()
                new_vehicles.append(vehicle)
        
        return new_vehicles
    
    def add_vehicles(self, vehicles: List[Dict]):
        """Add new vehicles to the previous matches"""
        for vehicle in vehicles:
            if 'id' not in vehicle:
                vehicle['id'] = self.generate_vehicle_id(vehicle)
            if 'first_seen' not in vehicle:
                vehicle['first_seen'] = datetime.now().isoformat()
        
        self.data['previous_matches'].extend(vehicles)
        self.save_data()
    
    def update_search_stats(self, vehicles_found: int, notifications_sent: bool = False, no_matches_notification_sent: bool = False):
        """Update search statistics"""
        self.data['last_search'] = datetime.now().isoformat()
        self.data['total_searches'] += 1
        
        if notifications_sent:
            self.data['notifications_sent'] += 1
            
        if no_matches_notification_sent:
            self.data['last_no_matches_notification'] = datetime.now().isoformat()
            if 'no_matches_notifications_sent' not in self.data:
                self.data['no_matches_notifications_sent'] = 0
            self.data['no_matches_notifications_sent'] += 1
        
        # Add search log entry
        if 'search_history' not in self.data:
            self.data['search_history'] = []
        
        self.data['search_history'].append({
            'timestamp': datetime.now().isoformat(),
            'vehicles_found': vehicles_found,
            'notifications_sent': notifications_sent,
            'no_matches_notification_sent': no_matches_notification_sent
        })
        
        # Keep only last 100 search history entries
        if len(self.data['search_history']) > 100:
            self.data['search_history'] = self.data['search_history'][-100:]
        
        self.save_data()
    
    def cleanup_old_matches(self, days_to_keep: int = 30):
        """Remove matches older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        original_count = len(self.data['previous_matches'])
        
        self.data['previous_matches'] = [
            match for match in self.data['previous_matches']
            if 'first_seen' in match and 
            datetime.fromisoformat(match['first_seen']) > cutoff_date
        ]
        
        removed_count = original_count - len(self.data['previous_matches'])
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old matches (older than {days_to_keep} days)")
            self.save_data()
    
    def should_send_no_matches_notification(self, frequency: str = 'daily') -> bool:
        """Check if we should send a no matches notification based on frequency setting"""
        if frequency == 'never':
            return False
        elif frequency == 'always':
            return True
        
        last_notification = self.data.get('last_no_matches_notification')
        if not last_notification:
            return True  # Never sent before
        
        try:
            last_notification_date = datetime.fromisoformat(last_notification)
            now = datetime.now()
            
            if frequency == 'daily':
                # Send once per day
                return (now - last_notification_date).days >= 1
            elif frequency == 'weekly':
                # Send once per week
                return (now - last_notification_date).days >= 7
            
        except ValueError:
            return True  # If we can't parse the date, send notification
        
        return False

    def get_stats(self) -> Dict:
        """Get summary statistics"""
        return {
            'total_matches_tracked': len(self.data['previous_matches']),
            'total_searches': self.data.get('total_searches', 0),
            'notifications_sent': self.data.get('notifications_sent', 0),
            'no_matches_notifications_sent': self.data.get('no_matches_notifications_sent', 0),
            'last_search': self.data.get('last_search'),
            'last_no_matches_notification': self.data.get('last_no_matches_notification'),
            'data_file_size': os.path.getsize(self.data_file) if os.path.exists(self.data_file) else 0
        }
    
    def get_recent_matches(self, days: int = 7) -> List[Dict]:
        """Get matches from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_matches = []
        for match in self.data['previous_matches']:
            if 'first_seen' in match:
                try:
                    seen_date = datetime.fromisoformat(match['first_seen'])
                    if seen_date > cutoff_date:
                        recent_matches.append(match)
                except ValueError:
                    continue
        
        return recent_matches
    
    def export_data(self, filename: str = None) -> str:
        """Export all data to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"honda_search_export_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
            
            logger.info(f"Data exported to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return None
    
    def reset_data(self):
        """Reset all data (useful for testing)"""
        self.data = {
            'previous_matches': [],
            'last_search': None,
            'total_searches': 0,
            'notifications_sent': 0,
            'search_history': []
        }
        self.save_data()
        logger.info("All data has been reset")