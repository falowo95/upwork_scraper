
import fire
from selenium.webdriver.remote.webdriver import WebDriver

from upwork_scraper.datatypes import UpworkAccount
from upwork_scraper.auth_handlers import get_credentials
from upwork_scraper.helper_Functions import *


class upworkCli:
    @staticmethod
    def main() -> WebDriver:
        """Main function to run the program."""


        credentials = get_credentials()

        # Access the credentials
        USERNAME = credentials["USERNAME"]
        PASSWORD = credentials["PASSWORD"]
        SECRET_ANSWER = credentials["SECRET_ANSWER"]
        
        """Main function to run the program."""
        driver = start_driver()

        login_to_upwork(driver, USERNAME, PASSWORD, SECRET_ANSWER)

        # Level 1
        scrape_main_portal_page(driver)

        # Level 2
        settings_data = scrape_settings(driver)
        account = UpworkAccount(**settings_data)

        # Write level 2 data to file.
        open(f'{account.id}.json', 'w').write(account.to_json())
        
        driver.close()



def entry():
    fire.Fire(upworkCli)












