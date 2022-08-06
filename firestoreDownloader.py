import os

from PyQt5 import QtWidgets, QtCore
from pyrebase import pyrebase


class FirestoreDownloader(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.firebaseinitialized = False
        self.setWindowTitle('Firestore Downloader')
        self.setGeometry(100, 100, 700, 500)
        # show a multiline input field
        self.input_field = QtWidgets.QTextEdit(self)
        self.input_field.move(20, 20)
        self.input_field.resize(400, 400)
        sample_config = str({
                         "apiKey": "AIzaSyBNc0hXikUAATpHiCzDgicxqcB8hKENcB8",
                         "authDomain": "lazafron-35184.firebaseapp.com",
                         "databaseURL": "https://lazafron-35184.firebaseio.com",
                         "storageBucket": "lazafron-35184.appspot.com",
                         "serviceAccount": {
                             "type": "service_account",
                             "project_id": "lazafron-35184",
                             "private_key_id": "dab9edeb5c237ffd9ea6655eeea340852ebf9797",
                             "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC+YnLCarjGdgFA\ngrY9TWW+RFV9MAQ032+SZmNDSUdyKXnnMAy4c49edd3jAxQb/QQkLKTgN05bIh1A\nsWUcshUAKPViKpZwmfvR2A82Ru8zdb6caSTp1xW57cXLRIhhNdJLcJAMg7UcfTGd\nsHZIJewv8ygWiIp7dkAt44OQGWJm8ejCtiTmfLtguiYOlPVigXC4HLQqNKt1hIWY\n0AGWnEmcCVb7wbB9dFaoM9Qo5fsXgLIW4IOpy0LBVxRszkV1bak1v1JuD0BnMp/X\nWQpBPwBGDE2XeZXUI7b2Cm7pubfk/yYwVOpelrfXybOquth2JzyteeUAh4ssawct\nda2Ti4ifAgMBAAECggEASeom69xLSKHf8o/M+RfnfGtDVYsi1vQ4ePpPZ3w3xNbd\ngShih+o1q1LPhqdXU1Z0GSdMC9DtFuyztr4op29sP9enDSnDpovh/KKJpWT80VnR\nWyBnOHJM+RabSEOfPz6KGsfk5TbtRdZFQReVlIVEoYkh8z2npi9O04IVPgjc72Io\nbjb1vVfidYn8OHy9FzgxbzzkYe5tkwoFT6uQusWIIZ/lXRaRW9UQOKC6ZVfvaWH3\nPntZSMveBdZTePYkDdFXLwevjrBUJ39om832k2xp1LS9jvGWbsR1HhgOzNO5aHxx\n3fjboiA0LsHlt+rm3adJnHw7lWTML+DgqQZtlqYTYQKBgQDpiB7sZ3OPMc2OxELl\nOf75q9sdtvw8UdJnkKi74lczDh0a1BkQ8qeFte45HrIpkikCwME+Sq6/0qwbQ/EK\nJepfHkwbocB548e/wb7u2SGpkoob+XSVi1y+/+GwLB5ajtzOQVedE0vJ85Lk/8V5\nHIm9z7Dh3ShVe4toPkAccTe4nQKBgQDQs51CCAOpNgC8c7kn0qdStk8ndy0roiaA\nxtOZMIZBlcU1D9WNcqs1/DPyogY2he6twykiJ82FnJBl8x7ciJELEFaIjXIfVhsR\nZImK1PKqhVJHeT51HNcwR3ukK33DCLlR6aZQ2I4dl6/cNlJPm8wGxt36teaoyRcn\nYwtSyIsrawKBgFk9nzOPxOUvjvHDphyasQkP10ffqTwTuGfDK/fAYror5oteCcYk\nNEgwYbyKMmMYa3uV1ULMn0LGauZwbCgInSuEFGlqwnbRyH9Ktn/nkamPSh+ukBKl\nkueaONBty5unhFF9PtHTkd62qafA5eGGOkzClUF6lfM0pu1K/Izh5v0xAoGAa6oN\nWXAq+1MZpB6LCUk5+oiEYxavHdBjzpFDvcZzrEfoWYxWncbnHk2COwxs6hnD3K5O\nfQlNlD0FnSKD7D8jnDKMgZt+oT3ZbuqPrihXG7L1lFuu5dnABW8LENFC6qeIewJv\nQ0vEXO3Q0mjPo7P62BAlmd3XJYG/yRjmUYmVigsCgYAIQWY1qGXxLE4fcean0zou\ncrZutRQBJyGvo3eTk6eAtmD2nJObvrN39pW+xpBkmQG+7GFSCp+irt4hlTi7JzmU\n84DaSXeBeAXmlpeVMnss1GbJSUDCDbu8sNMJxVXBugGvud4tIynpY4bpqGFHz36x\nHdwO0a009vg3banbYOAJrg==\n-----END PRIVATE KEY-----\n",
                             "client_email": "firebase-adminsdk-l5ex2@lazafron-35184.iam.gserviceaccount.com",
                             "client_id": "103507091449224493936",
                             "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                             "token_uri": "https://oauth2.googleapis.com/token",
                             "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                             "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-l5ex2%40lazafron-35184.iam.gserviceaccount.com"
                         }
                         })
        self.input_field.setText(sample_config)
        self.input_field.setPlaceholderText('Enter firebase config')

        # button to initialize firebase
        self.init_button = QtWidgets.QPushButton('Initialize', self)
        self.init_button.setGeometry(QtCore.QRect(20, 420, 80, 30))
        self.init_button.clicked.connect(self.init_firebase)

        #add a status at the bottom of the window
        self.status = QtWidgets.QLabel(self)
        self.status.setGeometry(QtCore.QRect(20, 460, 400, 30))
        self.status.setText('Status:')

        # show input field to enter dir path to download files from firestore
        self.dir_path = QtWidgets.QLineEdit(self)
        self.dir_path.setGeometry(QtCore.QRect(20, 480, 400, 30))
        self.dir_path.setPlaceholderText('Enter dir path to download files')

        # button to download files from firestore
        self.download_button = QtWidgets.QPushButton('Download', self)
        self.download_button.setGeometry(QtCore.QRect(20, 520, 80, 30))
        self.download_button.clicked.connect(self.download_files)


        #
        self.show()

    def download_files(self):
        # get dir path from dir_path QLineEdit
        dir_path = self.dir_path.text()
        # check if firebase is initialized
        if self.firebaseinitialized:
            # get firestore database
            downloadfiles(self.servicestorage, dir_path)
        else:
            # set status to 'Firebase not initialized'
            self.status.setText('Firebase not initialized')


    def init_firebase(self):
        # get firebase config from input_field QTextEdit
        config = self.input_field.toPlainText()
        # convert config to dict
        config = eval(config)
        # initialize firebase
        firebase = pyrebase.initialize_app(config)
        # get firestore database
        self.servicestorage = firebase.storage()
        # show a label indicating that firebase is initialized
        print('Firebase initialized')
        self.firebaseinitialized=True
        # set status to 'Firebase initialized'
        self.status.setText('Firebase initialized')

        print(self.servicestorage)

def downloadfiles(servicestorage, dir_path):
    # download files from firestore to dir_path
    files=servicestorage.bucket.list_blobs(prefix=dir_path)
    for file in files:
        # if file is not a directory , download it
        if not file.name.endswith('/'):
            print(file.name)
            #create empty file in downloads folder in current directory
            file_path = os.path.join(os.getcwd() ,'downloads',file.name)
            # create file in downloads folder in current directory if it doesn't exist
            if not os.path.exists(os.path.dirname(file_path)):
                try:
                    os.makedirs(os.path.dirname(file_path))
                except OSError as exc: # Guard against
                    print(exc)
            # download file to downloads folder in current directory

            file.download_to_filename(file_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    fsd = FirestoreDownloader()
    app.exec_()
