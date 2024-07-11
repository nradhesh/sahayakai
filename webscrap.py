from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,ar-EG;q=0.6,ar;q=0.5,hi-IN;q=0.4,hi;q=0.3',
    'origin': 'https://www.myscheme.gov.in',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-api-key': 'tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc',
}

def scrape_scheme_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the required information based on the provided HTML structure
        scheme_name = soup.find('h1', class_='font-bold text-green-600 text-xl sm:text-2xl mt-1 dark:text-green-500 dark:group-hover:text-green-400').text.strip() if soup.find('h1', class_='font-bold text-green-600 text-xl sm:text-2xl mt-1 dark:text-green-500 dark:group-hover:text-green-400') else 'N/A'
        detail = soup.find('div', id='details').text.strip() if soup.find('div', id='details') else 'N/A'
        benefit = soup.find('div', id='benefits').text.strip() if soup.find('div', id='benefits') else 'N/A'
        eligibility = soup.find('div', id='eligibility').text.strip() if soup.find('div', id='eligibility') else 'N/A'
        exclusion = soup.find('div', id='Exclusions').text.strip() if soup.find('div', id='Exclusions') else 'N/A'
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
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# List of scheme URLs to scrape
urls = [
    'https://www.myscheme.gov.in/schemes/dacsspostmsebcs',
    'https://www.myscheme.gov.in/schemes/aan',
    'https://www.myscheme.gov.in/schemes/pg-igssgc',
    'https://www.myscheme.gov.in/schemes/airavata',
    'https://www.myscheme.gov.in/schemes/nts-ug',
    'https://www.myscheme.gov.in/schemes/icdpsva-srgu',
    'https://www.myscheme.gov.in/schemes/dsctaecc',
    'https://www.myscheme.gov.in/schemes/acandabc',
    'https://www.myscheme.gov.in/schemes/akgbcsy',
    'https://www.myscheme.gov.in/schemes/icwf',
    'https://www.myscheme.gov.in/schemes/sjpfsgc',
    'https://www.myscheme.gov.in/schemes/jjoaps',
    'https://www.myscheme.gov.in/schemes/tdupw',
    'https://www.myscheme.gov.in/schemes/sapaandsdasdsggiapfafsd',
    'https://www.myscheme.gov.in/schemes/amrut',
    'https://www.myscheme.gov.in/schemes/safaew-bcew',
    'https://www.myscheme.gov.in/schemes/pmegp',
    'https://www.myscheme.gov.in/schemes/mgnrega',
    'https://www.myscheme.gov.in/schemes/ddskpdfs',
    'https://www.myscheme.gov.in/schemes/sbm-u'
]

# Initialize lists to store data
SchemeName = []
Details = []
Benefits = []
Eligibility = []
Exclusion = []
ApplicationProc = []
DocumentsReq = []
FAQ = []
Link = []
Keywords = []

# Scrape each URL and append data to lists
for url in urls:
    sample = scrape_scheme_page(url)
    if sample:
        SchemeName.append(sample['SchemeName'])
        Details.append(sample['Details'])
        Benefits.append(sample['Benefits'])
        Eligibility.append(sample['Eligibility'])
        Exclusion.append(sample['Exclusion'])
        ApplicationProc.append(sample['ApplicationProc'])
        DocumentsReq.append(sample['DocumentsReq'])
        FAQ.append(sample['FAQ'])
        Link.append(sample['Link'])
        Keywords.append(sample['Keywords'])

# Create a pandas DataFrame
df = pd.DataFrame({
    'SchemeName': SchemeName,
    'Details': Details,
    'Benefits': Benefits,
    'Eligibility': Eligibility,
    'Exclusion': Exclusion,
    'ApplicationProc': ApplicationProc,
    'DocumentsReq': DocumentsReq,
    'FAQ': FAQ,
    'Link': Link,
    'Keywords': Keywords
})

# Save DataFrame to CSV file on desktop
desktop_path = '/path/to/your/desktop/'  # Update with your desktop path
df.to_csv(desktop_path + 'scheme_data.csv', index=False)

print("Scraping and saving complete.")
