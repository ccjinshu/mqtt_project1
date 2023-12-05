# publisher_sensor.py
# Networking for Software Developer
# COMP216 Fall 2023 - Final Project
# Group : 4
# Group members:
#   Jin,Shu
#   Wang, Hui
#   Peng Gu, Peng
#   Cai,Ligeng

import random

import paho.mqtt.client as mqtt
import json
import time
import data_simulator

# 配置参数
BROKER = 'localhost'
PORT = 1883
TOPIC = 'sensor/data'
PUBLISH_INTERVAL = 2  # 发布间隔（秒）


#传感器状态数组
SENSOR_STATUS = ['active','active','active','active','active','inactive']
#传感器位置数组，用于随机生成传感器位置，数据来源为加拿大多伦多附近的各大滑雪场名字
SENSOR_LOCATION = ['Tremblant','Blue Mountain','Horseshoe Resort','Mount St. Louis Moonstone','Snow Valley','LakeRidge Ski Resort','Glen Eden','Dagmar Ski Resort','Sunshine Resort','Mountain View','Lake Louis','Cypress Mountain','Grouse Mountain','Whistler Blackcomb','Mount Seymour','Revelstoke Mountain Resort']

class Sensor:
    def __init__(self, broker=BROKER, port=PORT, topic=TOPIC):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.sensor_id=random.randint(1000, 9999)
        self.sensor_location =  random.choice(SENSOR_LOCATION)
        self.sensor_status = random.choice(SENSOR_STATUS)


    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def publish(self):
        try:
            while True:
                data = data_simulator.create_data(self.sensor_id,self.sensor_location,self.sensor_status)
                payload = json.dumps(data)
                self.client.publish(self.topic, payload)
                # print(f"Published: {payload}")
                data_simulator.print_data(data)
                time.sleep(PUBLISH_INTERVAL)
        except KeyboardInterrupt:
            print("Publishing stopped")

    def disconnect(self):
        self.client.disconnect()

    def run(self):
        self.connect()
        self.publish()
        self.disconnect()

if __name__ == '__main__':
    sensor = Sensor()
    sensor.run()
