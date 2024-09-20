from modules.vuln_detector import detect_xss
from modules.filter_detector import detect_filters
from modules.vector_detector import detect_attack_type
from models import RequestModel, AttackType, AttackVector
from selenium.webdriver.common.by import By
from modules.requestor import Requestor
from modules.logger import error, info, bingo, warn, big_info
from utils import get_args, get_params, save_config, config_already_exists, get_config, print_config, add_attack_types_to_config
import sys


__author__ = "b3liott"


ban = """
=========================================================================================

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

=========================================================================================
"""

info_ban = """This tool isn't finished yet, for instance it doesn't support the AUTO method.
Moreover, the request-bin feature is not implemented yet.

It has been tested only on the following challenges:
- XSS DOM based Introduction -> "http://challenge01.root-me.org/web-client/ch32/"
- XSS Stored 1 -> "http://challenge01.root-me.org/web-client/ch18/"
- XSS Stored 2 -> "http://challenge01.root-me.org/web-client/ch19/"
- XSS Volatile (no working yet) -> "http://challenge01.root-me.org/web-client/ch26/"
 
 Note: to also test theses challenges, you need to have a valid account on root-me.org and be connected.

"""


if __name__ == '__main__':
    # test 1 : XSS DOM based Introduction -> "http://challenge01.root-me.org/web-client/ch32/"
    # test 2 : XSS Stored 1 -> "http://challenge01.root-me.org/web-client/ch18/"
    # test 3 : XSS Stored 2 -> "http://challenge01.root-me.org/web-client/ch19/"
    # test 4 : XSS Volatile -> "http://challenge01.root-me.org/web-client/ch26/"

    print(ban)
    warn(message=info_ban)

    try:
        url, affected, display = get_args()

        # check if the configuration already exists
        cae = config_already_exists(url, affected)
        if already_exists:=cae[0]:
            path = cae[1]
            bingo(f"Configuration already exists for {url}: {path}")
            info("Do you want to continue with this configuration ?")
            if input("[y/n] -> ").lower() != 'y':
                # Ask user for attack vector / type...
                config = get_params(url, affected)

                if not config:
                    # AUTO vector detection
                    raise NotImplementedError("AUTO method is not implemented yet")
                
            else:
                config = get_config(path)
        
        else:
            config = get_params(url, affected)
            path = save_config(url, affected, config)

    except KeyboardInterrupt:
        sys.stdout.flush()
        warn(message="\rOUCH !\nIt's time to sleep X - X")
                
    except Exception as e:
        error(funcName='main', message=f"An error occured during attack configuration: {e}")
        exit(1)

    bingo("Attack configuration done !")
    print("Configuration:")
    print_config(config)     

    try:
        requestor = Requestor(display)
        requestor.clear_alerts()

        rm = RequestModel(
                url=url,
                affects=affected
            )

        # set misc inputs
        rm.set_misc_inputs(miscInputs=config['misc_inputs'])
        if 'by' in config['vector']:
            type = config['vector']['by'] if not config['vector']['isCookies'] else None
        else: 
            type = None

        if 'submit' in config:
            vector = AttackVector(isVectorCookies=config['vector']['isCookies'], type=type, value=config['vector']['name'], 
                                submitButtonType=config['submit']['by'], submitButtonValue=config['submit']['name']
                                )

        else:
            vector = AttackVector(isVectorCookies=config['vector']['isCookies'], type=type, value=config['vector']['name'])

        rm.set_vector(vector=vector)

        if 'attack_types' not in config:
            big_info(message="No attack type specified, the tool will try to detect it.")
            # TODO: alg to detect the attack type, and add it to the config file
            config['attack_types'] = detect_attack_type(requestor=requestor, requestModel=rm)

            # save the attack types to the config file
            add_attack_types_to_config(path, config['attack_types'])
            
            # TODO: detect which tech is used (for example, detect if it's Angular)

        for attack_type, escape_char in config['attack_types'].items():
            # set attack type
            rm.set_attack(attackType=AttackType(attack_type), escapeChar=escape_char)

            # detect xss
            detect_xss(requestor=requestor, requestModel=rm)

    except KeyboardInterrupt:
        sys.stdout.flush()
        warn(message="\rOUCH !\nIt's time to sleep X - X")

    except Exception as e:
        error(funcName="main" ,message=f"An error occured: {e}")

    finally:
        requestor.dispose()
