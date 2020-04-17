from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
import os, sys, time, pickle

listfile = "C:\\Users\\Gopnik\\Desktop\\codes on python\\papka\\data.data"#Name of file with data
directory = "C:\\Users\\Gopnik\\Desktop\\codes on python\\papka"#Folder to encrypt/decrypt
directory_secretKey = "C:\\Users\\Gopnik\\Desktop\\codes on python\\private.pem"#Private key
directory_publicKey = "C:\\Users\\Gopnik\\Desktop\\codes on python\\receiver.pem"#Public key

def kniga():
    global s,s1,f
    s = input("Input name: ")
    f = open(listfile, "wb")
    pickle.dump(s, f)
    f.close()
    s1 = input("Input surname: ")
    f = open(listfile, "wb")
    pickle.dump(s+s1, f)
    f.close()

def generate():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    print(private_key)

    public_key = key.publickey().export_key()
    file_out = open("receiver.pem", "wb")
    file_out.write(public_key)
    print(public_key)

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
        if os.path.isfile(path): Crypt.crypt1(path)
        else: walk(path)
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
        if os.path.isfile(path): Decrypt.decrypt1(path)
        else: walk(path)

time.sleep(1)
while True:
 g = input("Want write data?Y/N\n")
 if g ==("Y"):
  kniga()
  f = open(listfile, 'rb')
  storedlist = pickle.load(f)
  f.close()
  print(storedlist, end=" ")
  time.sleep(1)
  print("\n(system) Data write")
  break
 if g ==("N"):
  break

while True:
    a = input("Want generate keys?Y/N ")
    if a == ("Y"):
        generate()
        break
    if a == ("N"):
        break

while True:
 p = input("Want encrypt data? Y/N ")
 if p == ("Y"):
     Crypt.walk(directory)
     print("---------------------------------------------------------------")
     break
 if p == ("N"):
     break

while True:
 l = input("Want decrypt data? Y/N ")
 if l == ("Y"):
  Decrypt.walk(directory)
  break
 if l == ("N"):
  print("Goodbye!")
  break
