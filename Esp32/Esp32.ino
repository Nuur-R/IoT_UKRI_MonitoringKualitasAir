#include <WiFiManager.h> // Library untuk WiFiManager
#include <WiFiClient.h>
#include <PubSubClient.h> // Library untuk MQTT
#include <ArduinoJson.h>  // Library untuk JSON
#include <Arduino.h>
#include <random>

// Konfigurasi MQTT
const char* mqtt_server = "broker.hivemq.com"; // Ganti dengan alamat broker MQTT Anda
const int mqtt_port = 1883;
const char* mqtt_topic = "water_quality"; // Ganti dengan topik MQTT yang sesuai
String device_id = "ESP32_001"; // Ganti dengan Device ID unik

WiFiClient espClient;
PubSubClient client(espClient);

// Fungsi untuk menghasilkan data dummy kualitas air
float generateRandomFloat(float min, float max) {
  return min + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / (max - min)));
}

void generateWaterQualityData(JsonObject& data) {
  data["device_id"] = device_id;
  data["ph"] = generateRandomFloat(0.0, 14.0);
  data["turbidity"] = generateRandomFloat(0.0, 100.0);
  data["dissolved_oxygen"] = generateRandomFloat(0.0, 14.0);
  data["electrical_conductivity"] = generateRandomFloat(0.0, 2000.0);
  data["spectrophotometer"] = generateRandomFloat(0.0, 10.0);
}

// Fungsi untuk menghubungkan ke broker MQTT
void connectToMQTT() {
  while (!client.connected()) {
    Serial.print("Menghubungkan ke MQTT...");
    if (client.connect("ESP32Client", "username", "password")) { // Ganti jika broker membutuhkan autentikasi
      Serial.println("Berhasil terhubung ke MQTT.");
    } else {
      Serial.print("Gagal, rc=");
      Serial.print(client.state());
      Serial.println(" Coba lagi dalam 5 detik.");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  // Menggunakan WiFiManager untuk konfigurasi WiFi
  WiFiManager wifiManager;
  wifiManager.autoConnect("ESP32_WaterQuality"); // Nama Access Point saat konfigurasi WiFi

  Serial.println("WiFi terkoneksi.");

  // Mengatur server MQTT
  client.setServer(mqtt_server, mqtt_port);
  connectToMQTT();
}

void loop() {
  if (!client.connected()) {
    connectToMQTT();
  }

  client.loop();

  // Membuat JSON data
  StaticJsonDocument<256> jsonDoc;
  JsonObject data = jsonDoc.to<JsonObject>();
  generateWaterQualityData(data);

  // Serialisasi JSON
  char buffer[256];
  size_t n = serializeJson(data, buffer);

  // Kirim data ke MQTT
  Serial.println("Mengirim data ke MQTT:");
  Serial.println(buffer);
  client.publish(mqtt_topic, buffer, n);

  delay(15000); // Kirim data setiap 15 detik
}
