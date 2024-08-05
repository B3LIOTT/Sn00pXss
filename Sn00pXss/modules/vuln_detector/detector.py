from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models import RequestModel, FilterModel, PayloadType, Payload
from modules.requestor.requestor import Requestor
from modules.logger import info, error, bingo, warn, big_info
from .utils import get_payload_generator, TEST_INPUT
from time import sleep




def send_payload_by_input(requestor: Requestor, requestModel: RequestModel, payload: str):
    requestor.send_request(requestModel=requestModel)

    # write the payload in the vulnerable input
    input = requestor.driver.find_element(requestModel.vector.type, requestModel.vector.value)
    input.send_keys(payload)

    # write data in other required inputs   
    if requestModel.miscInputs is not None:
        for key, value in requestModel.miscInputs.items():
            input = requestor.driver.find_element(value, key)
            input.send_keys("This is random data")

    if requestModel.vector.submit_with_button():
        submit = requestor.driver.find_element(requestModel.vector.submitButtonType, requestModel.vector.submitButtonValue)
        submit.click()
    else:
        input.send_keys(Keys.ENTER)



def send_payload_by_url(requestor: Requestor, requestModel: RequestModel, payload: str):
    requestor.send_request(requestModel=requestModel, url=f"{requestModel.url}/?{requestModel.vector.value}={payload}")


def send_payload_by_cookies(requestor: Requestor, requestModel: RequestModel, payload: str):
    cookie_vector_key = requestModel.vector.value
    requestModel.set_cookie(key=cookie_vector_key, value=payload)

    requestor.send_request(requestModel=requestModel)


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


def fuzz(requestor: Requestor, requestModel: RequestModel):
    """
    Tests appropriate subset of payloads, based on filters
    """
    filterModel = FilterModel()

    if requestModel.vector.isVectorCookies:
        send_payload: callable = send_payload_by_cookies
    else:
        send_payload: callable = send_payload_by_input if requestModel.vector.type else send_payload_by_url

    next_payload: callable = get_payload_generator(requestModel.attackType)

    expected_position = detect_payload_position(requestor, requestModel, send_payload)

    payload : Payload = None
    failedData = []

    while payload:=next_payload(requestModel, filterModel, payload, failedData):
        try:
            info(message=f"Testing payload : {payload.value}")
            send_payload(requestor=requestor, requestModel=requestModel, payload=payload.value)
        
        except UnexpectedAlertPresentException:
            alert = requestor.driver.switch_to.alert
            alert.accept()
            bingo(message=f"Alert triggered with : {payload.value}\n")
            return

        except Exception as e:
            error(funcName="fuzz (send_payload)", message=f"Error for {payload.value}: {e}")
            continue

        # wait for the page to load
        #sleep(1)

        # request the page which is affected by the payload (if not the same)
        if requestModel.affects is not None:
            requestor.get_affected()


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
                result = requestor.driver.page_source[expected_position:expected_position+len(payload.value)]
                warn(message=f"Server response with payload : {result}\n->  Analysing why the payload failed...\n")
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
        "type": ""
    }
    for k in range(len(usedPayload.usedChars)):
        # check if the character is in the result
        if ucr:=usedPayload.usedCharsReplaced[k] not in result:
            # distinguish the type of data: char, function, args
            if usedPayload.usedChars[k] == "FUNCTION":
                data["type"] = "FUNCTION"
                data["value"] = ucr
                filterModel.add_filtered_func(data['value'])

            elif usedPayload.usedChars[k] == "ARGS":
                data["type"] = "ARGS"
                data["value"] = ucr
            
            else:
                filterModel.add_filtered_char(data['value'])
            
            failedData.append(data)



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

