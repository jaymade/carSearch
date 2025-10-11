#!/usr/bin/env python3
"""
Debug script to test Honda scraping functionality
"""

import sys
import os
import logging

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from scraper import HondaScraper

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_scraping():
    """Test both specific and broad scraping"""
    scraper = HondaScraper()
    
    print("🔍 Testing Honda Scraper")
    print("=" * 50)
    
    # Test 1: Original specific search
    print("\n1. Testing specific search (Civic, Sport trim, etc.):")
    specific_vehicles = scraper.search_vehicles()
    print(f"   Found {len(specific_vehicles)} specific matches")
    for vehicle in specific_vehicles[:3]:
        print(f"   - {vehicle.get('title', 'No title')}")
    
    # Test 2: Broader Honda search
    print("\n2. Testing broader Honda search:")
    broad_vehicles = scraper.search_all_honda_inventory()
    print(f"   Found {len(broad_vehicles)} Honda vehicles")
    for vehicle in broad_vehicles[:3]:
        print(f"   - {vehicle.get('title', 'No title')}")
    
    # Test 3: Check if website is reachable
    print("\n3. Testing website connectivity:")
    test_url = "https://www.autoparkhonda.com/"
    soup = scraper.get_page_content(test_url)
    if soup:
        title = soup.find('title')
        print(f"   ✅ Website reachable. Title: {title.get_text() if title else 'No title'}")
    else:
        print("   ❌ Website not reachable")
    
    return specific_vehicles, broad_vehicles

if __name__ == "__main__":
    specific, broad = test_scraping()
    
    print(f"\n📊 Summary:")
    print(f"   Specific search results: {len(specific)}")
    print(f"   Broad search results: {len(broad)}")
    
    if len(broad) > 0:
        print("   ✅ Scraper is working - found Honda vehicles")
        if len(specific) == 0:
            print("   ⚠️  No vehicles match your specific criteria (Civic Sport/Sport Touring, Black, Sedan)")
        else:
            print("   🎉 Found vehicles matching your criteria!")
    else:
        print("   ❌ Scraper may have issues - no vehicles found at all")