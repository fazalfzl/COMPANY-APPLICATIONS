import os
import shutil
import sys
import zipfile
from os.path import join
from subprocess import check_output
from time import sleep
import winsound
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet

startPath = os.getcwd()

path_to_project = r"C:\LAZAFRON\POS"


def onerror(func, path, exc_info):
    """
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def setupEmptyTempDir():
    os.chdir(startPath)
    if not os.path.exists("temp"):
        os.mkdir("temp")
    else:
        shutil.rmtree("temp\\", onerror=onerror)
        os.mkdir("temp")
    os.chdir("temp\\")
    print(os.getcwd())


def copyProjectToTempDir():
    for file in os.listdir(path_to_project):
        if os.path.isfile(os.path.join(path_to_project, file)):
            shutil.copy(os.path.join(path_to_project, file), os.getcwd())
        else:
            shutil.copytree(os.path.join(path_to_project, file), os.path.join(os.getcwd(), file))


def copy_non_pythonic_to_dist():
    unwanted_dirs = ["dist", "packages", ".idea", "temp", "__pycache__", "tempIMAGEdir", "logs", ".git"]
    for file in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(path_to_project, file)):
            if file.endswith(".py"):
                pass
            else:
                shutil.copy(os.path.join(os.getcwd(), file), os.path.join(os.getcwd(), "dist"))
        else:
            if not file in unwanted_dirs:
                shutil.copytree(os.path.join(os.getcwd(), file), os.path.join(os.getcwd(), "dist", file))


def obfuscateProject():
    print(check_output(["pyarmor", "obfuscate", "--no-runtime", "--recursive", "--no-cross-protection", "main.py"]))


def goToDistDir():
    os.chdir("dist\\")
    print(os.getcwd())
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    print(dirs)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print(files)
    return dirs, files


# create qMainwindow class with window size = 800x600
class qMainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("QMainWindow")
        # add Lineedit widget to get input for path
        self.lineedit = QLineEdit(self)
        self.lineedit.move(20, 20)
        self.lineedit.resize(400, 30)
        self.lineedit.setText(path_to_project)
        # add button to start obfuscation
        self.button_load_project = QPushButton(self)
        self.button_load_project.setText("Load Project")
        self.button_load_project.move(300, 60)

        # create qlistwidget to show files
        self.listWidget_files = QListWidget(self)
        self.listWidget_files.move(20, 100)
        self.listWidget_files.resize(200, 400)
        # create qlistwidget to show directories
        self.listWidget_dirs = QListWidget(self)
        self.listWidget_dirs.move(240, 100)
        self.listWidget_dirs.resize(200, 400)
        # create pushbuttons to remove files and directories
        self.button_remove_file = QPushButton(self)
        self.button_remove_file.setText("Remove File")
        self.button_remove_file.move(20, 520)
        self.button_remove_dir = QPushButton(self)
        self.button_remove_dir.setText("Remove Dir")
        self.button_remove_dir.move(240, 520)

        # label for version number
        self.label_version = QLabel(self)
        self.label_version.setText("Version: ")
        self.label_version.move(20, 60)

        # create lineedit for version number
        self.lineedit_version = QLineEdit(self)
        self.lineedit_version.move(80, 60)
        self.lineedit_version.resize(200, 30)
        self.lineedit_version.setText("1")

        # button to upload to firebase storage
        self.button_upload = QPushButton(self)
        self.button_upload.setText("Upload")
        self.button_upload.move(460, 520)

        # button ONLY PYTHON abow button_upload
        self.button_only_python = QPushButton(self)
        self.button_only_python.setText("Only Python")
        self.button_only_python.move(460, 480)

        # button only UI abow button_only_python
        self.button_only_ui = QPushButton(self)
        self.button_only_ui.setText("Only UI")
        self.button_only_ui.move(460, 440)

        # butto only resources abow button_only_ui
        self.button_only_resources = QPushButton(self)
        self.button_only_resources.setText("Only Resources")
        self.button_only_resources.move(460, 400)

        # button to add one to version number and call load_project
        self.button_add_version = QPushButton(self)
        self.button_add_version.setText("Version + & Load")
        self.button_add_version.move(400, 60)

        # button to add one to version number and call load_project then only python then upload
        self.button_add_version_only_python_upload = QPushButton(self)
        self.button_add_version_only_python_upload.setText("Version + && Load && Only Python && Upload")
        self.button_add_version_only_python_upload.move(500, 60)
        self.button_add_version_only_python_upload.resize(250, 30)

        self.button_remove_file.clicked.connect(self.remove_file)
        self.button_remove_dir.clicked.connect(self.remove_dir)
        self.button_load_project.clicked.connect(self.load_project)
        self.button_upload.clicked.connect(self.upload)
        self.button_only_python.clicked.connect(self.only_python)
        self.button_only_ui.clicked.connect(self.only_ui)
        self.button_only_resources.clicked.connect(self.only_resources)
        self.button_add_version.clicked.connect(self.add_version)
        self.button_add_version_only_python_upload.clicked.connect(self.add_version_only_python_upload)
        self.button_upload.setEnabled(False)
        self.button_remove_file.setEnabled(False)
        self.button_remove_dir.setEnabled(False)

    def add_version(self):
        self.lineedit_version.setText(str(int(self.lineedit_version.text()) + 1))
        self.load_project()

    def load_project(self):
        global path_to_project
        path_to_project = self.lineedit.text()
        # if version number is 1 show a notification to enter version number before obfuscation
        if self.lineedit_version.text() == "1":
            self.label_version.setText("Please enter version number")
            return
        setupEmptyTempDir()
        copyProjectToTempDir()

        def prepend_line(file_name, line):
            """ Insert given string as a new line at the beginning of a file """
            # define name of temporary dummy file
            dummy_file = file_name + '.bak'
            # open original file in read mode and dummy file in write mode
            with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
                # Write given line to the dummy file
                write_obj.write("version = " + line + '\n')
                # Read lines from original file one by one and append them to the dummy file
                for line in read_obj:
                    if not "version = " in line:
                        write_obj.write(line)
            # remove original file
            os.remove(file_name)
            # Rename dummy file as the original file
            os.rename(dummy_file, file_name)

        # get all python files in current directory as a list
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.py')]
        for f in files:
            if ".py" in f:
                prepend_line(join(os.getcwd(), f), self.lineedit_version.text())

        # create a directory dist and copy all contecnts of current directory to it

        obfuscateProject()
        copy_non_pythonic_to_dist()
        dirs, files = goToDistDir()
        self.listWidget_dirs.clear()
        self.listWidget_files.clear()
        # if files are .py files else add to first position in listwidget
        for f in files:
            if ".py" in f:
                self.listWidget_files.addItem(f)
            else:
                self.listWidget_files.insertItem(0, f)
        for dir in dirs:
            if "_pkg" in dir:
                self.listWidget_dirs.addItem(dir)
            else:
                self.listWidget_dirs.insertItem(0, dir)

        self.projectLoaded = True
        # print current working directory (cwd)
        print("WORKING DIR AT THE END OF LOAD PROJECT")
        print(os.getcwd())
        self.button_upload.setEnabled(True)
        self.button_upload.setText("Upload")
        self.button_remove_file.setEnabled(True)
        self.button_remove_dir.setEnabled(True)

    def remove_file(self):
        if self.listWidget_files.currentItem() is not None:
            os.remove(os.path.join(os.getcwd(), self.listWidget_files.currentItem().text()))
            self.listWidget_files.takeItem(self.listWidget_files.currentRow())

    def remove_dir(self):
        if self.listWidget_dirs.currentItem() is not None:
            shutil.rmtree(os.path.join(os.getcwd(), self.listWidget_dirs.currentItem().text()))
            self.listWidget_dirs.takeItem(self.listWidget_dirs.currentRow())

    def only_python(self):
        if self.projectLoaded:
            # for each file in listwidget_files , if not .py file remove it using os.remove
            for i in range(self.listWidget_files.count()):
                itemText = self.listWidget_files.item(i).text()
                if not ".py" in itemText[-3:]:
                    os.remove(os.path.join(os.getcwd(), itemText))
                    self.listWidget_files.takeItem(i)
                    self.only_python()
                    return

            # for each folder in listwidget_dirs , if not packages remove it using shutil.rmtree
            for i in range(self.listWidget_dirs.count()):
                if not "packages" in self.listWidget_dirs.item(i).text():
                    shutil.rmtree(os.path.join(os.getcwd(), self.listWidget_dirs.item(i).text()))
                    self.listWidget_dirs.takeItem(i)
                    self.only_python()
                    return

    def only_ui(self):
        if self.projectLoaded:
            for i in range(self.listWidget_files.count()):
                itemText = self.listWidget_files.item(i).text()
                if not ".py" in itemText[-3:]:
                    os.remove(os.path.join(os.getcwd(), itemText))
                    self.listWidget_files.takeItem(i)
                    self.only_ui()
                    return
            for i in range(self.listWidget_dirs.count()):
                if not "ui" in self.listWidget_dirs.item(i).text():
                    shutil.rmtree(os.path.join(os.getcwd(), self.listWidget_dirs.item(i).text()))
                    self.listWidget_dirs.takeItem(i)
                    self.only_ui()
                    return

    def only_resources(self):
        if self.projectLoaded:
            for i in range(self.listWidget_files.count()):
                itemText = self.listWidget_files.item(i).text()
                if not ".py" in itemText[-3:]:
                    os.remove(os.path.join(os.getcwd(), itemText))
                    self.listWidget_files.takeItem(i)
                    self.only_resources()
                    return
            for i in range(self.listWidget_dirs.count()):
                if not "resources" in self.listWidget_dirs.item(i).text():
                    shutil.rmtree(os.path.join(os.getcwd(), self.listWidget_dirs.item(i).text()))
                    self.listWidget_dirs.takeItem(i)
                    self.only_resources()
                    return

    def zipselected(self):
        # create version directory
        os.mkdir(os.path.join(os.getcwd(), self.lineedit_version.text()))
        os.mkdir(os.path.join(os.path.join(os.getcwd(), self.lineedit_version.text()), self.lineedit_version.text()))
        # copy files to version directory listed in listwidget
        for i in range(self.listWidget_files.count()):
            shutil.copy(os.path.join(
                os.getcwd(), self.listWidget_files.item(i).text()),
                os.path.join(os.getcwd(), self.lineedit_version.text(), self.lineedit_version.text()))
        # copy directories to version directory listed in listwidget
        for i in range(self.listWidget_dirs.count()):
            shutil.copytree(os.path.join(
                os.getcwd(), self.listWidget_dirs.item(i).text()),
                os.path.join(os.getcwd(), self.lineedit_version.text(), self.lineedit_version.text(),
                             self.listWidget_dirs.item(i).text()))
        # zip version directory
        shutil.make_archive(os.path.join(os.getcwd(), self.lineedit_version.text()), 'zip'
                            , os.path.join(os.getcwd(), self.lineedit_version.text()))

    def upload(self):
        if self.projectLoaded:

            self.zipselected()
            if True:
                self.button_remove_file.setEnabled(False)
                self.button_remove_dir.setEnabled(False)

                blob = bucket.blob("upgrades/" + self.lineedit_version.text() + '.zip')
                self.button_upload.setText("Uploading...")
                blob.upload_from_filename(self.lineedit_version.text() + '.zip', timeout=6000)

                self.button_upload.setEnabled(False)

                frequency = 2500  # Set Frequency To 2500 Hertz
                duration = 1500  # Set Duration To 1000 ms == 1 second
                winsound.Beep(frequency, duration)

    def add_version_only_python_upload(self):
        self.add_version()
        self.only_python()
        self.upload()


# configservice =  {
#                             "type": "service_account",
#                             "project_id": "lazafron-bill-ai",
#                             "private_key_id": "5e31d3d093584d77c55372ec0c48ec2fd64deebb",
#                             "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC038uMbWEJVtpo\n7E8yv+LQNOUsfqRFRu4RGGuqhQTSiCaie712eMrl3R3V6zFQSjDqJw6zxsULBVJJ\nLpfTqnQQy99M8Or7s61ykUtpVFMqMyaD4YHE2Sozie02mCYTZtwZ+nc9aVhkjTmp\nrvLcZcpBCEMG3Rdr2bNFNDo2IIidBO+A2fStjBCF8kCN/nM/5XEDBuE1nPurBDpy\nlom9VAz3R6HHfptXSM51M1wr5UDMCTnC2wqOZU4HM6lS+eZtcG1xYND4dhzaSIr4\n8MIl63Ykau3njJM0kqU4CBmCS9WfWis+xPPbYRTeuish/427SBujdo/0nIwRK+C4\nTzSZrPWRAgMBAAECggEAAuaP4hmi875j1Ejt4Dd5kLM4daU2RzIjAT0uBNcLQ8ER\nNYvcdvjq8BLCtrqF2O7HqAmmT7XBVTLppejMYIWcROSwGRDIA+9Wub6gwfirOMMH\nPBgyt5Bv/9GXb0ezXJ5Kq1P7840r8LjfEtyOYoBzZOWYBZUoGf+sw1BaGqIc7r+t\nnIk12TWZl22D5ZgvrJbQ9ZLJbrKAskNnq3wB0qsu192U42o6zYDWVZCDHLnTzF2h\nKJnKoc/9CKopd9cVg4ty8dvaI1lEAy0UHBVUbjIF6E6QoW/Cv3iGZl09Va70+aoo\nEEv5mBFFQNRv7WpgAGgufBIsl0I3JRgMuMg5/F+BUQKBgQDaedYkuoCbLLH10/IQ\nVmNCfAHwd81zehWVvSQ8HlrU9Yid42tzfxLk/jJFYftz9XU9vA3+707z0L6HV/YM\nsorX4esLmzvl9RtgQdvkbm4m8kCyJZnJyOQv+SNRcMQpiIOVtErvgDM36qraM62e\nNuZZqlKigfffkp1+Qa0x19LyTQKBgQDT8KYvVF3WCssNUYiLpPGbT8n+Q4zwf9Of\nYIRAylQxLMGCy7A1yyUlCyMGaTpL8EsG7nSR7dr0+A3S0TqRuLaytvgV8H5UBFUL\nQRU6ZFGvFct/OmyH14UU0OJrSMBD7iDxBAMtgqv1SWMqe0cd2ZbiTrga5DKUyr+h\n1aQEEpmKVQKBgQCvbBCkIRROhI7IAkxlDdhZc9Tizm8q/6YBO4OyufTY9eWiUQ7g\nB/KV5/1ZdJlAvKBM14itYF2Wq8+wQNKR03JkcUQXZ6eqtyoqGfeD7Z+Iqg+Ee2iG\ne0Wtt2/CXrdDWhe9xqw8rkVx6n0RA1mupgpDiN0dGxp6a/EFhZqZYOBCKQKBgF9g\nnBkOmY/6mXhr6cwWNZiUZq2jTqjojZ7au4nAw/TBVHB9I9aBjjzGb0OyVUbZY5pB\n83m8ld3KR8ZI3Fe5zZZNmwWcje1XacI/zsLRZKUrZMHj0/Wp+rzsaAip28R2RKLS\nEHAJr0MafKMgiVeYlTtQ+682ZMDrISQ+VapziF9lAoGAYXxwhde0ENnnHGadrBST\nNZ4VQY3xFxu4nXcU29ErWNJ14AuvQTJabqVRGhevtjP/ZgZoR4NwHRSjtSqM85u7\n2h1FF95wqphzYLkzzultlzofZuuiTPE5ttTIhsZQNe2Ct5gLypxamVzbsJsVhJKO\n/CeRbeMpejfWm50euzKnB2Q=\n-----END PRIVATE KEY-----\n",
#                             "client_email": "firebase-adminsdk-43t30@lazafron-bill-ai.iam.gserviceaccount.com",
#                             "client_id": "118248069704198016902",
#                             "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                             "token_uri": "https://oauth2.googleapis.com/token",
#                             "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#                             "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-43t30%40lazafron-bill-ai.iam.gserviceaccount.com"
#                         }

creds = {"type": "service_account",
         "project_id": "lazafron-cloud",
         "private_key_id": "8f6426919049bff88140994aaf998ce7890f8a6c",
         "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC7bx8sb0izF"
                        "+V3\nhSzx23GwQ7sBeTPX9r+U5e0lpPQp+aOSJUmVdDoMEouS8/XZBLVWVADKjQ/JJoCL\noUh5QJW1b"
                        "/60tTNBJa1Vjg7G4Ltj+0JUYuAy9KRjA2+pLeQ+CVX2KZJsKRa9GL28"
                        "\nvdBiDmb7UG9M2xYcMoQvn2jaE7NpSoO8oJiVPcKUpNNhpYumLn+1DJicYfmJhjWU\n"
                        "+LTindklH3eb1D0YJrY1n3vY2nswNBzmUQcQOwxhZunfOa5ovDXBwTfh0yQjhJRS\nPjf"
                        "+JS12uoK2FMcgy2yZYpffrLHJ8sHh0Y3YJ5gAELre7wZ6G41lqwBFFZD6E8Qo\nxIWZwy7jAgMBAAECggEAArCXDW"
                        "+xZuSOZfcyzGu+R23JZr2DCXPgjvX3v8UMvfd3\nqfbABhWLabXwa9T1b75aDdmZw05f7h6P1LElVZwgKeDoElbRW"
                        "/t679Hgk2kRN1+Z\nNZXPqtuI6mTXuuFON7exlJ1HHSc/zMnomydMMMQNJUkjt8IjIJd2/yn1+r8yoW2q"
                        "\niMkkOVsMaNVyLPkWw28EeDZzs04sR9jHDYrPJmLH/nMy8exenJt8Hut/pkXbQqPe\ngjR3rTlXpx7qRvl"
                        "/tt6GW9Cn4ZFnUCeJYzFlZq82g3d1lpeyBl9NLIv+RYjrHLz0\nbAO6FgoA1zsWka5+qA5+aTW"
                        "+/cxwSrGJJPdDbE1jGQKBgQDi/AGUmj7limnLqsjq\nUwSXCif19MAn0q2nvtzHVsktuDkY+cSCrsBUcz"
                        "+2Ml3QYnv1m12aRYIQJ7Zh6PzZ\nOg9A8rAR7hCIsQxi4j0ZkhIM4n5fZYr2sAPWs9MkZGG4j1hgw2siUWLXRndDpNfD"
                        "\nEzGkYuT9/9Yh9P/xiEkhgHdVuQKBgQDTZNfm2zXpL0ncuryVNLzI5ORjBu9fHU/N"
                        "\nlEZ5ZtSzzO6zQKp2O6UPlQViXHK5GEQFhTUObImoIH4z4if1Vlnf5LPeKvA7e34r"
                        "\nhdbETbGgmSROTrEdUUCQW6XSD9wmXuxERjx5eNy9H2uE5jy7+H9au7AK1R9KPMnU\nZU327jR3ewKBgQCw"
                        "/i7BUHFhDcgnPxoB1hBLMmksmdfIdbhhiCuh6KNg2jjzp7c6"
                        "\n68cfUurISIfsuQ7N2oNni3G65SyLNmELhgFk9Jikso0D+YKeDKn2KXeXwnkmLAjr\nCR9FKN2oj/m/L0"
                        "+LzHXawbmgAdt3zK9N9saL122WPgscWW3GSi40SHdFSQKBgQCf\nViV"
                        "+dsCd8OzlmUNH26Zobk7PbYzDzp42QIsWOrIcjF1nc1iJIc/6fMLALxqx9V5g"
                        "\nItWo95qSxVsa1F52CA5aOlJxJUBKNX0WZR1KfZ1jhcrd02agyHu307ybJyUzLt07\nYQ14KeeIDcTHOZuRu26S"
                        "/2Fj6Nxa4pLmqy0m8MlPPQKBgQDd5EtCxl7gwyEFslxY\nD1RCmv18in06eJwh/3ZL5psO3HS/8wEacd2sC2Wb9gT"
                        "/Pau8suYU6LLW5yMGEKos\nEXA28ibv9yK8rEcUnZtSoK8SxhH1A+b6rKz8kqDDZJI7XOgmky8jUfi3SL80wHzc"
                        "\nGfNgw+IjbA1CtkU+m3JBtjoe7w==\n-----END PRIVATE KEY-----\n",
         "client_email": "firebase-adminsdk-mw3pc@lazafron-cloud.iam.gserviceaccount.com",
         "client_id": "110323579871385072386",
         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
         "token_uri": "https://oauth2.googleapis.com/token",
         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
         "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-mw3pc"
                                 "%40lazafron-cloud.iam.gserviceaccount.com "
         }
# cred = credentials.Certificate(creds)

# upload file to firebase storage using firebase-admin

import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate(creds)
firebase_admin.initialize_app(cred, {'storageBucket': 'lazafron-cloud.appspot.com'})
bucket = storage.bucket()

app = QApplication(sys.argv)
# apply_stylesheet(app, theme='dark_purple.xml')
window = qMainwindow()
window.show()
sys.exit(app.exec_())
