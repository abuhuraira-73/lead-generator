# 🗺️ Google Maps Lead Generator - Pan India Edition

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

A powerful business lead generator for Indian markets. This tool now exclusively extracts **legitimate, real-time business data** directly from Google Maps based on your search queries. All previously simulated or "dummy" data generation features have been removed to ensure the integrity and accuracy of the collected leads.

## 🚀 Key Features

### 📊 **Multi-Format Export System**
- **CSV** - Excel & Google Sheets compatible with UTF-8 encoding
- **JSON** - Developer-friendly with metadata
- **TSV** - Database-ready tab-separated format  

### 🌍 **Real-Time Data Collection**
- Scrapes live business data from Google Maps
- Collects Name, Phone, Address, Rating, and Website
- Generates direct Google Maps links for each business

### ⚡ **Dependencies**
- Uses Python with `requests`, `beautifulsoup4`, `selenium`, and `webdriver_manager` for robust scraping.
- Works on all macOS versions.

## 📦 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/abuhuraira-73/lead-generator.git
cd lead-generator

# Install dependencies
pip install -r requirements.txt

# Make executable (optional)
chmod +x cli_scraper.py

# Run the lead generator
python3 cli_scraper.py
```

### Basic Usage

```bash

python3 cli_scraper.py

```



1. Select a category number from the menu (e.g., `2` for "Cafes").

2. Enter the location for your search (e.g., `New York`).

3. Choose number of results (1-50 or 'MAX' for all).

4. Choose an export format.

5. Your leads are ready!



Alternatively, you can type a full custom query like `hardware stores in Brooklyn` at the first prompt.



## 🇮🇳 Guided Search for India

For targeted searches within India, you can use the guided menu.

1.  **Start the script and choose `[1] Search within India`.**
2.  You will be asked to either scan all major cities or select a specific state.
3.  If you select a state, you can then choose to either scan all major cities within that state or select a specific city.
4.  Finally, you will be prompted to enter your search term (e.g., "Hospitals", "Restaurants").

This allows you to control the scope of your search from a single city to an entire state, or a broad scan across the country. The option to `[2] Search anywhere else in the world` remains available for all other queries.

## 📖 Quick Searches with Predefined Categories



To make searching easier, you can start by picking one of the following predefined categories:



--- **Food & Drink** ---

  - [1] Restaurants

  - [2] Cafes

  - [3] Bars

  - [4] Coffee Shops

  - [5] Bakeries

  - [6] Takeout

  - [7] Delivery



--- **Health & Wellness** ---

  - [8] Doctors

  - [9] Hospitals

  - [10] Clinics

  - [11] Dentists

  - [12] Pharmacies

  - [13] Gyms

  - [14] Spas



--- **Shopping** ---

  - [15] Supermarkets

  - [16] Grocery Stores

  - [17] Shopping Malls

  - [18] Clothing Stores

  - [19] Book Stores



--- **Services** ---

  - [20] Hotels

  - [21] Banks

  - [22] ATMs

  - [23] Gas Stations

  - [24] Hair Salons



--- **Things to Do** ---

  - [25] Parks

  - [26] Museums

  - [27] Movie Theaters

  - [28] Tourist Attractions

  

## 📁 Export Formats

### CSV Format (Google Sheets Ready)
```csv
name,phone,address,rating,website,scraped_at,google_maps_link
"Lilavati Hospital","+91-22-2675-1000","Bandra Reclamation, Bandra West, Mumbai, Maharashtra","4.5","lilavatihospital.com","2025-01-15 10:00:00","https://www.google.com/maps/search/?api=1&query=Lilavati%20Hospital%2C%20Bandra%20Reclamation%2C%20Bandra%20West%2C%20Mumbai%2C%20Maharashtra"
```

### JSON Format (Developer Friendly)
```json
{
  "export_info": {
    "total_records": 1,
    "export_timestamp": "2025-01-15T10:00:00.000000"
  },
  "businesses": [
    {
      "name": "Lilavati Hospital",
      "phone": "+91-22-2675-1000",
      "address": "Bandra Reclamation, Bandra West, Mumbai, Maharashtra",
      "rating": "4.5",
      "website": "lilavatihospital.com",
      "scraped_at": "2025-01-15 10:00:00",
      "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Lilavati%20Hospital%2C%20Bandra%20Reclamation%2C%20Bandra%20West%2C%20Mumbai%2C%20Maharashtra"
    }
  ]
}
```

### TSV Format (Tab Separated Values)
```tsv
name    phone   address rating  website scraped_at  google_maps_link
"Lilavati Hospital" "+91-22-2675-1000"  "Bandra Reclamation, Bandra West, Mumbai, Maharashtra"  "4.5"   "lilavatihospital.com"  "2025-01-15 10:00:00"   "https://www.google.com/maps/search/?api=1&query=Lilavati%20Hospital%2C%20Bandra%20Reclamation%2C%20Bandra%20West%2C%20Mumbai%2C%20Maharashtra"
```



## 🏙️ Supported Searches

This tool now dynamically scrapes Google Maps for any business type in any location you specify in your search query. The coverage is determined by Google Maps' own search capabilities.

### Example Search Queries
- `restaurants in Mumbai`
- `doctors in Bangalore`
- `gyms near Connaught Place Delhi`
- `shopping malls in Kolkata`



## 🔧 Technical Details

### Architecture
- **Modular design** focused on web scraping from Google Maps
- **Browser automation** using Selenium for dynamic content rendering
- **HTML parsing** with BeautifulSoup for data extraction
- **Error handling** for robust operation

### Data Structure
Each business record contains:
```python
{
    'name': str,           # Business name
    'phone': str,          # Primary phone number
    'address': str,        # Full address
    'rating': str,         # Google rating (e.g., "4.5")
    'website': str,        # Official website (if available)
    'scraped_at': str,     # Timestamp of when data was scraped
    'google_maps_link': str, # Direct link to the business on Google Maps
}
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Ideas for Contribution
- Add more cities (Ahmedabad, Surat, Jaipur)
- New business categories (Hotels, Schools, Clinics)
- Enhanced social media detection
- Email validation features
- Real-time data integration

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool performs real-time web scraping of publicly available data from Google Maps. Users are responsible for adhering to Google's Terms of Service and any applicable local regulations regarding data collection. Always respect `robots.txt` directives (where applicable) and avoid excessive requests to prevent service disruption. This tool is provided for educational and business development purposes; commercial use should be undertaken with full awareness of legal and ethical implications.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/abuhuraira-73/lead-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abuhuraira-73/lead-generator/discussions)
- **Email**: Create an issue for direct support

## 🌟 Show Your Support

If this project helped you generate leads or grow your business, please give it a ⭐ on GitHub!

---

**Made with ❤️ for ethical lead generation**

*Ready to gather real-time business insights? Clone, run, and start collecting legitimate leads today!*
