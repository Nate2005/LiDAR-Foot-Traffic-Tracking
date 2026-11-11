#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>

const char* WIFI_NAME = "";
const char* API_URL = "https://unrwalkingmap.com/data/";
const char* API_KEY = "";
const char* SENSOR = "test";

const unsigned long SEND_INTERVAL_MS = 10000;
unsigned long lastSend = 0;

void connectWIFI() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_NAME);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(5000);
    Serial.println("Connecting...");
  }
  Serial.print("\nConnected, IP: ");
  Serial.println(WiFi.localIP());
}

float readSensor() {
  return 10.0 + (random(0, 200) / 10.0);
}

bool postReading(const char* sensor, float value) {
  WiFiClientSecure client;
  client.setInsecure();

  HTTPClient http;
  http.setTimeout(10000);
  if (!http.begin(client, API_URL)) {
    Serial.println("http.begin failed");
    return false;
  }
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Api-Key", API_KEY);

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
