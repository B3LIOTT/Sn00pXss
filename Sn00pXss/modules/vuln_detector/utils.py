from models import AttackType, Payload, PayloadType, FilterModel
from modules import utils


BASE_PAYLOADS = {
    "ESCAPE_JS": ["'", ';', ' ','FUNCTION', '(', '"xss dom based"', ')', ';',  'var cat= ']
}


def build_ESCAPE_JS_payloads():
    """
    Builds payloads for the ESCAPE_JS attack type
    """
    return 


def get_payloads_subset(attackType: AttackType, filterModel: FilterModel) -> list[Payload]:
    """
    Returns a subset of payloads to test, based on the attack type, and the filters
    """
    
    return Payload(value="""'; alert("xss dom based"); var cat= ' """, payloadType=PayloadType.ALERT) # TODO