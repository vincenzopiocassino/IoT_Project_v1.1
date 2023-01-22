import time
import requests
from config import bot_token, chat_id
from firebase_admin import firestore
from firebase_admin import credentials, firestore
import firebase_admin

#La classe Telegram invia un messaggio all'utente che si trova al di sopra della soglia alcolica consentita 
#informandolo che un tassista sta provvedendo al suo recupero ed indicando un numero di telefono a cui può
#contattarlo.

class Telegram():

    def start(self,user_id):

        ##########
        message = 'Un autista UBER sta arrivando!\nNumero telefono: 3807654231'
        #########

        cred = credentials.Certificate('key2.json')

        try:
            firebase_admin.initialize_app(cred)
        except:
            print("Firebase è già inizializzato") 

        db = firestore.client()

        # prendiamo tutti i documenti con User Tiziano Ferro
        users_ref = db.collection(u'Data')

        while(True):
            query = users_ref.where(u'User', u'==', user_id).get()

            user_list = []

            #iteriamo sui documenti trovati
            for doc in query:
                user_list.append(doc.to_dict())

            #ordiniamo la lista in base al timestamp
            sorted_users = sorted(user_list, key=lambda x: x['unix_timestamp'], reverse=True)

            #prendiamo il primo elemento

            try:
                if sorted_users[0].get("Status")=="Preso in carico":
                    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}' #mex
                    requests.get(url) #invio del mex
                    print("Notifica: E' stato inviato il messaggio all'utente")
                    break
                else:
                    print("In attesa che un tassista prenda in carico il cliente.\n")
                    time.sleep(5)
            except:
                print("Documento non esiste")  #modifica
                time.sleep(3)



       

    