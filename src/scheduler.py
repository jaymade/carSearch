import schedule
import time
import logging
from datetime import datetime
from typing import List
from config import SEARCH_TIMES, BUSINESS_HOURS

logger = logging.getLogger(__name__)

class SearchScheduler:
    def __init__(self, search_function):
        """
        Initialize scheduler with a search function to call
        
        Args:
            search_function: Function to call that performs the search and sends notifications
        """
        self.search_function = search_function
        self.setup_schedule()
    
    def setup_schedule(self):
        """Set up the scheduled searches"""
        logger.info("Setting up search schedule...")
        
        # Schedule searches at specified times during business days
        for search_time in SEARCH_TIMES:
            # Schedule for each business day
            if 0 in BUSINESS_HOURS['days']:  # Monday
                schedule.every().monday.at(search_time).do(self.run_scheduled_search)
            if 1 in BUSINESS_HOURS['days']:  # Tuesday
                schedule.every().tuesday.at(search_time).do(self.run_scheduled_search)
            if 2 in BUSINESS_HOURS['days']:  # Wednesday
                schedule.every().wednesday.at(search_time).do(self.run_scheduled_search)
            if 3 in BUSINESS_HOURS['days']:  # Thursday
                schedule.every().thursday.at(search_time).do(self.run_scheduled_search)
            if 4 in BUSINESS_HOURS['days']:  # Friday
                schedule.every().friday.at(search_time).do(self.run_scheduled_search)
            if 5 in BUSINESS_HOURS['days']:  # Saturday
                schedule.every().saturday.at(search_time).do(self.run_scheduled_search)
            if 6 in BUSINESS_HOURS['days']:  # Sunday
                schedule.every().sunday.at(search_time).do(self.run_scheduled_search)
        
        logger.info(f"Scheduled searches at {SEARCH_TIMES} on business days")
    
    def is_business_hours(self) -> bool:
        """Check if current time is within business hours"""
        now = datetime.now()
        current_hour = now.hour
        current_weekday = now.weekday()
        
        # Check if it's a business day
        if current_weekday not in BUSINESS_HOURS['days']:
            return False
        
        # Check if it's within business hours
        if current_hour < BUSINESS_HOURS['start'] or current_hour >= BUSINESS_HOURS['end']:
            return False
        
        return True
    
    def run_scheduled_search(self):
        """Run the scheduled search with business hours check"""
        try:
            # Double-check business hours (in case system time changed)
            if not self.is_business_hours():
                logger.info("Skipping search - outside business hours")
                return
            
            logger.info("Running scheduled Honda car search...")
            self.search_function()
            logger.info("Scheduled search completed")
            
        except Exception as e:
            logger.error(f"Error during scheduled search: {e}")
    
    def run_manual_search(self):
        """Run a manual search (ignores business hours)"""
        try:
            logger.info("Running manual Honda car search...")
            self.search_function()
            logger.info("Manual search completed")
        except Exception as e:
            logger.error(f"Error during manual search: {e}")
    
    def run_scheduler(self):
        """Start the scheduler loop"""
        logger.info("Starting Honda car search scheduler...")
        logger.info(f"Next scheduled runs:")
        
        # Show upcoming scheduled jobs
        for job in schedule.jobs:
            logger.info(f"  - {job}")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
    
    def get_next_scheduled_runs(self) -> List[str]:
        """Get list of next scheduled run times"""
        runs = []
        for job in schedule.jobs:
            next_run = job.next_run
            if next_run:
                runs.append(next_run.strftime('%m/%d/%Y %I:%M %p'))
        return sorted(runs)
    
    def clear_schedule(self):
        """Clear all scheduled jobs"""
        schedule.clear()
        logger.info("All scheduled jobs cleared")
    
    def add_one_time_search(self, delay_minutes: int = 0):
        """Add a one-time search after specified delay"""
        if delay_minutes > 0:
            schedule.every(delay_minutes).minutes.do(self.run_one_time_search).tag('one-time')
            logger.info(f"One-time search scheduled in {delay_minutes} minutes")
        else:
            self.run_manual_search()
    
    def run_one_time_search(self):
        """Run one-time search and remove the job"""
        self.run_manual_search()
        # Remove the one-time job
        schedule.clear('one-time')
        return schedule.CancelJob