from modules.vuln_detector import detect_xss
from modules.filter_detector import detect_filters
from models import RequestModel, AttackType, AttackVector
from selenium.webdriver.common.by import By
from modules.requestor import Requestor


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
    input("Press Enter to start...")
    
    requestor = Requestor()
    url = "http://challenge01.root-me.org/web-client/ch32/"
    rm = RequestModel(
        url=url,
        affects=url,
    )

    # set attack type
    vector = AttackVector(type=By.NAME, value='number')
    rm.set_vector(vector=vector)

    # detect filters
    #filterModel = detect_filters(requestor=requestor, requestModel=rm)
    #print(filterModel)

    # TODO: algo qui détecte le(s) type(s) d'attaque(s)
    attacks = [(AttackType.ESCAPE_JS, "'")]

    for attack in attacks:
        # set attack type
        rm.set_attack(attackType=attack[0], escapeChar=attack[1])

        # detect xss
        detect_xss(requestor=requestor, requestModel=rm)

    requestor.dispose()
