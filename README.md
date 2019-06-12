# Data-Fusion
Framework establishment for data fusion algorithm in IoT

Sensor Nodes: Raspberry Pi 3B+ and ESP32

Sensor: DHT

Values Read: Temperature and Humidity

Work Flow:
  The Temperature and Humidity values are read using the sensors in the senor nodes and are sent continuosly to server using MQTT. The values received by the server are fused using the Data Fusion Algorithm and stored in a local database. 
  
  The purpose of this data fusion algorithm is that the quality of data used in any process is improved when the data is fused, as there are might be outliers which disturb the quality of data read by the sensor.
