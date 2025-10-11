# 🌐 Web Dashboard Setup Guide

Your Honda Car Search app now includes a beautiful web dashboard! Here's how to set it up on GitHub Pages.

## 📋 What You'll Get

- **🔍 Search Criteria Display** - Shows current search parameters (Honda Civic, 2015+, new/used)
- **📊 Live Statistics** - Total searches, vehicles found, notifications sent
- **🚗 Vehicle Results** - Dynamic list of found vehicles with direct links to dealer pages
- **📱 Mobile Responsive** - Works perfectly on phones, tablets, and desktop
- **🔄 Auto-Refresh** - Updates every 5 minutes automatically
- **🎨 Modern Design** - Professional, clean interface with Honda-themed styling

## 🚀 GitHub Pages Setup (5 minutes)

### Step 1: Push to GitHub
Your code is already committed locally. Push it to GitHub:

```bash
git push origin main
```

### Step 2: Enable GitHub Pages
1. Go to your GitHub repository settings
2. Scroll down to **"Pages"** in the left sidebar
3. Under **"Source"**, select **"Deploy from a branch"**
4. Choose **"main"** branch and **"/docs"** folder
5. Click **"Save"**

### Step 3: Access Your Dashboard
Your web dashboard will be available at:
```
https://[your-username].github.io/[repository-name]/
```

Example: `https://jayrich.github.io/honda-car-search/`

## 🔄 How It Works

### Automatic Updates
- **GitHub Actions** automatically updates the web data every hour during business hours
- **Main App Integration** updates the dashboard after each search
- **Real-time Refresh** keeps the page current when viewed

### Data Flow
1. Your app finds vehicles → Updates `previous_matches.json`
2. `web_updater.py` converts data → Creates `docs/data.json`
3. Web dashboard reads `data.json` → Shows latest results
4. GitHub Actions keeps everything synced

## 📁 Web Dashboard Files

```
docs/
├── index.html          # Main web page
├── styles.css          # Modern styling
├── script.js           # Interactive functionality
├── convert_data.py     # Data conversion script
└── data.json          # Current vehicle data (auto-generated)
```

## 🛠️ Manual Updates

### Update Web Data Manually
```bash
cd docs
python3 convert_data.py
```

### Test Locally
```bash
cd docs
python3 -m http.server 8000
# Visit: http://localhost:8000
```

### Force Refresh Dashboard
The web page includes a "Refresh" button for manual updates, plus auto-refresh every 5 minutes.

## 🎯 Features

### Search Criteria Section
- **Make & Model:** Honda Civic & Civic Hybrid
- **Year Range:** 2015 - 2025 (10+ years)
- **Inventory:** New & Used Vehicles
- **Dealership:** AutoPark Honda (Cary, NC)
- **Frequency:** 3x Daily (9AM, 1PM, 5PM)
- **Notification:** SMS to your phone

### Statistics Dashboard
- Total searches performed
- Total vehicles found and tracked
- SMS notifications sent
- Last search timestamp

### Vehicle Results
- **Dynamic Cards** for each found vehicle
- **Direct Links** to dealer inventory pages
- **Vehicle Details** (year, type, price, mileage)
- **Found Timestamp** showing when discovered
- **New/Used Badges** for easy identification

### System Status
- ✅ App Functional
- ✅ Web Scraping Active  
- ✅ Scheduling Operational
- ⚠️ SMS Status (carrier blocking info)

## 🔧 Customization

### Update Search Criteria Display
Edit the criteria in `docs/index.html` around line 30-55.

### Modify Styling
Edit `docs/styles.css` - includes responsive design and Honda-themed colors.

### Add Features
Edit `docs/script.js` for additional functionality like filters, sorting, etc.

## 🚨 Troubleshooting

### Web Dashboard Not Updating?
1. Check GitHub Actions are enabled in your repository settings
2. Verify the workflow file exists: `.github/workflows/update-dashboard.yml`
3. Check Actions tab for any errors

### Page Not Loading?
1. Ensure GitHub Pages is enabled for `/docs` folder
2. Check repository is public (or you have GitHub Pro for private repos)
3. Wait 5-10 minutes after enabling Pages

### Data Not Showing?
1. Run `python3 docs/convert_data.py` manually
2. Check `docs/data.json` exists and has content
3. Verify browser console for JavaScript errors

## 📱 Mobile Experience

The dashboard is fully responsive and includes:
- **Touch-friendly** buttons and links
- **Optimized layouts** for phone screens
- **Fast loading** with minimal data usage
- **Direct calling** links (when viewing dealer contacts)

## 🎉 Success!

Once set up, you'll have:
- **Professional web dashboard** at your GitHub Pages URL
- **Real-time vehicle tracking** with live updates
- **Mobile-accessible** interface you can check anywhere
- **Automated data sync** with your search app

Your Honda car search just got a major upgrade! 🚗✨