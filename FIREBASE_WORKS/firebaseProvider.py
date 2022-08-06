import pyrebase

firebaseConfig = {"apiKey": "AIzaSyDd9fMOiyfIPpSh_JIVMKo_QT8bgLEKB8s",
                  "authDomain": "lazafron-cloud.firebaseapp.com",
                  "databaseURL": "https://lazafron-cloud-default-rtdb.firebaseio.com",
                  "projectId": "lazafron-cloud",
                  "storageBucket": "lazafron-cloud.appspot.com",
                  "messagingSenderId": "736408897397",
                  "appId": "1:736408897397:web:f49201e1749440bd19753c",
                  "measurementId": "G-0BPMBC11LQ"}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def readData(path):
    data = db.child(path).get()
    return data

def writeData(path, data):
    db.child(path).set(data)
    return