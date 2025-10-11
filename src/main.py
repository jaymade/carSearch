#!/usr/bin/env python3
"""
Honda Car Search System

Automatically searches Honda dealership websites for specific Honda models
and tracks inventory matches with web dashboard display.
"""

import logging
import sys
import argparse
from datetime import datetime
from scraper import HondaScraper
from data_manager import DataManager
from scheduler import SearchScheduler
from config import LOG_FILE

# Set up logging
def setup_logging(log_level=logging.INFO):
    """Setup logging configuration"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def perform_search():
    """Perform a single search and track inventory matches"""
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        scraper = HondaScraper()
        data_manager = DataManager()
        
        logger.info("Starting Honda car search...")
        
        # Perform the search
        current_vehicles = scraper.search_vehicles()
        logger.info(f"Found {len(current_vehicles)} total vehicles")
        
        # Filter for new vehicles
        new_vehicles = data_manager.get_new_vehicles(current_vehicles)
        logger.info(f"Found {len(new_vehicles)} new vehicles")
        
        # Track new vehicles
        if new_vehicles:
            logger.info(f"Tracking {len(new_vehicles)} new vehicles")
            # Add new vehicles to tracking
            data_manager.add_vehicles(new_vehicles)
            logger.info("New vehicles added to tracking")
        else:
            logger.info("No new vehicles found")
        
        # Update statistics
        data_manager.update_search_stats(len(current_vehicles), len(new_vehicles) > 0, False)
        
        # Update web dashboard
        try:
            from web_updater import update_web_dashboard
            update_web_dashboard()
        except ImportError:
            pass  # Web dashboard not available
        except Exception as e:
            logger.warning(f"Failed to update web dashboard: {e}")
        
        # Clean up old data periodically
        data_manager.cleanup_old_matches(30)
        
        return len(new_vehicles)
        
    except Exception as e:
        logger.error(f"Error during search: {e}")
        return 0

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Honda Car Search System')
    parser.add_argument('--search-now', action='store_true', help='Perform a search right now')
    parser.add_argument('--stats', action='store_true', help='Show search statistics')
    parser.add_argument('--reset-data', action='store_true', help='Reset all stored data')
    parser.add_argument('--export-data', action='store_true', help='Export data to JSON file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("Honda Car Search Application Started")
    
    try:
        if args.search_now:
            # Perform immediate search
            logger.info("Performing manual search...")
            new_count = perform_search()
            print(f"Search completed. Found {new_count} new vehicles.")
            return
        
        elif args.stats:
            # Show statistics
            data_manager = DataManager()
            stats = data_manager.get_stats()
            
            print("\n📊 Honda Car Search Statistics")
            print("=" * 40)
            print(f"Total searches performed: {stats['total_searches']}")
            print(f"Total vehicles tracked: {stats['total_matches_tracked']}")
            print(f"Last search: {stats['last_search'] or 'Never'}")
            print(f"Data file size: {stats['data_file_size']} bytes")
            
            # Show recent matches
            recent_matches = data_manager.get_recent_matches(7)
            print(f"\n🚗 Recent matches (last 7 days): {len(recent_matches)}")
            for match in recent_matches[-5:]:  # Show last 5
                print(f"  - {match.get('title', 'Unknown')} ({match.get('first_seen', 'Unknown')})")
            
            return
        
        elif args.reset_data:
            # Reset all data
            data_manager = DataManager()
            data_manager.reset_data()
            print("✅ All data has been reset.")
            return
        
        elif args.export_data:
            # Export data
            data_manager = DataManager()
            filename = data_manager.export_data()
            if filename:
                print(f"✅ Data exported to: {filename}")
            else:
                print("❌ Failed to export data.")
            return
        
        else:
            # Start scheduled operation
            print("🚗 Honda Car Search System")
            print("=" * 50)
            print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("Monitoring Honda dealerships for new inventory matches...")
            print("Press Ctrl+C to stop")
            
            # Create scheduler with search function
            scheduler = SearchScheduler(perform_search)
            
            # Show next scheduled runs
            next_runs = scheduler.get_next_scheduled_runs()
            if next_runs:
                print(f"\nNext scheduled searches:")
                for run_time in next_runs[:5]:  # Show next 5
                    print(f"  📅 {run_time}")
            
            print("\n" + "=" * 50)
            
            # Start the scheduler
            scheduler.run_scheduler()
    
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        print("\n👋 Application stopped.")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())