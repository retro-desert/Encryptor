__author__ = "Retro Desert " \
             "github.com/retro-desert"
__license__ = "(c) 2020 GNU General Public License v3.0"
__version__ = "1.8"
__maintainer__ = "Retro Desert"
__email__ = "nethertrooper@tuta.io"
# PGP: A1AF 5641

###########################################
#           ENCRYPTOR v1.8                #
###########################################

import os, sys, time, pickle, random, tempfile, threading
from datetime import datetime
import twofish_encryption

try:
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Random import get_random_bytes
    from Cryptodome.Cipher import AES, PKCS1_OAEP
    from colorama import Style, Back, Fore
    from colorama import init
    import colorama
except ImportError:
     print("\nThere were no such modules installed\n")
     o = input("Are you want to install modules?Y/N ")
     if o == "Y":
        os.system("pip install requests")
        os.system("pip3 install pycryptodomex")
        os.system("pip3 install colorama")
        try:
             from Cryptodome.PublicKey import RSA
             from Cryptodome.Random import get_random_bytes
             from Cryptodome.Cipher import AES, PKCS1_OAEP
             from colorama import Style, Back, Fore
             from colorama import init
             import colorama
             print("\nModules were installed")
        except ImportError:
             print("Modules not installed :(")
             sys.exit(1)

     if o == "N":
         sys.exit(1)

colorama.init()
init(autoreset=True)
print(Style.BRIGHT + Fore.CYAN + "\nENCRYPTOR v1.8")

def arguments():
 global directory
 try:
  arg1 = sys.argv[1]
  arg2 = sys.argv[2]
  if (arg1 == "--dir" or
          arg1 == "-d"):
      directory = arg2
      print("Directory:", arg2)
  else:
      print("Error. Unknown param '{}'".format(arg1))
      sys.exit(1)
 except IndexError:
  directory = input("Input work path: ")

arguments()

version = ("1.8")

script_directory = os.path.abspath(os.curdir)
directory_secretKey = script_directory + "//private.pem"
directory_publicKey = script_directory + "//receiver.pem"
listfile = directory + "//data.data"
cleanfile = directory
encrypt_data = script_directory + "//encrypt.data"

global walk
global crypt1
global decrypt1


def book():
    s = input("Input data: ")
    f = open(listfile, "wb")
    pickle.dump(s, f)
    f.close()
    f = open(listfile, "rb")
    storedlist = pickle.load(f)
    print(storedlist, end=" ")
    f.close()
    time.sleep(1)
    print("\n(system)", Style.BRIGHT + Fore.GREEN + "Data write")


def generate():

    def writer():
        print("It may take a long time.\n"
              "Generating 4096 bit key...")

    def generate_keys():
        key = RSA.generate(4096)
        private_key = key.export_key()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        # print(private_key)
        print(Style.BRIGHT + Fore.GREEN + "\nPrivate key created!")

        public_key = key.publickey().export_key()
        file_out = open("receiver.pem", "wb")
        file_out.write(public_key)
        # print(public_key)
        print(Style.BRIGHT + Fore.GREEN + "Public key created!")

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
                print("Private and public keys are here")
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
    clean1 = os.path.getsize(directory_secretKey)
    clean2 = os.path.getsize(directory_publicKey)
    os.remove(directory_secretKey)
    erase(+clean1)
    os.remove(directory_publicKey)
    erase(+clean2)


def twofish_encrypt():
    op = input("Input Data (English only):\n")
    twofish_encryption.test = op
    print("\n256 bit password will be generated if you enter nothing")
    d = input("Input Password:\n")

    if d == "":

        chars = \
            "+-/]\*;:|!&$(#?={~@`<>_)}[abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        password = ""
        for i in range(32):
            password += random.choice(chars)
        print(Style.BRIGHT + "Password:\n", Style.BRIGHT + Fore.GREEN + password)
        twofish_encryption.key = password
    else:
        twofish_encryption.key = d
    twofish_encryption.start()
    twofish_encryption.encrypt()
    f = open(encrypt_data, "wb")
    pickle.dump(twofish_encryption.Cypher_text, f)
    f.close()
    print(Style.BRIGHT + "\nFile with cypher text", Style.BRIGHT + Fore.GREEN + "saved")


def twofish_decrypt():
    f = open(encrypt_data, 'rb')
    stored = pickle.load(f)
    f.close()
    vv = input(Style.BRIGHT + "Input Password:\n")
    twofish_encryption.key = vv
    twofish_encryption.test = stored
    twofish_encryption.start()
    twofish_encryption.decrypt()
    print(Style.BRIGHT + "Data:\n", twofish_encryption.plain_text)


def update(s=1):
    try:
        r = requests.get("https://raw.githubusercontent.com/retro-desert/Encryptor/master/version_server.txt")
        server_version = r.text

        if server_version <= __version__:
            if s == 1:
                print(Style.BRIGHT + Fore.GREEN + "\nVersion is up to date!")
        else:
            print(Style.BRIGHT + "\nNew version", Style.BRIGHT + Fore.GREEN + "available!",
                  "\nDownload:", Style.BRIGHT + "https://github.com/retro-desert/Encryptor/releases")
            input("Press ENTER")
    except OSError:
        print(Style.BRIGHT + Fore.RED + "Error:", Style.BRIGHT + "Internet is disabled!")


class Crypt:
 def crypt1(file):

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
    print(file + Style.BRIGHT + Fore.GREEN + " ENCRYPT!")
    folder_size = os.path.getsize(file)
    os.remove(file)

    dir2 = cleanfile
    erase(+folder_size, dir2)


 def walk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            Crypt.crypt1(path)
        else:
            walk(path)


class Decrypt:
 def decrypt1(file):
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
    print(file + Style.BRIGHT + Fore.GREEN + " DECRYPT!")
    file_in.close()
    file_out.close()
    os.remove(file)

 def walk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            Decrypt.decrypt1(path)
        else:
            walk(path)

update(s=0)

while True:
    print(Style.BRIGHT + "\nWhat do you want to do?\n")
    print(Style.BRIGHT + Fore.YELLOW + "----------------")
    print(Style.BRIGHT + Fore.YELLOW + "0) Check updates")
    print(Style.BRIGHT + Fore.YELLOW +"----------------")
    print(Style.BRIGHT +
            "1) Write data\n"
            "2) Generate keys\n"
            "3) Erase keys\n"
            "4) Encrypt data\n"
            "5) Decrypt data\n"
            "6) Twofish encrypt\n"
            "7) Twofish decrypt")
    print(Style.BRIGHT + Fore.RED + "8) EXIT\n")

    b = input(Style.BRIGHT + ">> ")

    if b ==("0"):
        update()

    if b ==("1"):
        book()

    if b ==("2"):
        generate()

    if b ==("3"):
        try:
            delete_keys()
            print(Style.BRIGHT + Fore.GREEN + "Deleted!")
        except FileNotFoundError:
            print(Style.BRIGHT + Fore.RED + "Error:", Style.BRIGHT + "No keys")

    if b ==("4"):
        try:
            startTime = datetime.now()
            Crypt.walk(directory)
            endTime = datetime.now()
            print("Time: ", endTime - startTime)
            print("---------------------------------------------------------------")
        except FileNotFoundError:
            print(Style.BRIGHT + Fore.RED + "Error:", Style.BRIGHT + "Generate keys first")

    if b ==("5"):
        try:
            startTime = datetime.now()
            Decrypt.walk(directory)
            endTime = datetime.now()
            print("Time: ", endTime - startTime)
            print("---------------------------------------------------------------")
        except FileNotFoundError:
            print(Style.BRIGHT + Fore.RED + "Error:", Style.BRIGHT + "File without extension / Invalid keys")
        except ValueError:
            print(Style.BRIGHT + Fore.RED + "Error:", Style.BRIGHT + "File decrypted or corrupt")

    if b == ("6"):
        twofish_encrypt()

    if b ==("7"):
        try:
            twofish_decrypt()
        except FileNotFoundError:
            print(Style.BRIGHT + Fore.RED + "Error:", Style.BRIGHT + "No file to decrypt data!")

    if b ==("8"):
        break
