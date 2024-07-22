from selenium.webdriver.common.by import By
from enum import Enum


class AttackType(Enum):
    """
    Enumerates the different types of XSS attacks
    """
    REFLECTED = "REFLECTED"
    STORED = "STORED"
    DOM = "DOM"


class AttackVector:
    """
    Defines the attack vector to be used (by name, id, etc...)
    """
    
    def __init__(self, type: By, value: str):
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
        self.payload = None


    def set_vector(self, vector: AttackVector):
        self.vector = vector

    def is_vector_defined(self):
        return self.vector is not None


    def set_payload(self, payload: str):
        self.payload = payload

    def is_payload_defined(self):
        return self.payload is not None


    def add_attackType(self, attackType: AttackType):
        self.attackType = attackType

    def is_attackType_defined(self):
        return self.attackType is not None
    


class FilterModel:
    """
    This class defines the supposed filters used to prevent XSS from the target.
    """

    def __init__(self, filteredChars: list, filteredFuncs: list):
        self.filteredChars = filteredChars
        self.filteredFuncs = filteredFuncs