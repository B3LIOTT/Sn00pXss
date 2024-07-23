from modules.vuln_detector import detect_xss
from modules.filter_detector import detect_filters
from models import RequestModel, AttackType, AttackVector
from selenium.webdriver.common.by import By
from modules.requestor import Requestor


if __name__ == '__main__':
    requestor = Requestor()
    url = "http://challenge01.root-me.org/web-client/ch32/"
    rm = RequestModel(
        url=url,
        affects=url,
    )

    vector = AttackVector(type=By.NAME, value='number')
    rm.set_vector(vector=vector)
    rm.set_attackType(attackType=AttackType.DOM)

    # detect filters
    filterModel = detect_filters(requestor=requestor, requestModel=rm)
    print(filterModel)

    # detect xss
    detect_xss(requestor=requestor, requestModel=rm, filterModel=filterModel)

    requestor.dispose()
