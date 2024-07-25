from selenium.webdriver.common.by import By
from enum import Enum


class AttackType(Enum):
    """
    Enumerates the different code injections, if we have to escape the JS or add tags in the HTML etc.
    """
    ESCAPE_JS = "ESCAPE_JS"
    ESCAPE_HTML = "ESCAPE_HTML"
    INJECT_HTML = "INJECT_HTML"


class AttackVector:
    """
    Defines the attack vector to be used (by name, id, etc...)
    """
    
    def __init__(self, type: By | None, value: str):
        """
        If the type is None, the vector is a GET parameter with the value as key
        """
        self.type = type
        self.value = value


class RequestModel:
    """
    This class represents the parameters of the request to be sent to the target    
    """
    
    def __init__(self, url: str, affects: str, cookies: dict=None):
        self.url = url
        self.cookies = cookies
        self.affects = affects
        self.vector = None
        self.attackType = None


    def set_vector(self, vector: AttackVector):
        self.vector = vector

    def is_vector_defined(self):
        return self.vector is not None


    def set_attackType(self, attackType: AttackType):
        self.attackType = attackType

    def is_attackType_defined(self):
        return self.attackType is not None
    


class FilterModel:
    """
    This class defines the supposed filters used to prevent XSS from the target.
    """

    def __init__(self, filteredChars: list, filteredFuncs: list, filteredTags: list=None):
        self.filteredChars = filteredChars
        self.filteredFuncs = filteredFuncs
        self.filteredTags = filteredTags

    def __str__(self):
        return f"FilteredChars : {self.filteredChars}\nFilteredFuncs : {self.filteredFuncs}\nFilteredTags : {self.filteredTags}"
    


class PayloadType(Enum):
    """
    Enumerates the different types of payloads
    """
    ALERT = "ALERT"
    REQUEST_BIN = "REQUEST_BIN"


class Payload:
    """
    This class represents the payload to be sent to the target
    """
    
    def __init__(self, payloadType: PayloadType, value: str):
        self.payloadType = payloadType
        self.value = value