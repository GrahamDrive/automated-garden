#include <OneWire.h>
#include <DallasTemperature.h>
#include<SPI.h>
#include<RF24.h>

#define ONE_WIRE_BUS 2

RF24 radio(9, 10);

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

void setup() {
  // put your setup code here, to run once:
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.openReadingPipe(1, 0xE8E8F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
  
  sensors.begin();
}

void loop() {
  radio.startListening();
  Serial.println("Started");
  char  receviedMessage[32] = {0};
  if(radio.available()){
    radio.read(receviedMessage, sizeof(receviedMessage));
    Serial.println(receviedMessage);
    Serial.println("Turning off Radio!");
    radio.stopListening();

    String stringMessage(receviedMessage);
    if(stringMessage == "GETDATA"){
      Serial.println("Fetching Data");
      sensors.requestTemperatures();
      float tempC = sensors.getTempCByIndex(0);
      float moistureLevel = analogRead(2); // Moisture Sensor Data
      String messageString = String(tempC) + " " + String(moistureLevel);
      char sentMessage[messageString.length()];
      messageString.toCharArray(sentMessage, messageString.length());
      
      radio.write(sentMessage, sizeof(sentMessage));
      Serial.println("Message Sent!");
    }
  }
  delay(100);
}
