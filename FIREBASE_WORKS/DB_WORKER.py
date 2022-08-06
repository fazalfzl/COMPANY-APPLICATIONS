import hashlib

from firebaseProvider import db, readData, writeData


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def createDealer(dealerID, password):
    # check if db/AUTH/DEALER/dealerID exists
    if readData("AUTH/DEALER/" + dealerID).val() is None:
        # if not, create it
        writeData("AUTH/DEALER/" + dealerID, {
            "DEALERID": dealerID,
            "Hpassword": hash_password(password)
        })
        print("DEALER " + dealerID + " created")
        return True
    else:
        print("DEALER " + dealerID + " already exists")
        return False


def createClient(dealerID, clientID, password):
    # check if db/AUTH/DEALER/dealerID/CLIENTS/clientID exists
    if readData("AUTH/CLIENT/" + clientID).val() is None:
        # if not, create it
        writeData("AUTH/CLIENT/" + clientID, {
            "CLIENTID": clientID,
            "Hpassword": hash_password(password)
        })
        writeData(f"/DEALERS/{dealerID}/CLIENTS/{clientID}", {
            "CLIENTID": clientID
        })
        print("CLIENT " + clientID + " created")
        return True
    else:
        print("CLIENT " + clientID + " already exists")
        return False


def createStore(dealerID, clientID, storeID, password):
    # check if db/AUTH/DEALER/dealerID/CLIENTS/clientID/STORES/storeID exists
    if readData("AUTH/STORE/" + storeID).val() is None:
        # if not, create it
        writeData("AUTH/STORE/" + storeID, {
            "STOREID": storeID,
            "Hpassword": hash_password(password)
        })
        writeData(f"/DEALERS/{dealerID}/CLIENTS/{clientID}/STORES/{storeID}", {
            "STOREID": storeID
        })

        print("STORE " + storeID + " created")
        return True
    else:
        print("STORE " + storeID + " already exists")
        return False


def insertUserDetails(userType, userID, address, phone, email, name):
    # userType can be DEALERS, CLIENTS, STORES
    # check if db/USERDETAILS/userType/userID exists
    if readData("USERDETAILS/" + userType + "/" + userID).val() is None:
        # if not, create it
        writeData("USERDETAILS/" + userType + "/" + userID, {
            "ADDRESS": address,
            "PHONE": phone,
            "EMAIL": email,
            "NAME": name
        })
        print("USERDETAILS for " + userType + " " + userID + " created")
        return True
    else:
        print("USERDETAILS for " + userType + " " + userID + " already exists")
        return False

# /STORES/STORE1/MACHINES/MACHINE1/MACHINEID

def insertMachine(storeID, machineID, machineType):
    # check if db/AUTH/DEALER/dealerID/CLIENTS/clientID/STORES/storeID/MACHINES/machineID exists
    if readData(f"/STORES/{storeID}/MACHINES/{machineID}").val() is None:
        # if not, create it
        writeData(f"/STORES/{storeID}/MACHINES/{machineID}", {
            "MACHINEID": machineID, # user defined machineID
            "MACHINETYPE": machineType # ATM model / desktop model
        })
        print("MACHINE " + machineID + " created")
        return True
    else:
        print("MACHINE " + machineID + " already exists")
        return False


def sampleDataInsert():
    createDealer(dealerID="DEALER1", password="test1")
    createClient(dealerID="DEALER1", clientID="CLIENT1", password="test1")
    createClient(dealerID="DEALER1", clientID="CLIENT2", password="test1")
    createStore(dealerID="DEALER1", clientID="CLIENT1", storeID="STORE1", password="test1")
    createStore(dealerID="DEALER1", clientID="CLIENT1", storeID="STORE2", password="test1")
    createStore(dealerID="DEALER1", clientID="CLIENT2", storeID="STORE3", password="test1")

    insertUserDetails(userType="DEALERS", userID="DEALER1", address="sample address", phone="sample phone",
                      email="sample email", name="sample name")
    insertUserDetails(userType="CLIENTS", userID="CLIENT1", address="sample address", phone="sample phone",
                      email="sample email", name="sample name")
    insertUserDetails(userType="CLIENTS", userID="CLIENT2", address="sample address", phone="sample phone",
                      email="sample email", name="sample name")
    insertUserDetails(userType="STORES", userID="STORE1", address="sample address", phone="sample phone",
                      email="sample email", name="sample name")
    insertUserDetails(userType="STORES", userID="STORE2", address="sample address", phone="sample phone",
                      email="sample email", name="sample name")
    insertUserDetails(userType="STORES", userID="STORE3", address="sample address", phone="sample phone",
                      email="sample email", name="sample name")
    insertMachine(storeID="STORE1", machineID="MACHINE1", machineType="ATM")
    insertMachine(storeID="STORE1", machineID="MACHINE2", machineType="ATM")
    insertMachine(storeID="STORE2", machineID="MACHINE1", machineType="DESKTOP")
    insertMachine(storeID="STORE2", machineID="MACHINE2", machineType="DESKTOP")
    insertMachine(storeID="STORE3", machineID="MACHINE1", machineType="DESKTOP")
    insertMachine(storeID="STORE3", machineID="MACHINE2", machineType="DESKTOP")


if __name__ == "__main__":
    sampleDataInsert()
    print("Done") # for testing purposes
