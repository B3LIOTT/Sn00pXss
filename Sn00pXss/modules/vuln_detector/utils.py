from models import AttackType, Payload, PayloadType, FilterModel


TEST_PAYLOADS = {
    "ESCAPE_JS": [Payload(value="""'; alert("xss dom based"); var cat= ' """, payloadType=PayloadType.ALERT)]
}


def get_payloads_subset(attackType: AttackType, filterModel: FilterModel) -> list[Payload]:
    """
    Returns a subset of payloads to test, based on the attack type, and the filters
    """
    
    return TEST_PAYLOADS[attackType.value] # TODO