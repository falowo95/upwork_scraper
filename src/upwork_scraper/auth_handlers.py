import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
import os

# Urls
SECURITY_DEVICE_AUTH_URL = 'https://www.upwork.com/ab/account-security/device-authorization'
SECURITY_REENTER_PASSWORD_URL = 'https://www.upwork.com/ab/account-security/reenter-password'



def get_credentials():
    # Read the credentials from the JSON file
    creds = os.environ.get("SCRAPER_CREDS")
 
    with open(creds, "r") as json_file:
        credentials = json.load(json_file)
    return credentials


# Access the credentials
credentials = get_credentials()
USERNAME = credentials["USERNAME"]
PASSWORD = credentials["PASSWORD"]
SECRET_ANSWER = credentials["SECRET_ANSWER"]


def handle_security_check(func):
    """Handles any security check redirects that can occur during scraping."""
    def wrapper(driver: WebDriver, *args, **kwargs):
        print('Handling security check...')
        while True:
            try:
                return func(driver, *args, **kwargs)
            except NoSuchElementException as e:
                if SECURITY_DEVICE_AUTH_URL in driver.current_url:
                    print('Device auth page detected.')
                    handle_device_auth_security_check(driver)
                elif SECURITY_REENTER_PASSWORD_URL in driver.current_url:
                    print('Re-enter password page detected.')
                    handle_reenter_password_security_check(driver)
            except Exception as e:
                raise e
    return wrapper


def handle_device_auth_security_check(driver: WebDriver):
    """Enter the secret answer to the security question and authorize the device."""
    print('Handling device auth security check...')
    security_answer_input = driver.find_element('css selector', '#deviceAuth_answer')
    security_answer_input.send_keys(SECRET_ANSWER)
    authorize_button = driver.find_element('css selector', '#control_save')
    authorize_button.click()
    print('Device auth security check handled.')


def handle_reenter_password_security_check(driver: WebDriver):
    """Enter the password to the password check."""
    print('Handling re-enter password security check...')
    password_input = driver.find_element('css selector', '#sensitiveZone_password')
    password_input.send_keys(PASSWORD)
    authorize_button = driver.find_element('css selector', '#control_continue')
    authorize_button.click()
    print('Re-enter password security check handled.')


