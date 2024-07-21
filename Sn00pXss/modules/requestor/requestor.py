from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from models import RequestModel
from modules.logger import error


class Requestor:
    """
    This class is responsible for sending requests to the target
    """

    def __init__(self):
        geko_driver_path = '/home/b3liott/Documents/Misc/chromedriver-linux64/chromedriver'  # TODO: put this in a yaml config file
        options = Options()
        options.binary_location = '/home/b3liott/Documents/Misc/chrome-linux64/chrome'
        options.add_argument("--headless")
        service = Service(geko_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)
        
    
    def send_request(self, requestModel: RequestModel, url=None) -> webdriver:
        try:
            if url is None:
                url = requestModel.url
          
            self.driver.get(url)  # TODO: remove this line

            # set cookies
            if requestModel.cookies is not None:
                for cookie in requestModel.cookies:
                    self.driver.add_cookie(cookie)

                self.driver.refresh()

            return self.driver
        
        except Exception as e:
            error(className=self.__class__.__name__, funcName='send_request', message=str(e))
            self.dispose()
            exit(1)


    def verify_reflected(self, requestModel: RequestModel) -> webdriver:
        return self.send_request(requestModel=requestModel, url=requestModel.affects)


    def dispose(self):
        self.driver.quit()