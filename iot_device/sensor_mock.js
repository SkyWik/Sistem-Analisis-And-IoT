const mqtt = require('mqtt');

const client = mqtt.connect('mqtt://test.mosquitto.org');
const topic = 'ptmajubersama/warehouse/sensor';

client.on('connect', () => {
  console.log('Terhubung ke MQTT Broker. Memulai pengiriman data sensor');
  setInterval(() => {
    const data = {
      timestamp: new Date().toISOString(),
      temperature: (25 + Math.random() * 5).toFixed(2), 
      humidity: (60 + Math.random() * 20).toFixed(2),   
      light_level: Math.floor(Math.random() * 1024),    
      target_anomaly: Math.random() > 0.85 ? 1 : 0      
    };
    
    client.publish(topic, JSON.stringify(data));
    console.log('Data terkirim:', data);
  }, 5000);
});
