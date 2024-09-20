from models import RequestModel, AttackType
from modules.requestor.requestor import Requestor
from modules.logger import info, error, bingo, warn, big_info
from modules.utils import get_actions_from_event, send_payload_by_input, send_payload_by_url, send_payload_by_cookies, send, detect_payload_position, TEST_INPUT
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re


def detect_attack_type(requestor: Requestor, requestModel: RequestModel):
    # TODO:
    # ESCAPE_JS: détecter si l'input se trouve dans un script JS
    # ESCAPE_HTML: détecter si l'input se trouve dans du HTML, dans une balise sous forme de texte
    # INJECT_HTML: détecter si l'input se trouve dans du HTML, dans une balise sous forme d'attribut/event
    # INJECT_EVENT: détecter si l'input se trouve dans un attribut HTML, un event
    # Detecter si l'attaque se fait par les cookies ou non

    # initiate the tested page
    requestor.send_request(requestModel=requestModel)

    # extract cookies
    cookies = requestor.get_cookies()
    info(message=f"Cookies: {cookies}")
    
    # detect test payload position
    position = detect_payload_position(
        requestor=requestor,
        requestModel=requestModel,
        send_payload=send_payload_by_input,
    )

    info(message=f"Payload in the page source: {requestor.driver.page_source[position-20:position+len(TEST_INPUT)+20]} ...\n")

    # detect attack types
    attack_types = {}
    
    # detect if the payload is in a script tag
    js_pattern = fr"<script\b[^>]*>(.*?)({TEST_INPUT})(.*?)<\/script>"  # CA MARCHE PAAAS :(
    print(requestor.driver.page_source)
    js_match = re.search(js_pattern, requestor.driver.page_source)

    if js_match:
        info(message=f"Payload in a script tag: {js_match.group(0)}")
        attack_types[AttackType.ESCAPE_JS.value] = "'"

    # TODO: continue
    # ...
    
    if len(attack_types) == 0:
        raise Exception("No attack type detected")

    return attack_types


# TODO
def detect_vectors(requestor: Requestor, requestModel: RequestModel):
    # TODO: detecter les potentiels vecteurs d'attaque

    # initiate the tested page
    requestor.send_request(requestModel=requestModel)
    page_source = requestor.driver.page_source

    # extract cookies
    cookies = requestor.get_cookies()
    info(message=f"Cookies: {cookies}")

    # extract inputs
    input_fields = requestor.driver.find_elements(By.TAG_NAME, "input")

    # extract textareas
    textareas = requestor.driver.find_elements(By.TAG_NAME, "textarea")

    # write text to input fields
    buttons = []
    for input_field in input_fields:
        try:
            input_type = input_field.get_attribute('type')

            if input_type in ['text', 'email', 'password', 'search', 'url', 'tel']:
                info(message=f"Found input: {input_type}")
                input_field.clear() 
                input_field.send_keys(TEST_INPUT)       
            
            elif input_type in ['checkbox', 'radio']:
                info(message=f"Found input: {input_type}")
                input_field.click()

            elif input_type in ['submit', 'button']:
                info(message=f"Found input: {input_type}")
                buttons.append(input_field)
            
            else:
                warn(message=f"Input type not supported: {input_type}")

        except Exception as e:
            error(funcName='detect_attack_type', message=f"Error while detecting input type: {e}")

    # write text to textareas
    for textarea in textareas:
        try:
            textarea.clear()
            textarea.send_keys(TEST_INPUT)

        except Exception as e:
            error(funcName='detect_attack_type', message=f"Error while detecting textarea: {e}")


    # TODO: click on buttons if ENTER is not enough
    # for each button clicked, check if the payload is in the page
    # ...
    
    
    # send the request
    input_field.send_keys(Keys.ENTER)

    # detect input position and context
    position = detect_payload_position(
        requestor=requestor,
        requestModel=requestModel,
        send_payload=send_payload_by_input,
    )

    print(f"Payload in the page source: {page_source}")

    raise NotImplementedError("Not implemented yet")
    
