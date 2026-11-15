#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>

// WiFi and API details
const char* WIFI_NAME = "";
const char* WIFI_PASSWORD = "";
const char* API_URL = "https://unrwalkingmap.com/data/";
const char* API_KEY = "";
const char* SENSOR = "test";

const unsigned long SEND_INTERVAL_MS = 10000;
unsigned long lastSend = 0;

void connectWIFI() {
  delay(500);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_NAME, WIFI_PASSWORD);

  Serial.print("Connecting to WiFi");
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");

    // If no connection after 20 seconds, print status and try again.
    if (millis() - start > 20000) {
      Serial.printf("\nFailed, status=%d, retrying\n", WiFi.status());
      WiFi.disconnect(true);
      delay(500);
      WiFi.begin(WIFI_NAME, WIFI_PASSWORD);
      start = millis();
    }
  }

  Serial.print("\nConnected, IP: ");
  Serial.println(WiFi.localIP());
}

// Placeholder function. Generates random number for testing.
float readSensor() {
  return 10.0 + (random(0, 200) / 10.0);
}

bool postReading(const char* sensor, float value) {
  // Creates and handles HTTPS connection.
  WiFiClientSecure client;
  client.setInsecure();

  // Create HTTP header, adding API key and Content Type.
  HTTPClient http;
  http.setTimeout(10000);
  if (!http.begin(client, API_URL)) {
    Serial.println("http.begin failed");
    return false;
  }
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Api-Key", API_KEY);

  // Creates json formatted row for the API endpoint.
  char body[100];
  snprintf(body, sizeof(body), "{\"sensor\":\"%s\",\"value\":%.2f}", sensor, value);

  int code = http.POST(body);
  Serial.printf("POST %s -> %d\n", body, code);
  if (code < 0) {
    Serial.println(HTTPClient::errorToString(code));
  }

  http.end();
  return code == 201;
}

void setup() {
  Serial.begin(9600);
  WiFi.persistent(false);
  WiFi.disconnect(true, true);
  delay(500);
  connectWIFI();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWIFI();

  unsigned long now = millis();
  if (now - lastSend >= SEND_INTERVAL_MS) {
    lastSend = now;
    postReading(SENSOR, readSensor());
  }
}
