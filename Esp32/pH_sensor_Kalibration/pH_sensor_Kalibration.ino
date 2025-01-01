#define PH_PIN 4  // pH Meter pada Pin GPIO32

// Variabel kalibrasi
float V_offset = 2.0; // Tegangan pH 7.0 (Anda akan mengatur ini berdasarkan pengukuran pH 7)
float slope = 0.18;   // Slope antara pH 4 dan pH 10 (Anda bisa menyesuaikan ini)

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);  // Resolusi ADC 12-bit (0-4095)
  analogSetAttenuation(ADC_11db);  // Rentang ADC hingga 3.3V
  Serial.println("Mulai Kalibrasi pH Meter");
}

void loop() {
  // Membaca nilai pH dari pH Meter
  int rawValue = analogRead(PH_PIN); // Membaca nilai ADC dari pH Meter
  float voltage = rawValue * (3.3 / 4095.0); // Menghitung tegangan dari nilai ADC (0-3.3V)

  // Menghitung pH berdasarkan tegangan (menggunakan offset dan slope)
  float phValue = (voltage - V_offset) / slope;

  // Menampilkan hasil pH dan tegangan
  Serial.print("Tegangan pH Meter: ");
  Serial.print(voltage);
  Serial.print(" V, ");
  Serial.print("Nilai pH: ");
  Serial.println(phValue);

  // Delay selama 2 detik untuk membaca ulang
  delay(2000);
}
