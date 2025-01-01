#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <WiFiManager.h>  // WiFiManager untuk pengaturan Wi-Fi
#include <PubSubClient.h>  // Library MQTT

// =====================
// Konfigurasi Pin Sensor
// =====================
#define ONE_WIRE_BUS 33  // DS18B20
#define PH_PIN 32        // pH Meter (Analog)
#define TDS_PIN 35       // TDS Meter (Analog)

// =====================
// Variabel Konfigurasi Sensor
// =====================
// DS18B20
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// pH Meter
float V_offset = 1.8;
float slope = 0.2; 

// TDS Meter
float tdsVoltageOffset = 0.0; // Offset kalibrasi TDS Meter (volt)
float tdsConversionFactor = 0.5; // Faktor konversi TDS (contoh: 0.5)

// =====================
// Konfigurasi MQTT
// =====================
String device_id = "ESP32_001"; // Ganti dengan Device ID unik
String mqtt_topic = "water_quality/" + device_id; // Topic MQTT unik per sensor
const char* mqtt_server = "broker.emqx.io"; // Broker EMQX
const int mqtt_port = 1883; // Port standar MQTT (non-SSL/TLS)

WiFiClient espClient;
PubSubClient client(espClient);

// =====================
// Fungsi Inisialisasi
// =====================
void setup() {
  Serial.begin(115200);

  // Inisialisasi DS18B20
  sensors.begin();

  // Konfigurasi ADC ESP32
  analogReadResolution(12); // Resolusi ADC 12-bit (0-4095)
  analogSetAttenuation(ADC_11db); // Rentang ADC hingga ~3.3V

  // Setup Wi-Fi dengan WiFiManager
  setupWiFi();

  // Setup MQTT
  setupMQTT();
}

// =====================
// Fungsi Pembacaan Sensor
// =====================

// Fungsi untuk membaca suhu dari DS18B20
float readTemperature() {
  sensors.requestTemperatures(); // Meminta data dari DS18B20
  return sensors.getTempCByIndex(0); // Membaca suhu dari sensor pertama
}

// Fungsi untuk membaca nilai analog dari pH Meter
float readPH() {
  // Membaca nilai analog dari pH Meter
  int rawValue = analogRead(PH_PIN);
  float voltage = rawValue * (3.3 / 4095.0);
  float phValue = (voltage - V_offset) / slope;
  return phValue;
}

// Fungsi untuk membaca nilai analog dari TDS Meter
float readTDS() {
  int rawValue = analogRead(TDS_PIN); // Membaca nilai analog
  float voltage = rawValue * (3.3 / 4095.0); // Konversi ke volt
  float tdsValue = (voltage + tdsVoltageOffset) * tdsConversionFactor; // Konversi ke nilai TDS
  return tdsValue;
}

// =====================
// Fungsi untuk Setup Wi-Fi
// =====================
void setupWiFi() {
  WiFiManager wifiManager;
  wifiManager.autoConnect("ESP32_Configuration"); // Nama SSID default jika tidak ada jaringan yang ditemukan
  Serial.println("Connected to Wi-Fi");
}

// =====================
// Fungsi Setup MQTT
// =====================
void setupMQTT() {
  client.setServer(mqtt_server, mqtt_port);
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect(device_id.c_str())) {
      Serial.println("Connected to MQTT");
    } else {
      Serial.print("Failed with state: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

// =====================
// Fungsi Kirim Data ke MQTT
// =====================
void sendDataToMQTT(float phValue, float temperature, float tdsValue) {
  String payload = "{\"device_id\":\"" + device_id + "\",\"pH\":" + String(phValue) + ",\"temperature\":" + String(temperature) + ",\"TDS\":" + String(tdsValue) + "}";
  client.publish(mqtt_topic.c_str(), payload.c_str()); // Kirim ke topic unik
}

// =====================
// Fungsi Loop Utama
// =====================
void loop() {
  if (!client.connected()) {
    setupMQTT();  // Jika koneksi MQTT terputus, coba sambungkan ulang
  }
  client.loop();  // Proses koneksi dan komunikasi MQTT

  // Membaca suhu
  float temperature = readTemperature();
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  // Membaca nilai pH
  float ph = readPH(); // Membaca nilai pH
  Serial.print("Nilai pH: ");
  Serial.println(ph);

  // Membaca nilai TDS
  float tds = readTDS();
  Serial.print("TDS Value: ");
  Serial.print(tds);
  Serial.println(" ppm");

  // Mengirim data ke MQTT
  sendDataToMQTT(ph, temperature, tds);

  // Delay 1 detik sebelum membaca lagi
  delay(1000);
}
