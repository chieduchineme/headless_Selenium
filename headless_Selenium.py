import pickle
import requests
from bs4 import BeautifulSoup
# from constants import collab_url, cookies_filepath, end_flag
from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Function to initialize the webdriver
def init_driver():
    import sys
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

    from selenium import webdriver
    import chromedriver_autoinstaller

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') # this is must
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to search on Google and get the first TripAdvisor link
def get_tripadvisor_link(query):
    wd = init_driver()
    wd.get("https://www.google.com")

    search_box = wd.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    sleep(2)  # Wait for results to load

    # Get the first result link
    first_result = wd.find_element(By.CSS_SELECTOR, 'h3')
    first_result.click()  # Click on the first result
    sleep(2)  # Wait for the page to load

    tripadvisor_url = wd.current_url
    wd.quit()
    return tripadvisor_url

# Function to scrape reviews from TripAdvisor
def scrape_tripadvisor_reviews(url):
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)

    # Find the review containers
    reviews = soup.find_all('div', class_='review-container', limit=2)

    for review in reviews:
        review_text = review.find('p', class_='partial_entry').get_text(strip=True)
        print("Review:", review_text)

        # Finding the response (if available)
        response_text = review.find('div', class_='mgrRspnInline')
        if response_text:
            print("Response:", response_text.get_text(strip=True))
        print("---")

if __name__ == "__main__":
    query = "BARCELO SANTS Trip Advisor"

    # Get TripAdvisor link
    tripadvisor_link = get_tripadvisor_link(query)
    print("TripAdvisor URL:", tripadvisor_link)

    # Scrape reviews
    scrape_tripadvisor_reviews(tripadvisor_link)

#
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller

# Initialize the Selenium WebDriver
def init_driver():
    chromedriver_autoinstaller.install()  # Automatically installs the Chrome driver
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = ChromeService()  # Use the Chrome driver service
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Function to search for the hotel and navigate to the amenities page
def search_and_navigate_to_amenities(hotel_name):
    driver = init_driver()

    # Perform Google Search with "Hotel" + input + "About"
    search_url = "https://www.google.com/"
    driver.get(search_url)

    search_box = driver.find_element(By.NAME, "q")
    search_query = f"Hotel {hotel_name} About"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)  # Wait for results to load

    try:
        # Find the div with role="complementary" (this is where the Knowledge Panel data is located)
        complementary_div = driver.find_element(By.XPATH, "//div[@role='complementary']")

        # Find the first link within the complementary div
        first_link = complementary_div.find_element(By.TAG_NAME, 'a')
        href_value = first_link.get_attribute('href')
        print(f"Navigating to: {href_value}")

        # Navigate to the href
        driver.get(href_value)
        time.sleep(2)  # Wait for the page to load

        # Now locate the "Amenities" section on the new page
        try:
            amenities_section = driver.find_element(By.XPATH, "//h3[contains(text(), 'Amenities')]/following-sibling::div")
            subheaders = amenities_section.find_elements(By.XPATH, ".//div[contains(@class, 'subheader')]")

            print("\nAmenities Information:")
            for subheader in subheaders:
                subheader_title = subheader.find_element(By.TAG_NAME, 'h4').text
                subheader_content = subheader.find_element(By.TAG_NAME, 'p').text
                print(f"{subheader_title}: {subheader_content}")

        except Exception as e:
            print("Could not find the amenities section:", e)

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()  # Close the browser session

if __name__ == "__main__":
    hotel_name = "Barceló Sants"  # Hotel name input
    search_and_navigate_to_amenities(hotel_name)
