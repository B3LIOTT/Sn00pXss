from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from models import RequestModel, FilterModel, Payload, PayloadType
from modules.requestor.requestor import Requestor
from modules.logger import info, error
from time import sleep


TEST_INPUT = "!!ABCDEFGHTESTHGFEDCBA!!"
TEST_PAYLOAD = Payload(value="""'; alert("xss dom based"); var cat= ' """, payloadType=PayloadType.ALERT)

# faire une BDD qui contient des payloads par type alert ou request bin
# comme ca on sait si on doit checker la request bin ou l'alerte


def fuzz(requestor: Requestor, requestModel: RequestModel, filterModel: FilterModel):
    """
    Tests given set of payloads 
    """
    for payload in [TEST_PAYLOAD]: # TODO
        try:
            driver = requestor.send_request(requestModel=requestModel)
            input = driver.find_element(requestModel.vector.type, requestModel.vector.value)
            input.send_keys(payload)    
            input.send_keys(Keys.ENTER)

        except Exception as e:
            error(funcName="detect_dom_xss", message=f"Error for {payload}: {e}")
            continue

        # wait for the page to load
        #sleep(1)

        # request the page which is affected by the payload (if not the same)
        if requestModel.url != requestModel.affects:
            driver.get(requestModel.affects)

        if (payload.payloadType == PayloadType.ALERT) and ("alert" not in filterModel.filteredFuncs):
            # check if alert is present
            try:
                driver.switch_to.alert.accept()
                info(message=f"Alerte détectée avec : {requestModel.payload}\n")
                
            except NoAlertPresentException:
                info(message="Aucune alerte détectée")
        
        else:
            # check request bin
            pass
    
    return


def detect_xss(requestor: Requestor, requestModel: RequestModel, filterModel: FilterModel):
    """
    Try to detect if the website is vulnerable to XSS
    """
    
    try:
        assert(requestModel.is_vector_defined())
        assert(requestModel.is_attackType_defined())

        fuzz(requestor, requestModel, filterModel)

    except Exception as e:
        error(funcName="detect_dom_xss", message=f"Error : {e}")

    return 


def is_injected(driver: webdriver):

    #buffer = driver.page_source.replace(TEST_INPUT, TEST_PAYLOAD)
    
    all_elements = driver.find_elements(By.XPATH, '//*')

    print("Toutes les balises de la page :")
    for element in all_elements:
        print(f"Balise : {element.tag_name} | Text : {element.text}")

    # regarder si on a bien injecté la balise
    return
