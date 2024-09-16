from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver (make sure to specify the path to your WebDriver executable)
driver = webdriver.Chrome()

try:
    # Navigate to Google
    driver.get("https://www.google.com")

    # Find the search box element
    search_box = driver.find_element(By.NAME, "q")

    # Enter a search query
    search_box.send_keys("Selenium WebDriver")

    # Submit the search query
    search_box.send_keys(Keys.RETURN)

    # Wait for a few seconds to see the results
    time.sleep(5)

finally:
    # Close the browser
    driver.quit()
