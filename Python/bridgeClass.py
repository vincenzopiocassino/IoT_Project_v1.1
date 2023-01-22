import serial
import numpy as np
from resetClass import Reset
from geolocationClass import Geolocation
from telegramClass import Telegram
import time
import uuid

#La classe Bridge è il core dell'applicazione e si occupa anche dell'orchestrazione delle funzionalità.

class Bridge():

    def start_read(self,portname,threshold,user_id,ride_id):
#La funzione start read è utilizzata per l'inizializzazione delle variabili che inviamo dal main,
#inoltre, apriamo la comunicazione con la porta seriale ed avviamo la funzione loop.

        # Open the port PORTNNAME , set BAUDTIME and TIMEOUT
        self.ser = serial.Serial(portname, 9600, timeout=0)
        self.treshold = threshold
        # Set an empty buffer to store value from microcontroller (serial port)
        self.internalBuffer = []
        self.ride_id= ride_id
        self.user_id = user_id
        self.loop()
        
    
    def useData(self):
#La funzione useData si occupa di gestire i byte ricevuti dalla comunicazione seriale con Arduino
#Oltre alla gestione viene effettuato un controllo sulla loro correttezza, se tutti i controlli sono
#soddisfatti si va a comparare il valore letto dalla comunicazione seriale con il valore di soglia
#che abbiamo impostato nel main dell'applicazione, se tale valore soddisfa la condizione allora
#parte il ciclo di blocco del motore, per i dettagli andremo ad analizzare nello specifico le classi
#Geolocation, Telegram e Reset.



        # Calculate buffer length to check that there are at least header, size, and footer
        lenghtBuffer = len(self.internalBuffer)
        
        # If lenght is less than 3 so return false due to lenghtBuffer
        if lenghtBuffer < 2:
            return False

        # Checks if the first character in the buffer is different from firstCharExpected then return false
        firstCharExpected = b'\xff'
        if self.internalBuffer[0] != firstCharExpected:
            return False

        # Cast to int
        # Return the integer represented by the given array of bytes.
		#Not yet useful because we have just one sensor now
        sizeValue = int.from_bytes(self.internalBuffer[1], byteorder='little')


		#Read the value frome the second position of buffer
        value = int.from_bytes(self.internalBuffer[2], byteorder='little')

		 #Print the value on the terminal
        stringValue = "Sensor Gas Value: %d. \n" % (value)
        print(stringValue) 

        #Se il valore supera il valore di soglia blocco la lettura dei dati perchè il motore è 
        #bloccato ed aspetto venga effettuato il reset
        if value > self.treshold :
            self.ser.close()

            g = Geolocation()
            g.start(self.user_id,self.ride_id)
            time.sleep(3)
            t = Telegram()
            t.start(self.user_id)
            time.sleep(3)
            r = Reset()
            r.check_reset_status(self.ride_id)
            return True
            
  
              


    def loop(self):
#La funzione loop è un ciclo infinito che viene utilizzato per leggere i valori inviati
#dal dispositivo Arduino, ogni volta che l'ultimo byte inviato corrisponde con quello expected
#andiamo a richiamare la funzione useData.

        # Infinite loop
        while (True):                         
            # Return the number of byte on the serial port
            serialQueue = self.ser.in_waiting            
            if serialQueue > 0:              
                # Read size bytes on the serial port
                lastChar = self.ser.read(1)
                # Last char expected from microcontroller for the end of string
                lastCharExpected = b'\xfe'
                if lastChar == lastCharExpected:                  
                   
                    # New function to use the data from serial port
                    if (self.useData() == True):
                        break

                     # Reset buffer due to communication has ended
                    self.internalBuffer = []
                                                                                                                                              
                # If the last char is different from 0xfe
                else:
                    # Append the last char to the Internal Buffer
                    self.internalBuffer.append(lastChar)

   
if __name__ == "__main__":
    serial_port ="COM5"
    alcool_treshold = 150
    username="UTENETE TEST"
    ride_id= str(uuid.uuid4())
    b = Bridge()
    b.start_read(serial_port,alcool_treshold,username,ride_id)