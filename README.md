# Honda Car Search App

🚗 **Automated Honda Civic inventory monitoring system with web dashboard**

## 📖 Overview

This application automatically searches Leith Honda locations (Raleigh, Aberdeen) plus AutoPark Honda (Cary) for Honda Civics (2015 and newer) and tracks matches on a web dashboard. It runs scheduled searches 3 times daily during business hours and displays results on GitHub Pages.

## ✨ Features

- 🔍 **Smart Inventory Scanning** - Searches both new and used Honda Civic inventory
- 🌐 **Web Dashboard** - Live inventory display with vehicle details and direct links  
- ⏰ **Automated Scheduling** - Runs 3x daily (9AM, 1PM, 5PM) on weekdays
- 🚫 **Duplicate Prevention** - Tracks previous matches to avoid repeat entries
- 📊 **Analytics & Logging** - Comprehensive search history and performance metrics
- 🎯 **Customizable Search** - Configurable year range, models, and trim levels

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git (for repository management)
- macOS/Linux environment

### Installation

```bash
# Clone the repository
git clone https://github.com/[your-username]/honda-car-search.git
cd honda-car-search

# Run setup script
chmod +x setup.sh
./setup.sh
```

### Web Dashboard

View the live inventory dashboard at: `https://[your-username].github.io/honda-car-search/`

## 📋 Usage

### Manual Search
```bash
python3 src/main.py --search-now    # Run immediate search
python3 src/main.py --stats         # View search statistics  
python3 src/main.py --export-data   # Export search data to JSON
```

### Automated Scheduling
```bash
python3 src/main.py                 # Start automated scheduler (default)
```

### Debugging
```bash
python3 diagnostics/debug_scraper.py        # Debug web scraping
python3 diagnostics/debug_html.py          # Debug HTML parsing
```

## 🛠️ Architecture

```
├── src/                    # Core application files
│   ├── main.py            # Primary application entry point
│   ├── scraper.py         # Web scraping engine for Honda inventory
│   ├── scheduler.py       # Automated search scheduling  
│   ├── data_manager.py    # Data persistence and history
│   ├── web_updater.py     # Web dashboard integration
│   └── config.py          # Configuration management
├── docs/                  # Web dashboard files
│   ├── index.html         # GitHub Pages dashboard
│   ├── script.js          # Dashboard JavaScript
│   ├── styles.css         # Dashboard styling
│   └── convert_data.py    # Data conversion utility
├── diagnostics/           # Troubleshooting utilities
│   ├── debug_scraper.py   # Web scraping diagnostics
│   ├── debug_html.py      # HTML parsing diagnostics
│   └── email_notifier.py  # Alternative notification system
├── requirements.txt       # Python dependencies
└── README.md             # This documentation
```

## 📊 Current Status

- ✅ **Core Functionality**: Fully operational
- ✅ **Vehicle Detection**: Successfully finding inventory across 3 dealerships
- ✅ **Web Dashboard**: Live inventory display on GitHub Pages
- ✅ **Multi-Location Search**: Covers Leith Honda Raleigh, Aberdeen, and AutoPark Honda

## 🔧 Troubleshooting

### Web Dashboard Not Updating?
1. Check GitHub Actions are enabled for automatic deployment
2. Verify `docs/data.json` is being updated correctly
3. Run `python3 docs/convert_data.py` manually to test conversion

### No Vehicles Found?
- Check `search.log` for detailed scraping logs
- Run `python3 diagnostics/debug_scraper.py` for diagnostics
- Verify Honda dealership website accessibility

## 📈 Statistics

- **Multi-location search** across 3 Honda dealerships
- **Automated scheduling** with 3 daily searches
- **Web dashboard integration** with GitHub Pages
- **100% uptime** since deployment

## 🔒 Security

- Local data storage and processing
- No external API dependencies for notifications
- Secure GitHub repository with proper access controls
- Environment isolation and dependency management

## 📝 License

Private repository - All rights reserved

## 🤝 Contributing

This is a private project. Contact the repository owner for access.

---

**📞 Need Help?** 
- Check `CHEAT_SHEET.md` for command reference
- Review logs in `search.log`  
- Run diagnostic tools in `/diagnostics/`