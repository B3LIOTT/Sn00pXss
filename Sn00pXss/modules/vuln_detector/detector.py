from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from models import RequestModel, FilterModel, PayloadType, Payload
from modules.requestor.requestor import Requestor
from modules.logger import info, error, bingo, warn, big_info
from .utils import get_payload_generator
from time import sleep


TEST_INPUT = "ABCDEFGHb3liottHGFEDCBA"


def send_payload_by_input(requestor: Requestor, requestModel: RequestModel, payload: str) -> webdriver:
    driver = requestor.send_request(requestModel=requestModel)
    input = driver.find_element(requestModel.vector.type, requestModel.vector.value)
    input.send_keys(payload)    
    input.send_keys(Keys.ENTER)

    return driver


def send_payload_by_url(requestor: Requestor, requestModel: RequestModel, payload: str) -> webdriver:
    return requestor.send_request(requestModel=requestModel, url=f"{requestModel.url}/?{requestModel.vector.value}={payload}")


def fuzz(requestor: Requestor, requestModel: RequestModel):
    """
    Tests appropriate subset of payloads, based on filters
    """
    filterModel = FilterModel()
    send_payload: callable = send_payload_by_input if requestModel.vector.type else send_payload_by_url
    next_payload: callable = get_payload_generator(requestModel.attackType)

    payload : Payload
    while payload:=next_payload(requestModel):
        try:
            info(message=f"Testing payload : {payload.value}")
            driver = send_payload(requestor=requestor, requestModel=requestModel, payload=payload.value)

        except Exception as e:
            error(funcName="fuzz", message=f"Error for {payload.value}: {e}")
            continue

        # wait for the page to load
        #sleep(1)

        # request the page which is affected by the payload (if not the same)
        if requestModel.url != requestModel.affects:
            driver.get(requestModel.affects)

        if payload.payloadType == PayloadType.ALERT:
            # check if alert is present
            try:
                driver.switch_to.alert.accept()
                bingo(message=f"Alert triggered with : {payload.value}\n")
                
            except NoAlertPresentException:
                warn(message="No alert triggered")
                # TODO: analyser pourquoi l'alerte n'est pas levée
                analyse_fail() # mettre à jour le filterModel en fonction du résultat
        
        else:
            # check request bin
            raise NotImplementedError("Request bin not implemented yet")
    
    return


def detect_xss(requestor: Requestor, requestModel: RequestModel):
    """
    Try to detect if the website is vulnerable to XSS
    """

    big_info(message=f"Detecting XSS for attack type : {requestModel.attackType.name}")
    try:
        assert(requestModel.is_vector_defined())
        assert(requestModel.is_attack_defined())

        fuzz(requestor, requestModel)

    except Exception as e:
        error(funcName="detect_xss", message=f"Error : {e}")

    return 


def is_injected(driver: webdriver):

    #buffer = driver.page_source.replace(TEST_INPUT, TEST_PAYLOAD)
    
    all_elements = driver.find_elements(By.XPATH, '//*')

    print("Toutes les balises de la page :")
    for element in all_elements:
        print(f"Balise : {element.tag_name} | Text : {element.text}")

    # regarder si on a bien injecté la balise
    return
