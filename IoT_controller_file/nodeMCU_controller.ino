#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Cloud server details
const char* serverUrl = "http://your-cloud-server.com/api/sensor-data";

// Sensor pins
const int moisturePin = A0;
const int dhtPin = D2;
const int npkPin = D3;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    // Read sensor data
    int moistureValue = analogRead(moisturePin);
    float moisturePercent = (1023.0 - moistureValue) * 100.0 / 1023.0;
    
    // In a real implementation, you would use DHT and NPK libraries
    float temperature = readDHTTemperature();
    float humidity = readDHTHumidity();
    int nitrogen = readNitrogen();
    int phosphorus = readPhosphorus();
    int potassium = readPotassium();
    
    // Create JSON payload
    StaticJsonDocument<200> doc;
    doc["moisture"] = moisturePercent;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["nitrogen"] = nitrogen;
    doc["phosphorus"] = phosphorus;
    doc["potassium"] = potassium;
    doc["device_id"] = "nodeMCU_001";
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    // Send POST request
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  }
  
  delay(300000); // Wait for 5 minutes before next reading
}

// Placeholder functions - in real implementation, use proper libraries
float readDHTTemperature() {
  return random(100, 400) / 10.0;
}

float readDHTHumidity() {
  return random(200, 900) / 10.0;
}

int readNitrogen() {
  return random(10, 200);
}

int readPhosphorus() {
  return random(5, 150);
}

int readPotassium() {
  return random(20, 300);
}