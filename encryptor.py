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

import os
import pickle
import random
import requests
import sys
import tempfile
import threading
import webbrowser

import PyQt5.QtGui
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal

import design
import twofish_encryption

src_dir = os.path.abspath(os.curdir)

try:
    image = sys._MEIPASS + "\\image.jpg"
    icon = sys._MEIPASS + "\\logo.ico"
except AttributeError:
    icon = src_dir + "\\logo.ico"
    image = src_dir + "\\image.jpg"

directory = ""
dir_secKey = src_dir + "\\private.pem"
dir_pubKey = src_dir + "\\receiver.pem"

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
        print(f"ENCRYPTOR {__version__}-SE\nHappy Halloween!")
        self.buttonClicked8(status=0)

    def resizeEvent(self, event):
        palette = PyQt5.QtGui.QPalette()
        img = PyQt5.QtGui.QImage(image)
        scaled = img.scaled(self.size(), PyQt5.QtCore.Qt.KeepAspectRatioByExpanding,
                            transformMode=PyQt5.QtCore.Qt.SmoothTransformation)
        palette.setBrush(PyQt5.QtGui.QPalette.Window, PyQt5.QtGui.QBrush(scaled))
        self.setPalette(palette)

    def append_log(self, text, severity):

        if severity == OutputLogger.Severity.ERROR:
            self.text_edit.append(f"{text}")
        else:
            self.text_edit.append(text)

    def browse_folder(self):
        global directory, encrypt_data
        self.listWidget.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder")
        print(directory)
        global bookfile, cleanfile
        bookfile = directory + "\\data.data"
        cleanfile = directory
        encrypt_data = directory + "\\encrypt.data"

        if directory:
            for file_name in os.listdir(directory):
                self.listWidget.addItem(file_name)

    def buttonClicked(self):
        try:
            global text
            text, data = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                        "Input Data:")

            if data:
                f = open(bookfile, "wb")
                pickle.dump(text, f)
                f.close()
                print("\n[+] Data write")
        except NameError or PermissionError:
            print("[-]Error: You didn't select a folder")

    def buttonClicked1(self):

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

                print("[+]Keys generated!")
            except:
                print("[-] Keys not generated")

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
                if os.path.getsize(dir_secKey) and os.path.getsize(dir_pubKey):
                    print("[*]Keys are here")
                    text, g = QtWidgets.QInputDialog.getText(self, "Input Dialog",
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
            print("[+]Keys deleted!")
        except FileNotFoundError:
            print("[-]Error: No keys")

    def buttonClicked3(self):
        try:
            Crypt.walk(directory)
        except FileNotFoundError:
            try:
                if os.path.getsize(dir_secKey) and os.path.getsize(dir_pubKey):
                    print("[-]Error: You didn't select a folder")
            except FileNotFoundError:
                print("[-]Error: Generate keys first")

    def buttonClicked4(self):
        try:
            Decrypt.walk(directory)

        except FileNotFoundError:
            try:
                if os.path.getsize(dir_secKey) and os.path.getsize(dir_pubKey):
                    print("[-]Error: You didn't select a folder /\n"
                          "File without extension")
            except FileNotFoundError:
                print("[-]Error: Generate keys first")

        except ValueError:
            print("[-]Error: File decrypted or corrupt")

    def buttonClicked5(self):

        sys.exit(1)

    def buttonClicked6(self):
        text, data = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                    "Input Data (only English):")

        if data:
            twofish_encryption.test = text

        text, password = QtWidgets.QInputDialog.getText(self, "Input Password",
                                                        "256 bit password will be generated if you enter nothing")
        if password:
            if text == "":
                chars = \
                    "+-/]\*;:|!&$(#?={~@`<>" \
                    "_)}[abcdefghijklnopqrs" \
                    "tuvwxyzABCDEFGHIJKLMNO" \
                    "PQRSTUVWXYZ1234567890"
                password = ""
                for i in range(32):
                    password += random.choice(chars)
                twofish_encryption.key = password
            else:
                twofish_encryption.key = text

        twofish_encryption.start()
        twofish_encryption.encrypt()
        try:
            f = open(encrypt_data, "wb")
            pickle.dump(twofish_encryption.Cypher_text, f)
            f.close()
            print("\n[+]File with cypher text saved")
            print("[*]Password:", password)
        except NameError:
            print("[-]Error: You didn't select a folder")

    def buttonClicked7(self):

        try:
            text, password = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                            "Input Password:")

            if password:
                twofish_encryption.key = text

                f = open(encrypt_data, "rb")
                stored = pickle.load(f)
                f.close()
                twofish_encryption.test = stored
                twofish_encryption.start()
                twofish_encryption.decrypt()
                print("[+]Data:", twofish_encryption.plain_text)

        except FileNotFoundError or NameError:
            print("[-]Error: No file to decrypt data!")

    def buttonClicked8(self, status=1):
        try:
            r = requests.get(
                "https://raw.githubusercontent.com/retro-desert/Encryptor/master/version_server.txt"
            )
            server_version = r.text

            if server_version <= __version__:
                if status == 1:
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
            if status == 1:
                PyQt5.QtWidgets.QMessageBox.question(self, "Message", "Internet is disabled!",
                                                     PyQt5.QtWidgets.QMessageBox.Ok)


def erase(size, dir1=src_dir):
    for i in range(1, 36):
        size = random.randint(100, 10000)
        random_filename = tempfile.mktemp(dir=dir1)
        c1 = open(random_filename, "wb")
        c1.write(os.urandom(size))
        c1.close()
        os.remove(random_filename)


def delete_keys():
    clean1 = os.path.getsize(dir_secKey)
    clean2 = os.path.getsize(dir_pubKey)
    os.remove(dir_secKey)
    erase(+clean1)
    os.remove(dir_pubKey)
    erase(+clean2)


class Crypt:

    def crypt1(file):

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
        private_key = RSA.import_key(open(dir_secKey).read())

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
