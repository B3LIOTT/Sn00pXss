from modules.requestor.requestor import Requestor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from models import RequestModel, FilterModel
from modules.logger import info, error
from time import sleep


TEST_INPUT = "!!ABCDEFGHTESTHGFEDCBA!!"


def inject_payload_JS(driver: webdriver, requestModel: RequestModel, filterModel: FilterModel):
    """
    Try to inject the payload in the javascript (~= escape with ' or ")
    """
    pass

def inject_payload_HTML(driver: webdriver, requestModel: RequestModel, filterModel: FilterModel):
    """
    Try to inject the payload in the html (~= add tags with <> and </>)
    """
    pass


def detect_xss(requestor: Requestor, requestModel: RequestModel, filterModel: FilterModel):
    """
    Try to detect if the website is vulnerable to XSS
    """

    # TODO: d'abord vérifier si on veut injecter dans le js ou dans le html
    # si html, on utilise <> et </> pour les balises
    # sinon il faut échapper le js avec ' ou " ...
    
    try:
        assert(requestModel.is_payload_defined())
        assert(requestModel.is_vector_defined())

        driver = requestor.send_request(requestModel=requestModel)
        input = driver.find_element(requestModel.vector.type, requestModel.vector.value)
        input.send_keys(requestModel.payload)    
        input.send_keys(Keys.ENTER)

    except Exception as e:
        error(funcName="detect_dom_xss", message=f"Error : {e}")
        return

    # wait for the page to load
    #sleep(1)

    # check if alert is present
    try:
        driver.switch_to.alert.accept()
        info(message=f"Alerte détectée avec : {requestModel.payload}\n")
        
    except NoAlertPresentException:
        info(message="Aucune alerte détectée")

    return 


def is_injected(driver: webdriver):

    #buffer = driver.page_source.replace(TEST_INPUT, TEST_PAYLOAD)
    
    all_elements = driver.find_elements(By.XPATH, '//*')

    print("Toutes les balises de la page :")
    for element in all_elements:
        print(f"Balise : {element.tag_name} | Text : {element.text}")

    # regarder si on a bien injecté la balise
    return
