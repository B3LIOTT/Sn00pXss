from modules.vuln_detector import detect_xss
from models import RequestModel, AttackType
from modules.requestor import Requestor



if __name__ == '__main__':
    requestor = Requestor()
    url = "http://challenge01.root-me.org/web-client/ch32/"
    rm = RequestModel(
        url=url,
        affects=url,
    )

    rm.add_attackType(attackType=AttackType.DOM)

    print(detect_xss(requestor=requestor, requestModel=rm))

    requestor.dispose()