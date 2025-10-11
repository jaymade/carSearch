import requests
from bs4 import BeautifulSoup
import logging
import re
from urllib.parse import urljoin, urlencode
from typing import List, Dict, Optional
from config import SEARCH_URL_NEW, SEARCH_URL_USED, SEARCH_PARAMS, MIN_YEAR, LEITH_HONDA_LOCATIONS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HondaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        })
    
    def search_all_honda_inventory(self) -> List[Dict]:
        """Search for any Honda vehicles (broader search for testing)"""
        vehicles = []
        
        # Search all Honda new inventory (no specific filters)
        search_url = "https://www.autoparkhonda.com/new-inventory/index.htm?make=Honda"
        
        soup = self.get_page_content(search_url)
        if not soup:
            logger.error("Failed to get page content for broad search")
            return vehicles
        
        # Look for any Honda vehicle links
        vehicle_links = soup.find_all('a', href=re.compile(r'/new/Honda/'))
        logger.info(f"Broad search found {len(vehicle_links)} Honda vehicle links")
        
        for link in vehicle_links[:10]:  # Limit to first 10 for testing
            try:
                text = link.get_text(strip=True)
                if text and len(text) > 5:  # Skip empty or very short links
                    vehicle_info = {
                        'title': text,
                        'url': urljoin(search_url, link.get('href', '')),
                        'source': 'broad_search'
                    }
                    vehicles.append(vehicle_info)
            except Exception as e:
                logger.debug(f"Error processing broad search link: {e}")
        
        return vehicles
    
    def build_search_url(self) -> str:
        """Build the search URL with parameters"""
        params = {}
        
        # Add basic search parameters
        params['make'] = SEARCH_PARAMS['make']
        
        # Add models (can be multiple)
        if isinstance(SEARCH_PARAMS['model'], list):
            for model in SEARCH_PARAMS['model']:
                params['model'] = model
        else:
            params['model'] = SEARCH_PARAMS['model']
        
        # Add trims (can be multiple)
        if isinstance(SEARCH_PARAMS['trim'], list):
            for trim in SEARCH_PARAMS['trim']:
                params['trim'] = trim
        else:
            params['trim'] = SEARCH_PARAMS['trim']
        
        # Add other parameters
        if 'normalExteriorColor' in SEARCH_PARAMS:
            params['normalExteriorColor'] = SEARCH_PARAMS['normalExteriorColor']
        if 'normalBodyStyle' in SEARCH_PARAMS:
            params['normalBodyStyle'] = SEARCH_PARAMS['normalBodyStyle']
        
        # Build the query string manually to handle multiple values with same key
        query_parts = []
        for key, value in params.items():
            if isinstance(value, list):
                for v in value:
                    query_parts.append(f"{key}={value}")
            else:
                query_parts.append(f"{key}={value}")
        
        query_string = "&".join(query_parts)
        return f"{SEARCH_URL_NEW}?{query_string}"
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse page content"""
        try:
            logger.info(f"Fetching page: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    def extract_vehicle_info(self, vehicle_element) -> Optional[Dict]:
        """Extract vehicle information from a vehicle listing element"""
        try:
            vehicle_info = {}
            
            # Get all text from the element for debugging
            element_text = vehicle_element.get_text(strip=True)
            logger.debug(f"Processing element with text: {element_text[:100]}...")
            
            # Look for any link that might be a vehicle link
            links = vehicle_element.find_all('a')
            vehicle_link = None
            
            for link in links:
                href = link.get('href', '')
                if '/new/Honda/' in href or 'Honda' in link.get_text():
                    vehicle_link = link
                    break
            
            if vehicle_link:
                vehicle_info['title'] = vehicle_link.get_text(strip=True)
                vehicle_info['url'] = vehicle_link.get('href')
                if vehicle_info['url'] and not vehicle_info['url'].startswith('http'):
                    vehicle_info['url'] = urljoin(SEARCH_URL_NEW, vehicle_info['url'])
            
            # If no vehicle link found, try to extract from text patterns
            if not vehicle_info.get('title'):
                # Look for year + Honda + model patterns
                text = vehicle_element.get_text()
                honda_match = re.search(r'(\d{4})\s+(Honda)\s+([\w\s]+)', text, re.I)
                if honda_match:
                    vehicle_info['title'] = f"{honda_match.group(1)} {honda_match.group(2)} {honda_match.group(3)}".strip()
                elif 'Honda' in text and 'Civic' in text:
                    vehicle_info['title'] = 'Honda Civic (Details in description)'
            
            # Extract price from anywhere in the element
            price_match = re.search(r'\$[\d,]+', element_text)
            if price_match:
                vehicle_info['price'] = price_match.group()
            
            # Extract VIN or stock number
            vin_match = re.search(r'/express/([A-Z0-9]+)', str(vehicle_element))
            if vin_match:
                vehicle_info['vin'] = vin_match.group(1)
            
            # Extract additional details from text
            if 'Sport' in element_text:
                vehicle_info['trim'] = 'Sport'
            if 'Hybrid' in element_text:
                vehicle_info['type'] = 'Hybrid'
            
            # Parse year, make, model if we have a title
            if vehicle_info.get('title'):
                title_parts = vehicle_info['title'].split()
                if len(title_parts) >= 2:
                    # Try to identify year (4 digits)
                    for part in title_parts:
                        if part.isdigit() and len(part) == 4:
                            vehicle_info['year'] = part
                            break
                    
                    # Identify make and model
                    if 'Honda' in vehicle_info['title']:
                        vehicle_info['make'] = 'Honda'
                        # Everything after Honda is likely the model
                        honda_index = next(i for i, part in enumerate(title_parts) if 'Honda' in part)
                        if honda_index + 1 < len(title_parts):
                            vehicle_info['model'] = ' '.join(title_parts[honda_index + 1:])
            
            # Only return if we have some meaningful information
            if vehicle_info.get('title') or vehicle_info.get('price') or vehicle_info.get('vin'):
                logger.debug(f"Extracted vehicle info: {vehicle_info}")
                return vehicle_info
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting vehicle info: {e}")
            return None
    
    def search_vehicles(self) -> List[Dict]:
        """Search for vehicles across all Leith Honda locations (new and used inventory)"""
        all_vehicles = []
        
        logger.info(f"🏢 Searching {len(LEITH_HONDA_LOCATIONS)} Leith Honda locations...")
        
        # Search each Leith Honda location
        for location_key, location_info in LEITH_HONDA_LOCATIONS.items():
            logger.info(f"🚗 Searching {location_info['name']} - {location_info['location']}")
            
            try:
                # Search new inventory for this location
                new_vehicles = self.search_location_inventory(location_info, "new")
                all_vehicles.extend(new_vehicles)
                
                # Search used inventory for this location  
                used_vehicles = self.search_location_inventory(location_info, "used")
                all_vehicles.extend(used_vehicles)
                
                logger.info(f"✅ Found {len(new_vehicles)} new + {len(used_vehicles)} used vehicles at {location_info['name']}")
                
            except Exception as e:
                logger.error(f"❌ Error searching {location_info['name']}: {e}")
                continue
        
        # Filter by year (2015 and newer)
        filtered_vehicles = []
        for vehicle in all_vehicles:
            year = self.extract_year_from_vehicle(vehicle)
            if year and year >= MIN_YEAR:
                filtered_vehicles.append(vehicle)
                logger.info(f"✅ Vehicle {vehicle.get('title')} ({year}) meets year criteria")
            elif year:
                logger.info(f"⏰ Vehicle {vehicle.get('title')} ({year}) too old (need 2015+), skipping")
            else:
                # If no year found, include it anyway (might be new)
                logger.info(f"❓ Vehicle {vehicle.get('title')} (year unknown) - including anyway")
                filtered_vehicles.append(vehicle)
        
        logger.info(f"Found {len(filtered_vehicles)} vehicles matching criteria across all locations")
        return filtered_vehicles
    
    def search_location_inventory(self, location_info: Dict, inventory_type: str) -> List[Dict]:
        """Search specific location's inventory (new or used)"""
        vehicles = []
        
        # Get the appropriate URL for this location and inventory type
        url_key = 'new_url' if inventory_type == 'new' else 'used_url'
        base_url = location_info.get(url_key)
        
        if not base_url:
            logger.warning(f"No {inventory_type} URL found for {location_info['name']}")
            return vehicles
        
        # Build search URLs for Honda Civic models
        search_urls = [
            f"{base_url}?make=Honda&model=Civic",
            f"{base_url}?make=Honda&model=Civic%20Hybrid"
        ]
        
        for search_url in search_urls:
            logger.info(f"Fetching {inventory_type} inventory: {search_url}")
            
            try:
                soup = self.get_page_content(search_url)
                if not soup:
                    logger.warning(f"Failed to get content from {search_url}")
                    continue
                
                # Extract vehicles from this page
                page_vehicles = self.extract_vehicles_from_page(soup, search_url)
                
                # Add location info to each vehicle
                for vehicle in page_vehicles:
                    vehicle['dealership'] = location_info['name']
                    vehicle['location'] = location_info['location']
                    vehicle['inventory_type'] = inventory_type
                
                vehicles.extend(page_vehicles)
                logger.info(f"Found {len(page_vehicles)} vehicles on page")
                
            except Exception as e:
                logger.error(f"Error processing {search_url}: {e}")
                continue
        
        return vehicles
    
    def extract_year_from_vehicle(self, vehicle: Dict) -> int:
        """Extract year from vehicle data"""
        # Try to get year from parsed data
        if 'year' in vehicle:
            try:
                year = int(vehicle['year'])
                logger.debug(f"Extracted year {year} from vehicle year field")
                return year
            except (ValueError, TypeError):
                pass
        
        # Try to extract from title
        if 'title' in vehicle:
            title = vehicle['title']
            logger.debug(f"Extracting year from title: {title}")
            # Look for 4-digit year (2000-2029)
            year_match = re.search(r'\b(20[0-2]\d)\b', title)
            if year_match:
                try:
                    year = int(year_match.group(1))
                    logger.debug(f"Extracted year {year} from title")
                    return year
                except ValueError:
                    pass
        
        # Try to extract from URL
        if 'url' in vehicle:
            url = vehicle['url']
            year_match = re.search(r'/(20[0-2]\d)-', url)
            if year_match:
                try:
                    year = int(year_match.group(1))
                    logger.debug(f"Extracted year {year} from URL")
                    return year
                except ValueError:
                    pass
        
        logger.debug(f"No year found for vehicle: {vehicle.get('title', 'Unknown')}")
        return None
    
    def search_inventory_type(self, inventory_type: str) -> List[Dict]:
        """Search specific inventory type (new or used)"""
        vehicles = []
        
        # Build search URLs for different inventory types
        if inventory_type == "new":
            # Search new inventory with expanded criteria
            search_urls = [
                f"{SEARCH_URL_NEW}?make=Honda&model=Civic",
                f"{SEARCH_URL_NEW}?make=Honda&model=Civic%20Hybrid"
            ]
        else:
            # Search used inventory
            search_urls = [
                f"{SEARCH_URL_USED}?make=Honda&model=Civic",
                f"{SEARCH_URL_USED}?make=Honda&model=Civic%20Hybrid"
            ]
        
        for search_url in search_urls:
            logger.info(f"Searching {inventory_type} inventory: {search_url}")
            
            soup = self.get_page_content(search_url)
            if not soup:
                logger.error(f"Failed to get page content for {search_url}")
                continue
            
            # Use the same vehicle extraction logic but for each URL
            page_vehicles = self.extract_vehicles_from_page(soup, search_url)
            vehicles.extend(page_vehicles)
            
        logger.info(f"Found {len(vehicles)} {inventory_type} vehicles")
        return vehicles
    
    def extract_vehicle_info_from_url(self, url: str) -> Dict:
        """Extract vehicle information from URL parameters"""
        from urllib.parse import urlparse, parse_qs
        
        vehicle_info = {}
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        # Extract year from URL path or parameters
        year_match = re.search(r'(20\d{2})', url)
        if year_match:
            vehicle_info['year'] = year_match.group(1)
        
        # Extract make, model, and trim from parameters
        if 'make' in params:
            vehicle_info['make'] = params['make'][0] if params['make'] else 'Honda'
        else:
            vehicle_info['make'] = 'Honda'  # Default for Honda dealerships
            
        if 'model' in params:
            models = params['model']
            # Handle multiple model parameters (like Civic Hybrid and Civic)
            for model in models:
                if 'civic' in model.lower():
                    vehicle_info['model'] = model
                    break
            if 'model' not in vehicle_info and models:
                vehicle_info['model'] = models[0]
        
        if 'trim' in params:
            trims = params['trim']
            if trims:
                vehicle_info['trim'] = ', '.join(trims)
        
        # Extract color if available
        if 'normalExteriorColor' in params:
            vehicle_info['color'] = params['normalExteriorColor'][0]
        elif 'color' in params:
            vehicle_info['color'] = params['color'][0]
            
        # Extract body style
        if 'normalBodyStyle' in params:
            vehicle_info['body_style'] = params['normalBodyStyle'][0]
        elif 'bodyStyle' in params:
            vehicle_info['body_style'] = params['bodyStyle'][0]
        
        return vehicle_info

    def create_vehicle_title(self, vehicle_info: Dict, text_title: str = None) -> str:
        """Create a meaningful vehicle title from extracted information"""
        parts = []
        
        # Add year if available
        if 'year' in vehicle_info:
            parts.append(vehicle_info['year'])
        
        # Add make
        if 'make' in vehicle_info:
            parts.append(vehicle_info['make'])
        
        # Add model
        if 'model' in vehicle_info:
            parts.append(vehicle_info['model'])
        elif text_title and text_title.strip() and text_title.strip() != 'Hybrid':
            parts.append(text_title.strip())
        
        # Add trim if available
        if 'trim' in vehicle_info:
            parts.append(f"({vehicle_info['trim']})")
        
        # Add color if available
        if 'color' in vehicle_info:
            parts.append(f"in {vehicle_info['color']}")
            
        # Fallback if no meaningful info extracted
        if not parts:
            if text_title and text_title.strip():
                return text_title.strip()
            return "Honda Civic"
        
        return ' '.join(parts)

    def extract_vehicles_from_page(self, soup, base_url: str) -> List[Dict]:
        """Extract vehicle information from a single page"""
        vehicles = []
        
        # Debug: Check if page has content
        page_text = soup.get_text().lower()
        logger.debug(f"Page contains 'civic': {'civic' in page_text}")
        logger.debug(f"Page contains 'honda': {'honda' in page_text}")
        
        # Try multiple approaches to find vehicles
        
        # Approach 1: Look for vehicle links directly (both new and used)
        vehicle_patterns = [
            r'/new/Honda/.*Civic',
            r'/used/Honda/.*Civic',
            r'/inventory/.*Honda.*Civic',
            r'\?.*model.*[Cc]ivic'  # URLs with civic in parameters
        ]
        
        for pattern in vehicle_patterns:
            vehicle_links = soup.find_all('a', href=re.compile(pattern, re.I))
            logger.debug(f"Pattern '{pattern}' found {len(vehicle_links)} vehicle links")
            
            for link in vehicle_links:
                try:
                    link_url = urljoin(base_url, link.get('href', ''))
                    text_title = link.get_text(strip=True)
                    
                    # Extract vehicle info from URL parameters
                    url_info = self.extract_vehicle_info_from_url(link_url)
                    
                    # Create a meaningful title
                    meaningful_title = self.create_vehicle_title(url_info, text_title)
                    
                    vehicle_info = {
                        'title': meaningful_title,
                        'url': link_url,
                        **url_info  # Include all extracted info
                    }
                    
                    # Look for price in nearby elements
                    parent = link.find_parent(['div', 'section', 'article', 'li'])
                    if parent:
                        price_text = parent.get_text()
                        price_match = re.search(r'\$[\d,]+', price_text)
                        if price_match:
                            vehicle_info['price'] = price_match.group()
                    
                    vehicles.append(vehicle_info)
                    logger.debug(f"Found vehicle: {vehicle_info['title']}")
                except Exception as e:
                    logger.debug(f"Error processing vehicle link: {e}")
        
        # Approach 2: Look for inventory page links that might contain vehicle data
        if not vehicles:
            # Look for links to inventory pages with Honda Civic parameters
            inventory_links = soup.find_all('a', href=re.compile(r'inventory.*honda|honda.*inventory', re.I))
            logger.debug(f"Found {len(inventory_links)} inventory links")
            
            for link in inventory_links:
                try:
                    link_url = urljoin(base_url, link.get('href', ''))
                    if 'civic' in link_url.lower():
                        url_info = self.extract_vehicle_info_from_url(link_url)
                        meaningful_title = self.create_vehicle_title(url_info, link.get_text(strip=True))
                        
                        vehicle_info = {
                            'title': meaningful_title,
                            'url': link_url,
                            **url_info
                        }
                        vehicles.append(vehicle_info)
                        logger.debug(f"Found inventory vehicle: {meaningful_title}")
                except Exception as e:
                    logger.debug(f"Error processing inventory link: {e}")
        
        # Approach 3: Look for text patterns that indicate vehicles
        if not vehicles:
            # Look for Honda Civic text patterns with years
            civic_patterns = [
                r'(20\d{2})\s+Honda\s+Civic[^<]*',
                r'Honda\s+Civic[^<]*',
                r'Civic\s+(Hybrid|Sport|EX|LX)[^<]*'
            ]
            
            for pattern in civic_patterns:
                matches = re.findall(pattern, soup.get_text(), re.I)
                for match in matches:
                    title_text = match if isinstance(match, str) else ' '.join(match)
                    vehicle_info = {
                        'title': title_text,
                        'url': base_url,  # Fallback URL
                    }
                    vehicles.append(vehicle_info)
                    logger.debug(f"Found vehicle by pattern: {vehicle_info['title']}")
        
        # Approach 4: Try broader Honda search
        if not vehicles:
            logger.debug("Trying broader search approach...")
            
            # Try to find any links with Honda and Civic in them
            honda_links = soup.find_all('a', text=re.compile(r'Honda.*Civic|Civic.*Honda', re.I))
            logger.debug(f"Found {len(honda_links)} Honda Civic links")
            
            for link in honda_links:
                text = link.get_text(strip=True)
                link_url = urljoin(base_url, link.get('href', ''))
                url_info = self.extract_vehicle_info_from_url(link_url)
                meaningful_title = self.create_vehicle_title(url_info, text)
                
                vehicle_info = {
                    'title': meaningful_title,
                    'url': link_url,
                    **url_info
                }
                vehicles.append(vehicle_info)
                logger.debug(f"Found Honda vehicle: {meaningful_title}")
        
        # Remove duplicates based on URL or title
        unique_vehicles = []
        seen_identifiers = set()
        
        for vehicle in vehicles:
            identifier = vehicle.get('url') or vehicle.get('title')
            if identifier and identifier not in seen_identifiers:
                seen_identifiers.add(identifier)
                unique_vehicles.append(vehicle)
        
        logger.debug(f"Found {len(unique_vehicles)} unique vehicles on this page")
        return unique_vehicles
    
    def get_vehicle_details(self, vehicle_url: str) -> Optional[Dict]:
        """Get detailed information about a specific vehicle"""
        soup = self.get_page_content(vehicle_url)
        if not soup:
            return None
        
        details = {}
        
        try:
            # Extract more detailed information from the vehicle detail page
            # This would include specifications, features, etc.
            
            # Extract price
            price_elem = soup.find(text=re.compile(r'MSRP|Price'))
            if price_elem:
                price_parent = price_elem.parent
                price_text = price_parent.get_text() if price_parent else ""
                price_match = re.search(r'\$[\d,]+', price_text)
                if price_match:
                    details['price'] = price_match.group()
            
            # Extract specifications
            spec_elements = soup.find_all(['dt', 'dd', 'li'], text=re.compile(r'Engine|Transmission|MPG|Color', re.I))
            for elem in spec_elements:
                text = elem.get_text(strip=True)
                if ':' in text:
                    key, value = text.split(':', 1)
                    details[key.strip().lower()] = value.strip()
            
            return details
            
        except Exception as e:
            logger.error(f"Error extracting vehicle details: {e}")
            return None