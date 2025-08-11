#!/usr/bin/env python3
"""
Generate sample output files for the lead generator
"""
from cli_scraper import CLIGoogleMapsScraper

def generate_samples():
    """Generate sample files with different formats"""
    scraper = CLIGoogleMapsScraper()
    
    # Simulate a search to get sample data
    scraper.scraped_data = [
        {
            "name": "Lilavati Hospital",
            "phone": "+91-22-2675-1000",
            "address": "A-791, Bandra Reclamation, Bandra West, Mumbai 400050",
            "rating": "4.5",
            "website": "lilavatihospital.com",
            "email": "info@lilavatihospital.com",
            "timing": "24/7",
            "services": "Multi-specialty Hospital, Emergency Care",
            "established": "1978",
            "scraped_at": "2025-01-11 08:45:54",
            "category": "Medical"
        },
        {
            "name": "Trishna Restaurant",
            "phone": "+91-22-2270-3213",
            "address": "7, Sai Baba Marg, Kala Ghoda, Fort, Mumbai 400001",
            "rating": "4.6",
            "website": "trishnaindia.com",
            "email": "info@trishnaindia.com",
            "timing": "12:00 PM - 3:30 PM, 7:00 PM - 11:30 PM",
            "services": "Seafood, Contemporary Indian",
            "established": "2008",
            "scraped_at": "2025-01-11 08:45:55",
            "category": "Restaurant"
        },
        {
            "name": "Gold's Gym Bandra",
            "phone": "+91-22-2640-8888",
            "address": "Linking Road, Bandra West, Mumbai 400050",
            "rating": "4.4",
            "website": "goldsgym.in",
            "email": "bandra@goldsgym.in",
            "timing": "5:30 AM - 11:30 PM",
            "services": "Premium Fitness, Personal Training",
            "established": "2003",
            "scraped_at": "2025-01-11 08:45:56",
            "category": "Fitness"
        }
    ]
    
    # Add enhanced data for demonstration
    for i, business in enumerate(scraper.scraped_data):
        business.update({
            'lead_score': [85, 78, 72][i],
            'priority_level': ['🔥 ULTRA HIGH', '⚡ HIGH', '⚡ HIGH'][i],
            'instagram': ['@lilavatihospital', '@trishnaindia', '@goldsgym_bandra'][i],
            'facebook': ['fb.com/lilavatihospital', 'fb.com/trishnaindia', 'fb.com/goldsgym'][i],
            'whatsapp_business': ['+91 22 2675 1000', '+91 22 2270 3213', '+91 22 2640 8888'][i],
            'owner_manager': ['Dr. Sharma', 'Mr. Patel', 'Ms. Singh'][i],
            'social_opportunities': ['Social media revival opportunity!', 'Already active - collaboration opportunity!', 'No Instagram presence - setup opportunity!'][i]
        })
    
    # Generate sample files in different formats
    print("🔥 Generating sample output files...")
    
    # Basic CSV
    csv_file = scraper.export_to_csv("sample_basic_leads", enhanced=False)
    print(f"✅ Generated: {csv_file}")
    
    # Enhanced CSV
    enhanced_csv = scraper.export_to_csv("sample_enhanced_leads", enhanced=True)
    print(f"✅ Generated: {enhanced_csv}")
    
    # JSON
    json_file = scraper.export_to_json("sample_leads", enhanced=True)
    print(f"✅ Generated: {json_file}")
    
    # TSV
    tsv_file = scraper.export_to_tsv("sample_leads", enhanced=True)
    print(f"✅ Generated: {tsv_file}")
    
    # VCF
    vcf_file = scraper.export_to_vcf("sample_contacts", enhanced=True)
    print(f"✅ Generated: {vcf_file}")
    
    print("\n🚀 All sample files generated successfully!")
    print("📁 Check the project directory for sample output files.")

if __name__ == "__main__":
    generate_samples()
