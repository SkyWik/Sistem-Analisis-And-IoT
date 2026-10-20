## Arsitektur Sistem
1. **IoT Device (Mock ESP32)**: Mensimulasikan pengiriman data lingkungan (Sensor SHT31 untuk Suhu & Kelembaban, serta sensor LDR untuk pencahayaan) menggunakan protokol MQTT.
2. **Backend (Express.js & SQLite)**: Menerima data dari broker MQTT (seperti Mochi MQTT) dan menyimpannya secara efisien ke dalam database SQLite.
3. **Analytics (Python)**: Melakukan pemodelan AI. Sesuai dengan studi kasus, model ini membandingkan *Logistic Regression*, *Decision Tree*, dan *Random Forest* untuk mengklasifikasikan kondisi anomali. Evaluasi menggunakan metrik **ROC-AUC** dan **Confusion Matrix**.

## Cara Penggunaan
1. **Menjalankan Device Simulator:**
   `cd iot_device && npm install mqtt && node sensor_mock.js`
2. **Menjalankan Backend:**
   `cd backend && npm install express mqtt sqlite3 && node server.js`
3. **Analitik Data & Training Model:**
   `cd analytics && pip install pandas scikit-learn && python model_training.py`
