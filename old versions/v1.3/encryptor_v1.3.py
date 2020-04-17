# Author github.com/retro-desert
# (c) 2019 GNU General Public License v3.0
# Mail nethertrooper@tuta.io
# PGP A1AF 5641

###########################################
#             ENCRYPTOR v1.3              |
#                                         |
# NEED MODULES:                           |
# pycryptodomex                           |
###########################################


import os, sys, time, pickle
try:
 from Cryptodome.PublicKey import RSA
 from Cryptodome.Random import get_random_bytes
 from Cryptodome.Cipher import AES, PKCS1_OAEP
 print("\nModules were installed")
except ImportError:
     print("\nThere were no such modules installed\n")
     o = input("Are you want to install modules?Y/N")
     if o == "Y":
         install = "pip install pycryptodomex"
         os.system(install)
         try:
             from Cryptodome.PublicKey import RSA
             from Cryptodome.Random import get_random_bytes
             from Cryptodome.Cipher import AES, PKCS1_OAEP

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

secretKey = "\\private.pem"
publicKey = "\\receiver.pem"
list = "\\data.data"

directory_secretKey = os.path.abspath(os.curdir)+secretKey
directory_publicKey = os.path.abspath(os.curdir)+publicKey
listfile = directory+list

def book():
    s = input("Input data: ")
    f = open(listfile, "wb")
    pickle.dump(s, f)
    f.close()

def view_data():
     f = open(listfile, 'rb')
     storedlist = pickle.load(f)
     print(storedlist, end=" ")
     f.close()
     time.sleep(1)
     print("\n(system) Data write")

def generate():
    print("It may take a long time.\nGenerating 4096 key...")
    key = RSA.generate(4096)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    #print(private_key)
    print("Private key created!")

    public_key = key.publickey().export_key()
    file_out = open("receiver.pem", "wb")
    file_out.write(public_key)
    #print(public_key)
    print("Public key created!")

global walk
global crypt1
global decrypt1

class Crypt:
 def crypt1(file):

    f = open(file, "rb")
    data = f.read();
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
    time.sleep(1)
    os.remove(file)

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
    time.sleep(1)
    os.remove(file)

 def walk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            Decrypt.decrypt1(path)
        else:
            walk(path)

time.sleep(1)

while True:
 b = input("What do you want to do?\n1)Write data\n2)Generate keys\n3)Encrypt data\n4)Decrypt data\n5) EXIT\n")
 if b ==("1"):
     book()
     view_data()
     break
 if b ==("2"):
     generate()
     break
 if b ==("3"):
     Crypt.walk(directory)
     print("---------------------------------------------------------------")
     break
 if b ==("4"):
     Decrypt.walk(directory)
     print("---------------------------------------------------------------")
     break
 if b ==("5"):
     break
