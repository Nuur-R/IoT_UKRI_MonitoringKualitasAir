import paho.mqtt.client as mqtt
from supabase import create_client, Client
import json
from datetime import datetime

# ============================
# Konfigurasi MQTT
# ============================
mqtt_broker = "broker.emqx.io"  # Broker MQTT yang digunakan
mqtt_port = 1883                 # Port MQTT standar
mqtt_topic = "water_quality/ESP32_001"  # Topik yang digunakan untuk menerima data

# ============================
# Konfigurasi Supabase
# ============================
SUPABASE_URL = "http://202.159.35.232:8000"  # URL Supabase self-hosted Anda
SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q"
)  # API Key Anda

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================
# Callback MQTT
# ============================

# Callback ketika terhubung ke broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    # Subscribe ke topik yang diinginkan
    client.subscribe(mqtt_topic)

# Callback ketika menerima pesan
def on_message(client, userdata, msg):
    try:
        # Mengonversi payload pesan menjadi dictionary
        payload = json.loads(msg.payload.decode())
        print(f"Data Received: {payload}")
        
        # Mengambil nilai dari payload
        ph = payload.get("pH")
        temperature = payload.get("temperature")
        tds = payload.get("TDS")

        # Tampilkan data yang diterima
        print(f"pH: {ph}, Temperature: {temperature} °C, TDS: {tds} ppm")

        # Kirim data ke Supabase
        send_to_supabase(ph, temperature, tds)

    except Exception as e:
        print(f"Error parsing message: {e}")

# Fungsi untuk mengirim data ke Supabase
def send_to_supabase(ph, temperature, tds):
    try:
        data = {
            "ph": ph,
            "temperature": temperature,
            "tds": tds,
        }
        response = supabase.table("ESP32_001").insert(data).execute()
        print("Data sent to Supabase:", response.data)
    except Exception as e:
        print(f"Error sending data to Supabase: {e}")

# ============================
# Setup MQTT Client
# ============================

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Menghubungkan ke broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Memulai loop untuk menerima pesan
client.loop_forever()
