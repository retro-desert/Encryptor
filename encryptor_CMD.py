__author__ = "Retro Desert " \
             "github.com/retro-desert"
__license__ = "(c) 2020 GNU General Public License v3.0"
__version__ = "1.935"
__maintainer__ = "Retro Desert"
__email__ = "iljaaz@yandex.ru"

# PGP: 502b 51e0

###########################################
#           ENCRYPTOR v1.935-SE           #
###########################################

import argparse
import os
import pickle
import random
import sys
import tempfile
import threading
from sys import platform

import twofish_encryption

if platform == "linux" or platform == "linux2":
    platform_var = "lin"
elif platform == "win32":
    platform_var = "win"

while True:
    try:
        from Cryptodome.PublicKey import RSA
        from Cryptodome.Random import get_random_bytes
        from Cryptodome.Cipher import AES, PKCS1_OAEP
        import requests
        from colorama import Style, Back, Fore
        from colorama import init
        import colorama

        break
    except ImportError:
        print("\n[-]There were no such modules installed\n")
        o = input("Are you want to install modules?Y/N ")
        if o == "Y":
            if platform_var == "lin":
                os.system("pip3 install requests")
                os.system("pip3 install pycryptodomex")
                os.system("pip3 install colorama")

            elif platform_var == "win":
                os.system("pip install requests")
                os.system("pip install pycryptodome")
                os.system("pip install colorama")
            continue

        if o == "N":
            sys.exit(1)

directory = ""
args = ""
colorama.init()
init(autoreset=True)
print(Style.BRIGHT + Fore.CYAN + """
███████╗███╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ██████╗
██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
█████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║██████╔╝
██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║██╔══██╗
███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝██║  ██║
╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝
""")
print(Style.BRIGHT + Fore.CYAN + f"ENCRYPTOR {__version__}-SE")
print(Style.BRIGHT + Fore.RED + "Happy Halloween!")


def arguments():
    global directory
    global args

    parser = argparse.ArgumentParser(description=
                                     "Example: "
                                     "python encryptor_CMD.py -P "
                                     "/home/admin/test"
                                     " (or"
                                     " 'C:\\Users\\admin\\test')")

    parser.add_argument(
        "-P", "--path",
        type=str,
        help="Path to files"
    )

    parser.add_argument(
        "-G", "--generate",
        action="store_true",
        help="Generate keys"
    )

    parser.add_argument(
        "-EK", "--erase_keys",
        action="store_true",
        help="Erase Keys"
    )

    parser.add_argument(
        "-C", "--crypt",
        action="store_true",
        help="Crypt Files"
    )

    parser.add_argument(
        "-D", "--decrypt",
        action="store_true",
        help="Decrypt Files"
    )

    parser.add_argument(
        "-TE", "--twofish_enc",
        action="store_true",
        help="Twofish encryption"
    )

    parser.add_argument(
        "-TD", "--twofish_dec",
        action="store_true",
        help="Twofish decryption"
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run dev test"
    )

    args = parser.parse_args()

    if args.path:
        directory = args.path
        print("Directory: ", directory)
    else:
        directory = input("[+]Input work path: ")


arguments()

src_dir = os.path.abspath(os.curdir)
cleanfile = directory
if platform_var == "lin":
    dir_secKey = src_dir + "//private.pem"
    dir_pubKey = src_dir + "//receiver.pem"
    bookfile = directory + "//data.data"
    encrypt_data = src_dir + "//encrypt.data"

elif platform_var == "win":
    dir_secKey = src_dir + "\\private.pem"
    dir_pubKey = src_dir + "\\receiver.pem"
    bookfile = directory + "\\data.data"
    encrypt_data = directory + "\\encrypt.data"

global walk
global crypt1
global decrypt1


def book(test=0, data=""):
    try:
        if test == 0:
            data = input("Input data: ")
        f = open(bookfile, "wb")
        pickle.dump(data, f)
        f.close()
        print("\n[✓]", Style.BRIGHT + Fore.GREEN + "Data write")
    except FileNotFoundError or PermissionError:
        print(Style.BRIGHT + Fore.RED + "[-] Error:", Style.BRIGHT + "You selected an invalid folder")


def generate():
    def writer():
        print("[*]It may take a long time.\n"
              "Generating 4096 bit key...")

    def generate_keys():
        try:
            key = RSA.generate(4096)
            private_key = key.export_key()
            file_out = open("private.pem", "wb")
            file_out.write(private_key)
            # print(private_key)

            public_key = key.publickey().export_key()
            file_out = open("receiver.pem", "wb")
            file_out.write(public_key)
            # print(public_key)

            print(Style.BRIGHT + Fore.GREEN + "[✓]Keys generated!")
        except:
            print("[-] Keys not generated")

    def generate2():
        # init events
        e1 = threading.Event()
        e2 = threading.Event()

        # init threads
        t1 = threading.Thread(target=writer)
        t2 = threading.Thread(target=generate_keys)

        # start threads
        t1.start()
        t2.start()

        e1.set()  # initiate the first event

        # join threads to the main thread
        t1.join()
        t2.join()

    while True:
        try:
            if os.path.getsize(dir_secKey) and os.path.getsize(dir_pubKey):
                print("[*]Keys are here")
                print(Style.BRIGHT + "Do you want to make new keys? ",
                      Style.BRIGHT + Fore.GREEN + "Y",
                      "/", Style.BRIGHT + Fore.RED + "N")
                g = input()
                if g == "Y":
                    generate2()
                    break
                else:
                    break
        except FileNotFoundError:
            generate2()
            break


def erase(size, dir1=src_dir):
    for i in range(1, 36):
        size = random.randint(100, 10000)
        random_filename = tempfile.mktemp(dir=dir1)
        c1 = open(random_filename, "wb")
        c1.write(os.urandom(size))
        c1.close()
        os.remove(random_filename)


def delete_keys():
    try:
        clean1 = os.path.getsize(dir_secKey)
        clean2 = os.path.getsize(dir_pubKey)
        os.remove(dir_secKey)
        erase(+clean1)
        os.remove(dir_pubKey)
        erase(+clean2)
        print(Style.BRIGHT + Fore.GREEN + "[+]Keys deleted!")
    except FileNotFoundError:
        print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "No keys")


def twofish_encrypt(test=0, data="", password=""):
    try:
        if test == 0:
            data = input("Input Data (English only):\n")
        twofish_encryption.test = data
        print("\n256 bit password will be generated if you enter nothing")
        if test == 0:
            password = input("Input Password:\n")

        if password == "":

            chars = \
                "+-/]\*;:|!&$(#?={~@`<>" \
                "_)}[abcdefghijklnopqrs" \
                "tuvwxyzABCDEFGHIJKLMNO" \
                "PQRSTUVWXYZ1234567890"

            password = ""
            for i in range(32):
                password += random.choice(chars)
            print(Style.BRIGHT + "[*]Password:\n", Style.BRIGHT + Fore.GREEN + password)
            twofish_encryption.key = password
        else:
            twofish_encryption.key = password
        twofish_encryption.start()
        twofish_encryption.encrypt()
        f = open(encrypt_data, "wb")
        pickle.dump(twofish_encryption.Cypher_text, f)
        f.close()
        print(Style.BRIGHT + "\n[✓]File with cypher text", Style.BRIGHT + Fore.GREEN + "saved")
    except FileNotFoundError or NameError:
        print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "You selected an invalid folder")


def twofish_decrypt(test=0, password=""):
    try:
        f = open(encrypt_data, "rb")
        stored = pickle.load(f)
        f.close()
        if test == 0:
            password = input("Input Password:\n")
        twofish_encryption.key = password
        twofish_encryption.test = stored
        twofish_encryption.start()
        twofish_encryption.decrypt()
        print(Style.BRIGHT + "[+]Data:\n", twofish_encryption.plain_text)

    except FileNotFoundError:
        print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "No file to decrypt data!")


def update(status=1):
    try:
        r = requests.get(
            "https://raw.githubusercontent.com/retro-desert/Encryptor/master/version_server.txt"
        )
        server_version = r.text

        if server_version <= __version__:
            if status == 1:
                print(Style.BRIGHT + Fore.GREEN + "\nVersion is up to date!")
        else:
            print(Style.BRIGHT + "\n[*]New version", Style.BRIGHT + Fore.GREEN + "available!",
                  "\nDownload:", Style.BRIGHT +
                  "https://github.com/retro-desert/Encryptor/releases")
            input("Press ENTER")
    except OSError:
        print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "Internet is disabled!")


def crypt2():
    # startTime = datetime.now()
    Crypt.walk(directory)
    # endTime = datetime.now()
    # print("Time: ", endTime - startTime)
    # print("---------------------------------------------------------------")


def decrypt2():
    # startTime = datetime.now()
    Decrypt.walk(directory)
    # endTime = datetime.now()
    # print("Time: ", endTime - startTime)
    # print("---------------------------------------------------------------")


def testing():
    update()
    book(test=1, data="lol1234-_-/testing")
    generate()
    crypt2()
    decrypt2()
    twofish_encrypt(test=1, data="lol1234-_-/testing", password="1234password_test")
    twofish_decrypt(test=1, password="1234password_test")
    delete_keys()


class Crypt:
    def crypt1(file):
        try:
            f = open(file, "rb")
            data = f.read()
            f.close()

            file_out = open(str(file) + ".bin", "wb")

            recipient_key = RSA.import_key(open(dir_pubKey).read())
            session_key = get_random_bytes(16)

            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            enc_session_key = cipher_rsa.encrypt(session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)

            [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
            file_out.close()
            print("[✓]" + file + Style.BRIGHT + Fore.GREEN + " ENCRYPT!")
            folder_size = os.path.getsize(file)
            os.remove(file)

            dir2 = cleanfile
            erase(+folder_size, dir2)

        except FileNotFoundError:
            try:
                if os.path.getsize(dir_secKey) and os.path.getsize(dir_pubKey):
                    print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "You selected an invalid folder")
            except FileNotFoundError:
                print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "Generate keys first")

    def walk(dir):
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                Crypt.crypt1(path)
            else:
                walk(path)


class Decrypt:
    def decrypt1(file):
        try:
            file_in = open(file, "rb")
            file_out = open(str(file[:-4]), "wb")
            private_key = RSA.import_key(open(dir_secKey).read())

            enc_session_key, nonce, tag, ciphertext = \
                [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            file_out.write(data)
            print("[✓]" + file + Style.BRIGHT + Fore.GREEN + " DECRYPT!")
            file_in.close()
            file_out.close()
            os.remove(file)

        except FileNotFoundError:
            try:
                if os.path.getsize(dir_secKey) and os.path.getsize(dir_pubKey):
                    print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "You selected an invalid folder /\n"
                                                                                "File without extension")
            except FileNotFoundError:
                print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "Generate keys first")
        except ValueError:
            print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "File decrypted or corrupt")

    def walk(dir):
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                Decrypt.decrypt1(path)
            else:
                walk(path)


if args.generate:
    generate()
    sys.exit(1)

elif args.erase_keys:
    delete_keys()
    sys.exit(1)

elif args.crypt:
    crypt2()
    sys.exit(1)

elif args.decrypt:
    decrypt2()
    sys.exit(1)

elif args.twofish_enc:
    twofish_encrypt()
    sys.exit(1)

elif args.twofish_dec:
    twofish_decrypt()
    sys.exit(1)

if not args.test:
    update(status=0)

    while True:
        print(Style.BRIGHT + "\n--What do you want to do?--\n")
        print(Style.BRIGHT + Fore.YELLOW +
              "   _________________\n0) ┤║Check updates║├\n   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        print(Style.BRIGHT +
              "1) Write data\n"
              "2) Generate keys\n"
              "3) Erase keys\n"
              "4) Encrypt data\n"
              "5) Decrypt data\n"
              "6) Twofish encrypt\n"
              "7) Twofish decrypt")
        print(Style.BRIGHT + Fore.RED + "8) EXIT\n")

        b = input(">> ")

        if b == "0":
            update()

        if b == "1":
            book()

        if b == "2":
            generate()

        if b == "3":
            delete_keys()

        if b == "4":
            crypt2()

        if b == "5":
            decrypt2()

        if b == "6":
            twofish_encrypt()

        if b == "7":
            twofish_decrypt()

        if b == "8":
            break

else:
    testing()
