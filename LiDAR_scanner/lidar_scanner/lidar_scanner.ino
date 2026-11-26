#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>

// WiFi and API details
const char* WIFI_NAME = "";
const char* WIFI_PASSWORD = "";
const char* API_URL = "https://unrwalkingmap.com/data/";
const char* API_KEY = "";
const char* SENSOR = "test";

const unsigned long SEND_INTERVAL_MS = 10000;
unsigned long lastSend = 0;

// TF-Luna details
const int LIDAR_RX_PIN = 16;
const int LIDAR_TX_PIN = 17;

HardwareSerial lidar(2);

// Servo details
const int SERVO_PIN = 18;
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;
const int STEP_DELAY_MS = 15;

Servo servo;

void connectWIFI() {
  delay(500);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_NAME, WIFI_PASSWORD);

  Serial.print("Connecting to WiFi");
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");

    // If no connection after 25 seconds, print status and try again.
    if (millis() - start > 25000) {
      Serial.printf("\nFailed, status=%d, retrying\n", WiFi.status());
      WiFi.disconnect(true);
      delay(500);
      WiFi.mode(WIFI_STA);
      WiFi.begin(WIFI_NAME, WIFI_PASSWORD);
      start = millis();
    }
  }

  Serial.print("\nConnected, IP: ");
  Serial.println(WiFi.localIP());
}

// Use if not connecting to WiFi
// void onWifiEvent(WiFiEvent_t event, WiFiEventInfo_t info) {
//   if (event == ARDUINO_EVENT_WIFI_STA_DISCONNECTED) {
//     Serial.printf("Disconnected, reason=%d\n", info.wifi_sta_disconnected.reason);
//   }
// }

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
  char body[96];
  snprintf(body, sizeof(body), "{\"sensor\":\"%s\",\"value\":%.2f}", sensor, value);

  int code = http.POST(body);
  Serial.printf("POST %s -> %d\n", body, code);
  if (code < 0) {
    Serial.println(HTTPClient::errorToString(code));
  }

  http.end();
  return code == 201;
}

// Get readings from TF-Luna LiDAR scanner
uint16_t distanceCm = 0;
uint16_t strength = 0;

bool readLidar() {
  bool gotFrame = false;
  while (lidar.available() >= 9) {
    if (lidar.read() != 0x59) continue;
    if (lidar.peek() != 0x59) continue;
    lidar.read();

    uint8_t buf[7];
    if (lidar.readBytes(buf, 7) != 7) return gotFrame;

    uint8_t sum = 0x59 + 0x59;
    for (int i = 0; i < 6; i++) sum += buf[i];
    if (sum != buf[6]) continue;

    distanceCm = buf[0] | (buf[1] << 8);
    strength = buf[2] | (buf[3] << 8);
    gotFrame = true;
  }
  return gotFrame;
}

void moveServo() {
  for (int angle = MIN_ANGLE; angle <= MAX_ANGLE; angle++) {
    servo.write(angle);
    delay(STEP_DELAY_MS);
  }
  for (int angle = MAX_ANGLE; angle >= MIN_ANGLE; angle--) {
    servo.write(angle);
    delay(STEP_DELAY_MS);
  }
}

void setup() {
  Serial.begin(115200);
  // lidar.begin(115200, SERIAL_8N1, LIDAR_RX_PIN, LIDAR_TX_PIN);

  servo.setPeriodHertz(50);
  servo.attach(SERVO_PIN, 500, 2400);
  servo.write(90);
  delay(1000);

  // WiFi.onEvent(onWifiEvent); // Use if not connecting to WiFi
  // WiFi.persistent(false);
  // WiFi.disconnect(true, true);
  // delay(500);
  // connectWIFI();
}

unsigned long lastPrint = 0;

void loop() {
  moveServo();

  // if (millis() - lastPrint >= 1000) {
  //   lastPrint = millis();
  //   if (readLidar()) {
  //     Serial.printf("Distance: %4u cm Strength: %5u\n", distanceCm, strength);
  //   } else {
  //     Serial.println("No data from sensor");
  //   }
  // }

  // if (WiFi.status() != WL_CONNECTED) connectWIFI();

  // unsigned long now = millis();
  // if (now - lastSend >= SEND_INTERVAL_MS) {
  //   lastSend = now;
  //   postReading(SENSOR, readSensor());
  // }
}
