from selenium.webdriver.common.action_chains import ActionChains
import base64 as b64
from models import HtmlEvent
from modules.logger import error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models import RequestModel, FilterModel, PayloadType, Payload, CookieException, AttackType
from modules.requestor.requestor import Requestor
from modules.logger import info, error, bingo, warn, big_info
from random import randint

TEST_INPUT = f"ABCDEFGHb3liottHGFEDCBA{randint(1000, 9999)}"

# Special characters
SPECIAL_CHARS = {
    'plain': ['<', '>', '(', ')', '[', ']', '{', '}', '=', '+', '-', '*', '/', '\\', '|', '&', '^', '%', '$', '#', '@', '!', '~', '`', '?', ':', ';', ',', '.', ' ', '\t', '\n'],
    'encoded': ['&lt;', '&gt;', '&#40;', '&#41;', '&#91;', '&#93;', '&#123;', '&#125;', '&#61;', '&#43;', '&#45;', '&#42;', '&#47;', '&#92;', '&#124;', '&#38;', '&#94;', '&#37;', '&#36;', '&#35;', '&#64;', '&#33;', '&#126;', '&#96;', '&#63;', '&#58;', '&#59;', '&#44;', '&#46;', '&#32;', '&#9;', '&#10;'],
    'url_encoded': ['%3C', '%3E', '%28', '%29', '%5B', '%5D', '%7B', '%7D', '%3D', '%2B', '%2D', '%2A', '%2F', '%5C', '%7C', '%26', '%5E', '%25', '%24', '%23', '%40', '%21', '%7E', '%60', '%3F', '%3A', '%3B', '%2C', '%2E', '%20', '%09', '%0A']
}


# TOUT CHANGER, FAIRE UN DICT AVEC TOUS LES CARACTERES SPECIAUX ET LEURS EQUIVALENTS
# FAIRE UNE FONCTION QUI CONSTRUIT DES ÉQUIVALENTS DE FONCTIONS, EXEMPE: ALERT(ARG) = ATOB(BASE64)

SPECIAL_CHARS['for_html_tags'] = {
    '<': ['<', '&lt;', '%3C'],
    '>': ['>', '&gt;', '%3E'],
    '/': ['/', '&#47;', '%2F']
}


# TODO: change the data structure in order to optimise the fuzzing research
EQUIVALENTS = {
    '<': ['%3C', '&lt;', '&#60'],
    '>': ['%3E', '&gt;', '&#62'],
    '(': ['%28', '&#40'],
    ')': ['%29', '&#41'],
    '[': ['%5B', '&#91'],
    ']': ['%5D', '&#93'],
    '{': ['%7B', '&#123'],
    '}': ['%7D', '&#125'],
    '=': ['%3D', '&#61'],
    '+': ['%2B', '&#43'],
    '-': ['%2D', '&#45'],
    '*': ['%2A', '&#42'],
    '/': ['%2F', '&#47'],
    '\\': ['%5C', '&#92'],
    '|': ['%7C', '&#124'],
    '&': ['%26', '&#38'],
    '^': ['%5E', '&#94'],
    '%': ['%25', '&#37'],
    '"': ['%22', '&#34'],
    "'": ['%27', '&#39'],
    '`': ['%60', '&#96'],
    '?': ['%3F', '&#63'],
    ':': ['%3A', '&#58'],
    ';': ['%3B', '&#59'],
    ',': ['%2C', '&#44'],
    '.': ['%2E', '&#46'],
    ' ': ['%20', '&#32'],
}


HTML_TAGS = [
    'html', 'head', 'title', 'base', 'link', 'meta', 'style', 'script', 'noscript',
    'body', 'section', 'nav', 'article', 'aside', 'h1', 'h2', 'h3', 'div', 'a', 
    'data', 'time', 'code', 'span', 'br', 'picture', 'source', 'img', 'iframe', 
    'embed', 'object','video', 'audio', 'input', 'button', 'option', 'textarea', 
    'dialog', 'script','svg'
]

USEFUL_JS_FUNCTION = [
    'alert', 'fetch', 'eval', '[].filter.constructor', 'atob', 'document.write', 'document.writeln', 'document.writeIn', 'document.createElement'
]

HTML_EVENTS = [
    # Keyboard events
    ("onkeydown", HtmlEvent.KEY),
    ("onkeypress", HtmlEvent.KEY),
    ("onkeyup", HtmlEvent.KEY),
    # Mouse events
    ("onclick", HtmlEvent.CLICK),
    ("onmousedown", HtmlEvent.MOUSE),
    ("onmousemove", HtmlEvent.MOUSE),
    ("onmouseout", HtmlEvent.MOUSE),
    ("onmouseover", HtmlEvent.MOUSE),
    ("onmouseup", HtmlEvent.MOUSE),
]


def get_actions_from_event(driver, event: HtmlEvent, element):
    try:
        if event == HtmlEvent.MOUSE:
            actions = ActionChains(driver)
            # TODO: fix out of bounds error and "no size and location" error
            # move down
            actions.move_by_offset(0, 5).perform()
            # # move up
            actions.move_by_offset(0, -5).perform()

            # go to the element (to be over it)
            # actions.move_to_element(element).perform()
        
        elif event == HtmlEvent.KEY:
            ActionChains(driver).send_keys("A").perform()

        elif event == HtmlEvent.CLICK:
            ActionChains(driver).click(element).perform()
    
    except Exception as e:
        error(funcName='get_actions_from_event', message=f"An error occured during the event action: {e}")


def send(requestor: Requestor, requestModel: RequestModel, vulnerableInput = None):
    # write data in other required inputs 
    if requestModel.miscInputs is not None:
        for key, value in requestModel.miscInputs.items():
            input = requestor.driver.find_element(value, key)
            input.send_keys("Th1s 1s r4ndom d4t4")

    if requestModel.vector.submit_with_button():
        # submit the form by clicking the button if we need to (= if ENTER is not enough)
        submit = requestor.driver.find_element(requestModel.vector.submitButtonType, requestModel.vector.submitButtonValue)
        submit.click()

    elif requestModel.vector.isVectorCookies:
        # if the vector is a cookie, we need to refresh the page to apply the cookie
        requestor.send_request(requestModel=requestModel)

    elif vulnerableInput is not None:
        vulnerableInput.send_keys(Keys.ENTER)


def send_payload_by_input(requestor: Requestor, requestModel: RequestModel, payload: str):
    # write the payload in the vulnerable input
    input = requestor.driver.find_element(requestModel.vector.type, requestModel.vector.value)
    input.send_keys(payload)

    send(requestor, requestModel, vulnerableInput=input)


def send_payload_by_url(requestor: Requestor, requestModel: RequestModel, payload: str):
    url = f"{requestModel.url}/?{requestModel.vector.value}={payload}"
    info(message=f"Url: {url}")
    requestor.send_request(requestModel=requestModel, url=url)


def send_payload_by_cookies(requestor: Requestor, requestModel: RequestModel, payload: str):
    cookie_vector_key = requestModel.vector.value
    #requestModel.set_cookie(key=cookie_vector_key, value=payload)
    requestor.set_cookies({cookie_vector_key: payload})

    send(requestor, requestModel)



def detect_payload_position(requestor: Requestor, requestModel: RequestModel, send_payload: callable):
    """
    Detect the position of the payload in the page
    """
    send_payload(requestor=requestor, requestModel=requestModel, payload=TEST_INPUT)

    # request the page which is affected by the payload (if not the same)
    if requestModel.affects is not None:
        requestor.get_affected()

    # get the page source
    page_source = requestor.driver.page_source

    # check if the payload is in the page source
    if TEST_INPUT in page_source:
        start_index = page_source.index(TEST_INPUT)
        bingo(message=f"Payload position expected at index {start_index}")

        return start_index
    
    else:
        error(funcName="detect_payload_position", message="Payload not detected in the page, maybe the page is not affected by the payload.\nVerify if you put the right affected page.")
        requestor.dispose()
        exit(1)

    
def get_end_position(start_index: int, page_source: str):
    """
    Get the end position of the payload
    """
    return page_source.index("EOP", start_index)
        