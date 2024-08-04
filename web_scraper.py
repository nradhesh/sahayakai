from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

def setup_selenium(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def extract_links_from_page(driver, wait):
    links = []
    divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.p-4.lg\\:p-8.w-full")))
    for div in divs:
        try:
            a_tag = div.find_element(By.XPATH, ".//h2/a")
            link = a_tag.get_attribute("href")
            if link:
                links.append(link)
        except Exception as e:
            print(f"Error finding link in div: {e}")
    return links

def scrape_all_links(driver, wait, base_url):
    all_links = []
    driver.get(base_url)
    
    while True:
        all_links.extend(extract_links_from_page(driver, wait))
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ml-2.text-darkblue-900.dark\\:text-white.cursor-pointer")))
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)  # Wait for scrolling to complete
            next_button.click()
            time.sleep(1.5)  # Adjust the sleep time if needed to allow the next page to load properly
        except Exception as e:
            #print("No more pages or error navigating to the next page. Stopping.")
            break
    
    driver.quit()
    print(f"Scraped {len(all_links)} links.")
    return list(set(all_links))  # Ensure uniqueness

def requests_session_with_retries(retries=3, backoff_factor=1):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(429, 500, 502, 503, 504),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def scrape_scheme_page(session, url):
    retries = 5
    delay = 1  # initial delay in seconds
    for i in range(retries):
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 429:
                print(f"Rate limit hit. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # exponential backoff
                continue
            elif response.status_code != 200:
                print(f"Failed to fetch {url} with status code {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            scheme_name = soup.find('h1', class_="font-bold text-xl sm:text-2xl mt-1 text-[#24262B] dark:text-white").text.strip() if soup.find('h1', class_="font-bold text-xl sm:text-2xl mt-1 text-[#24262B] dark:text-white") else 'N/A'
            detail = soup.find('div', id='details').text.strip() if soup.find('div', id='details') else 'N/A'
            benefit = soup.find('div', id='benefits').text.strip() if soup.find('div', id='benefits') else 'N/A'
            eligibility = soup.find('div', id='eligibility').text.strip() if soup.find('div', id='eligibility') else 'N/A'
            exclusion = soup.find('div', id='exclusions').text.strip() if soup.find('div', id='exclusions') else 'N/A'
            application_process = soup.find('div', id='application-process').text.strip() if soup.find('div', id='application-process') else 'N/A'
            documents_required = soup.find('div', id='documents-required').text.strip() if soup.find('div', id='documents-required') else 'N/A'
            faq = soup.find('div', id='faqs').text.strip() if soup.find('div', id='faqs') else 'N/A'
            keyword = soup.find('div', class_='mb-2 md:mb-0 w-full').text.strip() if soup.find('div', class_='mb-2 md:mb-0 w-full') else 'N/A'
            
            return {
                'SchemeName': scheme_name,
                'Details': detail,
                'Benefits': benefit,
                'Eligibility': eligibility,
                'Exclusion': exclusion,
                'ApplicationProc': application_process,
                'DocumentsReq': documents_required,
                'FAQ': faq,
                'Link': url,
                'Keywords': keyword
            }
        except requests.RequestException as e:
            print(f"Request error scraping {url}: {e}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return None

def main():
    base_url = "https://www.myscheme.gov.in/search"    
    # Setup Selenium and extract links
    driver, wait = setup_selenium()
    all_links = scrape_all_links(driver, wait, base_url)

    print(f"Unique {len(all_links)} links.")

    # Load existing data if available
    if os.path.exists('scheme_sample3.csv'):
        existing_data = pd.read_csv('scheme_sample3.csv')
    else:
        existing_data = pd.DataFrame()
    
    # Initialize lists to store new data
    new_data = []

    # Create a requests session with retries
    session = requests_session_with_retries()

    # Use ThreadPoolExecutor to manage concurrent scraping
    with ThreadPoolExecutor(max_workers=20) as executor:  # Increased workers for faster scraping
        futures = [executor.submit(scrape_scheme_page, session, url) for url in all_links]
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                new_data.append(result)
                print(f"Scraped data from {result['Link']}")
                time.sleep(random.uniform(0.5, 1.5))  # Reduced sleep to speed up processing

    # Create a pandas DataFrame for new data
    new_data_df = pd.DataFrame(new_data)
    print(f"Scraped data for {len(new_data_df)} schemes.")

    # Combine new data with existing data
    if not existing_data.empty:
        combined_data = pd.concat([existing_data, new_data_df])
    else:
        combined_data = new_data_df

    # Remove duplicates and keep the latest
    combined_data = combined_data.drop_duplicates(keep='last')
    
    # Remove duplicates based on 'SchemeName' and keep the latest
    combined_data = combined_data.sort_values('Link').drop_duplicates(subset=['SchemeName'], keep='last')

    # Save the combined data to CSV file
    combined_data.to_csv('scheme_sample3.csv', index=False)
    print("Scraping and updating complete. Data saved to scheme_sample3.csv.")

if __name__ == "__main__":
    main()
