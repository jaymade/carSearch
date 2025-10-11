# 🚗 Honda Car Search App - Script Cheat Sheet

## 📋 **MAIN APPLICATION FILES**

### `src/main.py` - **Primary Application** ⭐
```bash
python3 src/main.py --search-now    # Run manual search immediately  
python3 src/main.py --stats         # Show search statistics
python3 src/main.py --export-data   # Export search data to JSON
python3 src/main.py                 # Start automated scheduler (runs 3x daily)
python3 src/main.py --help          # Show all available options
```
**Purpose:** Main entry point for all Honda Civic search operations

---

### `src/scraper.py` - **Multi-Location Scraper Engine**
**Purpose:** Scrapes ALL Leith Honda locations + AutoPark Honda for Civics (new & used, 2015+)
- Searches 3 dealership locations simultaneously
- Extracts vehicle details, pricing, links with location info
- Filters by year (2015 and newer)
- Handles duplicate detection across all locations

---

### `src/web_updater.py` - **Web Dashboard Integration**  
**Purpose:** Updates web dashboard with search results
- Converts search data to web format
- Updates GitHub Pages dashboard
- Formats vehicle details for web display
- Manages data conversion pipeline

---

### `src/scheduler.py` - **Automated Search Scheduler**
**Purpose:** Runs searches automatically 3x daily (9AM, 1PM, 5PM)
- Business hours only (Mon-Fri)
- Prevents weekend/holiday searches
- Handles timezone management

---

### `src/data_manager.py` - **Data Persistence & History**
**Purpose:** Manages previous matches and search history
- Prevents duplicate notifications
- Tracks search statistics  
- JSON file storage
- Search performance analytics

---

### `src/config.py` - **Configuration Settings**
**Purpose:** Centralized app configuration
- Search parameters (make, model, year range)
- Dealership location configuration
- Scheduling configuration  
- URL endpoints for all Honda locations

---

## 🔧 **DIAGNOSTIC & UTILITY SCRIPTS**

### `diagnostics/debug_html.py` - **Website Structure Analysis** 🔍
```bash
python3 diagnostics/debug_html.py
```
**Purpose:** 
- Analyzes Honda website HTML structure
- Debugs scraping issues
- Finds vehicle data elements
- Tests different CSS selectors

---

### `diagnostics/debug_scraper.py` - **Scraper Testing** 🐛
```bash
python3 diagnostics/debug_scraper.py
```
**Purpose:** 
- Tests scraper functionality in isolation
- Verbose logging for debugging
- Vehicle data extraction testing
- Year filtering validation

---

### `diagnostics/email_notifier.py` - **Alternative Notification System** �
```bash
python3 diagnostics/email_notifier.py
```
**Purpose:** 
- Alternative email-based notification system
- Backup notification method
- HTML formatted vehicle details
- SMTP integration

---

## 📁 **CONFIGURATION FILES**

### `docs/` - **Web Dashboard Files** 🌐
```bash
docs/index.html     # GitHub Pages dashboard
docs/script.js      # Dashboard JavaScript  
docs/styles.css     # Dashboard styling
docs/convert_data.py# Data conversion utility
```
**Purpose:** Live web dashboard hosted on GitHub Pages

---

### `requirements.txt` - **Python Dependencies** 📦
```bash
pip3 install -r requirements.txt
```
**Purpose:** Installs all required Python packages

---

### `setup.sh` - **Initial Setup Script** ⚙️
```bash
chmod +x setup.sh && ./setup.sh
```
**Purpose:** One-command app setup and installation

---

## 📊 **DATA FILES**

### `previous_matches.json` - **Search History Database**
**Purpose:** 
- Stores found vehicles to prevent duplicates
- Search statistics and performance metrics
- Notification history tracking

---

### `search.log` - **Application Logs**
**Purpose:** 
- Detailed logging of all operations
- Error tracking and debugging
- Search result history

---

## 🚀 **QUICK START COMMANDS**

```bash
# 🔥 ESSENTIAL COMMANDS
python3 src/main.py --search-now     # Manual search
python3 src/main.py --stats          # Check status
python3 src/main.py --export-data    # Export search data

# ⚙️ SETUP & CONFIG  
./setup.sh                           # Initial setup
python3 docs/convert_data.py         # Update web dashboard manually

# 🔍 DEBUGGING
python3 diagnostics/debug_scraper.py # Test scraper
python3 diagnostics/debug_html.py    # Analyze website
```

---

## 🌐 **WEB DASHBOARD ACCESS**

**Live Dashboard:** `https://[your-username].github.io/honda-car-search/`
- Real-time inventory display
- Direct links to vehicle listings
- Search history and statistics
- Mobile-responsive design

---

## 📈 **CURRENT STATS**
- **Multi-location search** across 3 Honda dealerships
- **Automated scheduling** with 3 daily searches  
- **Web dashboard integration** with GitHub Pages
- **Status:** Fully operational with web-based tracking

---

*🎯 Your Honda Civic search app is **100% functional** with comprehensive web dashboard!*