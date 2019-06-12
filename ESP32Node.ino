#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHTesp.h>

#define SENSOR 18

const char* ssid = "Mithul";
const char* mqttServer = "m15.cloudmqtt.com";
const int mqttPort = 12861;
const char* mqttUser = "clnyrexp";
const char* mqttPassword = "s8WgWnydSOzB";
DHTesp dht;

WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() 
{ 
  Serial.begin(115200);
  Serial.println();
  WiFi.begin(ssid);
   
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
  
  client.setServer(mqttServer, mqttPort);
  
  while (!client.connected()) 
  {
    Serial.println("Connecting to CloudMQTT...");
 
    if (client.connect("ESP32Client", mqttUser, mqttPassword)) 
    {
      Serial.println("Connected");
    }
    else 
    {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  dht.setup(SENSOR, DHTesp::DHT11);
  StaticJsonBuffer<300> JSONbuffer;
  JsonObject& JSONencoder = JSONbuffer.createObject();
 
  JSONencoder["Loc"] = "RegionB";
  JsonArray& Temp = JSONencoder.createNestedArray("Temp");
  JsonArray& Hum = JSONencoder.createNestedArray("Hum");
  //char temperature[10],humidity[10];
  uint32_t period = 18000L;
  Serial.println("Location: RegionB");
  Serial.println("Receiving Temperature and Humidity data from Sensor");
  Serial.println(" ------------------------------------------- ");
  Serial.println("|                                           |");
  Serial.println("|         Data sent from RegionB            |");
  Serial.println("|                                           |");
  Serial.println("|-------------------------------------------|");
  Serial.println("|   S.NO   |   TEMPERATURE   |   HUMIDITY   |");
  Serial.println("|-------------------------------------------|");
  int i=1;
  for( uint32_t tStart = millis(); (millis()-tStart) < period; )
  {
    int dhtPin = 18;
    TempAndHumidity newValues = dht.getTempAndHumidity();
    if (dht.getStatus() == 0) 
    {
      Temp.add(newValues.temperature);
      Hum.add(newValues.humidity);
      Serial.println("|     "+String(i)+"    |      "+String(newValues.temperature)+"      |    "+String(newValues.humidity)+"     |");
      delay(1000);
      i++;
    }
  }
  
  Serial.println("---------------------------------------------");
 
  char JSONmessageBuffer[100];
  JSONencoder.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  Serial.println("Sending message to MQTT topic: THData");
  //Serial.println(JSONmessageBuffer);
 
  if (client.publish("THData", JSONmessageBuffer) == true) {
    Serial.println("Message is sent successfully");
  } else {
    Serial.println("Error sending message");
  }
  
  client.loop();
  Serial.println("-------------");
}
 
void loop() 
{
}
