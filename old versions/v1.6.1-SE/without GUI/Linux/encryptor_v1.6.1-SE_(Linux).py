# Author github.com/retro-desert
# (c) 2019 GNU General Public License v3.0
# Mail nethertrooper@tuta.io
# PGP A1AF 5641

###########################################
#           ENCRYPTOR v1.6.1-SE           #
#                                         #
# NEED MODULES:                           #
# pycryptodomex                           #
###########################################


print("\nENCRYPTOR v1.6.1-SE\n"
      "Happy Halloween!")

import os, sys, time, pickle, random, tempfile, threading
from datetime import datetime

try:
 from Crypto.PublicKey import RSA
 from Crypto.Random import get_random_bytes
 from Crypto.Cipher import AES, PKCS1_OAEP
 import twofish_encryption1
 print("\nModules were installed")
except ImportError:
     print("\nThere were no such modules installed\n")
     o = input("Are you want to install modules?Y/N")
     if o == "Y":
         install = "pip3 install pycryptodomex"
         os.system(install)
         try:
             from Crypto.PublicKey import RSA
             from Crypto.Random import get_random_bytes
             from Crypto.Cipher import AES, PKCS1_OAEP
             import twofish_encryption1
             print("\nModules were installed")
         except ImportError:
             print("Modules not installed :(")
             sys.exit(1)

     if o == "N":
         sys.exit(1)

def arguments():
 global directory
 arg1 = sys.argv[1]
 arg2 = sys.argv[2]

 if (arg1 == "--dir" or
        arg1 == "-d"):
            directory = arg2
            print("Directory:", arg2)
 else:
            print("Error. Unknown param '{}'".format(arg1))
            sys.exit(1)

arguments()

script_directory = os.path.abspath(os.curdir)
directory_secretKey = script_directory + "//private.pem"
directory_publicKey = script_directory + "//receiver.pem"
listfile = directory + "//data.data"
cleanfile = directory
encrypt_data = directory + "//encrypt.data"

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
    print("\n(system) Data write")


def generate():
    def writer():
        print("It may take a long time.\n"
              "Generating 4096 key...")

    def generate_keys():
        key = RSA.generate(4096)
        private_key = key.export_key()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        # print(private_key)
        print("Private key created!")

        public_key = key.publickey().export_key()
        file_out = open("receiver.pem", "wb")
        file_out.write(public_key)
        # print(public_key)
        print("Public key created!")

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
            if os.path.getsize(directory_secretKey) > 1:
                print("Private key is here")
        except FileNotFoundError:
            generate2()
            break

        try:
            if os.path.getsize(directory_publicKey) > 1:
                print("Public key is here")
                g = input("Do you want to make new keys? Y/N")
                if g == "N":
                    break
                if g == "Y":
                    generate2()
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
 else:
         print("Cleaned!")


def delete_keys():
    clean1 = os.path.getsize(directory_secretKey)
    clean2 = os.path.getsize(directory_publicKey)
    os.remove(directory_secretKey)
    erase(+clean1)
    os.remove(directory_publicKey)
    erase(+clean2)

def twofish_encrypt():
    op = input("Input Data (English only):\n")
    twofish_encryption1.test = op
    print(twofish_encryption1.test)
    d = input("If you enter nothing, a 256-bit password will be generated"
              "\nInput Password:\n")

    if d == "":

        chars = \
            "+-/]\*;:|!&$(#?={~@`<>_)}[abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        password = ""
        for i in range(32):
            password += random.choice(chars)
        print("Password:\n", password)
        twofish_encryption1.key = password
    else:
        twofish_encryption1.key = d
    twofish_encryption1.start()
    twofish_encryption1.encrypt()
    f = open(encrypt_data, "wb")
    pickle.dump(twofish_encryption1.Cypher_text, f)
    f.close()
    print("\n File with cypher text saved")

def twofish_decrypt():
    f = open(encrypt_data, 'rb')
    stored = pickle.load(f)
    f.close()
    vv = input("Input Password:\n")
    twofish_encryption1.key = vv
    twofish_encryption1.test = stored
    twofish_encryption1.start()
    twofish_encryption1.decrypt()
    print("Data:\n", twofish_encryption1.plain_text)

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
    print(file + " ENCRYPT!")
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
    print(file + " DECRYPT!")
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

time.sleep(0.5)

while True:
 b = input("\nWhat do you want to do?\n"
           "1)Write data\n"
           "2)Generate keys\n"
           "3)Erase keys\n"
           "4)Encrypt data\n"
           "5)Decrypt data\n"
           "6)Twofish encrypt\n"
           "7)Twofish decrypt\n"
           "8) EXIT\n")

 if b ==("1"):
        book()
        break

 if b ==("2"):
     generate()
     break

 if b ==("3"):
    try:
        delete_keys()
        break
    except FileNotFoundError:
        print("No keys")
        break

 if b ==("4"):
         startTime = datetime.now()
         Crypt.walk(directory)
         endTime = datetime.now()
         print("Time: ", endTime - startTime)
         print("---------------------------------------------------------------")
         break

 if b ==("5"):
    try:
          startTime = datetime.now()
          Decrypt.walk(directory)
          endTime = datetime.now()
          print("Time: ", endTime - startTime)
          print("---------------------------------------------------------------")
          break
    except FileNotFoundError:
          print("File without extension")
          break
    except ValueError:
          print("File decrypted or corrupt")
          break

 if b == ("6"):
     twofish_encrypt()
     break

 if b ==("7"):
    try:
        twofish_decrypt()
        break
    except FileNotFoundError:
        print("No file with decrypt data!")

 if b ==("8"):
     break
