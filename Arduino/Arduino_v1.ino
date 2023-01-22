// Arduino project code on smart breathalyzer
#define PIN_LED_ENGINE 2
#define PIN_LED_ALCOL 5

int pinButton = 11;

// Analog pin 0 will be called 'sensor'
int sensor = A0;

// Set the initial sensorValue to 0
int sensorValue = 0;

 int maxValueRead = 0;  //set maxValueRead to 0

void setup()
{

  // Initialize the Led pin as output
  pinMode(PIN_LED_ENGINE, OUTPUT);
  pinMode(PIN_LED_ALCOL, OUTPUT);

  // Initialize the button as input
  pinMode(pinButton, INPUT);

 

  // Initialize serial communication at 9600 bits per second
  Serial.begin(9600);

}

void loop()
{

  // Variable to store the button value
  int valButton = digitalRead(pinButton);

  // If button is pressed then read input from sensor
  if (valButton == HIGH)
  {

    // Read the input on analog pin 0 (named 'sensor')
    sensorValue = analogRead(sensor);

    if (sensorValue > maxValueRead)
    {
      maxValueRead = sensorValue;
    }
   
  }
  else
  {
    
 // If sensorValue is greater than 180
    if (maxValueRead > 150)
    {
      // Print out the value you read

      Serial.write(0xff); 
      Serial.write(0x02);
      Serial.write((char)map(sensorValue,0,1024,0,1024));
      Serial.write(0xfe);

      // Turn off the PIN_LED_ENGINE and turn up the PIN_LED_ALCOL
      digitalWrite(PIN_LED_ALCOL, HIGH);
      digitalWrite(PIN_LED_ENGINE, LOW);
      Serial.flush();
      if (Serial.available() > 0) 
      {
          String message = Serial.readString();
          Serial.println("Received message: " + message);
          if (message == "R")
          {
            maxValueRead = 0;
            digitalWrite(PIN_LED_ALCOL, LOW);

          }
      }
    }
    else if (maxValueRead > 100 && maxValueRead <140)
    {

      digitalWrite(PIN_LED_ALCOL, LOW);
      digitalWrite(PIN_LED_ENGINE, HIGH);
    }
  }
}