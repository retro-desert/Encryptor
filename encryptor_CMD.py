__author__ = "Retro Desert " \
             "github.com/retro-desert"
__license__ = "(c) 2020 GNU General Public License v3.0"
__version__ = "1.9"
__maintainer__ = "Retro Desert"
__email__ = "nethertrooper@tuta.io"
# PGP: A1AF 5641

###########################################
#           ENCRYPTOR v1.9                #
###########################################

import os, sys, pickle, random, tempfile, threading, argparse
from datetime import datetime
import twofish_encryption
from sys import platform

try:
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Random import get_random_bytes
    from Cryptodome.Cipher import AES, PKCS1_OAEP
    import requests
    from colorama import Style, Back, Fore
    from colorama import init
    import colorama
except ImportError:
    print("\n[-]There were no such modules installed\n")
    o = input("Are you want to install modules?Y/N ")
    if o == "Y":
        if platform == "linux" or platform == "linux2":
            os.system("pip3 install requests")
            os.system("pip3 install pycryptodomex")
            os.system("pip3 install colorama")

        elif platform == "win32":
            os.system("pip install requests")
            os.system("pip install pycryptodome")
            os.system("pip install colorama")
        try:

            from Cryptodome.PublicKey import RSA
            from Cryptodome.Random import get_random_bytes
            from Cryptodome.Cipher import AES, PKCS1_OAEP
            import requests
            from colorama import Style, Back, Fore
            from colorama import init
            import colorama
            print("\n[✓]Modules were installed")
        except ImportError:
            print("[-]Modules not installed :(")
            sys.exit(1)

    if o == "N":
         sys.exit(1)

directory = ""
args = ""
colorama.init()
init(autoreset=True)
print(Style.BRIGHT + Fore.CYAN + "\nENCRYPTOR v1.9")

def arguments():
 global directory
 global args

 parser = argparse.ArgumentParser(description=
                                    "Example: "
                                    "python encryptor_windows.py -P "
                                    "/home/admin/test"
                                    " or"
                                    " 'C:\\Users\\admin\\test'")

 parser.add_argument(
     "-P", "--path",
     type=str,
     help="Path to files"
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

script_directory = os.path.abspath(os.curdir)
cleanfile = directory
if platform == "linux" or platform == "linux2":
    directory_secretKey = script_directory + "//private.pem"
    directory_publicKey = script_directory + "//receiver.pem"
    listfile = directory + "//data.data"
    encrypt_data = script_directory + "//encrypt.data"

elif platform == "win32":
    directory_secretKey = script_directory + "\\private.pem"
    directory_publicKey = script_directory + "\\receiver.pem"
    listfile = directory + "\\data.data"
    encrypt_data = directory + "\\encrypt.data"

global walk
global crypt1
global decrypt1


def book(test=0, s="0"):
    if test == 0:
        s = input("Input data: ")
    f = open(listfile, "wb")
    pickle.dump(s, f)
    f.close()
    print("\n[✓]", Style.BRIGHT + Fore.GREEN + "Data write")


def generate():

    def writer():
        print("[+]It may take a long time.\n"
              "Generating 4096 bit key...")

    def generate_keys():
        key = RSA.generate(4096)
        private_key = key.export_key()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        #print(private_key)
        print(Style.BRIGHT + Fore.GREEN + "\n[✓]Private key created!")

        public_key = key.publickey().export_key()
        file_out = open("receiver.pem", "wb")
        file_out.write(public_key)
        # print(public_key)
        print(Style.BRIGHT + Fore.GREEN + "[✓]Public key created!")

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
            if os.path.getsize(directory_secretKey) > 1 and os.path.getsize(directory_publicKey) > 1:
                print("[+]Private and public keys are here")
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


def erase(size, dir1=script_directory):
    for i in range(1, 36):
         more_size = random.randint(100, 10000)
         size = more_size
         x = os.urandom(size)
         random_filename = tempfile.mktemp(dir=dir1)
         c1 = open(random_filename, "wb")
         c1.write(x)
         c1.close()
         os.remove(random_filename)


def delete_keys():
    try:
        clean1 = os.path.getsize(directory_secretKey)
        clean2 = os.path.getsize(directory_publicKey)
        os.remove(directory_secretKey)
        erase(+clean1)
        os.remove(directory_publicKey)
        erase(+clean2)
        print(Style.BRIGHT + Fore.GREEN + "[+]Deleted!")
    except FileNotFoundError:
        print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "No keys")


def twofish_encrypt(test=0, op="", d=""):
    if test == 0:
        op = input("Input Data (English only):\n")
    twofish_encryption.test = op
    print("\n256 bit password will be generated if you enter nothing")
    if test == 0:
        d = input("Input Password:\n")

    if d == "":

        chars = \
            "+-/]\*;:|!&$(#?={~@`<>"\
            "_)}[abcdefghijklnopqrs"\
            "tuvwxyzABCDEFGHIJKLMNO"\
            "PQRSTUVWXYZ1234567890"

        password = ""
        for i in range(32):
            password += random.choice(chars)
        print(Style.BRIGHT + "[+]Password:\n", Style.BRIGHT + Fore.GREEN + password)
        twofish_encryption.key = password
    else:
        twofish_encryption.key = d
    twofish_encryption.start()
    twofish_encryption.encrypt()
    f = open(encrypt_data, "wb")
    pickle.dump(twofish_encryption.Cypher_text, f)
    f.close()
    print(Style.BRIGHT + "\n[✓]File with cypher text", Style.BRIGHT + Fore.GREEN + "saved")


def twofish_decrypt(test=0, vv=""):
    try:
        f = open(encrypt_data, "rb")
        stored = pickle.load(f)
        f.close()
        if test == 0:
            vv = input("Input Password:\n")
        twofish_encryption.key = vv
        twofish_encryption.test = stored
        twofish_encryption.start()
        twofish_encryption.decrypt()
        print(Style.BRIGHT + "[+]Data:\n", twofish_encryption.plain_text)

    except FileNotFoundError:
        print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "No file to decrypt data!")


def update(s=1):
    try:
        r = requests.get(
            "https://raw.githubusercontent.com/retro-desert/Encryptor/master/version_server.txt"
        )
        server_version = r.text

        if server_version <= __version__:
            if s == 1:
                print(Style.BRIGHT + Fore.GREEN + "\nVersion is up to date!")
        else:
            print(Style.BRIGHT + "\n[+]New version", Style.BRIGHT + Fore.GREEN + "available!",
                  "\nDownload:", Style.BRIGHT + "https://github.com/retro-desert/Encryptor/releases")
            input("Press ENTER")
    except OSError:
        print(Style.BRIGHT + Fore.RED + "Error:", Style.BRIGHT + "Internet is disabled!")


def crypt2():
        startTime = datetime.now()
        Crypt.walk(directory)
        endTime = datetime.now()
        print("Time: ", endTime - startTime)
        print("---------------------------------------------------------------")


def decrypt2():
        startTime = datetime.now()
        Decrypt.walk(directory)
        endTime = datetime.now()
        print("Time: ", endTime - startTime)
        print("---------------------------------------------------------------")

def testing():
        update()
        book(test=1, s="lol1234-_-/testing")
        generate()
        crypt2()
        decrypt2()
        twofish_encrypt(test=1, op="lol1234-_-/testing", d="1234password_test")
        twofish_decrypt(test=1, vv="1234password_test")
        delete_keys()


class Crypt:
 def crypt1(file):
    try:
        f = open(file, "rb")
        data = f.read()
        f.close()

        file_out = open(str(file) + ".bin", "wb")

        recipient_key = RSA.import_key(open(directory_publicKey).read())
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
        private_key = RSA.import_key(open(directory_secretKey).read())

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
        print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "File without extension / Invalid keys")
    except ValueError:
        print(Style.BRIGHT + Fore.RED + "[-]Error:", Style.BRIGHT + "File decrypted or corrupt")

 def walk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            Decrypt.decrypt1(path)
        else:
            walk(path)

if args.crypt:
    crypt2()
    sys.exit(1)

if args.decrypt:
    decrypt2()
    sys.exit(1)

if args.twofish_enc:
    twofish_encrypt()
    sys.exit(1)

if args.twofish_dec:
    twofish_decrypt()
    sys.exit(1)

if not args.test:
    update(s=0)

    while True:
        print(Style.BRIGHT + "\n--What do you want to do?--\n")
        print(Style.BRIGHT + Fore.YELLOW +
              "----------------\n0) Check updates\n----------------")
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

        if b ==("0"):
            update()

        if b ==("1"):
            book()

        if b ==("2"):
            generate()

        if b ==("3"):
            delete_keys()

        if b ==("4"):
            crypt2()

        if b ==("5"):
            decrypt2()

        if b == ("6"):
            twofish_encrypt()

        if b ==("7"):
            twofish_decrypt()

        if b ==("8"):
            break

else:
        testing()