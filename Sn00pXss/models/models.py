from enum import Enum


class AttackType(Enum):
    REFLECTED = "REFLECTED"
    STORED = "STORED"
    DOM = "DOM"


class RequestModel:
    """
    This class represents the parameters of the request to be sent to the target    
    """
    
    def __init__(self, url: str, affects: str, cookies: dict=None):
        self.url = url
        self.cookies = cookies
        self.affects = affects
        self.attackType = None
        self.payload = None


    def set_payload(self, payload: str):
        self.payload = payload

    
    def is_payload_defined(self):
        return self.payload is not None


    def add_attackType(self, attackType: AttackType):
        self.attackType = attackType


    def is_attackType_defined(self):
        return self.attackType is not None