from modules.vuln_detector import detect_xss
from modules.filter_detector import detect_filters
from models import RequestModel, AttackType, AttackVector
from selenium.webdriver.common.by import By
from modules.requestor import Requestor
from modules.logger import error, info, bingo
from utils import get_args, get_params, save_config, config_already_exists, get_config


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

    try:
        url, affected = get_args()

        # check if the configuration already exists
        cae = config_already_exists(url, affected)
        if already_exists:=cae[0]:
            path = cae[1]
            bingo(f"Configuration already exists: {path}")
            info("Do you want to continue with this configuration ?")
            if input("[Y/n] ->").lower() != 'y':
                # Ask user for attack vector / type...
                config = get_params()

                if not config:
                    # AUTO vector detection
                    raise NotImplementedError("AUTO method is not implemented yet")
                
            else:
                config = get_config(path)
        
        config = get_params()
                
    except Exception as e:
        error(f"An error occured during attack configuration: {e}")
        exit(1)

    print("Attack configuration done !")
    print("Configuration:")
    for k, v in config.items():
        print(k, v)

    if not already_exists:
        save_config(url, affected, config)

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


    # TODO: alg to detect the attack type
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
