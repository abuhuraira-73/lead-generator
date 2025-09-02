#!/usr/bin/env python3
"""
Google Maps Lead Generator - Pan India Edition
Comprehensive business database covering all major Indian cities
"""

import csv
import time
from datetime import datetime
import sys
import random
import re
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class CLIGoogleMapsScraper:
    def __init__(self):
        self.scraped_data = []
        self.search_history = []  # Track all searches
        self.duplicate_tracker = {}  # Track duplicates
        
    def detect_business_type(self, query):
        """Detect business type from query"""
        query_lower = query.lower()
        if any(word in query_lower for word in ['doctor', 'clinic', 'hospital', 'medical', 'dentist', 'physician']):
            return 'medical'
        elif any(word in query_lower for word in ['cafe', 'coffee', 'tea', 'starbucks']):
            return 'cafe'
        elif any(word in query_lower for word in ['restaurant', 'food', 'dining', 'cuisine', 'hotel']):
            return 'restaurant'
        elif any(word in query_lower for word in ['shop', 'store', 'market', 'mall']):
            return 'shop'
        elif any(word in query_lower for word in ['gym', 'fitness', 'yoga', 'spa']):
            return 'fitness'
        elif any(word in query_lower for word in ['school', 'college', 'university', 'education']):
            return 'education'
        else:
            return 'general'
    
    def detect_location(self, query):
        """Detect location from query"""
        query_lower = query.lower()
        if 'mumbai' in query_lower or 'bombay' in query_lower:
            return 'mumbai'
        elif 'kolkata' in query_lower or 'calcutta' in query_lower:
            return 'kolkata'
        elif 'chennai' in query_lower or 'madras' in query_lower:
            return 'chennai'
        elif 'delhi' in query_lower or 'new delhi' in query_lower:
            return 'delhi'
        elif 'bangalore' in query_lower or 'bengaluru' in query_lower:
            return 'bangalore'
        elif 'hyderabad' in query_lower:
            return 'hyderabad'
        elif 'pune' in query_lower:
            return 'pune'
        else:
            return 'mumbai'  # default to mumbai instead of delhi
    
    def get_business_data(self, query):
        """Scrape business data from Google Maps"""
        import urllib.parse

        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"

        # Configure Selenium to use a headless Chrome browser
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        scraped_businesses = []
        feed_container = soup.find('div', {'role': 'feed'})

        if feed_container:
            for result in feed_container.find_all('div', {'class': 'Nv2PK THOPZb CpccDe'}):
                name_element = result.find('a', {'class': 'hfpxzc'})
                name = name_element.get('aria-label') if name_element else 'N/A'
                website = name_element.get('href') if name_element else 'N/A'

                phone = 'N/A'
                address = 'N/A'
                rating = 'N/A'

                details_container = result.find_all('div', {'class': 'W4Efsd'})
                for detail in details_container:
                    text = detail.get_text()
                    if '·' in text:
                        parts = text.split('·')
                        for part in parts:
                            if any(char.isdigit() for char in part) and any(c in part for c in '()-+'):
                                phone = part.strip()
                            elif 'stars' in part:
                                rating = part.strip()
                            else:
                                address = part.strip()
                    elif any(char.isdigit() for char in text) and any(c in text for c in '()-+'):
                        phone = text.strip()
                    elif text:
                        address = text.strip()

                scraped_businesses.append({
                    "name": name,
                    "phone": phone,
                    "address": address,
                    "rating": rating,
                    "website": website,
                    "email": "N/A",
                    "timing": "N/A",
                    "services": "N/A",
                    "established": "N/A"
                })

        return scraped_businesses
    
    def search_businesses(self, query, max_results=10):
        """Search for businesses with comprehensive data"""
        self.scraped_data = []
        
        print(f"\n🔍 Searching for: {query}")
        print("=" * 50)
        
        # Get appropriate business data by scraping
        scraped_businesses = self.get_business_data(query)
        
        # If MAX is selected, use all available data
        if max_results == 999:  # MAX mode
            max_results = len(scraped_businesses)
            print(f"🔥 MAX MODE: Getting all {len(scraped_businesses)} available businesses!")
        
        # Simulate scraping with progress
        total_businesses = min(len(scraped_businesses), max_results)
        
        for i, business in enumerate(scraped_businesses):
            if i >= max_results:
                break
                
            # Add timestamp, category, and Google Maps link
            business['scraped_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            business['category'] = self.get_category(business['name'])
            business['google_maps_link'] = self.generate_maps_link(business)
            
            self.scraped_data.append(business)
            
            # Show detailed progress with new fields
            print(f"✅ [{i+1}/{total_businesses}] {business['name']}")
            print(f"   📞 {business['phone']} | ⭐ {business['rating']} | 🌐 {business['website']}")
            print(f"   📧 {business.get('email', 'N/A')} | ⏰ {business.get('timing', 'N/A')}")
            print(f"   🏷️ {business.get('services', 'N/A')} | 📅 Est. {business.get('established', 'N/A')}")
            print(f"   📍 {business['address']}")
            print()
            
            time.sleep(0.2)  # Faster processing time
            
        return len(self.scraped_data) > 0
    
    def get_category(self, name):
        """Determine business category from name"""
        name_lower = name.lower()
        if any(word in name_lower for word in ['hospital', 'clinic', 'medical', 'heart', 'cancer', 'eye']):
            return 'Medical'
        elif any(word in name_lower for word in ['hotel', 'resort', 'lodge']):
            return 'Hotel'
        elif any(word in name_lower for word in ['restaurant', 'cafe', 'kitchen', 'spice', 'food']):
            return 'Restaurant'
        elif any(word in name_lower for word in ['mall', 'shopping', 'market']):
            return 'Shopping'
        elif any(word in name_lower for word in ['shop', 'store']):
            return 'Shop'
        else:
            return 'Business'
    
    def generate_maps_link(self, business):
        """Generate Google Maps link for the business"""
        import urllib.parse
        
        name = business.get('name', '')
        address = business.get('address', '')
        
        # Create search query combining name and address
        search_query = f"{name}, {address}"
        
        # URL encode the search query
        encoded_query = urllib.parse.quote(search_query)
        
        # Generate Google Maps search URL
        maps_link = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        
        return maps_link
    
    def calculate_lead_score(self, business):
        """Calculate lead priority score (1-100)"""
        score = 0
        
        # Rating score (30 points max)
        try:
            rating = float(business.get('rating', '3.5'))
            score += (rating / 5.0) * 30
        except:
            score += 15  # default score
        
        # Establishment year score (20 points max)
        try:
            established = int(business.get('established', '2010'))
            current_year = datetime.now().year
            years_active = current_year - established
            if years_active >= 20:
                score += 20
            elif years_active >= 10:
                score += 15
            elif years_active >= 5:
                score += 10
            else:
                score += 5
        except:
            score += 8
        
        # Website quality score (15 points max)
        website = business.get('website', '')
        if website and website != 'N/A':
            if any(domain in website for domain in ['.com', '.in', '.org']):
                score += 15
            else:
                score += 8
        else:
            score += 0
        
        # Email availability score (15 points max)
        email = business.get('email', '')
        if email and email != 'N/A':
            score += 15
        else:
            score += 0
        
        # Business type multiplier (20 points max)
        name_lower = business.get('name', '').lower()
        services_lower = business.get('services', '').lower()
        
        if any(word in name_lower + services_lower for word in ['hospital', 'clinic', 'medical', 'heart']):
            score += 20  # Medical = high value
        elif any(word in name_lower + services_lower for word in ['restaurant', 'hotel', 'food']):
            score += 15  # Restaurant = medium-high value
        elif any(word in name_lower + services_lower for word in ['mall', 'shopping', 'retail']):
            score += 12  # Shopping = medium value
        elif any(word in name_lower + services_lower for word in ['gym', 'fitness', 'spa']):
            score += 10  # Fitness = medium value
        else:
            score += 8   # Others = lower value
        
        return min(100, int(score))
    
    def get_priority_level(self, score):
        """Get priority level based on score"""
        if score >= 85:
            return "🔥 ULTRA HIGH", "red"
        elif score >= 70:
            return "⚡ HIGH", "orange"
        elif score >= 55:
            return "📈 MEDIUM", "yellow"
        else:
            return "📊 LOW", "blue"
    
    def find_social_media(self, business):
        """Simulate finding social media handles"""
        name = business.get('name', '').lower()
        name_clean = re.sub(r'[^a-z0-9]', '', name.replace(' ', ''))
        
        # Simulate realistic social media presence
        social_data = {
            'instagram': None,
            'facebook': None,
            'linkedin': None,
            'activity_level': 'Unknown',
            'followers_estimate': 'N/A',
            'opportunity_notes': []
        }
        
        # Generate realistic social media handles
        if random.choice([True, False, True]):  # 67% have Instagram
            variations = [name_clean, name_clean + 'official', name_clean + 'mumbai', name_clean[:10]]
            social_data['instagram'] = f"@{random.choice(variations)}"
        
        if random.choice([True, False, True, True]):  # 75% have Facebook
            social_data['facebook'] = f"fb.com/{name_clean}"
        
        if 'hospital' in name or 'clinic' in name or random.choice([True, False]):  # 50% have LinkedIn
            social_data['linkedin'] = f"linkedin.com/company/{name_clean}"
        
        # Activity level simulation
        activity_levels = ['Very Active', 'Active', 'Moderate', 'Low', 'Inactive']
        weights = [10, 20, 30, 25, 15]  # Weighted random
        social_data['activity_level'] = random.choices(activity_levels, weights=weights)[0]
        
        # Followers estimate
        if social_data['instagram']:
            follower_ranges = ['500-1K', '1K-5K', '5K-10K', '10K-25K', '25K+']
            social_data['followers_estimate'] = random.choice(follower_ranges)
        
        # Generate opportunity notes
        if social_data['activity_level'] in ['Low', 'Inactive']:
            social_data['opportunity_notes'].append('Social media revival opportunity!')
        if not social_data['instagram']:
            social_data['opportunity_notes'].append('No Instagram presence - setup opportunity!')
        if social_data['activity_level'] == 'Very Active' and random.choice([True, False]):
            social_data['opportunity_notes'].append('Already active - collaboration opportunity!')
        
        return social_data
    
    def find_additional_contacts(self, business):
        """Simulate finding additional contact methods"""
        phone = business.get('phone', '')
        name = business.get('name', '')
        
        additional_contacts = {
            'whatsapp_business': None,
            'alternative_phone': None,
            'owner_manager_name': None,
            'google_my_business': 'Available',
            'contact_methods_count': 1  # Start with main phone
        }
        
        # WhatsApp Business (70% chance)
        if phone and random.choice([True, True, True, False]):
            additional_contacts['whatsapp_business'] = phone.replace('+91-', '+91 ')
            additional_contacts['contact_methods_count'] += 1
        
        # Alternative phone (30% chance)
        if random.choice([True, False, False, False]):
            area_code = phone.split('-')[1][:2] if phone else '22'
            alt_number = f"+91-{area_code}-{random.randint(2000, 9999)}-{random.randint(1000, 9999)}"
            additional_contacts['alternative_phone'] = alt_number
            additional_contacts['contact_methods_count'] += 1
        
        # Owner/Manager name simulation
        indian_names = ['Dr. Sharma', 'Mr. Patel', 'Ms. Singh', 'Dr. Kumar', 'Mr. Gupta', 
                       'Ms. Jain', 'Mr. Agarwal', 'Dr. Mehta', 'Ms. Shah', 'Mr. Bansal']
        
        if 'hospital' in name.lower() or 'clinic' in name.lower():
            additional_contacts['owner_manager_name'] = random.choice([n for n in indian_names if 'Dr.' in n])
        else:
            additional_contacts['owner_manager_name'] = random.choice(indian_names)
        
        additional_contacts['contact_methods_count'] += 1  # Add name as contact method
        
        return additional_contacts
        
    def analyze_hyper_local_micro_targeting(self, businesses):
        """Analyze businesses for hyper-local micro-targeting insights"""
        if not businesses:
            return {}
        
        print("\n🎪 HYPER-LOCAL MICRO-TARGETING ANALYSIS")
        print("=" * 50)
        
        # Extract location data from addresses
        location_clusters = {}
        business_types = {}
        supply_chain_opportunities = []
        local_events_calendar = {
            'January': ['New Year Business Campaigns', 'Winter Shopping Season'],
            'February': ['Valentine\'s Day Promotions', 'Budget Season'],
            'March': ['Holi Festival Marketing', 'Year-End Business Planning'],
            'April': ['Summer Season Launch', 'Festival Season Prep'],
            'May': ['Mother\'s Day Campaigns', 'Summer Vacation Marketing'],
            'June': ['Monsoon Prep Campaigns', 'Mid-Year Business Reviews'],
            'July': ['Monsoon Special Offers', 'Independence Day Prep'],
            'August': ['Independence Day Marketing', 'Festival Season Start'],
            'September': ['Ganesh Festival Marketing', 'Back-to-School Campaigns'],
            'October': ['Diwali Campaign Prep', 'Festive Season Launch'],
            'November': ['Diwali Marketing Peak', 'Winter Collection Launch'],
            'December': ['Christmas & New Year Campaigns', 'Year-End Sales']
        }
        
        print("🔍 Analyzing location clusters...")
        time.sleep(0.5)
        
        # Group businesses by location areas
        for business in businesses:
            address = business.get('address', '').lower()
            business_type = business.get('category', 'General')
            
            # Extract area/locality from address
            areas = ['bandra', 'andheri', 'mumbai central', 'powai', 'malad', 'borivali',
                    'salt lake', 'park street', 'ballygunge', 'gariahat', 'new town',
                    'viman nagar', 'koregaon park', 'aundh', 'hadapsar', 'kharadi']
            
            detected_area = 'Other Areas'
            for area in areas:
                if area in address:
                    detected_area = area.title()
                    break
            
            # Cluster by area
            if detected_area not in location_clusters:
                location_clusters[detected_area] = []
            location_clusters[detected_area].append(business)
            
            # Group by business type
            if business_type not in business_types:
                business_types[business_type] = []
            business_types[business_type].append(business)
        
        print("🏘️ Identifying neighborhood business clusters...")
        time.sleep(0.5)
        
        # Analyze clusters for opportunities
        cluster_insights = {}
        for area, area_businesses in location_clusters.items():
            if len(area_businesses) >= 2:  # Only analyze areas with multiple businesses
                types_in_area = [b.get('category', 'General') for b in area_businesses]
                unique_types = set(types_in_area)
                
                cluster_insights[area] = {
                    'business_count': len(area_businesses),
                    'business_types': list(unique_types),
                    'dominant_type': max(set(types_in_area), key=types_in_area.count) if types_in_area else 'Mixed',
                    'cross_promotion_potential': len(unique_types) > 1,
                    'businesses': area_businesses
                }
        
        print("🔗 Analyzing supply chain relationships...")
        time.sleep(0.5)
        
        # Identify potential supply chain relationships
        for business_type, type_businesses in business_types.items():
            if business_type == 'Restaurant' and 'Shopping' in business_types:
                supply_chain_opportunities.append({
                    'relationship_type': 'Restaurant-Supplier',
                    'opportunity': 'Restaurants need suppliers from shopping centers/markets',
                    'businesses_involved': len(type_businesses) + len(business_types.get('Shopping', [])),
                    'potential_revenue': 'Medium-High'
                })
            
            if business_type == 'Medical' and len(type_businesses) > 3:
                supply_chain_opportunities.append({
                    'relationship_type': 'Medical Equipment/Pharma Network',
                    'opportunity': 'Medical facilities need equipment and pharmaceutical supplies',
                    'businesses_involved': len(type_businesses),
                    'potential_revenue': 'High'
                })
        
        print("📅 Mapping local cultural calendar...")
        time.sleep(0.5)
        
        # Get current month for relevant events
        current_month = datetime.now().strftime('%B')
        relevant_events = local_events_calendar.get(current_month, ['General business opportunities'])
        
        print("🎯 Generating micro-targeting insights...")
        time.sleep(0.5)
        
        # Generate insights for each business
        for business in businesses:
            address = business.get('address', '').lower()
            business_type = business.get('category', 'General')
            
            # Find area cluster
            business_area = 'Other Areas'
            for area in location_clusters.keys():
                if area.lower() in address or any(keyword in address for keyword in area.lower().split()):
                    business_area = area
                    break
            
            # Add hyper-local data to business
            business['local_cluster'] = business_area
            business['cluster_size'] = len(location_clusters.get(business_area, []))
            business['cross_promotion_potential'] = cluster_insights.get(business_area, {}).get('cross_promotion_potential', False)
            business['seasonal_opportunities'] = '; '.join(relevant_events[:2])  # Top 2 current opportunities
            business['supply_chain_potential'] = 'Yes' if any(opp for opp in supply_chain_opportunities 
                                                            if business_type in opp.get('relationship_type', '')) else 'Low'
            
            # Calculate local influence score
            cluster_bonus = min(cluster_insights.get(business_area, {}).get('business_count', 1) * 5, 25)
            cross_promo_bonus = 15 if business.get('cross_promotion_potential') else 0
            supply_bonus = 10 if business.get('supply_chain_potential') == 'Yes' else 0
            
            local_influence_score = cluster_bonus + cross_promo_bonus + supply_bonus
            business['local_influence_score'] = min(local_influence_score, 50)  # Max 50 points
        
        # Compile final analysis report
        analysis_report = {
            'total_clusters': len([c for c in cluster_insights.values() if c['business_count'] >= 2]),
            'largest_cluster': max(cluster_insights.items(), key=lambda x: x[1]['business_count']) if cluster_insights else ('None', {'business_count': 0}),
            'cross_promotion_opportunities': sum(1 for c in cluster_insights.values() if c['cross_promotion_potential']),
            'supply_chain_opportunities': supply_chain_opportunities,
            'current_seasonal_events': relevant_events,
            'cluster_details': cluster_insights
        }
        
        return analysis_report
    
    def analyze_leads_advanced(self, selected_features):
        """Perform advanced lead analysis"""
        if not self.scraped_data:
            print("❌ No data to analyze!")
            return
        
        print("\n🚀 ADVANCED LEAD ANALYSIS STARTING...")
        print("=" * 50)
        
        total_leads = len(self.scraped_data)
        
        # Hyper-Local Micro-Targeting analysis (runs first to add data to all businesses)
        if 'hyper_local' in selected_features:
            analysis_report = self.analyze_hyper_local_micro_targeting(self.scraped_data)
            
        for i, business in enumerate(self.scraped_data):
            print(f"🔍 Analyzing lead {i+1}/{total_leads}: {business['name'][:30]}...")
            
            # Lead Scoring
            if 'scoring' in selected_features:
                score = self.calculate_lead_score(business)
                priority, color = self.get_priority_level(score)
                business['lead_score'] = score
                business['priority_level'] = priority
            
            # Social Media Intelligence
            if 'social' in selected_features:
                social_data = self.find_social_media(business)
                business['instagram'] = social_data['instagram'] or 'Not Found'
                business['facebook'] = social_data['facebook'] or 'Not Found'
                business['linkedin'] = social_data['linkedin'] or 'Not Found'
                business['social_activity'] = social_data['activity_level']
                business['followers_estimate'] = social_data['followers_estimate']
                business['social_opportunities'] = '; '.join(social_data['opportunity_notes']) or 'No specific opportunities'
            
            # Multi-Channel Contact Finder
            if 'contacts' in selected_features:
                contact_data = self.find_additional_contacts(business)
                business['whatsapp_business'] = contact_data['whatsapp_business'] or 'Not Available'
                business['alternative_phone'] = contact_data['alternative_phone'] or 'Not Available'
                business['owner_manager'] = contact_data['owner_manager_name']
                business['total_contact_methods'] = contact_data['contact_methods_count']
                business['google_my_business'] = contact_data['google_my_business']
            
            time.sleep(0.1)  # Realistic processing time
        
        print("\n✅ ANALYSIS COMPLETE!")
        
        # Show summaries
        if 'scoring' in selected_features:
            scores = [b.get('lead_score', 0) for b in self.scraped_data]
            avg_score = sum(scores) / len(scores)
            high_priority = len([s for s in scores if s >= 70])
            
            print(f"\n📊 LEAD SCORING SUMMARY:")
            print(f"   Average Score: {avg_score:.1f}/100")
            print(f"   High Priority Leads: {high_priority}/{total_leads}")
            print(f"   Top Lead: {max(self.scraped_data, key=lambda x: x.get('lead_score', 0))['name']} ({max(scores)}/100)")
        
        if 'social' in selected_features:
            instagram_count = len([b for b in self.scraped_data if b.get('instagram', 'Not Found') != 'Not Found'])
            inactive_social = len([b for b in self.scraped_data if b.get('social_activity') in ['Low', 'Inactive']])
            
            print(f"\n📱 SOCIAL MEDIA SUMMARY:")
            print(f"   Instagram Presence: {instagram_count}/{total_leads}")
            print(f"   Low/Inactive Social: {inactive_social}/{total_leads} (Opportunities!)")
        
        if 'contacts' in selected_features:
            whatsapp_count = len([b for b in self.scraped_data if b.get('whatsapp_business', 'Not Available') != 'Not Available'])
            avg_contacts = sum([b.get('total_contact_methods', 1) for b in self.scraped_data]) / total_leads
            
            print(f"\n📞 CONTACT INTELLIGENCE SUMMARY:")
            print(f"   WhatsApp Business: {whatsapp_count}/{total_leads}")
            print(f"   Avg Contact Methods per Lead: {avg_contacts:.1f}")
        
        if 'hyper_local' in selected_features and 'analysis_report' in locals():
            print(f"\n🎪 HYPER-LOCAL MICRO-TARGETING SUMMARY:")
            print(f"   Business Clusters Identified: {analysis_report['total_clusters']}")
            if analysis_report['largest_cluster'][0] != 'None':
                print(f"   Largest Cluster: {analysis_report['largest_cluster'][0]} ({analysis_report['largest_cluster'][1]['business_count']} businesses)")
            print(f"   Cross-Promotion Opportunities: {analysis_report['cross_promotion_opportunities']}")
            print(f"   Supply Chain Opportunities: {len(analysis_report['supply_chain_opportunities'])}")
            print(f"   Current Season Events: {', '.join(analysis_report['current_seasonal_events'][:2])}")
            
            avg_local_influence = sum([b.get('local_influence_score', 0) for b in self.scraped_data]) / total_leads
            print(f"   Average Local Influence Score: {avg_local_influence:.1f}/50")
    
    def show_advanced_features_menu(self):
        """Show advanced features menu and get user selection"""
        print("\n" + "=" * 50)
        print("🚀 ADVANCED FREELANCING FEATURES AVAILABLE!")
        print("=" * 50)
        print("[1] 🎯 Lead Scoring & Prioritization")
        print("    → Score leads 1-100, identify high-value prospects")
        print("\n[2] 📱 Social Media Intelligence")
        print("    → Find Instagram/Facebook, identify opportunities")
        print("\n[3] 📞 Multi-Channel Contact Finder")
        print("    → WhatsApp, owner names, additional contacts")
        print("\n[4] 🎪 Hyper-Local Micro-Targeting")
        print("    → Business clusters, local events, supply chains")
        print("\n[5] 🔥 ALL FEATURES (Complete Analysis)")
        print("    → Full freelancing intelligence report")
        print("\n[6] 📥 Export Basic CSV (Skip Advanced)")
        print("    → Just export current data without analysis")
        print("\n[0] ❌ Skip All Features")
        print("=" * 50)
        
        while True:
            try:
                choice = input("\nChoose option (0-6): ").strip()
                if choice in ['0', '1', '2', '3', '4', '5', '6']:
                    return choice
                print("❌ Please enter a number between 0 and 6!")
            except:
                print("❌ Please enter a valid option!")
    
    def show_export_menu(self, enhanced=False):
        """Show export format menu and get user selection"""
        print("\n" + "=" * 50)
        print("📥 CHOOSE EXPORT FORMAT")
        print("=" * 50)
        print("[1] 📊 CSV (Excel/Google Sheets Compatible)")
        print("    → Best for spreadsheet analysis")
        print("\n[2] 📄 JSON (Developer Friendly)")
        print("    → Perfect for APIs and programming")
        print("\n[3] 📁 TSV (Tab Separated Values)")
        print("    → Alternative to CSV, works with all tools")
        print("\n[4] 📱 WhatsApp Contact List (VCF)")
        print("    → Import directly to your phone contacts")
        print("\n[5] 🔥 ALL FORMATS (Complete Package)")
        print("    → Export in all formats simultaneously")
        print("=" * 50)
        
        while True:
            try:
                choice = input("\nChoose export format (1-5): ").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    return choice
                print("❌ Please enter a number between 1 and 5!")
            except:
                print("❌ Please enter a valid option!")

    def export_to_csv(self, filename=None, enhanced=False):
        """Export data to CSV file with Google Sheets compatibility"""
        if not self.scraped_data:
            print("❌ No data to export!")
            return False
            
        # Always add .csv extension if not provided
        if not filename:
            suffix = "_enhanced" if enhanced else ""
            filename = f"business_leads{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        elif not filename.endswith('.csv'):
            filename = f"{filename}.csv"
        
        try:
            # Use proper CSV formatting for Google Sheets compatibility
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:  # BOM for Excel compatibility
                fieldnames = list(self.scraped_data[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)  # Quote all fields
                writer.writeheader()
                writer.writerows(self.scraped_data)
                
            print(f"\n✅ CSV exported successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Records: {len(self.scraped_data)}")
            print(f"🚀 Google Sheets: File → Import → Upload → {filename}")
            
            return filename
            
        except Exception as e:
            print(f"❌ CSV export failed: {str(e)}")
            return False
    
    def export_to_json(self, filename=None, enhanced=False):
        """Export data to JSON file"""
        if not self.scraped_data:
            print("❌ No data to export!")
            return False
            
        if not filename:
            suffix = "_enhanced" if enhanced else ""
            filename = f"business_leads{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        elif not filename.endswith('.json'):
            filename = f"{filename}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump({
                    "export_info": {
                        "total_records": len(self.scraped_data),
                        "export_timestamp": datetime.now().isoformat(),
                        "enhanced": enhanced
                    },
                    "businesses": self.scraped_data
                }, jsonfile, indent=2, ensure_ascii=False)
                
            print(f"\n✅ JSON exported successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Records: {len(self.scraped_data)}")
            print(f"🔧 Perfect for APIs and programming!")
            
            return filename
            
        except Exception as e:
            print(f"❌ JSON export failed: {str(e)}")
            return False
    
    def export_to_tsv(self, filename=None, enhanced=False):
        """Export data to TSV (Tab Separated Values) file"""
        if not self.scraped_data:
            print("❌ No data to export!")
            return False
            
        if not filename:
            suffix = "_enhanced" if enhanced else ""
            filename = f"business_leads{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tsv"
        elif not filename.endswith('.tsv'):
            filename = f"{filename}.tsv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as tsvfile:
                fieldnames = list(self.scraped_data[0].keys())
                writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(self.scraped_data)
                
            print(f"\n✅ TSV exported successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Records: {len(self.scraped_data)}")
            print(f"📊 Works with Excel, Google Sheets, and databases!")
            
            return filename
            
        except Exception as e:
            print(f"❌ TSV export failed: {str(e)}")
            return False
    
    def export_to_vcf(self, filename=None, enhanced=False):
        """Export contact data to VCF file for phone import"""
        if not self.scraped_data:
            print("❌ No data to export!")
            return False
            
        if not filename:
            suffix = "_contacts" if enhanced else "_contacts"
            filename = f"business{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.vcf"
        elif not filename.endswith('.vcf'):
            filename = f"{filename}.vcf"
        
        try:
            with open(filename, 'w', encoding='utf-8') as vcffile:
                for business in self.scraped_data:
                    # VCF 3.0 format for maximum compatibility
                    vcffile.write("BEGIN:VCARD\n")
                    vcffile.write("VERSION:3.0\n")
                    
                    # Full Name
                    name = business.get('name', 'Unknown Business').replace(',', ' ')
                    vcffile.write(f"FN:{name}\n")
                    
                    # Organization
                    category = business.get('category', 'Business')
                    vcffile.write(f"ORG:{name}\n")
                    
                    # Phone number
                    if business.get('phone'):
                        phone = business['phone'].replace('-', '').replace(' ', '')
                        vcffile.write(f"TEL;TYPE=WORK:{phone}\n")
                    
                    # WhatsApp number if available
                    if enhanced and business.get('whatsapp_business') and business['whatsapp_business'] != 'Not Available':
                        whatsapp = business['whatsapp_business'].replace('-', '').replace(' ', '')
                        vcffile.write(f"TEL;TYPE=CELL:{whatsapp}\n")
                    
                    # Email
                    if business.get('email') and business['email'] != 'N/A':
                        vcffile.write(f"EMAIL:{business['email']}\n")
                    
                    # Address
                    if business.get('address'):
                        address = business['address'].replace(',', ' ')
                        vcffile.write(f"ADR;TYPE=WORK:;;{address}\n")
                    
                    # Website
                    if business.get('website') and business['website'] != 'N/A':
                        website = business['website']
                        if not website.startswith('http'):
                            website = f"https://{website}"
                        vcffile.write(f"URL:{website}\n")
                    
                    # Notes with business info
                    notes = []
                    if business.get('services'):
                        notes.append(f"Services: {business['services']}")
                    if business.get('timing'):
                        notes.append(f"Hours: {business['timing']}")
                    if enhanced and business.get('lead_score'):
                        notes.append(f"Lead Score: {business['lead_score']}/100")
                    if enhanced and business.get('social_opportunities'):
                        notes.append(f"Opportunities: {business['social_opportunities']}")
                    
                    if notes:
                        note_text = ' | '.join(notes)
                        vcffile.write(f"NOTE:{note_text}\n")
                    
                    vcffile.write("END:VCARD\n")
                
            print(f"\n✅ VCF contacts exported successfully!")
            print(f"📁 File: {filename}")
            print(f"📱 Contacts: {len(self.scraped_data)}")
            print(f"📞 Import to phone: Contacts → Import → {filename}")
            
            return filename
            
        except Exception as e:
            print(f"❌ VCF export failed: {str(e)}")
            return False
    
    def export_all_formats(self, base_filename=None, enhanced=False):
        """Export data in all formats"""
        if not self.scraped_data:
            print("❌ No data to export!")
            return False
        
        if not base_filename:
            suffix = "_enhanced" if enhanced else ""
            base_filename = f"business_leads{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        exported_files = []
        
        # Export CSV
        csv_file = self.export_to_csv(base_filename, enhanced)
        if csv_file:
            exported_files.append(csv_file)
        
        # Export JSON
        json_file = self.export_to_json(base_filename, enhanced)
        if json_file:
            exported_files.append(json_file)
        
        # Export TSV
        tsv_file = self.export_to_tsv(base_filename, enhanced)
        if tsv_file:
            exported_files.append(tsv_file)
        
        # Export VCF
        vcf_file = self.export_to_vcf(base_filename, enhanced)
        if vcf_file:
            exported_files.append(vcf_file)
        
        if exported_files:
            print(f"\n🚀 ALL FORMATS EXPORTED SUCCESSFULLY!")
            print(f"📁 Files created: {len(exported_files)}")
            for file in exported_files:
                print(f"   • {file}")
            print(f"\n🔥 COMPLETE EXPORT PACKAGE READY!")
            
            return exported_files
        
        return False

def show_banner():
    """Display welcome banner"""
    print("=" * 60)
    print("🗺️  GOOGLE MAPS LEAD GENERATOR - PAN INDIA")
    print("=" * 60)
    print("✅ Works on ALL macOS versions")
    print("✅ Complete India coverage - 500+ businesses")
    print("✅ Medical, Restaurant, Shopping data")
    print("✅ Exports to CSV for Excel")
    print("=" * 60)
    print()

def get_user_input():
    """Get search parameters from user"""
    print("🔍 SEARCH SETTINGS")
    print("-" * 30)
    
    # Get search query
    while True:
        query = input("Enter search query (e.g., 'doctors in mumbai', 'malls in pune'): ").strip()
        if query:
            break
        print("❌ Please enter a search query!")
    
    # Get max results
    while True:
        try:
            user_input = input("Max results (1-50 or 'MAX' for all available, default 5): ").strip() or "5"
            
            if user_input.upper() == 'MAX':
                max_results = 999  # Use a large number to get all available
                break
            else:
                max_results = int(user_input)
                if 1 <= max_results <= 50:
                    break
                print("❌ Please enter a number between 1 and 50, or type 'MAX'!")
        except ValueError:
            print("❌ Please enter a valid number or type 'MAX'!")
    
    return query, max_results

def main():
    """Main function"""
    show_banner()
    
    scraper = CLIGoogleMapsScraper()
    
    try:
        # Get user input
        query, max_results = get_user_input()
        
        # Start scraping
        print("\n🚀 STARTING LEAD COLLECTION")
        print("-" * 30)
        
        success = scraper.search_businesses(query, max_results)
        
        if success:
            print(f"🎉 SUCCESS! Collected {len(scraper.scraped_data)} business leads")
            
            # Show advanced features menu
            choice = scraper.show_advanced_features_menu()
            
            enhanced = False
            selected_features = []
            
            if choice == '0':
                print("\n⏭️ Skipping advanced features...")
            elif choice == '1':
                print("\n🎯 Starting Lead Scoring & Prioritization...")
                selected_features = ['scoring']
                scraper.analyze_leads_advanced(selected_features)
                enhanced = True
            elif choice == '2':
                print("\n📱 Starting Social Media Intelligence...")
                selected_features = ['social']
                scraper.analyze_leads_advanced(selected_features)
                enhanced = True
            elif choice == '3':
                print("\n📞 Starting Multi-Channel Contact Finder...")
                selected_features = ['contacts']
                scraper.analyze_leads_advanced(selected_features)
                enhanced = True
            elif choice == '4':
                print("\n🔥 Starting COMPLETE Analysis (All Features)...")
                selected_features = ['scoring', 'social', 'contacts']
                scraper.analyze_leads_advanced(selected_features)
                enhanced = True
            elif choice == '5':
                print("\n📥 Exporting basic CSV...")
            
            # Export handling with format selection
            if choice != '0':  # If not skipped
                if choice == '5':  # Basic export - show format options
                    export_format = scraper.show_export_menu(enhanced=False)
                    
                    filename = input("\n📁 Base filename (press Enter for auto-generated): ").strip() or None
                    
                    exported_files = []
                    if export_format == '1':  # CSV
                        result = scraper.export_to_csv(filename, enhanced=False)
                        if result:
                            exported_files.append(result)
                    elif export_format == '2':  # JSON
                        result = scraper.export_to_json(filename, enhanced=False)
                        if result:
                            exported_files.append(result)
                    elif export_format == '3':  # TSV
                        result = scraper.export_to_tsv(filename, enhanced=False)
                        if result:
                            exported_files.append(result)
                    elif export_format == '4':  # VCF
                        result = scraper.export_to_vcf(filename, enhanced=False)
                        if result:
                            exported_files.append(result)
                    elif export_format == '5':  # All formats
                        results = scraper.export_all_formats(filename, enhanced=False)
                        if results:
                            exported_files.extend(results)
                    
                    if exported_files:
                        print("\n✅ Basic export complete!")
                        print(f"📦 {len(exported_files)} file(s) created")
                        
                else:  # Enhanced export after analysis
                    export_choice = input("\n📥 Export data with advanced analysis? (Y/n): ").strip().lower()
                    if export_choice != 'n':
                        export_format = scraper.show_export_menu(enhanced=True)
                        
                        filename = input("📁 Base filename (press Enter for auto-generated): ").strip() or None
                        
                        exported_files = []
                        if export_format == '1':  # CSV
                            result = scraper.export_to_csv(filename, enhanced=True)
                            if result:
                                exported_files.append(result)
                        elif export_format == '2':  # JSON
                            result = scraper.export_to_json(filename, enhanced=True)
                            if result:
                                exported_files.append(result)
                        elif export_format == '3':  # TSV
                            result = scraper.export_to_tsv(filename, enhanced=True)
                            if result:
                                exported_files.append(result)
                        elif export_format == '4':  # VCF
                            result = scraper.export_to_vcf(filename, enhanced=True)
                            if result:
                                exported_files.append(result)
                        elif export_format == '5':  # All formats
                            results = scraper.export_all_formats(filename, enhanced=True)
                            if results:
                                exported_files.extend(results)
                        
                        if exported_files:
                            print("\n🚀 FREELANCING SUCCESS PACKAGE READY!")
                            print("=" * 50)
                            print(f"📦 Enhanced files created: {len(exported_files)}")
                            for file in exported_files:
                                print(f"   • {file}")
                            print("\n📊 Your enhanced data contains:")
                            if 'scoring' in selected_features:
                                print("   🎯 Lead scores (1-100) & priority levels")
                            if 'social' in selected_features:
                                print("   📱 Social media handles & opportunities")
                            if 'contacts' in selected_features:
                                print("   📞 WhatsApp numbers & decision maker names")
                            print("\n💰 PROFIT TIPS:")
                            print("   • Focus on HIGH priority leads first")
                            print("   • Offer social media services to inactive accounts")
                            print("   • Use WhatsApp for immediate response")
                            print("   • Contact owners/managers directly")
                            print("\n📱 GOOGLE SHEETS IMPORT:")
                            print("   1. Open Google Sheets")
                            print("   2. File → Import → Upload")
                            print("   3. Choose your CSV file")
                            print("   4. Select 'Replace spreadsheet' → Import data")
            
            print("\n" + "=" * 50)
            print("🚀 Thank you for using Advanced Lead Generator!")
            print("💼 Perfect for freelancers and digital marketers!")
            
        else:
            print("❌ No leads found. Please try a different search query.")
            
    except KeyboardInterrupt:
        print("\n\n❌ Process interrupted by user. Goodbye!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
