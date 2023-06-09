from datetime import datetime
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import WebDriver
from upwork_scraper.auth_handlers import handle_security_check






# Urls
LOGIN_URL = 'https://www.upwork.com/ab/account-security/login'
MAIN_PORTAL_URL = 'https://www.upwork.com/nx/find-work/best-matches'
SETTINGS_CONTACTINFO_URL = 'https://www.upwork.com/freelancers/settings/contactInfo'
SETTINGS_DEFAULT_URL = SETTINGS_CONTACTINFO_URL
SETTINGS_TAXINFO_URL = 'https://www.upwork.com/nx/tax/'
SETTINGS_PROFILE_URL = 'https://www.upwork.com/freelancers/~'




def start_driver() -> WebDriver:
 
    """Starts the Chrome driver and returns it."""
    print('Starting Chrome driver...')
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage"),
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',options=chrome_options)
    print('Chrome driver started.')
    return driver






def login_to_upwork(driver: WebDriver, username: str, password: str, secret_answer: str):
    """
    Logs in to Upwork using the provided credentials.

    Args:
        driver (WebDriver): The WebDriver instance for browser automation.ls
        
        username (str): The Upwork username.
        password (str): The Upwork password.
        secret_answer (str): The secret answer, if required.

    Returns:
        None
    """
    print('Logging in...')
    driver.get(LOGIN_URL)
    handle_cookie_dialogue_box(driver)
    submit_username(driver, username)
    submit_password(driver, password)
    print('Should be logged in now.')
    print(driver.current_url)
    try:
        submit_secret_answer(driver, secret_answer)
        print("i am in")
    except NoSuchElementException as e:
        print('No secret answer required or login. Skipping...')
    


def handle_cookie_dialogue_box(driver: WebDriver):
    """
        Handles the cookie dialogue box, if present.

    Args:
        driver (WebDriver): The WebDriver instance for browser automation.

    Returns:
        None
    
    """
    print('Closing cookie dialog box.')
    driver.implicitly_wait(30)  # Wait for it to popup.
    accept_button = driver.find_element('css selector', '#onetrust-accept-btn-handler')
    while True:
        try:
            accept_button.click()
            print('Cookie dialog box closed.')
            break
        except ElementClickInterceptedException as e:
            feedback = 'Click intercepted. Retrying...'
            print(feedback)
            time.sleep(1)
        except Exception as e:
            raise e


def submit_username(driver: WebDriver, username: str):
    """
    Submits the username field on the login page.

    Args:
        driver (WebDriver): The WebDriver instance for browser automation.
        username (str): The Upwork username.

    Returns:
        None
    """
    print('Submitting username...')
    username_field = driver.find_element('css selector', '#login_username')
    username_field.send_keys(username)
    continue_with_email_button = driver.find_element('css selector', '#login_password_continue')
    continue_with_email_button.click()
    print('Username submitted.')


def submit_password(driver: WebDriver, password: str):
    """
    Submits the password field on the login page.

    Args:
        driver (WebDriver): The WebDriver instance for browser automation.
        password (str): The Upwork password.

    Returns:
        None
    """
    print('Submitting password...')
    driver.implicitly_wait(30)
    while True:
        try:
            password_field = driver.find_element('css selector', '#login_password')
            password_field.send_keys(password)
            print('Password submitted.')
            break
        except (StaleElementReferenceException, ElementNotInteractableException) as e:
            print(f'Error: {e}')
            print(f'Retrying...')
            time.sleep(1)
        except Exception as e:
            raise e
    login_button = driver.find_element('css selector', '#login_control_continue')
    login_button.click()


def submit_secret_answer(driver: WebDriver, secret_answer: str):
    """
    Submits the secret answer field on the login page.

    Args:
        driver (WebDriver): The WebDriver instance for browser automation.
        secret_answer (str): The secret answer, if required.

    Returns:
        None
    """
    print('Submitting secret answer...')
    driver.implicitly_wait(30)
    secret_answer_field = driver.find_element('id', 'login_answer')
    secret_answer_field.send_keys(secret_answer)
    secret_answer_submit_button = driver.find_element('id', 'login_control_continue')
    secret_answer_submit_button.click()
    print('Secret answer submitted.')


def scrape_main_portal_page(driver: WebDriver) -> dict:
    print('Scraping main portal page...')
    if driver.current_url != MAIN_PORTAL_URL:
        print('Not on main portal page. Going there now...')
        driver.get(MAIN_PORTAL_URL)
    remove_profile_completeness_popup(driver)
    name = driver.find_element('css selector', '#fwh-sidebar-profile > div > h3 > a').text
    first_name, last_name = name.split(' ')
    title = driver.find_element('css selector', '#fwh-sidebar-profile > div > p').text
    available_connects_selector = '#main > div.container > div.row.app-frame > aside > div > div.up-card.mt-0.py-0 > section:nth-child(3)'
    available_connects = int(driver.find_element('css selector', available_connects_selector).text.split(' ')[0])
    hours_per_week = driver.find_element( 'css selector', '#main > div.container > div.row.app-frame > aside > div > div.up-card.mt-0.py-0 > section:nth-child(4) > div:nth-child(2) > div.pb-20 > span > span').text
    profile_visibility = driver.find_element('css selector', '#main > div.container > div.row.app-frame > aside > div > div.up-card.mt-0.py-0 > section:nth-child(4) > div:nth-child(3) > span').text
    print('Main portal page scraped.')
    data =  {
        "abbreviated_name": name,
        "first_name": first_name,
        "last_name_initial": last_name,
        "title": title,
        "available_connects": available_connects,
        "hours_per_week": hours_per_week,
        "profile_visibility": profile_visibility,
    }
    with open("main_portal_data.json", "w") as json_file:
        json.dump(data, json_file)


def remove_profile_completeness_popup(driver: WebDriver):
    """Remove the profile completeness pop-up modal if it exists."""
    print('Removing profile completeness pop-up modal...')
    modal = driver.find_element('xpath', '//*[@id="main"]/div[2]/div[4]/aside/div/div[1]/div/section/div[2]/div[1]')
    modal_parent = modal.find_element('xpath', '..')
    driver.execute_script('arguments[0].remove()', modal_parent)
    print('Profile completeness pop-up modal removed.')


def scrape_settings(driver: WebDriver) -> dict:
    contact_info_data = scrape_settings_contactinfo(driver)
    tax_info_data = scrape_settings_taxinfo(driver)
    profile_data = scrape_settings_profile(driver)
    return {
        **profile_data,
        **contact_info_data,
        **tax_info_data,
    }


@handle_security_check
def scrape_settings_contactinfo(driver: WebDriver) -> dict:
    """Scrapes the settings page and returns the data as a dictionary."""
    print('Scraping settings Contact Info page...')
    if driver.current_url != SETTINGS_CONTACTINFO_URL:
        driver.get(SETTINGS_CONTACTINFO_URL)
    user_id = driver.find_element('css selector', '#main > div > div > div.col-md-9 > main > div:nth-child(2) > section > div:nth-child(1) > div:nth-child(2)').text

    # Get full name
    full_name = driver.find_element('css selector', '#main > div > div > div.col-md-9 > main > div:nth-child(2) > section > div:nth-child(2) > div:nth-child(2)').text

    # Compensate for different name formats
    if len(full_name.split()) == 2:
        first_name, last_name = full_name.split()
    elif len(full_name.split()) == 3:
        first_name, _, last_name = full_name.split()
    else:
        first_name = full_name
        last_name = None
    edit_button = driver.find_element('css selector', '#main > div > div > div.col-md-9 > main > div:nth-child(2) > header > button')
    edit_button.click()
    email_field = driver.find_element('css selector', '#main > div > div > div.col-md-9 > main > div:nth-child(2) > section > div:nth-child(2) > div:nth-child(3) > input')
    email = email_field.get_attribute('value')
    address = driver.find_element('css selector', '#main > div > div > div.col-md-9 > main > div:nth-child(4) > section > div:nth-child(2) > div:nth-child(2)').text
    street_address, city_state_zip, country = address.splitlines()
    city, state = city_state_zip.split(', ')
    if len(state.split()) == 2:
        zip_code = state.split()[1]
    else:
        zip_code = None
    phone_number = driver.find_element('css selector', '#main > div > div > div.col-md-9 > main > div:nth-child(4) > section > div:nth-child(3) > div:nth-child(2)').text
    print('Settings Contact Info page scraped.')
    return {
        'id': user_id,
        'full_name': full_name,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'address': {
            'city': city,
            'country': country,
            'line1': street_address,
            'line2': None,
            'postal_code': zip_code,
            'state': state,
        },
        'phone_number': phone_number,
    }
            

@handle_security_check
def scrape_settings_taxinfo(driver: WebDriver) -> dict:
    print('Scraping settings Tax Info page...')
    if driver.current_url != SETTINGS_TAXINFO_URL:
        driver.get(SETTINGS_TAXINFO_URL)
    ssn = driver.find_element('css selector', '#tax-info-form > section > div > div.up-form-group.mb-0 > div > span').text
    print('Settings Tax Info page scraped.')
    return {'ssn': ssn}


@handle_security_check
def scrape_settings_profile(driver: WebDriver) -> dict:
    print('Scraping settings Profile page...')
    # SETTINGS_PROFILE_URL is a dynamic url, so you can't have the full url to check until you're already in the settings pages, you need to grab it from the profile page link in the settings.
    if SETTINGS_PROFILE_URL not in driver.current_url:
        driver.get(SETTINGS_DEFAULT_URL)
        profile_url = driver.find_element('css selector', '#main > div > div > div.col-md-3 > div > nav > div > div:nth-child(2) > ul > li.up-settings-list-item.up-settings-list-item-userProfile > a').get_attribute('href')
        print(profile_url)
        driver.get(profile_url)
    account_id = driver.current_url.split('/')[-1][1:]
    picture_url = driver.find_element('css selector', '#main > div.container > div:nth-child(4) > div > div > div > div:nth-child(3) > div.up-card.py-0.my-0.d-none.d-lg-block > section.up-card-section.py-30 > div > div:nth-child(1) > div:nth-child(1) > div > div.mr-10.mr-lg-30.position-relative > div > div > img').get_attribute('src')
    job_title = driver.find_element('css selector', '#main > div.container > div:nth-child(4) > div > div > div > div:nth-child(3) > div.up-card.py-0.my-0.d-none.d-lg-block > section.row > div.col.min-width-0 > section:nth-child(1) > div.mb-30 > div > div:nth-child(1) > h2').text
    amount = driver.find_element('css selector', '#main > div.container > div:nth-child(4) > div > div > div > div:nth-child(3) > div.up-card.py-0.my-0.d-none.d-lg-block > section.row > div.col.min-width-0 > section:nth-child(1) > div.mb-30 > div > div.d-flex.align-items-center.col.col-auto > div:nth-child(1) > h3 > span').text
    period = 'hourly'
    currency = 'USD'
    employement_history_list = driver.find_element('css selector', '#main > div.container > div:nth-child(4) > div > div > div > div:nth-child(3) > div:nth-child(8) > section > div > ul')

    # Get employment info
    employment_status = None
    employer = None
    hire_date = None
    if employement_history_list:
        # Find the li tags
        employment_history_lis = employement_history_list.find_elements('css selector', 'li')
        for employment_history_li in employment_history_lis:
            employment_range = employment_history_li.find_element('css selector', 'div.mt-10.text-muted').text
            employment_status = 'active' if 'Present' in employment_range else 'inactive'
            if employment_status == 'active':
                employer = employment_history_li.find_element('tag name', 'h4').text.split('|')[-1].strip()
                hire_date_str = employment_range.split(' - ')[0]
                hire_date = datetime.strptime(hire_date_str, '%B %Y').date()
                break
    print('Settings Profile page scraped.')
    return {
        'account': account_id,
        'job_title': job_title,
        'base_pay': {
            'amount': amount,
            'period': period,
            'currency': currency,
        },
        'picture_url': picture_url,
        'employment_status': employment_status,
        'employer': employer,
        'hire_date': hire_date,
    }



