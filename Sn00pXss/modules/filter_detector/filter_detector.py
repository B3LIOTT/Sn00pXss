from .utils import *
from modules.requestor import Requestor
from modules.logger import info, error
from models import RequestModel
from selenium.webdriver.common.keys import Keys
from time import sleep


TEST_INPUT = "ABCDEFGHTESTHGFEDCBA"


def detect_filters(requestor: Requestor, requestModel: RequestModel):
    """
    Try to detect if the website is filtering some characters
    """
    filtered_chars = []
    for key in SPECIAL_CHARS.keys():
        for char in SPECIAL_CHARS[key]:
            try:
                # send the request
                payload = f"{char}{TEST_INPUT}{char}"
                requestModel.set_payload(payload=payload)
                driver = requestor.send_request(requestModel=requestModel)
                number_input = driver.find_element(requestModel.vector.type, requestModel.vector.value)
                number_input.send_keys(requestModel.payload)    
                number_input.send_keys(Keys.ENTER)

                # check if the char is filtered
                if payload not in driver.page_source:
                    filtered_chars.append(char)
                    info(message=f"Le caractère {char} est filtré")
                else:
                    info(message=f"Le caractère {char} n'est pas filtré")

            except Exception as e:
                error(funcName="detect_filters", message=f"Erreur : {e}")
            # finally:
            #     sleep(0.5)

    return filtered_chars
