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
PUBLISH_INTERVAL = 0.1  # 发布间隔（秒）

#模拟器线程数
THREAD_NUM = 6
START_ID = 1

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
        self.data_start_id = START_ID


    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def publish(self):
        try:
            while True:
                data = data_simulator.create_data(self.data_start_id,self.sensor_id,self.sensor_location,self.sensor_status)
                self.data_start_id += 1
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
    # sensor = Sensor()
    # sensor.run()
    # ask user how many sensors they want to simulate (1-10)
    sensor_num = input(f'How many sensors do you want to simulate? (1-{THREAD_NUM})\n')
    # print(sensor_num)
    # print(type(sensor_num))
    # check if the input is a number
    while not sensor_num.isdigit() or int(sensor_num) < 1 or int(sensor_num) > THREAD_NUM:
        sensor_num = input(f'Please enter a number between 1 and {THREAD_NUM}.\n')
    sensor_num = int(sensor_num)

    # create sensor objects
    sensor_list = []
    for i in range(sensor_num):
        sensor_list.append(Sensor())
    # run all sensors by mutithreading
    import threading
    for i in range(sensor_num):
        t = threading.Thread(target=sensor_list[i].run)
        t.start()





