import serial,time
import firebase_admin
from firebase_admin import credentials, firestore

class Reset():
    
#La funzione Reset si occupa di effettuare il ripristino dello stato del controllare allo stato
#iniziale.
#Il reset viene effettuato quando dall'applicazione il tassista che ha preso in carico il cliente
#invia il segnale "Reset Car Engine", questo segnale modifica la variabile RESET all'interno
#del DB Firestore che viene letta da questo script e se impostata a SI parte con la procedura di 
#ripristino inviando tramite porta seriale il byte R ad Arduino così che possa effettuare l'operazione di
#ripristino (LED VERDE OFF e LED ROSSO OFF).

    def dataread(self):
        self.db = firestore.client()
        ref = self.db.collection("Data").document(self.user_id)
        return ref.get()

    def serialwrite(self):
        SerialObj = serial.Serial('COM5')
        SerialObj.baudrate = 9600  # set Baud rate to 9600
        SerialObj.bytesize = 8     # Number of data bits = 8
        SerialObj.parity   ='N'    # No parity
        SerialObj.stopbits = 1     # Number of Stop bits = 1
        time.sleep(3) 
        SerialObj.write(b'R')  
        SerialObj.close()

    def check_reset_status(self,user_id):
        self.user_id = user_id.strip()
        print("ID--->"+ user_id)
        cred = credentials.Certificate('key2.json')
        try:
            firebase_admin.initialize_app(cred)
        except:
            print("Firebase è già inizializzato") 
        
        while(True):
            reset_status = self.dataread()
            
            if (reset_status.get("Reset") == "SI"):
                print("Reset effettuato la macchina può ripartire!")
                print(self.user_id)

                self.serialwrite()
                self.update_state()

            elif (reset_status.get("Reset") == "NO"):
                print("In attesa di reset da parte del tassista!")
                time.sleep(5)
            else :
                print("Il reset è stato già effettuato!")
                return 0
                
                

    def update_state(self):
        self.db.collection("Data").document(self.user_id).update({ "Reset": "Concluso" })

if __name__ == "__main__":
    r = Reset()
    r.check_reset_status("dd6f90f4-9e8e-44e6-94a8-5b8658a1feb6")
