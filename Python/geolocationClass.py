import datetime
import time
import requests
import subprocess
import json
import re
import os
from firebase_admin import credentials, firestore
import firebase_admin
import uuid

#La classe Geolocation attraverso l'utilizzo di un comando di sistema e le Google Api inserisce
#all'interno del record ride_id le informazioni sulla posizione geografica dell'automobile del cliente.

class Geolocation():

    def start(self, user_id,ride_id):

    #La funzione start viene utilizzata per l'inizializzazione delle variabili e per l'apertura del file
    #api_key.json al cui interno sono contenute le chiavi private per l'autenticazione alle Google Api.
    #Dopo aver effettuato queste operazioni la funzione effettua un controllo sul tipo di sistema operativo
    #utilizzato così da lanciare la funzione windows_os o unix_os.

    #Le funzioni windows_os e unix_os operano alla stessa maniera, attraverso un comando di sistema vanno
    #a scrivere all'interno del file data.json la lista degli indirizzi BSSID che la scheda di rete ha rilevato.
    #Tale funzione risulta di fondamentale importanza poichè questo file sarà "dato in pasto" alle API di Google
    #per poter effettuare l'operazione di geolocalizzazione.

        self.user_id = user_id
        print("USER: " + user_id)
        time.sleep(3)
        self.ride_id = ride_id
        print("RIDE: " + ride_id)
        time.sleep(3)
        with open("api_key.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        self.API_KEY = jsonObject['key']
        if os.name == 'nt':
            self.mac_address = self.windows_os()
        else:
            mac_address = self.unix_os()
        self.handle_mac_address("false")
        self.location = self.get_location()
        self.add_record()

    def handle_mac_address(self, ip_state):

#Questa funzione si occupa della pulizia dei BSSID letti dal sistema e della successiva scrittura nel file json.
#handle_mac_address si avvale della funzione regex_BSSID la quale effettua dei controlli attraverso un
#espressione regex per estrapolare il dato in modo congruente a quanto chiesto da Google API.

        template_json = '{"considerIp":'+ip_state+',"wifiAccessPoints": [] }'
        self.json_file = json.loads(template_json)
        self.regex_BSSID()
        self.json_file = json.dumps(self.json_file)
        jsonAP = open("data.json", "w")
        jsonAP.write(self.json_file)
        jsonAP.close()

    def generate_unique_id():
        return str(uuid.uuid4())

    def windows_os(self):
        netshcmd = subprocess.Popen('netsh wlan show networks mode=bssid | findstr BSSID',
                                    shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output, errors = netshcmd.communicate()
        if errors:
            return ("WARNING: ", errors)
        else:
            return output

    def unix_os(self):
        iwdev = subprocess.Popen('sudo iw dev wlan0 scan | grep SSID',
                                 shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output, errors = iwdev.communicate()
        if errors:
            return ("WARNING: ", errors)
        else:
            return output

    def get_location(self):
#La funzione get_location effettua la chiamata alla Google API utilizzando il file data.json e la risposta
#anch'essa in formato json viene salvata nel file location.json che verrà utilizzato nella funzione
#add_record
        url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + self.API_KEY

        response = requests.post(url, data=self.json_file)

        location = response.json()
        print(location)
        return location

    def regex_BSSID(self):
        p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        found = re.findall(p, self.mac_address.decode('UTF-8'))
        for a in found:
            self.json_file["wifiAccessPoints"].append({"macAddress": a})

    def add_record(self):
        
#La funzione add_record si occupa di stabilire una connessione con il DB Firestore, effettua la lettura 
#del file location.json ed effettua l'inserimento delle coordinate GPS all'interno del DB.
#Abbiamo dovuto gestire un'errore relativo alle API di Google che si verifica nel caso in cui
#i punti di accesso (BSSID) non sono abbastanza, in questo caso con il costrutto try catch l'errore viene
#catturato e il metodo di chiamata all'API cambia, andiamo ad impostare il valore considerIp: "true",
#effettaundo questa modifica andremo a ricalcolare il valore di LAT e LONG prendendo in considerazione
#l'indirizzo IP dell' "automobile" ma un'accuratezza esponenzialmente minore rispetto al metodo precedente.

        cred = credentials.Certificate('key2.json')

        try:
            firebase_admin.initialize_app(cred)
        except:
            print("Firebase è già inizializzato") 

        
        
        db = firestore.client()
        try:
            position1 = f"{self.location['location']['lat']}"
        except:
            self.handle_mac_address("true")
            self.location = self.get_location()
            position1 = f"{self.location['location']['lat']}"

        position2 = f"{self.location['location']['lng']}"
        accuracy = float(f"{self.location['accuracy']}")
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        current_unix_time = int(time.time())
        data = {
            "Device": "7",
            "Lat": position1,
            "Long": position2,
            "Accuracy": round(accuracy,0),
            "ModelloAuto": "Reanult Twingo",
            "PhoneNumber": "3498552051",
            "Reset": "NO",
            "Status": "In Attesa",
            "TimeStamp": str(timestamp),
            "unix_timestamp": current_unix_time,
            "User": self.user_id
        }
        print("ID GEOLOCATION---> "+self.ride_id)
        db.collection("Data").document(self.ride_id).set(data)
        time.sleep(3)


def generate_unique_id():
    # ID univoco casuale
    return str(uuid.uuid4())


if __name__ == "__main__":
    id = generate_unique_id()
    g = Geolocation()
    g.start("Gerard Pique",id)