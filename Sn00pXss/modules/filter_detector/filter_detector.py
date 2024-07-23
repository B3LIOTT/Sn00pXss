from .utils import *
from modules.requestor import Requestor
from modules.logger import info, error
from models import RequestModel, FilterModel
from selenium.webdriver.common.keys import Keys
from time import sleep


TEST_INPUT = "ABCDEFGHTESTHGFEDCBA"


def detect_char_filters(requestor: Requestor, requestModel: RequestModel):
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


def detect_html_tags_filters(requestor: Requestor, requestModel: RequestModel, usable_chars: dict):
    """
    Try to detect if the website is filtering some html tags
    """
    filtered_tags = []
    for tag in HTML_TAGS:
        try:
            # send the request
            payload = f"{usable_chars['<'][0]}{tag}{usable_chars['>'][0]}{TEST_INPUT}{usable_chars['<'][0]}{usable_chars['/'][0]}{tag}{usable_chars['>'][0]}"
            raw_payload = f"<{tag}>{TEST_INPUT}</{tag}>"
            requestModel.set_payload(payload=payload)
            driver = requestor.send_request(requestModel=requestModel)
            number_input = driver.find_element(requestModel.vector.type, requestModel.vector.value)
            number_input.send_keys(requestModel.payload)    
            number_input.send_keys(Keys.ENTER)

            # check if the tag is filtered
            if (payload not in driver.page_source) and (raw_payload not in driver.page_source):
                filtered_tags.append(tag)
                info(message=f"La balise {tag} est filtrée")

            else:
                if raw_payload in driver.page_source: info(message=f"La balise {tag} est interprétée !!!")
                else: info(message=f"La balise {tag} n'est pas filtrée")
                

        except Exception as e:
            error(funcName="detect_filters", message=f"Erreur : {e}")
        # finally:
        #     sleep(0.5)

    return filtered_tags


def detect_func_filters(requestor: Requestor, requestModel: RequestModel):
    """
    Try to detect if the website is filtering some useful js functions
    """
    return []


def detect_filters(requestor: Requestor, requestModel: RequestModel) -> FilterModel:
    """
    Try to detect if the website is filtering characters, functions or html tags
    """
    # get filtered characters
    filtered_chars = detect_char_filters(requestor=requestor, requestModel=requestModel)

    # determine usable characters for html tags
    usable_html_tags_chars = {
        '<': [char for char in SPECIAL_CHARS['for_html_tags']['<'] if char not in filtered_chars],
        '>': [char for char in SPECIAL_CHARS['for_html_tags']['>'] if char not in filtered_chars],
        '/': [char for char in SPECIAL_CHARS['for_html_tags']['/'] if char not in filtered_chars],
    }

    info(message=f"Les caractères utilisables pour les balises html sont : {usable_html_tags_chars}")

    # get filtered html tags
    filtered_tags = None
    if usable_html_tags_chars['<'] and usable_html_tags_chars['>'] and usable_html_tags_chars['/']:
        filtered_tags = detect_html_tags_filters(
            requestor=requestor, 
            requestModel=requestModel, 
            usable_chars=usable_html_tags_chars
        )

    filtered_funcs = detect_func_filters(requestor=requestor, requestModel=requestModel)

    return FilterModel(filteredChars=filtered_chars, filteredTags=filtered_tags, filteredFuncs=filtered_funcs)
   