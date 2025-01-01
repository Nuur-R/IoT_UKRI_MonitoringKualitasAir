import json
import paho.mqtt.client as mqtt

# Konfigurasi broker MQTT
BROKER = "broker.emqx.io"  # Ganti dengan alamat broker Anda
PORT = 1883
TOPIC = "water_quality/ESP32_001"  # Harus sesuai dengan topik yang digunakan ESP32

# Callback saat koneksi berhasil
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Terhubung ke broker MQTT.")
        # Subscribe ke topik
        client.subscribe(TOPIC)
        print(f"Subscribed ke topik: {TOPIC}")
    else:
        print(f"Koneksi gagal, kode: {rc}")

# Callback saat menerima pesan
def on_message(client, userdata, msg):
    try:
        # Decode payload JSON
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        # Menampilkan data yang diterima
        print("Data diterima:")
        print(json.dumps(data, indent=4))

        # (Opsional) Simpan data ke file
        with open("water_quality_data.json", "a") as file:
            file.write(json.dumps(data) + "\n")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Konfigurasi klien MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Hubungkan ke broker MQTT
print("Menghubungkan ke broker MQTT...")
client.connect(BROKER, PORT, 60)

# Loop untuk menerima pesan
try:
    print("Menunggu data...")
    client.loop_forever()
except KeyboardInterrupt:
    print("\nProgram dihentikan.")
    client.disconnect()
