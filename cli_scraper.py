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


INDIA_GEOGRAPHY = {
    "All Major Cities": [
        "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur"
    ],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore"],
    "Arunachal Pradesh": ["Itanagar"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur"],
    "Chhattisgarh": ["Raipur", "Bhilai"],
    "Goa": ["Panaji", "Vasco da Gama"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Haryana": ["Faridabad", "Gurgaon", "Panipat"],
    "Himachal Pradesh": ["Shimla", "Manali"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad"],
    "Karnataka": ["Bangalore", "Hubli", "Mysore", "Mangalore"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Manipur": ["Imphal"],
    "Meghalaya": ["Shillong"],
    "Mizoram": ["Aizawl"],
    "Nagaland": ["Kohima", "Dimapur"],
    "Odisha": ["Bhubaneswar", "Cuttack"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
    "Sikkim": ["Gangtok"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Tripura": ["Agartala"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Ghaziabad", "Agra", "Varanasi"],
    "Uttarakhand": ["Dehradun", "Haridwar"],
    "West Bengal": ["Kolkata", "Asansol", "Siliguri"],
    "Andaman and Nicobar Islands": ["Port Blair"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Silvassa"],
    "Delhi": ["Delhi", "New Delhi"],
    "Jammu and Kashmir": ["Srinagar", "Jammu"],
    "Ladakh": ["Leh"],
    "Lakshadweep": ["Kavaratti"],
    "Puducherry": ["Puducherry"]
}


class CLIGoogleMapsScraper:
    def __init__(self):
        self.scraped_data = []
        self.search_history = []  # Track all searches
        self.duplicate_tracker = {}  # Track duplicates
    
    def get_business_data(self, query):
        """
        Scrapes data by first getting all business links from a search query,
        then visiting each link individually to extract detailed information.
        A visible Chrome window will be used.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        import urllib.parse

        # --- Part 1: Get all business links from the search results page ---
        
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/maps/search/{encoded_query}"

        options = webdriver.ChromeOptions()
        # REMOVED: options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print(f"Navigating to search page: {url}")
        driver.get(url)

        business_links = []
        try:
            wait = WebDriverWait(driver, 20)
            results_panel_selector = 'div[role="feed"]'
            results_panel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, results_panel_selector)))
            
            print("Scrolling to load all business listings...")
            last_height = driver.execute_script("return arguments[0].scrollHeight", results_panel)
            while True:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
                time.sleep(3)
                new_height = driver.execute_script("return arguments[0].scrollHeight", results_panel)
                if new_height == last_height:
                    break
                last_height = new_height

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for result in soup.select('div[role="feed"] a[class="hfpxzc"]'):
                link = result.get('href')
                if link and not link.startswith('/maps/place/'):
                    business_links.append(link)

        except Exception as e:
            print(f"❌ Error during search page scraping: {e}")
            driver.quit()
            return []

        print(f"Found {len(business_links)} potential business links.")

        # --- Part 2: Visit each business link and scrape detailed data ---
        
        scraped_businesses = []
        for i, link in enumerate(business_links):
            print(f"\n--- Scraping Business {i+1}/{len(business_links)} ---")
            try:
                print(f"Navigating to: {link}")
                driver.get(link)
                # Wait for a key element on the page to ensure it's loaded
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
                time.sleep(2) # Extra wait for dynamic elements

                page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                name = page_soup.select_one('h1').get_text(strip=True) if page_soup.select_one('h1') else 'N/A'
                print(f"Name: {name}")

                # Use data-tooltip attributes for reliable extraction
                phone_element = page_soup.find('button', {'data-tooltip': 'Copy phone number'})
                phone = phone_element.get('aria-label', '').replace('Phone: ', '').strip() if phone_element else 'N/A'

                address_element = page_soup.find('button', {'data-tooltip': 'Copy address'})
                address = address_element.get('aria-label', '').replace('Address: ', '').strip() if address_element else 'N/A'

                website_element = page_soup.find('a', {'data-tooltip': 'Open website'})
                website = website_element.get('href', 'N/A') if website_element else 'N/A'
                
                rating_element = page_soup.select_one('div.fontDisplayLarge')
                rating = rating_element.get_text(strip=True) if rating_element else 'N/A'

                business_data = {
                    "name": name,
                    "phone": phone,
                    "address": address,
                    "rating": rating,
                    "website": website,
                    "google_maps_link": link
                }
                scraped_businesses.append(business_data)

            except Exception as e:
                print(f"❌ Could not scrape {link}. Error: {e}")

        driver.quit()
        return scraped_businesses
    
    def get_user_input(self):
        """Guides the user through a multi-level menu to generate search queries."""
        print("🔍 SEARCH SETTINGS")
        print("-" * 30)
        
        # --- Main Menu: India vs World ---
        print("[1] Search within India (Guided Menu)")
        print("[2] Search anywhere else in the world (Custom Query)")
        main_choice = ""
        while main_choice not in ["1", "2"]:
            main_choice = input("Enter your choice: ").strip()

        queries = []
        search_term = ""

        # --- Guided India Search ---
        if main_choice == '1':
            print("\n--- India Search Menu ---")
            print("[1] Scan all major cities in India")
            print("[2] Select a specific State/UT")
            india_choice = ""
            while india_choice not in ["1", "2"]:
                india_choice = input("Enter your choice: ").strip()

            # Scan All India
            if india_choice == '1':
                while not search_term:
                    search_term = input("Enter the search term (e.g., 'Cafes', 'Hospitals'): ").strip()
                queries = [f"{search_term} in {city}" for city in INDIA_GEOGRAPHY["All Major Cities"]]

            # Select a State
            elif india_choice == '2':
                states = list(INDIA_GEOGRAPHY.keys())
                states.remove("All Major Cities")
                for i, state in enumerate(states):
                    print(f"[{i+1}] {state}")
                
                state_idx = -1
                while state_idx < 0 or state_idx >= len(states):
                    try:
                        state_idx = int(input("Select a State/UT by number: ").strip()) - 1
                    except (ValueError, IndexError):
                        print("❌ Invalid selection.")
                        state_idx = -1
                selected_state = states[state_idx]

                print(f"\n--- {selected_state} Menu ---")
                print(f"[1] Scan all major cities in {selected_state}")
                print(f"[2] Select a specific city in {selected_state}")
                state_choice = ""
                while state_choice not in ["1", "2"]:
                    state_choice = input("Enter your choice: ").strip()
                
                # Scan all cities in State
                if state_choice == '1':
                    while not search_term:
                        search_term = input(f"Enter search term for {selected_state} (e.g., 'Cafes'): ").strip()
                    queries = [f"{search_term} in {city}" for city in INDIA_GEOGRAPHY[selected_state]]

                # Select a city in State
                elif state_choice == '2':
                    cities = INDIA_GEOGRAPHY[selected_state]
                    for i, city in enumerate(cities):
                        print(f"[{i+1}] {city}")
                    
                    city_idx = -1
                    while city_idx < 0 or city_idx >= len(cities):
                        try:
                            city_idx = int(input(f"Select a city in {selected_state}: ").strip()) - 1
                        except (ValueError, IndexError):
                            print("❌ Invalid selection.")
                            city_idx = -1
                    selected_city = cities[city_idx]
                    
                    while not search_term:
                        search_term = input(f"Enter search term for {selected_city}: ").strip()
                    queries = [f"{search_term} in {selected_city}"]

        # --- Custom World Search ---
        else:
            custom_query = ""
            while not custom_query:
                custom_query = input("\nEnter your full custom query (e.g., 'Restaurants in Paris'): ").strip()
            queries = [custom_query]
        
        # --- Get Max Results (common for all paths) ---
        while True:
            try:
                user_input = input("\nMax results per location (1-50 or 'MAX', default 5): ").strip() or "5"
                if user_input.upper() == 'MAX':
                    max_results = 999
                    break
                else:
                    max_results = int(user_input)
                    if 1 <= max_results <= 50:
                        break
                    print("❌ Please enter a number between 1 and 50, or type 'MAX'!")
            except ValueError:
                print("❌ Please enter a valid number or type 'MAX'!")
        
        return queries, max_results
    
    def search_businesses(self, queries, max_results=10):
        """Search for businesses using a list of queries for better coverage."""
        self.scraped_data = []
        
        all_businesses = []
        
        for sub_query in queries:
            print(f"\n🔍 Searching for: {sub_query}")
            print("-" * 50)
            all_businesses.extend(self.get_business_data(sub_query))

        print(f"\n✅ Total raw results found: {len(all_businesses)}")
        print(" de-duplicating and processing...")

        # De-duplicate results based on the Google Maps link
        unique_businesses = {}
        for business in all_businesses:
            link = business.get('google_maps_link')
            if link and link not in unique_businesses:
                unique_businesses[link] = business

        self.scraped_data = list(unique_businesses.values())
        
        # The max_results from user now applies to the total unique results
        # If user did not select MAX, we cap the total results.
        if max_results != 999:
            print(f"Capping total unique results to {max_results}")
            self.scraped_data = self.scraped_data[:max_results]
        else:
            print(f"Processing all {len(self.scraped_data)} unique businesses!")

        total_businesses = len(self.scraped_data)

        for i, business in enumerate(self.scraped_data):
            # Add timestamp
            business['scraped_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Show detailed progress with new fields
            print(f"✅ [{i+1}/{total_businesses}] {business['name']}")
            print(f"   📞 {business['phone']} | ⭐ {business['rating']} | 🌐 {business['website']}")
            print(f"   📍 {business['address']}")
            print(f"   🗺️  {business['google_maps_link']}")
            print()
            
            time.sleep(0.1)
            
        return len(self.scraped_data) > 0
    
    def show_export_menu(self):
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
        print("=" * 50)
        
        while True:
            try:
                choice = input("\nChoose export format (1-3): ").strip()
                if choice in ['1', '2', '3']:
                    return choice
                print("❌ Please enter a number between 1 and 3!")
            except:
                print("❌ Please enter a valid option!")

    def export_to_csv(self, filename=None):
        """Export data to CSV file with Google Sheets compatibility"""
        if not self.scraped_data:
            print("❌ No data to export!")
            return False
            
        # Always add .csv extension if not provided
        if not filename:
            filename = f"business_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
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
    
    def export_to_json(self, filename=None):
        """Export data to JSON file"""
        if not self.scraped_data:
            print("❌ No data to export!")
            return False
            
        if not filename:
            filename = f"business_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        elif not filename.endswith('.json'):
            filename = f"{filename}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump({
                    "export_info": {
                        "total_records": len(self.scraped_data),
                        "export_timestamp": datetime.now().isoformat(),
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
    
    def export_to_tsv(self, filename=None):
        """Export data to TSV (Tab Separated Values) file"""
        if not self.scraped_data:
            print("❌ No data to export!")
            return False
            
        if not filename:
            filename = f"business_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tsv"
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
    """Get search parameters from user via a category menu or custom query."""
    print("🔍 SEARCH SETTINGS")
    print("-" * 30)

    categories = {
        "Food & Drink": ["Restaurants", "Cafes", "Bars", "Coffee Shops", "Bakeries", "Takeout", "Delivery"],
        "Health & Wellness": ["Doctors", "Hospitals", "Clinics", "Dentists", "Pharmacies", "Gyms", "Spas"],
        "Shopping": ["Supermarkets", "Grocery Stores", "Shopping Malls", "Clothing Stores", "Book Stores"],
        "Services": ["Hotels", "Banks", "ATMs", "Gas Stations", "Hair Salons"],
        "Things to Do": ["Parks", "Museums", "Movie Theaters", "Tourist Attractions"]
    }

    print("Please choose a category by number, or type your own custom search query.")
    
    # Flatten the dictionary into a numbered list for user selection
    flat_categories = []
    for group, items in categories.items():
        print(f"\n--- {group} ---")
        for item in items:
            flat_categories.append(item)
            print(f"  [{len(flat_categories)}] {item}")
    
    query = ""
    while not query:
        choice = input("\nEnter a category number or your custom query: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(flat_categories):
            selected_category = flat_categories[int(choice) - 1]
            location = ""
            while not location:
                location = input(f"Enter location for '{selected_category}': ").strip()
            query = f"{selected_category} in {location}"
        elif choice:
            query = choice  # Treat non-numeric input as a full custom query
            print(f"Using custom query: '{query}'")
        else:
            print("❌ Please enter a valid choice.")

    # Get max results
    while True:
        try:
            user_input = input("Max results (1-50 or 'MAX' for all available, default 5): ").strip() or "5"
            
            if user_input.upper() == 'MAX':
                max_results = 999
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
        # Get user input, which now returns a list of queries
        queries, max_results = scraper.get_user_input()
        
        # Start scraping
        print("\n🚀 STARTING LEAD COLLECTION")
        
        success = scraper.search_businesses(queries, max_results)
        
        if success:
            print(f"\n🎉 SUCCESS! Collected {len(scraper.scraped_data)} unique business leads.")
            
            export_choice = input("\n📥 Export data? (Y/n): ").strip().lower()
            if export_choice != 'n':
                export_format = scraper.show_export_menu()
                
                filename = input("\n📁 Base filename (press Enter for auto-generated): ").strip() or None
                
                exported_files = []
                if export_format == '1':  # CSV
                    result = scraper.export_to_csv(filename)
                    if result:
                        exported_files.append(result)
                elif export_format == '2':  # JSON
                    result = scraper.export_to_json(filename)
                    if result:
                        exported_files.append(result)
                elif export_format == '3':  # TSV
                    result = scraper.export_to_tsv(filename)
                    if result:
                        exported_files.append(result)

                if exported_files:
                    print("\n" + "=" * 50)
                    print(f"📦 {len(exported_files)} file(s) created.")
                    print("✅ Export complete!")

            print("\n" + "=" * 50)
            print("🚀 Thank you for using the Lead Generator!")
            
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
