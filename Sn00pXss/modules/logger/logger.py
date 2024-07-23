class Colors:
    RESET = "\033[0m"
    BOLD = "\033[01m"
    UNDERLINE = "\033[04m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    ORANGE = "\033[38;5;214m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"



def error(className: str, funcName: str, message: str):
    print(f"{Colors.RED}[!] {className} -> in {funcName} {message}{Colors.RED}")

def error(funcName: str, message: str):
    print(f"{Colors.RED}[!] In {funcName} -> {message}{Colors.RED}")



def warn(funcName: str, message: str):
    print(f"{Colors.ORANGE}[?] In {funcName} -> {message}{Colors.ORANGE}")

def warn(message: str):
    print(f"{Colors.ORANGE}[?] {message}{Colors.ORANGE}")



def info(className: str, funcName: str, message: str):
    print(f"{Colors.WHITE}[+] {className} -> in {funcName} {message}{Colors.WHITE}")

def info(message: str):
    print(f"{Colors.WHITE}[+] {message}{Colors.WHITE}")



def bingo(message: str):
    print()
    print(f"{Colors.GREEN}[+] {message}{Colors.GREEN}")
    print()
