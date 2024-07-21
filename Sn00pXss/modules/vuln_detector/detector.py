from modules.requestor.requestor import Requestor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from models import RequestModel
from modules.logger import info
from time import sleep


TEST_INPUT = "!!ABCDEFGHTESTHGFEDCBA!!"

TEST_PAYLOAD = """'; alert("xss dom based"); var cat= ' """


def detect_dom_xss(requestor: Requestor, requestModel: RequestModel):
    """
    Try to detect if the website is vulnerable to DOM based XSS
    """
    
    driver = requestor.send_request(requestModel=requestModel)

    number_input = driver.find_element(By.NAME, 'number')

    number_input.send_keys(TEST_PAYLOAD)    

    number_input.send_keys(Keys.ENTER)

    sleep(1)

    # check if alert is present
    try:
        driver.switch_to.alert.accept()
        info(message=f"Alerte détectée avec : {TEST_PAYLOAD}\n")
        
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
