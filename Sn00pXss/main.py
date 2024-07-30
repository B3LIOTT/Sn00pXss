from modules.vuln_detector import detect_xss
from modules.filter_detector import detect_filters
from models import RequestModel, AttackType, AttackVector
from selenium.webdriver.common.by import By
from modules.requestor import Requestor
from modules.logger import error, info
import argparse


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


def get_args() -> list:
    parser = argparse.ArgumentParser(description='Sn00pXss - XSS detection tool')
    parser.add_argument('-u', '--url', type=str, help='Un argument optionnel', required=True)
    parser.add_argument('-a', '--affects', type=str, help='Url which could be affected by an XSS', required=False)
    #parser.add_argument('-v', '--vector', type=str, help='todo', required=True)

    args = parser.parse_args()

    return args.url, args.affects


if __name__ == '__main__':
    print(ban)

    url, affected = get_args()

    # Ask user for attack vector / type...
    # TODO

    requestor = Requestor()
    
    # test 1 : XSS DOM based Introduction -> "http://challenge01.root-me.org/web-client/ch32/"
    
    # test 2 : XSS Stored 1 -> "http://challenge01.root-me.org/web-client/ch18/"

    rm = RequestModel(
            url=url,
            affects=affected
        )
    
    # test 2
    rm.set_misc_inputs(miscInputs={'titre': By.NAME})

    # set attack type
    # test 1
    # vector = AttackVector(type=By.NAME, value='number')

    # test 2
    vector = AttackVector(type=By.NAME, value='message', submitButtonType=By.CSS_SELECTOR, submitButtonValue='input[type="submit"]')

    rm.set_vector(vector=vector)

    # TODO: algo qui détecte le(s) type(s) d'attaque(s)
    # test 1
    # attacks = [(AttackType.ESCAPE_JS, "'")]

    # test 2
    attacks = [(AttackType.INJECT_HTML, None)]

    for attack in attacks:
        # set attack type
        rm.set_attack(attackType=attack[0], escapeChar=attack[1])

        # detect xss
        detect_xss(requestor=requestor, requestModel=rm)


    requestor.dispose()
