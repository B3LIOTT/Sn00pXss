from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from models import RequestModel
from modules.logger import error
import os
import dotenv


dotenv.load_dotenv()


class Requestor:
    """
    This class is responsible for sending requests to the target
    """

    def __init__(self):
        chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
        options = Options()
        options.binary_location = os.getenv("CHROME_BINARY_PATH")
        options.add_argument("--headless")  # comment this line to see the browser
        service = Service(chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)
        
    
    def send_request(self, requestModel: RequestModel, url=None):
        try:
            if url is None:
                url = requestModel.url
          
            self.driver.get(url)

            # set cookies
            if requestModel.cookies is not None:
                for cookie in requestModel.cookies:
                    self.driver.add_cookie(cookie)

                self.driver.refresh()
        
        except Exception as e:
            error(className=self.__class__.__name__, funcName='send_request', message=str(e))
            self.dispose()
            exit(1)


    def get_affected(self, requestModel: RequestModel):
        self.send_request(requestModel=requestModel, url=requestModel.affects)


    def dispose(self):
        self.driver.quit()