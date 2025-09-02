# Gemini's Web Scraping Project Plan

This document outlines the detailed steps to transform the existing `lead-generator` project from a hardcoded data simulator into a functional web scraper for Google Maps business listings.

## Project Goal:
To enable the `cli_scraper.py` script to fetch real-time business data from Google Maps based on user queries, rather than relying on internal hardcoded datasets.

## Core Constraints & Considerations:
*   **Current "Zero Dependencies" Status:** The existing project explicitly avoids external libraries. Implementing web scraping will necessitate introducing new dependencies. This is a fundamental shift in the project's architecture.
*   **Google Maps' Dynamic Nature:** Google Maps is a highly dynamic, JavaScript-rendered application. This implies that simple HTTP requests might not suffice, and a headless browser solution (like Selenium or Playwright) might be required.
*   **Anti-Bot Measures:** Google actively employs measures to prevent automated scraping. This will require implementing strategies to mimic human behavior and avoid detection.
*   **Ethical Considerations:** Scraping should be done responsibly, respecting `robots.txt` (though Google Maps doesn't typically have one for its search results) and avoiding excessive load on servers.

---

## Detailed Steps:

### Step 1: Initial Setup & Dependency Management
1.  **Create `requirements.txt`:** Introduce a `requirements.txt` file to manage new Python dependencies.
2.  **Add Core Scraping Libraries:**
    *   `requests`: For making HTTP requests to fetch web page content.
    *   `beautifulsoup4`: For parsing HTML content and extracting data.
    *   `selenium`: (Conditional, but highly likely needed for Google Maps) For browser automation to handle JavaScript rendering.
    *   `webdriver_manager`: (If using Selenium) To automatically manage browser drivers (e.g., ChromeDriver).
3.  **Update `cli_scraper.py` Imports:** Add necessary import statements for the new libraries.

### Step 2: Understanding Google Maps Structure & Data Identification
1.  **Manual Inspection:** Manually perform searches on Google Maps (e.g., "cafes in kolkata") in a web browser.
2.  **Developer Tools Analysis:** Use browser developer tools (Inspect Element) to:
    *   Examine the HTML structure of search results pages.
    *   Identify unique HTML elements (tags, classes, IDs) that contain business names, addresses, phone numbers, websites, ratings, etc.
    *   Observe how pagination works (e.g., "Next" button, URL changes).
    *   Note how individual business details are loaded (e.g., clicking on a listing might load details dynamically).
3.  **URL Pattern Analysis:** Understand how Google Maps constructs its search URLs based on query and location.

### Step 3: Implementing Basic Scraping Logic (Replacing Hardcoded Data)
1.  **Refactor `get_business_data`:** Completely remove the hardcoded data within this method.
2.  **Construct Search URL:** Based on the user's `query` and `location`, dynamically build the Google Maps search URL.
3.  **Fetch Page Content:**
    *   **Option A (requests/BeautifulSoup):** Attempt to fetch the page using `requests`. If the content is not fully rendered (due to JavaScript), this approach will be insufficient.
    *   **Option B (Selenium/Playwright - Recommended for Google Maps):** Initialize a headless browser (e.g., Chrome). Navigate to the constructed URL. Wait for the page to fully load and render its JavaScript content.
4.  **Parse HTML and Extract Listings:**
    *   Use `BeautifulSoup` (with the HTML obtained from `requests` or `Selenium`) to find all elements representing individual business listings on the search results page.
    *   Iterate through each listing element.
5.  **Extract Business Details:** For each listing, extract the following data points using `BeautifulSoup`'s methods (e.g., `find`, `find_all`, `get_text`, `get` attributes):
    *   `name`
    *   `phone`
    *   `address`
    *   `rating`
    *   `website`
    *   `email` (if visible on the search results page, often not)
    *   `timing` (if visible)
    *   `services` (if visible)
    *   `established` (unlikely to be on search results, might require clicking into individual listings)
    *   `category` (can be inferred or extracted if present)
    *   `google_maps_link` (can be constructed from the listing's URL or ID)
6.  **Populate `self.scraped_data`:** Store the extracted data in the `self.scraped_data` list, ensuring it matches the expected dictionary structure.

### Step 4: Handling Pagination
1.  **Identify Next Page Mechanism:** Determine how to navigate to the next page of search results (e.g., a "Next" button, a specific URL parameter).
2.  **Implement Loop:** Create a loop that continues fetching and parsing pages until no more results or next pages are found.
3.  **Dynamic URL Updates:** If pagination involves changing URL parameters, update the URL for the next request.
4.  **Selenium Interaction (if applicable):** If using Selenium, simulate clicks on "Next" buttons or scroll to trigger lazy loading.

### Step 5: Implementing Robustness & Ethical Considerations
1.  **Error Handling:**
    *   Implement `try-except` blocks for network errors, parsing errors (e.g., element not found), and potential anti-bot blocks.
    *   Log errors for debugging.
2.  **Rate Limiting/Delays:** Introduce `time.sleep()` calls between requests to avoid overwhelming the server and to mimic human browsing patterns. Randomize delays for better evasion.
3.  **User-Agent Rotation:** (Advanced) Use a list of common browser user-agents and rotate them with each request to appear as different users.
4.  **Proxy Rotation:** (Advanced, if getting blocked) Use a pool of proxy IP addresses to route requests through different locations.
5.  **Headless Browser Configuration:** If using Selenium, configure it to run in headless mode (without a visible browser window) for efficiency.

### Step 6: Data Enhancement & Advanced Features (Re-evaluation)
1.  **Review Existing Enhancement Logic:** The current `analyze_leads_advanced` method and related functions (`calculate_lead_score`, `find_social_media`, `find_additional_contacts`, `analyze_hyper_local_micro_targeting`) rely on the completeness of the `business` dictionary.
2.  **Dynamic Data for Enhancements:**
    *   **Social Media/Email:** If social media handles or emails are not directly available on the search results page, consider:
        *   **Individual Page Scraping:** Clicking into each business listing and scraping its dedicated page for more details (significantly increases scraping time and complexity).
        *   **External APIs:** Using third-party APIs for social media lookup or email verification (requires API keys and might incur costs).
        *   **Maintaining Simulation:** Continue to simulate these details if real-time retrieval is too complex or costly.
    *   **Lead Scoring:** Ensure the `calculate_lead_score` function can work with the newly scraped data (e.g., handling `N/A` values for missing fields).
    *   **Hyper-Local Micro-Targeting:** This feature relies on addresses. Ensure addresses are accurately scraped and parsed.

### Step 7: Output & Export (Adaptation)
1.  **Existing Export Functions:** The `export_to_csv`, `export_to_json`, `export_to_tsv`, and `export_to_vcf` methods should largely work as-is, as they process the `self.scraped_data` list.
2.  **Field Mapping:** Ensure that the keys in the scraped business dictionaries (`name`, `phone`, etc.) match the `fieldnames` expected by the export functions.

### Step 8: Testing, Debugging & Maintenance
1.  **Unit Testing (if applicable):** Write tests for the new scraping functions.
2.  **End-to-End Testing:** Run the script with various queries and verify the output.
3.  **Debugging:** Use print statements, logging, and browser developer tools to debug issues.
4.  **Continuous Maintenance:** Web scraping is an ongoing task. Websites change their structure, and anti-bot measures evolve. The scraper will require regular updates and maintenance.

---

This plan provides a comprehensive roadmap. We will start with Step 1.
