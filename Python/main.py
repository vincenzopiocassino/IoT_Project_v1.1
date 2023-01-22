import uuid
from bridgeClass import Bridge

#Nel file main abbiamo la partenza del nostro progetto.
#Importo la classe Bridge che rappresenta il core dell'applicazione e vado a settare le variabili
#identificative di ogni dispositivo Arduino, infatti ogni dispositivo avrà un utente diverso che 
#sarà settato da questo file.
#Inoltre impostiamo anche un valore di soglia alcolica (treshold) che verosimilmente è lo stesso impostato
#sul dispositivo arduino.


if __name__ == '__main__':
    
    
    serial_port ="COM5"
    alcool_treshold = 145
    username="Tizio Caio"

    br = Bridge()
    #Set te serial port, the Alcol Threshold and the User Name to start read value 

    #Il while in questo caso viene utilizzato per l'esecuzione "infinita" dell'applicazione
    #in questo modo ad ogni lettura del valore il ciclo non viene mai arrestato.

    #Dopo ogni reset del dispositivo, che indica quindi la possibilità di far ripartire l'automobile
    #e quindi effettuare una nuova lettura, viene creato un nuovo valore ride_id il quale indica in modo
    #univoco all'interno del DB Firestore la corsa.

    #In questo modo ad ogni reset abbiamo una nuova corsa nel databese
    # che può essere gestita dalla nostra applicazione ed il sistema continua a generare nuovi id 
    # ad ogni nuova lettura.

    while(True):
        ride_id= str(uuid.uuid4())
        print(ride_id)
        br.start_read(serial_port,alcool_treshold,username,ride_id)


    
    
