#!/usr/bin/env python3
"""
Debug HTML structure to understand why we're only getting "Hybrid" as title
"""

import sys
import os
import requests
from bs4 import BeautifulSoup

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from config import SEARCH_URL_NEW, SEARCH_URL_USED, SEARCH_PARAMS

def debug_html_structure():
    """Debug the HTML structure to see what elements we're finding"""
    
    # Test with new inventory first
    url = f"{SEARCH_URL_NEW}?make=Honda&model=Civic"
    print(f"Fetching: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"Page title: {soup.title.text if soup.title else 'No title'}")
        
        # Look for specific Honda website patterns
        # Check if this is a search results page or if no results were found
        if "no vehicles match" in soup.get_text().lower() or "no results" in soup.get_text().lower():
            print("No vehicles found on this page")
            return
        
        # Look for vehicle cards/listings with various selectors
        possible_selectors = [
            '.vehicle-card',
            '.inventory-item', 
            '.vehicle-listing',
            '.search-result',
            '.vehicle',
            '[data-vehicle]',
            '.srp-list-item',
            '.vehicle-tile',
            '.ws-vehicle-tile',
            '.ws-inv-item',
            '[id*="vehicle"]',
            '[class*="vehicle"]',
            '[class*="inventory"]'
        ]
        
        found_vehicles = False
        for selector in possible_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"\nFound {len(elements)} elements with selector '{selector}'")
                found_vehicles = True
                for i, element in enumerate(elements[:2]):  # Show first 2
                    print(f"  Element {i+1}:")
                    text = element.get_text(strip=True)
                    print(f"    Text (first 300 chars): {text[:300]}...")
                    print(f"    Classes: {element.get('class', [])}")
                    
                    # Look for links in this element
                    links = element.find_all('a', href=True)
                    if links:
                        for j, link in enumerate(links[:3]):
                            print(f"    Link {j+1}: '{link.get_text(strip=True)[:50]}' -> {link.get('href')}")
                    
                    # Look for images
                    images = element.find_all('img')
                    if images:
                        for j, img in enumerate(images[:2]):
                            print(f"    Image {j+1}: alt='{img.get('alt', 'No alt')}' src='{img.get('src', 'No src')[:50]}...'")
                break
        
        if not found_vehicles:
            print("No vehicle elements found with common selectors")
        
        # Also look for any links that might contain vehicle info
        all_links = soup.find_all('a', href=True)
        vehicle_links = [link for link in all_links if 'vehicle' in link.get('href', '').lower() or 'details' in link.get('href', '').lower()]
        
        if vehicle_links:
            print(f"\nFound {len(vehicle_links)} potential vehicle links:")
            for i, link in enumerate(vehicle_links[:5]):
                print(f"  Link {i+1}: {link.get_text(strip=True)[:100]} -> {link.get('href')}")
        
        # Look for any element containing "Civic"
        civic_elements = soup.find_all(text=lambda text: text and 'civic' in text.lower())
        if civic_elements:
            print(f"\nFound {len(civic_elements)} elements containing 'civic':")
            for i, element in enumerate(civic_elements[:5]):
                parent = element.parent if hasattr(element, 'parent') else None
                print(f"  Text {i+1}: '{element.strip()}' (parent: {parent.name if parent else 'None'})")
                
    except Exception as e:
        print(f"Error fetching page: {e}")

if __name__ == "__main__":
    debug_html_structure()