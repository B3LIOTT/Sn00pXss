from modules.requestor.requestor import Requestor
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from models import RequestModel
from time import sleep


TEST_INPUT = "!!ABCDEFGHTESTHGFEDCBA!!"

TEST_PAYLOAD = """'; alert("xss dom based"); var cat= ' """


def detect_xss(requestor: Requestor, requestModel: RequestModel):
    driver = requestor.send_request(requestModel=requestModel)

    number_input = driver.find_element(By.NAME, 'number')

    number_input.send_keys(TEST_PAYLOAD)

    number_input.send_keys(Keys.ENTER)

    sleep(2)

    #buffer = driver.page_source.replace(TEST_INPUT, TEST_PAYLOAD)

    # check if alert is present
    try:
        driver.switch_to.alert.accept()
        print("Alerte détectée")
        
    except NoAlertPresentException:
        print("Aucune alerte détectée")


    # verifiy if script changes when injecting random data

    # same for 'values' parameters

    return 
