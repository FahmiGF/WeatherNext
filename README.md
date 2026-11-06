# 🌦️ WeatherNow AI

**Weather Intelligence & Voice Assistant Platform**

Platform aplikasi cuaca modern, andal, dan hemat biaya yang menggabungkan data cuaca real-time dari **Open-Meteo API** (gratis tanpa API key) dan **BMKG Indonesia**, dilengkapi dengan **AI Weather Chatbot** serta **AI Voice Assistant**.

---

## ✨ Fitur Utama

1. **Dashboard Cuaca Real-Time**: Suhu aktual, suhu terasa (*feels like*), kelembapan, kecepatan angin, curah hujan, dan indeks UV untuk Surabaya & 20+ kota di Indonesia.
2. **Prakiraan 7 Hari**: Grafik tren suhu (min & maks), probabilitas & estimasi curah hujan harian.
3. **Outlook 30 Hari**: Estimasi tren cuaca jangka panjang dengan kalender dan proyeksi suhu.
4. **Histori Cuaca & Evaluasi**: Penyimpanan observasi masa lalu untuk analisis dan perbandingan periode (minggu ini vs minggu lalu).
5. **AI Weather Chatbot**: Asisten interaktif dalam Bahasa Indonesia yang menjawab pertanyaan cuaca langsung berdasarkan data API.
6. **AI Voice Assistant**: Fitur *Speech-to-Text* (berbicara langsung ke aplikasi) dan *Text-to-Speech* (aplikasi membacakan prakiraan dengan suara natural).
7. **Model & System Monitoring**: Status integrasi Open-Meteo, BMKG MEWS, dan metrik akurasi (MAE, RMSE, Brier Score).

---

## 🚀 Cara Menjalankan (1 Klik)

Cukup **klik dua kali** file berikut:
```bash
Buka_WeatherNow_AI.bat
```

Browser akan otomatis membuka:
- **Web Dashboard**: [http://localhost:8001](http://localhost:8001)
- **Dokumentasi REST API (Swagger)**: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 🛠️ Menjalankan via Terminal (Manual)

```bash
cd backend
pip install -r requirements.txt
python run.py
```

Buka browser di `http://localhost:8001`.

---

## 📡 Sumber Data Cuaca
- **Open-Meteo**: Data cuaca global real-time & prakiraan 7-16 hari (WMO standard, 100% gratis).
- **BMKG MEWS**: Data prakiraan cuaca & peringatan dini resmi Indonesia.
