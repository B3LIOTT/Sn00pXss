from modules.vuln_detector import detect_xss
from modules.filter_detector import detect_filters
from models import RequestModel, AttackType, AttackVector
from selenium.webdriver.common.by import By
from modules.requestor import Requestor
from modules.logger import error, info


__author__ = "b3liott"


ban = """
===================================

      ,-~~-.___.
     / |  '     \         
    (  )         0  
     \_/-, ,----'        __    
        ====            / /
       /  \-'~;        / /   
      /  __/~|  ______/ /    
    =(  _____| (________|

    
<script>alert("Sn00pXss")</script>
          
         By b3liott

===================================
"""


if __name__ == '__main__':
    print(ban)
    choice = """
-----------------------
1. Test XSS
2. Test Filters
-----------------------
-> """

    choice = int(input(choice))
    
    requestor = Requestor()
    url = "http://challenge01.root-me.org/web-client/ch32/"
    rm = RequestModel(
        url=url,
        affects=url,
    )

    # set attack type
    vector = AttackVector(type=By.NAME, value='number')
    rm.set_vector(vector=vector)

    if choice == 2:
        # detect filters
        filterModel = detect_filters(requestor=requestor, requestModel=rm)
        info(filterModel)

    elif choice == 1:
        # TODO: algo qui détecte le(s) type(s) d'attaque(s)
        attacks = [(AttackType.ESCAPE_JS, "'")]

        for attack in attacks:
            # set attack type
            rm.set_attack(attackType=attack[0], escapeChar=attack[1])

            # detect xss
            detect_xss(requestor=requestor, requestModel=rm)

    else:
        error(message="Invalid choice")

    requestor.dispose()
