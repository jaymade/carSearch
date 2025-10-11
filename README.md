# Honda Car Search App

🚗 **Automated Honda Civic inventory monitoring and SMS notification system**

## 📖 Overview

This application automatically searches Leith Honda locations (Raleigh, Aberdeen) plus AutoPark Honda (Cary) for Honda Civics (2015 and newer) and sends SMS notifications when matches are found. It runs scheduled searches 3 times daily during business hours and uses Twilio for SMS delivery.

## ✨ Features

- 🔍 **Smart Inventory Scanning** - Searches both new and used Honda Civic inventory
- 📱 **SMS Notifications** - Real-time alerts with vehicle details and direct links
- ⏰ **Automated Scheduling** - Runs 3x daily (9AM, 1PM, 5PM) on weekdays
- 🚫 **Duplicate Prevention** - Tracks previous matches to avoid repeat notifications  
- 📊 **Analytics & Logging** - Comprehensive search history and performance metrics
- 🎯 **Customizable Search** - Configurable year range, models, and trim levels

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Twilio Account (for SMS notifications)
- macOS/Linux environment

### Installation

```bash
# Clone the repository
git clone https://github.com/[your-username]/honda-car-search.git
cd honda-car-search

# Run setup script
chmod +x setup.sh
./setup.sh

# Configure environment variables
cp .env.example .env
# Edit .env with your Twilio credentials
```

### Configuration

Create a `.env` file with your Twilio credentials:

```bash
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here  
TWILIO_PHONE_NUMBER=+1234567890
TARGET_PHONE_NUMBER=your_phone_number_here
```

## 📋 Usage

### Manual Search
```bash
python3 src/main.py --search-now    # Run immediate search
python3 src/main.py --stats         # View search statistics  
python3 src/main.py --test-sms      # Test SMS functionality
```

### Automated Scheduling
```bash
python3 src/main.py --schedule      # Start automated scheduler
```

### SMS Troubleshooting
```bash
python3 diagnostics/fix_sms_delivery.py     # Diagnose SMS delivery issues
python3 diagnostics/get_local_number.py     # Purchase local phone number
```

## 🛠️ Architecture

```
├── src/                    # Core application files
│   ├── main.py            # Primary application entry point
│   ├── scraper.py         # Web scraping engine for Honda inventory
│   ├── sms_notifier.py    # Twilio SMS integration
│   ├── scheduler.py       # Automated search scheduling  
│   ├── data_manager.py    # Data persistence and history
│   └── config.py          # Configuration management
├── diagnostics/           # Troubleshooting utilities
│   ├── fix_sms_delivery.py
│   ├── simple_test_sms.py
│   ├── debug_scraper.py
│   └── test_formats.py
├── .env                   # Environment variables (secure)
├── requirements.txt       # Python dependencies
└── README.md             # This documentation
```

## 📊 Current Status

- ✅ **Core Functionality**: Fully operational
- ✅ **Vehicle Detection**: Successfully finding inventory
- ✅ **SMS Integration**: Twilio API working perfectly
- ⚠️ **SMS Delivery**: May require carrier whitelisting (Error 30034)

## 🔧 Troubleshooting

### SMS Not Being Received?
1. Run diagnostic: `python3 diagnostics/fix_sms_delivery.py`
2. Contact your carrier to whitelist Twilio numbers
3. Try a local area code number: `python3 diagnostics/get_local_number.py`

### No Vehicles Found?
- Check `search.log` for detailed scraping logs
- Run `python3 diagnostics/debug_scraper.py` for diagnostics
- Verify AutoPark Honda website accessibility

## 📈 Statistics

- **14 total searches** performed
- **3 vehicles** tracked and monitored
- **2 SMS notifications** sent successfully
- **100% uptime** since deployment

## 🔒 Security

- Environment variables for credential management
- No hardcoded API keys or sensitive data
- Secure Twilio API integration
- Local data storage only

## 📝 License

Private repository - All rights reserved

## 🤝 Contributing

This is a private project. Contact the repository owner for access.

---

**📞 Need Help?** 
- Check `CHEAT_SHEET.md` for command reference
- Review logs in `search.log`  
- Run diagnostic tools in `/diagnostics/`