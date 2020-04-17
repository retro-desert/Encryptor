# Author github.com/retro-desert
# (c) 2019 GNU General Public License v3.0
# Mail nethertrooper@tuta.io
# PGP A1AF 5641

###########################################
#             ENCRYPTOR v1.5              |
#                                         |
# NEED MODULES:                           |
# pycryptodomex                           |
###########################################


print("\nENCRYPTOR v1.5")

import os, sys, time, pickle, random, tempfile

from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
from PyQt5 import QtWidgets
import design
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QObject


script_directory = os.path.abspath(os.curdir)
secretKey = "\\private.pem"
publicKey = "\\receiver.pem"
list = "\\data.data"
directory = "lol"
directory_secretKey = os.path.abspath(os.curdir) + secretKey
directory_publicKey = os.path.abspath(os.curdir) + publicKey
listfile = directory + list
cleanfile = directory

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

    def append_log(self, text, severity):
        text = repr(text)

        if severity == OutputLogger.Severity.ERROR:
            self.text_edit.append('<b>{}</b>'.format(text))
        else:
            self.text_edit.append(text)

    def buttonClicked(self):
        global text
        text,\
        s = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
                                                  'Input Data:')

        if s:
            f = open(listfile, "wb")
            pickle.dump(text, f)
            f.close()
            f = open(listfile, 'rb')
            storedlist = pickle.load(f)
            print(storedlist, end=" ")
            f.close()
            time.sleep(0.5)
            print("\n(system) Data write")

    def buttonClicked1(self):
            generate()

    def buttonClicked2(self):
            delete_keys()

    def buttonClicked3(self):
            Crypt.walk(directory)
            print("---------------------------------------------------------------")

    def buttonClicked4(self):
            Decrypt.walk(directory)
            print("---------------------------------------------------------------")

    def buttonClicked5(self):
            sys.exit(1)

    def browse_folder(self):
        self.listWidget.clear()
        global directory
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder")
        print(directory)


        if directory:
            for file_name in os.listdir(directory):
                self.listWidget.addItem(file_name)

    global walk
    global crypt1
    global decrypt1


def generate():
        print("It may take a long time.\n"
              "Generating 4096 key...")
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

class Decrypt():

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


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("QLabel {background-color: black; color: white}"
                      "QMainWindow { border-image: url(image.jpg)}"
                      "QTextEdit {background-color: black; color: white}"
                      "QListWidget {background-color: black; color: white}")
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()