from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Function to extract links from the current page
def extract_links_from_page():
    links = []
    # Find all divs with class 'p-4 lg:p-8 w-full'
    divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.p-4.lg\\:p-8.w-full")))
    for div in divs:
        try:
            # Within each div, find the h2 tag and then the a tag within it
            a_tag = div.find_element(By.XPATH, ".//h2/a")
            link = a_tag.get_attribute("href")
            if link:
                links.append(link)
        except Exception as e:
            print(f"Error finding link in div: {e}")
    return links

# Open the initial URL
driver.get("https://www.myscheme.gov.in/search")

all_links = []

# Loop through each page and extract links
for page_num in range(1,242):  # Adjust this range to the number of pages you have
    all_links.extend(extract_links_from_page())
    try:
        # Find the current page number
        current_page_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.bg-green-700")))  # This selector should find the current active page
        current_page_number = int(current_page_element.text)

        # Find the ul element containing the page numbers
        pagination_ul = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list-none.flex.flex-wrap.items-center.justify-center")))

        # Find the next page number element within the ul
        next_page_element = pagination_ul.find_element(By.XPATH, f".//li[text()='{current_page_number + 1}']")

        # Scroll the next page element into view and click it
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page_element)
        time.sleep(1)  # Wait for scrolling to complete

        # Click the next page element
        driver.execute_script("arguments[0].click();", next_page_element)
        time.sleep(2)  # Adjust the sleep time if needed to allow the next page to load properly
    except Exception as e:
        print(f"Error navigating to the next page on page {page_num}: {e}")
        break

# Save links to a file
with open("extracted_links.txt", "w") as f:
    for link in all_links:
        f.write(link + "\n")

# Close the WebDriver
driver.quit()

print(f"Scraped {len(all_links)} links.")
