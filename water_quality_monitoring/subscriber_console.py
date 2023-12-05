# subscriber_console.py
# Networking for Software Developer
# COMP216 Fall 2023 - Final Project
# Group : 4
# Group members:
#   Jin,Shu
#   Wang, Hui
#   Peng Gu, Peng
#   Cai,Ligeng


import paho.mqtt.client as mqtt
import json
import data_simulator

# 配置参数
BROKER = 'localhost'
PORT = 1883
TOPIC = 'sensor/data'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    data_simulator.print_data(payload)  # 使用DataGenerator的打印方法

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
