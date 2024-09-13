from models import RequestModel
from modules.requestor.requestor import Requestor
import re


def detect_attack_type(requestor: Requestor, requestModel: RequestModel):
    # TODO: detecter les potentiels vecteurs d'attaque
    # ESCAPE_JS: détecter si l'input se trouve dans un script JS
    # ESCAPE_HTML: détecter si l'input se trouve dans du HTML, dans une balise sous forme de texte
    # ESCAPE_ATTR: détecter si l'input se trouve dans un attribut HTML, un event
    
    raise NotImplementedError("Not implemented yet")
    
