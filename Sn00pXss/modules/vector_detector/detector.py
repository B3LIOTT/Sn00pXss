from models import RequestModel
from modules.requestor.requestor import Requestor
from modules.logger import info, error, bingo, warn, big_info
from modules.utils import get_actions_from_event, send_payload_by_input, send_payload_by_url, send_payload_by_cookies, send, detect_payload_position, TEST_INPUT
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re


def detect_attack_type(requestor: Requestor, requestModel: RequestModel):
    # TODO: detecter les potentiels vecteurs d'attaque
    # ESCAPE_JS: détecter si l'input se trouve dans un script JS
    # ESCAPE_HTML: détecter si l'input se trouve dans du HTML, dans une balise sous forme de texte
    # ESCAPE_ATTR: détecter si l'input se trouve dans un attribut HTML, un event
    # Detecter si l'attaque se fait par les cookies ou non

    # initiate the tested page
    requestor.send_request(requestModel=requestModel)
    page_source = requestor.driver.page_source

    # extract cookies
    cookies = requestor.get_cookies()
    info(message=f"Cookies: {cookies}")

    # extract inputs
    input_fields = requestor.driver.find_elements(By.TAG_NAME, "input")

    # send text to input fields and analyse the response
    for input_field in input_fields:
        try:
            input_type = input_field.get_attribute('type')

            if input_type in ['text', 'email', 'password', 'search', 'url', 'tel']:
                info(message=f"Found input: {input_type}")
                input_field.clear() 
                input_field.send_keys(TEST_INPUT)       
                #input_field.send_keys(Keys.ENTER)

                # TODO: detect input position and context
            else:
                warn(message=f"Input type not supported: {input_type}")

        except Exception as e:
            error(funcName='detect_attack_type', message=f"Error while detecting input type: {e}")


    raise NotImplementedError("Not implemented yet")
    
