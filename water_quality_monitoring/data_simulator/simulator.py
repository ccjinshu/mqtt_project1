import random
import time
import json
import sys
import paho.mqtt.client as mqtt

# 仿真器配置
MQTT_BROKER = "localhost"  # MQTT Broker地址
MQTT_PORT = 1883           # MQTT端口
MQTT_TOPIC_PREFIX = "water_quality/" # MQTT主题前缀

class DataSimulator:
    def __init__(self, simulator_id):
        self.simulator_id = simulator_id
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)

    def generate_data(self):
        """ 随机生成水温和二氧化碳含量的数据 """
        water_temp = round(random.uniform(10, 25), 2)  # 生成10到25之间的水温
        co2_level = round(random.uniform(300, 400), 2)  # 生成300到400之间的二氧化碳含量
        #数据采集的时间戳
        timestamp = int(time.time())

        return {"simulator_id": self.simulator_id, "timestamp":timestamp,  "water_temp": water_temp, "co2_level": co2_level}

    def publish_data(self):
        """ 通过MQTT发布数据 """
        data = self.generate_data()
        topic = f"{MQTT_TOPIC_PREFIX}{self.simulator_id}"
        self.client.publish(topic, json.dumps(data))
        print(f"Published data to {topic}: {data}")

    def run(self):
        """ 运行仿真器，定期生成和发送数据 """
        try:
            while True:
                self.publish_data()
                time.sleep(0.5)  # 每5秒发布一次数据
        except KeyboardInterrupt:
            print("Data Simulator stopped")
            self.client.disconnect()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python simulator.py <simulator_id>")
        sys.exit(1)

    simulator_id = sys.argv[1]
    simulator = DataSimulator(simulator_id)
    simulator.run()
