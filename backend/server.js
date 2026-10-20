const express = require('express');
const mqtt = require('mqtt');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = 3000;

// Setup Database SQLite
const db = new sqlite3.Database('./warehouse_data.db', (err) => {
  if (err) console.error(err.message);
  console.log('Terhubung ke database SQLite.');
});

db.run(`CREATE TABLE IF NOT EXISTS sensor_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT,
  temperature REAL,
  humidity REAL,
  light_level INTEGER,
  target_anomaly INTEGER
)`);

// Setup MQTT Subscriber
const client = mqtt.connect('mqtt://test.mosquitto.org');
const topic = 'ptmajubersama/warehouse/sensor';

client.on('connect', () => {
  client.subscribe(topic);
  console.log(`Subscribed ke topik: ${topic}`);
});

client.on('message', (topic, message) => {
  const data = JSON.parse(message.toString());
  const query = `INSERT INTO sensor_logs (timestamp, temperature, humidity, light_level, target_anomaly) VALUES (?, ?, ?, ?, ?)`;
  
  db.run(query, [data.timestamp, data.temperature, data.humidity, data.light_level, data.target_anomaly], function(err) {
    if (err) {
      console.log('Gagal menyimpan data:', err.message);
    }
  });
});

app.get('/api/data', (req, res) => {
  db.all('SELECT * FROM sensor_logs ORDER BY id DESC LIMIT 100', [], (err, rows) => {
    if (err) return res.status(500).json({error: err.message});
    res.json({ data: rows });
  });
});

app.listen(port, () => {
  console.log(`Backend Server berjalan di http://localhost:${port}`);
});
