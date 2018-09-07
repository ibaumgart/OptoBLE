/**
RFD_Implant for OptoBLE system


@author Ian Baumgart
@version 2.6

*/
#include <RFduinoBLE.h>

//WARNING: Turning on debug mode will greatly increase the power consumption.
//         Be sure to disable debug before uploading. Use serial monitor for debugging.
bool debug = false;

int led1 = 2; //GPIO 0
int led2 = 3; //GPIO 1

int adDuration = 500; //Duration of advertising
bool host = false;    //Signal for host connection


void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  // BE SURE TO CHANGE THIS FOR EACH RFduino. BE SURE KEEP "optoRFD" as first characters in name.
  RFduinoBLE.deviceName = "optoRFD01";                            //Implant name
  RFduinoBLE.customUUID = "576a7d7f-3db0-44c3-8047-1446bf7c054d"; //Custom UUID for added security

  //Debugging circuit LEDs not on implant
  // led used to indicate that the RFduino is advertising
//  pinMode(advertisement_led, OUTPUT);
//  
//  // led used to indicate that the RFduino is connected
//  pinMode(connection_led, OUTPUT);

  if(debug){  Serial.begin(9600); }
}

//Advertising function to broadcast to controller unit
void advertise(){
  RFduinoBLE.begin();
  if(debug){  Serial.println("advertising");  }
  delay(adDuration);
  RFduinoBLE.end();
}

//Input string parser and stimulation function
void runPulse(String inString, int len){
  String params[]={"","", "","", "",""};
  
  int j=0;
  for(int i=0;i<len;i++){
    if(inString[i]=='!'){
      if(debug){  Serial.println(params[j]);  }
      j++;
    }else{
      params[j] += inString[i];
    }
  }
  //Check that the password is "rats"
  if(params[0]=="rats"){
    if(debug){  Serial.println("correct pswd"); }
    for(int k=0; k<params[1].toInt(); k++){
      if(debug){  Serial.println("illumination"); }
      digitalWrite(led1,HIGH);
      if(debug){  Serial.println(params[1].toInt()); }
      if(debug){  Serial.println(params[2].toInt()); }
      if(debug){  Serial.println(params[3].toInt()); }
      if(debug){  Serial.println(params[4].toInt()); }
      if(debug){  Serial.println(params[5].toInt()); }
      delay(params[2].toInt());
      digitalWrite(led1,LOW);
      delay(params[3].toInt()*1000);
      digitalWrite(led2,HIGH);
      delay(params[4].toInt());
      digitalWrite(led2,LOW);
      delay(params[5].toInt()*1000);
    }
    RFduinoBLE.sendFloat(1);
    //Leave this signal in output for some delay to be sure it's seen
    RFduino_ULPDelay(SECONDS(5));
    host = false;
  }else{
    RFduinoBLE.sendFloat(0);
    RFduino_ULPDelay(SECONDS(5));
  }
  RFduinoBLE.end();
}

void loop() {
  if(host){
    if(debug){  Serial.println("host stack begin"); }
    RFduinoBLE.begin();
    //Send temperature measurements for 5 min before disconnecting due to inactivity
    for(int i=0; i<60; i++){
      float T = RFduino_temperature(CELSIUS);
      RFduinoBLE.sendFloat(T);
      RFduino_ULPDelay(SECONDS(5));
    }
    RFduinoBLE.end();
    host = false;
    return;
  }
  // switch to lower power mode
  RFduino_ULPDelay(SECONDS(10));
  advertise();
}

//Receive parameters
void RFduinoBLE_onReceive(char *data, int len){
  runPulse(data, len);
}

void RFduinoBLE_onConnect()
{
  if(debug){  Serial.println("connected");  }
  host = true;
}

void RFduinoBLE_onDisconnect()
{
  if(debug){  Serial.println("disconnected"); }
  RFduinoBLE.end();
  host = false;
}

