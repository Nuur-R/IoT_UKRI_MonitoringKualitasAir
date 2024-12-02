import paho.mqtt.client as mqtt
import json
import random
import time

# Konfigurasi MQTT
MQTT_BROKER = "broker.hivemq.com"  # Ganti dengan alamat broker MQTT Anda
MQTT_PORT = 1883
MQTT_TOPIC = "water_quality"  # Ganti dengan topik MQTT yang sesuai
DEVICE_ID = "Python_Dumy_001"  # Ganti dengan Device ID unik

# Fungsi untuk menghasilkan data random
def generate_random_float(min_value, max_value):
    return round(random.uniform(min_value, max_value), 2)

# Fungsi untuk membuat data kualitas air
def generate_water_quality_data():
    return {
        "device_id": DEVICE_ID,
        "ph": generate_random_float(0.0, 14.0),
        "turbidity": generate_random_float(0.0, 100.0),
        "dissolved_oxygen": generate_random_float(0.0, 14.0),
        "electrical_conductivity": generate_random_float(0.0, 2000.0),
        "spectrophotometer": generate_random_float(0.0, 10.0)
    }

# Callback untuk koneksi berhasil
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Terhubung ke broker MQTT.")
    else:
        print(f"Gagal terhubung ke broker MQTT. Kode: {rc}")

# Callback untuk log aktivitas
def on_log(client, userdata, level, buf):
    print(f"Log: {buf}")

# Fungsi utama
def main():
    # Inisialisasi klien MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_log = on_log

    # Hubungkan ke broker MQTT
    print("Menghubungkan ke broker MQTT...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Loop untuk mengirim data
    client.loop_start()  # Start loop untuk menjaga koneksi tetap hidup
    try:
        while True:
            # Membuat data dummy
            data = generate_water_quality_data()

            # Mengonversi data ke JSON
            json_data = json.dumps(data)
            print(f"Mengirim data ke MQTT:\n{json_data}")

            # Mengirim data ke topik MQTT
            client.publish(MQTT_TOPIC, json_data)

            # Tunggu 15 detik sebelum mengirim data berikutnya
            time.sleep(15)
    except KeyboardInterrupt:
        print("Program dihentikan oleh pengguna.")
    finally:
        client.loop_stop()  # Hentikan loop MQTT
        client.disconnect()
        print("Terputus dari broker MQTT.")

if __name__ == "__main__":
    main()
