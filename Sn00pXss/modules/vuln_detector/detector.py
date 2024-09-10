from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models import RequestModel, FilterModel, PayloadType, Payload, CookieException, AttackType
from modules.requestor.requestor import Requestor
from modules.logger import info, error, bingo, warn, big_info
from .utils import get_payload_generator
from modules.utils import get_actions_from_event, send_payload_by_input, send_payload_by_url, send_payload_by_cookies, send, detect_payload_position, TEST_INPUT
from time import sleep



def fuzz(requestor: Requestor, requestModel: RequestModel):
    """
    Tests appropriate subset of payloads, based on filters
    """
    filterModel = FilterModel()

    # initiate the vulnerable page
    requestor.send_request(requestModel=requestModel)

    if requestModel.vector.isVectorCookies:
        send_payload: callable = send_payload_by_cookies
    else:
        send_payload: callable = send_payload_by_input if requestModel.vector.type else send_payload_by_url

    next_payload: callable = get_payload_generator(requestModel.attackType)

    expected_position_start = detect_payload_position(requestor, requestModel, send_payload)

    payload : Payload = None
    failedData = []

    while payload:=next_payload(requestModel, filterModel, payload, failedData):

        # TODO: remove
        # input(f"\nPress enter to continue...\n")
        # ------------

        try:
            info(message=f"Testing payload : {payload.value}")
            send_payload(requestor=requestor, requestModel=requestModel, payload=payload.value)
   
        except UnexpectedAlertPresentException:
            alert = requestor.driver.switch_to.alert
            alert.accept()
            bingo(message=f"Alert triggered with : {payload.value}\n")
            return

        except CookieException as e:
            warn(message=str(e))
            failedData.clear() # TODO: instead of clearing the list, we should add the data which break the cookie
            continue

        except Exception as e:
            error(funcName="fuzz (send_payload)", message=f"Error for {payload.value}: {e}")
            continue

        # wait for the page to load
        # sleep(1)

        # request the page which is affected by the payload (if not the same)
        if requestModel.affects is not None:
            requestor.get_affected()

        result = None
        if requestModel.attackType == AttackType.INJECT_EVENT:
            # Detect the html tag where the payload is located
            quote = '"' if "'" in payload.usedChars else "'"
            result = requestor.driver.page_source[expected_position_start:get_end_position(expected_position_start, requestor.driver.page_source)]
            element = requestor.driver.find_element(By.XPATH, f"""//*[contains(text(), {quote}{result}{quote})]""")
  
            get_actions_from_event(
                driver=requestor.driver, 
                event=payload.event,
                element=element
            )

        if payload.payloadType == PayloadType.ALERT:
            # check if alert is present
            try:
                alert = requestor.driver.switch_to.alert
                alert.accept()
                bingo(message=f"Alert triggered with : {payload.value}\n")
                return
                
            except NoAlertPresentException:
                warn(message="No alert triggered")

                # get the payload in the response
                if not result:
                    result = requestor.driver.page_source[expected_position_start:get_end_position(expected_position_start, requestor.driver.page_source)]
                warn(message=f"Server responded with payload : {result}\n->  Analysing why the payload failed...\n")
                analyse_fail(result=result, usedPayload=payload, filterModel=filterModel, failedData=failedData)
        
        else:
            # check request bin
            raise NotImplementedError("Request bin not implemented yet")


    warn(message="No more payloads available, stopping the fuzzing process")
    return


def analyse_fail(result, usedPayload: Payload, filterModel: FilterModel, failedData: list):
    """
    Analyse the repsonse when the payload failed and add the data to the filter model.
    It also adds the data to the failedData list.
    """

    data = {
        "value": "",
        "type": "",
    }
    for k in range(len(usedPayload.usedChars)):
        # check if the character is in the result
        if (ucr:=usedPayload.usedCharsReplaced[k]) not in result:
            # distinguish the type of data: char, function, args
            if usedPayload.usedChars[k] == "FUNCTION":
                data["type"] = "FUNCTION"
                data["value"] = ucr
                filterModel.add_filtered_func(data['value'])

            elif usedPayload.usedChars[k] == "ARGS":
                data["type"] = "ARGS"
                data["value"] = ucr

            else:
                data["type"] = "CHAR"
                data["value"] = ucr
                filterModel.add_filtered_char(data['value'])
            
            failedData.append(data.copy())
    
    warn(message=f"Failed data: {failedData}")



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
        error(funcName="detect_xss", message=str(e))

    return 

