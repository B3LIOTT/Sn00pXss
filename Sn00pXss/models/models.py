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
    
    def __init__(self, type: By | None, value: str, submitButtonType: By | None, submitButtonValue: str | None):
        """
        If the type is None, the vector is a GET parameter with the value as key
        """
        self.type = type
        self.value = value
        self.submitButtonType = submitButtonType
        self.submitButtonValue = submitButtonValue

    
    def submit_with_button(self):
        return self.submitButtonType is not None and self.submitButtonValue is not None


class RequestModel:
    """
    This class represents the parameters of the request to be sent to the target    
    """
    
    def __init__(self, url: str, affects: str = None, cookies: dict=None):
        self.url = url
        self.cookies = cookies
        self.affects = affects
        self.vector = None
        self.miscInputs = None
        self.attackType = None
        self.escapeChar = None


    def set_vector(self, vector: AttackVector):
        self.vector = vector

    def is_vector_defined(self):
        return self.vector is not None
    

    def set_misc_inputs(self, miscInputs: dict[str, By]):
        # dict with key as input name/id... and value as By (and we put a random value).
        self.miscInputs = miscInputs


    def set_attack(self, attackType: AttackType, escapeChar: str=None):
        self.attackType = attackType
        self.escapeChar = escapeChar

    def is_attack_defined(self):
        return self.attackType is not None
    


class FilterModel:
    """
    This class defines the supposed filters used to prevent XSS from the target.
    """

    def __init__(self):
        self.filteredChars = []
        self.filteredFuncs = []
        self.filteredTags = []


    def add_filtered_char(self, char: str):
        self.filteredChars.append(char)

    def add_filtered_func(self, func: str):
        self.filteredFuncs.append(func)

    def add_filtered_tag(self, tag: str):
        self.filteredTags.append(tag)
    

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
    
    def __init__(self, payloadType: PayloadType, value: str, usedChars: list, usedCharsReplaced: list):
        self.payloadType = payloadType
        self.value = value
        self.usedChars = usedChars
        self.usedCharsReplaced = usedCharsReplaced