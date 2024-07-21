
def error(className: str, funcName: str, message: str):
    print(f"[!] {className}: in {funcName} {message}")


def info(className: str, funcName: str, message: str):
    print(f"[+] {className}: in {funcName} {message}")


def info(message: str):
    print(f"[+] {message}")
