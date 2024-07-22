
def error(className: str, funcName: str, message: str):
    print(f"[!] {className} -> in {funcName} {message}")

def error(funcName: str, message: str):
    print(f"[!] In {funcName} -> {message}")


def info(className: str, funcName: str, message: str):
    print(f"[+] {className} -> in {funcName} {message}")

def info(message: str):
    print(f"[+] {message}")
