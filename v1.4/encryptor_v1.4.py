# Author github.com/retro-desert
# (c) 2019 GNU General Public License v3.0
# Mail nethertrooper@tuta.io
# PGP A1AF 5641

###########################################
#             ENCRYPTOR v1.4              |
#                                         |
# NEED MODULES:                           |
# pycryptodomex                           |
###########################################


print("\nENCRYPTOR v1.4")

import os, sys, time, pickle, random, tempfile

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
cleanfile = directory
script_directory = os.path.abspath(os.curdir)

global walk
global crypt1
global decrypt1

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
    print("It may take a long time.\n"
          "Generating 4096 key...")
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
           "6) EXIT\n")
 if b ==("1"):
     book()
     view_data()
     break
 if b ==("2"):
     generate()
     break
 if b ==("3"):
     delete_keys()
     break
 if b ==("4"):
     Crypt.walk(directory)
     print("---------------------------------------------------------------")
     break
 if b ==("5"):
     Decrypt.walk(directory)
     print("---------------------------------------------------------------")
     break
 if b ==("6"):
     break
