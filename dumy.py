import time
import random
from supabase import create_client, Client

# URL dan API Key Supabase Anda
SUPABASE_URL = "http://202.159.35.232:8000"  # Ganti dengan URL self-hosted Anda
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q"  # Ganti dengan API Key Anda

# Inisialisasi klien Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Nama tabel Supabase Anda
TABLE_NAME = "Water Quality Monitoring DUMY"  # Ganti dengan nama tabel Anda

def generate_random_data():
    # Generate nilai acak untuk parameter kualitas air
    ph_value = random.uniform(0, 14)  # pH antara 0-14
    turbidity_value = random.uniform(0, 100)  # Kekeruhan (0-100 NTU)
    do_value = random.uniform(0, 14)  # Dissolved Oxygen dalam mg/L
    ec_value = random.uniform(0, 2000)  # Electrical Conductivity dalam µS/cm
    spectrophotometer_value = random.uniform(0, 10)  # Contoh untuk nilai absorbansi spektral

    # Membuat dictionary data untuk dikirim ke Supabase
    data = {
        "ph": ph_value,
        "turbidity": turbidity_value,
        "dissolved_oxygen": do_value,
        "electrical_conductivity": ec_value,
        "spectrophotometer": spectrophotometer_value,
    }
    
    return data

def send_random_data():
    try:
        # Dapatkan data acak
        data = generate_random_data()
        
        # Kirim data ke Supabase
        response = supabase.table(TABLE_NAME).insert(data).execute()

        # Validasi respons
        if response.data:
            print(f"Data berhasil dikirim: {data}")
        elif response.error:
            print(f"Gagal mengirim data: {response.error.message}")
        else:
            print("Respons tidak dikenal:", response)
    except Exception as e:
        print(f"Error: {e}")

# Loop untuk mengirimkan data setiap 15 detik
if __name__ == "__main__":
    print("Mengirim data setiap 15 detik. Tekan Ctrl+C untuk berhenti.")
    try:
        while True:
            send_random_data()
            time.sleep(15)  # Tunggu 15 detik sebelum mengirim data berikutnya
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")
