//#include "Arduino_SensorKit.h"

const int RELAY_PIN = 13;  // the Arduino pin, which connects to the IN pin of relay

// used to check if the relay module is working and interfaced correctly
const int time_on = 2*1000; // ms
const int time_off = 2*1000; // ms



// the setup function runs once when you press reset or power the board
void setup() {
  pinMode(RELAY_PIN, OUTPUT); // initialize the pin connected to the relay
  	
  //Serial.begin(9600);
  //Environment.begin();
  
}

void loop() {
  // checking if the relay module is working and interfaced correctly: manually turns on and off the relay
  digitalWrite(RELAY_PIN, HIGH); //High is On
  delay(time_on); 
  digitalWrite(RELAY_PIN, LOW); //Low is off
  delay(time_off);

  // interface with the temperature sensor
  
}
