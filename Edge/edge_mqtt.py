import sqlite3
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# Konfigurasi MQTT
BROKER = "broker.hivemq.com"  # Ganti dengan alamat broker Anda
PORT = 1883
TOPIC = "water_quality"  # Harus sesuai dengan topik yang dikirim ESP32

# Nama file SQLite
DB_FILE = "water_quality.db"

# Membuat koneksi ke database SQLite
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS water_quality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            ph REAL NOT NULL,
            turbidity REAL NOT NULL,
            dissolved_oxygen REAL NOT NULL,
            electrical_conductivity REAL NOT NULL,
            spectrophotometer REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Menyimpan data ke SQLite
def save_to_database(data):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO water_quality (device_id, ph, turbidity, dissolved_oxygen, 
                                        electrical_conductivity, spectrophotometer, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data["device_id"],
            data["ph"],
            data["turbidity"],
            data["dissolved_oxygen"],
            data["electrical_conductivity"],
            data["spectrophotometer"],
            data["timestamp"]
        ))
        conn.commit()
        conn.close()
        print("Data berhasil disimpan ke database.")
    except Exception as e:
        print(f"Error menyimpan data ke database: {e}")

# Callback saat koneksi berhasil
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Terhubung ke broker MQTT.")
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

        # Tambahkan timestamp ke data
        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Menampilkan data yang diterima
        print("Data diterima:")
        print(json.dumps(data, indent=4))

        # Simpan ke database SQLite
        save_to_database(data)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Main program
if __name__ == "__main__":
    # Membuat database jika belum ada
    create_database()

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
