
def error(className: str, funcName: str, message: str) -> None:
    print(f"[!] {className}: in {funcName} {message}")


def info(className: str, funcName: str, message: str) -> None:
    print(f"[+] {className}: in {funcName} {message}")