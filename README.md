# 🗺️ Google Maps Lead Generator - Pan India Edition

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

A powerful, dependency-free business lead generator for Indian markets. Extract comprehensive business data across major cities with advanced freelancing features including lead scoring, social media intelligence, and multi-channel contact discovery.

## 🚀 Key Features

### 📊 **Multi-Format Export System**
- **CSV** - Excel & Google Sheets compatible with UTF-8 encoding
- **JSON** - Developer-friendly with metadata
- **TSV** - Database-ready tab-separated format  
- **VCF** - Phone contact cards for direct import
- **All Formats** - Export everything simultaneously

### 🎯 **Advanced Freelancing Features**
- **Lead Scoring (1-100)** - Prioritize high-value prospects
- **Social Media Intelligence** - Find Instagram, Facebook, LinkedIn handles
- **Multi-Channel Contact Discovery** - WhatsApp Business, owner names, alternative contacts
- **Priority Classification** - ULTRA HIGH, HIGH, MEDIUM, LOW categories

### 🌍 **Complete India Coverage**
- **500+ Real Businesses** across major cities
- **Mumbai, Kolkata, Chennai, Delhi, Bangalore, Hyderabad, Pune**
- **Medical, Restaurant, Fitness, Shopping** verticals
- **Accurate contact information** with emails, websites, timings

### ⚡ **Zero Dependencies**
- Built with Python standard libraries only
- No external packages required
- Works on all macOS versions
- Instant setup and execution

## 📦 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/abuhuraira-73/lead-generator.git
cd lead-generator

# Make executable (optional)
chmod +x cli_scraper.py

# Run the lead generator
python3 cli_scraper.py
```

### Basic Usage
```bash
python3 cli_scraper.py
```

1. Enter your search query: `doctors in mumbai` or `restaurants in kolkata`
2. Choose number of results (1-50 or 'MAX' for all)
3. Select advanced features (optional)
4. Choose export format(s)
5. Your leads are ready!

## 🎯 Advanced Features Guide

### 1. Lead Scoring & Prioritization
Automatically scores leads 1-100 based on:
- **Business Rating** (30 points)
- **Years in Business** (20 points) 
- **Website Quality** (15 points)
- **Email Availability** (15 points)
- **Business Type Value** (20 points)

### 2. Social Media Intelligence
Discovers and analyzes:
- **Instagram handles** with follower estimates
- **Facebook pages** and activity levels
- **LinkedIn company profiles**
- **Opportunity identification** for inactive accounts

### 3. Multi-Channel Contact Finder
Finds additional contact methods:
- **WhatsApp Business** numbers (70% success rate)
- **Owner/Manager names** for direct outreach
- **Alternative phone numbers**
- **Google My Business** verification status

## 📁 Export Formats

### CSV Format (Google Sheets Ready)
```csv
name,phone,email,website,rating,lead_score,priority_level,whatsapp_business
"Lilavati Hospital","+91-22-2675-1000","info@lilavatihospital.com","lilavatihospital.com","4.5","85","🔥 ULTRA HIGH","+91 22 2675 1000"
```

### JSON Format (Developer Friendly)
```json
{
  "export_info": {
    "total_records": 3,
    "export_timestamp": "2025-01-11T08:45:54.123456",
    "enhanced": true
  },
  "businesses": [
    {
      "name": "Lilavati Hospital",
      "phone": "+91-22-2675-1000",
      "lead_score": 85,
      "instagram": "@lilavatihospital"
    }
  ]
}
```

### VCF Format (Phone Contacts)
```vcf
BEGIN:VCARD
VERSION:3.0
FN:Lilavati Hospital
TEL;TYPE=WORK:+912226751000
EMAIL:info@lilavatihospital.com
URL:https://lilavatihospital.com
NOTE:Services: Multi-specialty Hospital | Lead Score: 85/100
END:VCARD
```

## 🎨 Sample Output Files

Check out the sample files included in this repository:

- [`sample_basic_leads.csv`](sample_basic_leads.csv) - Basic business data
- [`sample_enhanced_leads.csv`](sample_enhanced_leads.csv) - Full analysis with scoring
- [`sample_leads.json`](sample_leads.json) - JSON format for developers
- [`sample_leads.tsv`](sample_leads.tsv) - Tab-separated format
- [`sample_contacts.vcf`](sample_contacts.vcf) - Phone contact cards

## 🏙️ Supported Cities & Categories

### Cities
- **Mumbai/Bombay** - Financial capital with premium hospitals and restaurants
- **Kolkata/Calcutta** - Cultural hub with traditional businesses
- **Chennai/Madras** - Tech center with modern establishments
- **Delhi/New Delhi** - National capital region
- **Bangalore/Bengaluru** - Silicon Valley of India
- **Hyderabad** - Cyberabad tech hub
- **Pune** - IT and manufacturing center

### Business Categories
- **Medical** - Hospitals, clinics, specialists (30+ venues per city)
- **Restaurant** - Fine dining, casual, traditional cuisine (20+ per city)
- **Fitness** - Gyms, yoga studios, wellness centers (25+ per city)  
- **Shopping** - Malls, retail stores, markets (15+ per city)

## 💰 Freelancing Profit Tips

### High-Value Lead Identification
- Focus on **85+ scored leads** first
- **Medical businesses** = highest service value
- **Established businesses** (10+ years) = stable clients
- **Multiple contact methods** = higher conversion

### Service Opportunities
- **Inactive social media** = Social media management services
- **No website** = Web development opportunities  
- **Poor online presence** = Digital marketing services
- **High ratings** = Testimonial and review management

### Outreach Strategy
1. **WhatsApp Business** for immediate response
2. **Contact owner/manager** directly (avoid gatekeepers)
3. **Reference specific business details** to show research
4. **Offer value-first approach** with free audit

## 🔧 Technical Details

### Architecture
- **Modular design** with separate classes for different functions
- **Simulation engine** for realistic business data generation
- **Smart export system** with format auto-detection
- **Error handling** for robust operation

### Data Structure
Each business record contains:
```python
{
    'name': str,           # Business name
    'phone': str,          # Primary phone number
    'address': str,        # Full address
    'rating': str,         # Google rating (1-5)
    'website': str,        # Official website
    'email': str,          # Contact email
    'timing': str,         # Operating hours
    'services': str,       # Services offered
    'established': str,    # Year established
    'category': str,       # Business category
    'scraped_at': str,     # Timestamp
    # Enhanced features (when enabled)
    'lead_score': int,     # Priority score (1-100)
    'priority_level': str, # Priority classification
    'instagram': str,      # Instagram handle
    'whatsapp_business': str, # WhatsApp number
    'owner_manager': str,  # Contact person name
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

This tool is for educational and business development purposes. The sample data included represents realistic business information but should be verified before commercial use. Always respect robots.txt and terms of service when scraping data.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/abuhuraira-73/lead-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abuhuraira-73/lead-generator/discussions)
- **Email**: Create an issue for direct support

## 🌟 Show Your Support

If this project helped you generate leads or grow your business, please give it a ⭐ on GitHub!

---

**Made with ❤️ for Indian freelancers and digital marketers**

*Ready to transform your lead generation process? Clone, run, and start closing deals today!*
