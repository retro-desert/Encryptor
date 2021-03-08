__author__ = "Retro Desert " \
             "github.com/retro-desert"
__license__ = "(c) 2021 GNU General Public License v3.0"
__version__ = "1.990"
__maintainer__ = "Retro Desert"

###########################################
#         ENCRYPTOR v1.990-FINAL          #
###########################################

import logging
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
from PyQt5.QtCore import QObject, QRect

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
secKey = src_dir + "\\private.pem"
pubKey = src_dir + "\\receiver.pem"

global walk
global crypt1
global decrypt1


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class App(QtWidgets.QMainWindow, design.Ui_Encryptor):
    global error

    def __init__(self):

        super().__init__()

        self.setupUi(self)
        self.btnBrowseFiles.clicked.connect(lambda: self.browse(status=1))
        self.pushButton.clicked.connect(lambda: self.buttonClicked())
        self.pushButton_2.clicked.connect(lambda: self.buttonClicked2())
        self.pushButton_3.clicked.connect(lambda: self.buttonClicked3())
        self.pushButton_4.clicked.connect(lambda: self.buttonClicked4())
        self.pushButton_5.clicked.connect(lambda: self.buttonClicked5())
        self.pushButton_6.clicked.connect(lambda: self.buttonClicked6())
        self.pushButton_7.clicked.connect(lambda: self.buttonClicked7())
        self.pushButton_8.clicked.connect(lambda: self.buttonClicked8())
        self.pushButton_9.clicked.connect(lambda: self.buttonClicked9())
        self.btnBrowseFolder.clicked.connect(lambda: self.browse(status=0))
        self.setWindowIcon(PyQt5.QtGui.QIcon(icon))

        logTextBox = QTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter())
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.INFO)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(logTextBox.widget)
        layout.setGeometry(QRect(200, 250, 341, 151))
        self.setLayout(layout)

        print(f"ENCRYPTOR {__version__}")
        self.buttonClicked9(status=0)

    def resizeEvent(self, event):
        palette = PyQt5.QtGui.QPalette()
        img = PyQt5.QtGui.QImage(image)
        scaled = img.scaled(self.size(), PyQt5.QtCore.Qt.KeepAspectRatioByExpanding,
                            transformMode=PyQt5.QtCore.Qt.SmoothTransformation)
        palette.setBrush(PyQt5.QtGui.QPalette.Window, PyQt5.QtGui.QBrush(scaled))
        self.setPalette(palette)

    def browse(self, status):
        global directory, files, encrypt_data, bookfile, cleanfile
        self.listWidget.clear()
        if status == 0:
            directory = QtWidgets.QFileDialog.getExistingDirectory()
            if directory != "":
                self.listWidget.addItem("Directory: ")
                self.listWidget.addItem(directory)
            else:
                directory = ""

        else:
            files = QtWidgets.QFileDialog.getOpenFileNames()
            try:
                if os.path.dirname(files[0][0]) != os.path.dirname(files[0][-1]):  # Potential vuln
                    print("[-]Error: Names of the directories does not equal")
            except IndexError:
                self.listWidget.clear()
                directory = ""
            else:
                directory = os.path.dirname(files[0][0])
                self.listWidget.addItem("Directory: ")
                self.listWidget.addItem(directory)
                self.listWidget.addItem("Files: ")
                for file_name in files[0]:
                    self.listWidget.addItem(file_name[len(directory) + 1:])

        bookfile = directory + "\\data.data"
        cleanfile = directory
        encrypt_data = directory + "\\encrypt.data"

    def buttonClicked(self):
        if not os.path.isdir(directory):
            print("[-]Error: You didn't select a folder")
        else:
            global text
            text, data = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                        "Input Data:")

            if data:
                f = open(bookfile, "wb")
                pickle.dump(text, f)
                f.close()
                print("[+]Data write")

    def buttonClicked2(self):

        def writer():
            print("[*]It may take a long time.\n"
                  "Generating 4096 bit key...")

        def generate_keys():
            key = RSA.generate(4096)
            private_key = key.export_key()
            file_out = open("private.pem", "wb")
            file_out.write(private_key)
            file_out.close()

            public_key = key.publickey().export_key()
            file_out = open("receiver.pem", "wb")
            file_out.write(public_key)
            file_out.close()

            print("[+]Keys generated!")

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

        if os.path.isfile(secKey) or os.path.isfile(pubKey):
            text, g = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                     "Do you want to make new keys? Y/N:")
            if text == "Y":
                generate2()

        else:
            generate2()

    def buttonClicked3(self):
        if os.path.isfile(secKey) or os.path.isfile(pubKey):
            text, g = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                     "Do you want to delete keys? Y/N:")
            if text == "Y":
                delete_keys()
                print("[+]Keys deleted!")
        else:
            print("[-]Error: No keys")

    def buttonClicked4(self):
        try:
            if os.path.isfile(secKey) and os.path.isfile(pubKey):
                Crypt.walk(files[0])
                for fle in files[0]:
                    files[0][files[0].index(fle)] = fle + ".bin"
            else:
                print("[-]Error: Generate keys first")

        except (NameError, IndexError):
            if os.path.isfile(secKey) and os.path.isfile(pubKey):
                if directory != "":
                    Crypt.walk(directory)
                else:
                    print("[-]Error: You didn't select a folder")
            else:
                print("[-]Error: Generate keys first")

    def buttonClicked5(self):
        try:
            if os.path.isfile(secKey) and os.path.isfile(pubKey):
                Decrypt.walk(files[0])
                for fle in files[0]:
                    files[0][files[0].index(fle)] = fle[:-4]
            else:
                print("[-]Error: Generate keys first")

        except (NameError, IndexError):
            try:
                if os.path.isfile(secKey) and os.path.isfile(pubKey):
                    if directory != "":
                        Decrypt.walk(directory)
                    else:
                        print("[-]Error: You didn't select a folder*")  # Maybe file without extension
                else:
                    print("[-]Error: Generate keys first")

            except Exception:
                print("[-]Error: No files(.bin) to decrypt")

        except ValueError:
            print("[-]Error: File decrypted or corrupt")

        except Exception:
            print("[-]Error: No files(.bin) to decrypt")

    def buttonClicked6(self):
        sys.exit(1)

    def buttonClicked7(self):
        if not os.path.isdir(directory):
            print("[-]Error: You didn't select a folder")
        else:
            text, data = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                        "Input Data (only English):")

            if text != "":
                twofish_encryption.test = text

                text, password = QtWidgets.QInputDialog.getText(self, "Input Password",
                                                                "256 bit password will be generated if you enter nothing")
                if password:
                    if text == "":
                        chars = \
                            "+-/]\*;:|!&$(#?={~@`<>" \
                            "_)}[abcdefghijklmnopqr" \
                            "stuvwxyzABCDEFGHIJKLMN" \
                            "OPQRSTUVWXYZ1234567890"
                        password = ""
                        for i in range(32):
                            password += random.choice(chars)
                        twofish_encryption.key = password
                    else:
                        twofish_encryption.key = text

                twofish_encryption.start()
                twofish_encryption.encrypt()
                f = open(encrypt_data, "wb")
                pickle.dump(twofish_encryption.Cypher_text, f)
                f.close()
                print("[+]File with cypher text saved")
                print("[*]Password:", password)

    def buttonClicked8(self):
        if not os.path.isdir(directory):
            print("[-]Error: You didn't select a folder")
        else:
            try:
                f = open(encrypt_data, "rb")
                text, password = QtWidgets.QInputDialog.getText(self, "Input Dialog",
                                                                "Input Password:")

                if text != "":
                    twofish_encryption.key = text

                    stored = pickle.load(f)
                    f.close()
                    twofish_encryption.test = stored
                    twofish_encryption.start()
                    twofish_encryption.decrypt()
                    print("[+]Data:", twofish_encryption.plain_text)

            except FileNotFoundError:
                print("[-]Error: No file to decrypt data!")

    def buttonClicked9(self, status=1):
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
    if os.path.isfile(secKey):
        clean1 = os.path.getsize(secKey)
        os.remove(secKey)
        erase(+clean1)
    if os.path.isfile(pubKey):
        clean2 = os.path.getsize(pubKey)
        os.remove(pubKey)
        erase(+clean2)


class Crypt:

    def crypt1(file):

        f = open(file, "rb")
        data = f.read()
        f.close()

        file_out = open(str(file) + ".bin", "wb")

        recipient_key = RSA.import_key(open(pubKey).read())
        session_key = get_random_bytes(16)

        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)

        [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
        file_out.close()
        print("[+]" + file[len(directory) + 1:] + " ENCRYPT!")
        folder_size = os.path.getsize(file)
        os.remove(file)

        dir2 = cleanfile
        erase(+folder_size, dir2)

    def walk(dir):
        if not os.path.isfile(dir[0]) and os.path.isdir(dir):
            if not os.listdir(dir):
                print("[-]Error: File not found")
            for name in os.listdir(dir):
                path = os.path.join(dir, name)
                Crypt.crypt1(path)
        else:
            for name in dir:
                path = os.path.join(directory, name)
                if os.path.isfile(path):
                    Crypt.crypt1(path)
                else:
                    try:
                        Crypt.crypt1(path + ".bin")
                        break
                    except FileNotFoundError:
                        pass

                    try:
                        Crypt.crypt1(path[:-4])
                        break
                    except FileNotFoundError:
                        print("[-]Error: File not found")


class Decrypt:

    def decrypt1(file):
        if not str(file[-4:]) == ".bin":
            raise Exception
        else:
            file_in = open(file, "rb")
            file_out = open(str(file[:-4]), "wb")
            private_key = RSA.import_key(open(secKey).read())

            enc_session_key, nonce, tag, ciphertext = \
                [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            file_out.write(data)
            print("[+]" + file[len(directory) + 1:] + " DECRYPT!")
            file_in.close()
            file_out.close()
            os.remove(file)

    def walk(dir):
        if dir is False:
            raise FileNotFoundError
        if not os.path.isfile(dir[0]) and os.path.isdir(dir):
            if not os.listdir(dir):
                print("[-]Error: File not found")
            for name in os.listdir(dir):
                path = os.path.join(dir, name)
                Decrypt.decrypt1(path)
        else:
            for name in dir:
                path = os.path.join(directory, name)
                if os.path.isfile(path):
                    Decrypt.decrypt1(path)
                else:
                    try:
                        Decrypt.decrypt1(path + ".bin")
                        break
                    except FileNotFoundError:
                        pass

                    try:
                        Decrypt.decrypt1(path[:-4])
                        break
                    except FileNotFoundError:
                        print("[-]Error: File not found")


def print(*text_log):
    for i in text_log:
        logging.info(f"{text_log[text_log.index(i)]}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("QLabel {color: white}"
                      "QMainWindow { border-image: url(image)}"
                      "QTextEdit {background-color: black; color: white; font-weight: bold}"
                      "QListWidget {background-color: black; color: white; font-weight: bold}"
                      "QInputDialog {background-color: black; color: white; font-weight: bold}"
                      "QMessageBox {background-color: black; color: white; font-weight: bold}"
                      "QPlainTextEdit {background-color: black; color: white; font-weight: bold}")
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
