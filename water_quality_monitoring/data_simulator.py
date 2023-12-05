#data_simulator.py
# Networking for Software Developer
# COMP216 Fall 2023 - Final Project
# Group : 4
# Group members:
#   Jin,Shu
#   Wang, Hui
#   Peng Gu, Peng
#   Cai,Ligeng
import random
import time

# Configuration parameters (配置参数)
START_ID = 1

# Realistic parameters for ski resort sensors (滑雪场传感器的真实参数)
TEMPERATURE_MEAN = -5    # Average temperature in degrees Celsius (平均温度，摄氏度)
TEMPERATURE_STD = 5      # Temperature standard deviation (温度标准差)
HUMIDITY_MEAN = 85       # Average humidity (平均湿度)
HUMIDITY_STD = 10        # Humidity standard deviation (湿度标准差)
SNOW_DEPTH_RANGE = (0, 200)  # Snow depth range in cm (积雪深度范围，厘米)
WIND_SPEED_RANGE = (0, 100)  # Wind speed range in km/h (风速范围，千米/小时)



def simulateTime():
    global START_ID
    start_date ='2021-01-01 11:00:00'
    #模拟数据采集时间为 START_ID * 1天
    v_time  = time.mktime(time.strptime(start_date,'%Y-%m-%d %H:%M:%S')) + START_ID * 24 * 60 * 60
    return v_time
def create_data(device_id, location, status):
    global START_ID
    # Generate payload with environmental data (生成带有环境数据的载荷)
    payload = {
        'data_id': START_ID,
        'device': {
            'id': device_id,
            'location': location,  # Location of the sensor (传感器位置)
            'status': status  # Sensor status (传感器状态)
        },
        'environment': {
            'timestamp': int(simulateTime()),
            'temperature': round(random.gauss(TEMPERATURE_MEAN, TEMPERATURE_STD), 2),
            'humidity': round(random.gauss(HUMIDITY_MEAN, HUMIDITY_STD), 2),
            'snow_depth': round(random.gauss(*SNOW_DEPTH_RANGE), 2),
            'wind_speed': round(random.uniform(*WIND_SPEED_RANGE), 2)
        }
    }
    START_ID += 1
    return payload

def print_data(data):
    #change the timestamp to date String
    str1= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['environment']['timestamp']))
    # print(str1)

    # Print the generated data (打印生成的数据)
    print(f"Sensor ID: {data['device']['id']}, "
          f"Data ID: {data['data_id']}, "
          f"Timestamp: {data['environment']['timestamp']}({ str1}), "
          f"Temperature: {data['environment']['temperature']}°C, "
          f"Humidity: {data['environment']['humidity']}%, "
          f"Snow Depth: {data['environment']['snow_depth']}cm, "
          f"Wind Speed: {data['environment']['wind_speed']}km/h, "
          f"Location: {data['device']['location']}")

