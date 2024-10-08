from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
from models import RequestModel, CookieException
from modules.logger import error, info, warn
from time import sleep
import dotenv
import os


dotenv.load_dotenv()


class Requestor:
    """
    This class is responsible for sending requests to the target
    """

    def __init__(self, display: bool):
        chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
        options = Options()
        options.binary_location = os.getenv("CHROME_BINARY_PATH")
        options.add_argument('--incognito')
        if not display:
            options.add_argument("--headless")
        service = Service(chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)
        
    
    def set_cookies(self, cookies: dict):
        for name, value in cookies.items():
            current_cookie = self.driver.get_cookie(name=name)
            value = value.replace(' ', '')
            try:
                self.driver.add_cookie({'name': name, 'value': value, 'path': current_cookie['path']})
            except Exception:
                raise CookieException(f"Cookie ({name}:{value}) not set. It might contains some special characters which makes the cookie invalid, or try again to ensure that the browser had the time to set cookies.")

    def get_cookies(self):
        try:
            return self.driver.get_cookies()
        except Exception as e:
            error(funcName='get_cookies', message=str(e))
            return []

    def send_request(self, requestModel: RequestModel, url=None):
        try:
            if url is None:
                url = requestModel.url
            self.driver.get(url)

            if len(requestModel.cookies) > 0:
                self.set_cookies(cookies=requestModel.cookies)
                self.driver.refresh()

        except Exception as e:
            error(funcName='send_request', message=str(e))
            self.dispose()
            exit(1)


    def get_affected(self, requestModel: RequestModel):
        self.send_request(requestModel=requestModel, url=requestModel.affects)


    def clear_alerts(self):
        while True:
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                info(message="alert cleared") 

            except NoAlertPresentException:
                return


    def dispose(self):
        self.driver.quit()
