import pytest
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from upwork_scraper.helper_Functions import start_driver

from upwork_scraper.helper_Functions import start_driver
from upwork_scraper.helper_Functions import login_to_upwork,scrape_main_portal_page
from upwork_scraper.auth_handlers import get_credentials

@pytest.fixture
def driver():
    print('Setting up Chrome driver...')
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--headless=new')
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument('--log-level=3')
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    service.start()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    print('Tearing down Chrome driver...')
    

credentials = get_credentials()
# Access the credentials
USERNAME = credentials["USERNAME"]
PASSWORD = credentials["PASSWORD"]
SECRET_ANSWER = credentials["SECRET_ANSWER"]

def test_start_driver(driver):
    # Test if the driver starts successfully
    assert "data:," in driver.current_url

def test_login_to_upwork(driver):
    login_to_upwork(driver,USERNAME,PASSWORD,SECRET_ANSWER)

    assert "https://www.upwork.com/nx/find-work/best-matches" in driver.current_url

    
def test_scrape_main_portal_page(driver):
    scrape_main_portal_page(driver)

    assert "https://www.upwork.com/nx/find-work/best-matches" in driver.current_url

    driver.quit()
