
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
from pathlib import Path

# Define path
PROJECT_ROOT = Path(__file__).parent  # Path to the current script's directory
CONTENT_DIR = PROJECT_ROOT / "content"
OUTPUT_FILE = CONTENT_DIR / "hites_comments.csv"
URLS_FILE = CONTENT_DIR / "test_hites_urls.txt"

# Load URLs
urls = []
try:
    with open(URLS_FILE, 'r') as f:
        for line in f:
            urls.append(line.strip())
except FileNotFoundError:
    print(f"Error: URL file not found at {URLS_FILE}")
    exit()

# Selenium setup
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

# Initialize driver
driver = webdriver.Chrome(options=options) # Consider using webdriver_manager

all_comments = []

try:
    for url in urls:
        print(f"Scraping comments from: {url}")
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "yotpo-review"))) # Wait for at least one review

        while True:
            time.sleep(2) # Delay to ensure elements render

            try:
                category_element = driver.find_element(By.CLASS_NAME, "breadcrumb-item")
                category = category_element.text
            except NoSuchElementException:
                print("Category element not found.")
                category = "Unknown"

            comments = driver.find_elements(By.CLASS_NAME, "yotpo-review")
            for comment in comments:
                comment_data = {'category': category} # Initialize comment data
                try:
                    comment_data['author'] = comment.find_element(By.CLASS_NAME, "yotpo-user-name").text
                    comment_data['text'] = comment.find_element(By.CLASS_NAME, "content-review").text
                    comment_data['rating'] = comment.find_element(By.CLASS_NAME, "sr-only").text

                except NoSuchElementException:
                    print("Some review elements not found, skipping this review.")
                    continue  # Skip to the next comment

                all_comments.append(comment_data)

            try:
                next_button = driver.find_element(By.XPATH, '//a[@class="yotpo-page-element yotpo-icon yotpo-icon-right-arrow yotpo_next " and @aria-label="Next Page"]')
                driver.execute_script("arguments[0].scrollIntoView();", next_button)

                next_button.click()
            except (NoSuchElementException, TimeoutException):
                print("No more comment pages or next button not found.")
                break # Exit the inner loop

except Exception as e:
  print(f"An error occurred during scraping: {e}")

finally:
    driver.quit() # Close WebDriver session

# Create and clean DataFrame
df = pd.DataFrame(all_comments)
for index, row in df.iterrows():
    if row['author'] == '' or row['text'] == '' or row['rating'] == '':
        df.drop(index, inplace=True)

# Save to CSV
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')

print(f"Comments saved to: {OUTPUT_FILE}")