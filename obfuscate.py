from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os
import random
from colorama import init, Fore, Style

init(autoreset=True)

def pad(data):
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)

def encrypt_code(code, key):
    key = key.ljust(32)[:32].encode()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_code = pad(code)
    encrypted = cipher.encrypt(padded_code.encode())
    return base64.b64encode(iv + encrypted).decode()

def generate_stub(encrypted_code, key):
    return f'''
import base64
from Crypto.Cipher import AES

def run():
    def unpad(data):
        return data[:-ord(data[-1])]

    key = "{key}".ljust(32)[:32].encode()
    data = base64.b64decode("{encrypted_code}")
    iv = data[:16]
    encrypted = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted).decode()
    decrypted = decrypted[:-ord(decrypted[-1])]
    exec(decrypted, {{}})

run()
'''


def print_banner():
    banner = f"""{Fore.RED}{Style.BRIGHT}
██████╗ ██╗   ██╗███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗
██████╔╝ ╚████╔╝ ███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗  ██║  ██║
██╔═══╝   ╚██╔╝  ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝  ██║  ██║
██║        ██║   ███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗██████╔╝
╚═╝        ╚═╝   ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝                                                                          
                  {Fore.CYAN} Python Code Obfuscator 
                     {Fore.LIGHTBLACK_EX}by: IanNarito
    """
    print(banner)

def mysterious_print(text, color=Fore.WHITE):
    styles = [Style.BRIGHT, Style.NORMAL, Style.DIM]
    style = random.choice(styles)
    print(f"{style}{color}{text}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

    mysterious_print("[+] Enter the path to the Python file to obfuscate:", Fore.GREEN)
    filepath = input(">>> ").strip()

    if not os.path.exists(filepath):
        mysterious_print(" File not found! Exiting...", Fore.RED)
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    mysterious_print("[+] Enter your encryption key (leave blank to auto-generate):", Fore.YELLOW)
    key = input(">>> ").strip()
    if not key:
        key = base64.b64encode(get_random_bytes(16)).decode()[:16]
        mysterious_print(f"Generated Key: {key}", Fore.CYAN)

    mysterious_print(" Obfuscating your Python file with AES-256...", Fore.MAGENTA)
    encrypted_code = encrypt_code(code, key)

    stub = generate_stub(encrypted_code, key)
    output_file = filepath.replace(".py", "_obfuscated.py")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stub)

    mysterious_print(f"\n Obfuscation complete!", Fore.GREEN)
    mysterious_print(f" Output saved as: {output_file}", Fore.BLUE)

if __name__ == "__main__":
    main()
