__author__ = "Retro Desert " \
             "github.com/retro-desert"
__license__ = "(c) 2020 GNU General Public License v3.0"
__version__ = "1.910"
__maintainer__ = "Retro Desert"
__email__ = "nethertrooper@tuta.io"
# PGP: A1AF 5641

###########################################
#           ENCRYPTOR v1.910              #
###########################################

print("\nENCRYPTOR v1.910")

import os, sys, pickle, random, tempfile, threading, webbrowser, requests

from datetime import datetime
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
from PyQt5 import QtWidgets
import design, twofish_encryption
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QObject
import PyQt5.QtGui
from PIL import Image

image1 = Image.open("logo.ico")
image2 = Image.open("image.jpg")

script_directory = os.path.abspath(os.curdir)
icon = script_directory + "\\logo.ico"
directory = ""
image = script_directory + "\\image.jpg"
directory_secretKey = script_directory + "\\private.pem"
directory_publicKey = script_directory + "\\receiver.pem"


global walk
global crypt1
global decrypt1


class OutputLogger(QObject):

    emit_write = Signal(str, int)

    class Severity:
        DEBUG = 0
        ERROR = 1

    def __init__(self, io_stream, severity):
        super().__init__()

        self.io_stream = io_stream
        self.severity = severity

    def write(self, text):
        self.io_stream.write(text)
        self.emit_write.emit(text, self.severity)

    def flush(self):
        self.io_stream.flush()


OUTPUT_LOGGER_STDOUT = OutputLogger(sys.stdout, OutputLogger.Severity.DEBUG)
OUTPUT_LOGGER_STDERR = OutputLogger(sys.stderr, OutputLogger.Severity.ERROR)

sys.stdout = OUTPUT_LOGGER_STDOUT
sys.stderr = OUTPUT_LOGGER_STDERR


class App(QtWidgets.QMainWindow, design.Ui_Encryptor):
    global error
    def __init__(self):

        global secretKey
        global publicKey
        
        super().__init__()

        OUTPUT_LOGGER_STDOUT.emit_write.connect(self.append_log)
        OUTPUT_LOGGER_STDERR.emit_write.connect(self.append_log)

        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.browse_folder)
        self.pushButton.clicked.connect(lambda: self.buttonClicked())
        self.pushButton_2.clicked.connect(lambda: self.buttonClicked1())
        self.pushButton_3.clicked.connect(lambda: self.buttonClicked2())
        self.pushButton_4.clicked.connect(lambda: self.buttonClicked3())
        self.pushButton_5.clicked.connect(lambda: self.buttonClicked4())
        self.pushButton_6.clicked.connect(lambda: self.buttonClicked5())
        self.pushButton_7.clicked.connect(lambda: self.buttonClicked6())
        self.pushButton_8.clicked.connect(lambda: self.buttonClicked7())
        self.pushButton_9.clicked.connect(lambda: self.buttonClicked8())
        self.setWindowIcon(PyQt5.QtGui.QIcon(icon))
        print("ENCRYPTOR v1.910\n")
        self.buttonClicked8(s=0)

    def append_log(self, text, severity):

        if severity == OutputLogger.Severity.ERROR:
            self.text_edit.append("{}".format(text))
        else:
            self.text_edit.append(text)

    def browse_folder(self):
        global directory, encrypt_data
        self.listWidget.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder")
        print(directory)
        global listfile, cleanfile
        listfile = directory + "\\data.data"
        cleanfile = directory
        encrypt_data = directory + "\\encrypt.data"

        if directory:
            for file_name in os.listdir(directory):
                self.listWidget.addItem(file_name)

    def buttonClicked(self):
      try:
        global text
        text,\
        s = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                  "Input Data:")

        if s:
            f = open(listfile, "wb")
            pickle.dump(text, f)
            f.close()
            print("\n[+] Data write")
      except NameError:
            print("[-]Error: You didn't select a folder")


    def buttonClicked1(self):

        def writer():
            print("[*]It may take a long time.\n"
                  "Generating 4096 bit key...")

        def generate_keys():
            key = RSA.generate(4096)
            private_key = key.export_key()
            file_out = open("private.pem", "wb")
            file_out.write(private_key)
            # print(private_key)
            print("[+]Private key created!")

            public_key = key.publickey().export_key()
            file_out = open("receiver.pem", "wb")
            file_out.write(public_key)
            # print(public_key)
            print("[+]Public key created!")

        def generate2():
            # init events
            e1 = threading.Event()
            # e2 = threading.Event()

            # init threads
            s = PyQt5.QtWidgets.QMessageBox.question(self, "Message", "It may take a long time.\n "
                                                                      "Generating 4096 bit key...",
                                                     PyQt5.QtWidgets.QMessageBox.Ok)
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
                if os.path.getsize(directory_secretKey) and os.path.getsize(directory_publicKey):
                    print("[*]Private and public keys are here")
                    text, \
                    g = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                       "Do you want to make new keys? Y/N:")
                    if text == "Y":
                        generate2()
                        break
                    else:
                        break
            except FileNotFoundError:
                generate2()
                break

    def buttonClicked2(self):
          try:
            delete_keys()
            print("[+]Deleted!")
          except FileNotFoundError:
            print("[-]Error: No keys")

    def buttonClicked3(self):
         try:
            startTime = datetime.now()
            Crypt.walk(directory)
            endTime = datetime.now()
            print("Time: ", endTime - startTime)
            print("--------------------------------------------------------------")
         except FileNotFoundError:
            print("[-]Error: You didn't select a folder/"
                  "Generate keys first")

    def buttonClicked4(self):
          try:
            startTime = datetime.now()
            Decrypt.walk(directory)
            endTime = datetime.now()
            print("Time: ", endTime - startTime)
            print("--------------------------------------------------------------")

          except FileNotFoundError:
              print("[-]Error: You didn't select a folder/"
                    "Generate keys first/"
                    "File without extension")

          except ValueError:
              print("[-]Error: File decrypted or corrupt")

    def buttonClicked5(self):

            sys.exit(1)

    def buttonClicked6(self):

            text, \
            op = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                           "Input Data (only English):")

            if op:
                twofish_encryption.test = text

            text, \
            op1 = QtWidgets.QInputDialog.getText(self, "Input Password",
                                                "256 bit password will be generated if you enter nothing")
            if op1:
                if text == "":
                    chars = \
                        "+-/]\*;:|!&$(#?={~@`<>"\
                        "_)}[abcdefghijklnopqrs"\
                        "tuvwxyzABCDEFGHIJKLMNO"\
                        "PQRSTUVWXYZ1234567890"
                    password = ""
                    for i in range(32):
                        password += random.choice(chars)
                    print("[*]Password:", password)
                    twofish_encryption.key = password
                else:
                    twofish_encryption.key = text

            twofish_encryption.start()
            twofish_encryption.encrypt()
            f = open(encrypt_data, "wb")
            pickle.dump(twofish_encryption.Cypher_text, f)
            f.close()
            print("\n[+]File with cypher text saved")

    def buttonClicked7(self):

         try:
            text, \
            po = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                "Input Password:")

            if po:
                    twofish_encryption.key = text

                    f = open(encrypt_data, "rb")
                    stored = pickle.load(f)
                    f.close()
                    twofish_encryption.test = stored
                    twofish_encryption.start()
                    twofish_encryption.decrypt()
                    print("[+]Data:", twofish_encryption.plain_text)

         except FileNotFoundError:
                    print("[-]Error: No file with decrypt data!")

    def buttonClicked8(self, s=1):
        try:
            r = requests.get(
                "https://raw.githubusercontent.com/retro-desert/Encryptor/master/version_server.txt"
            )
            server_version = r.text

            if server_version <= __version__:
                if s == 1:
                 print("[*]Version is up to date!")
            else:
                msgBox = PyQt5.QtWidgets.QMessageBox()
                msgBox.setIcon(PyQt5.QtWidgets.QMessageBox.Information)
                msgBox.setWindowIcon(PyQt5.QtGui.QIcon(icon))
                msgBox.setText("New version available!\n"
                               "Download?")
                msgBox.setWindowTitle("Message")
                msgBox.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Ok | PyQt5.QtWidgets.QMessageBox.No)

                returnValue = msgBox.exec()
                if returnValue == PyQt5.QtWidgets.QMessageBox.Ok:
                    webbrowser.open("https://github.com/retro-desert/Encryptor/releases", new=2)

        except OSError:
            if s == 1:
                PyQt5.QtWidgets.QMessageBox.question(self, "Message", "Internet is disabled!",
                                                PyQt5.QtWidgets.QMessageBox.Ok)


def erase(size, dir1=script_directory):

        for i in range(1, 36):
            size = random.randint(100, 10000)
            random_filename = tempfile.mktemp(dir=dir1)
            c1 = open(random_filename, "wb")
            c1.write(os.urandom(size))
            c1.close()
            os.remove(random_filename)


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
            print("[+]" + file + " ENCRYPT!")
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
            print("[+]" + file + " DECRYPT!")
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


def main():

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("QLabel {color: white}"
                      "QMainWindow { border-image: url(image)}"
                      "QTextEdit {background-color: black; color: white; font-weight: bold}"
                      "QListWidget {background-color: black; color: white; font-weight: bold}"
                      "QInputDialog {background-color: black; color: white; font-weight: bold}"
                      "QMessageBox {background-color: black; color: white; font-weight: bold}")
    window = App()
    window.show()
    app.exec_()

sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    # print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    try:
     main()
    except:
     sys.excepthook()