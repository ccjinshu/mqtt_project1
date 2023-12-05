# subscriber_gui_dashboard.py
# Networking for Software Developer
# COMP216 Fall 2023 - Final Project
# Group : 4
# Group members:
#   Jin,Shu
#   Wang, Hui
#   Peng Gu, Peng
#   Cai,Ligeng

# subscriber_gui_dashboard.py

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import paho.mqtt.client as mqtt
import json

# MQTT Configuration (MQTT配置)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [("sensor/data", 0)]  # Subscribed topics (订阅的主题)

# Data Cache (数据缓存)
data_cache = {}
sensor_info = {}  # Dictionary to store sensor information (存储传感器信息的字典)

# Assign different colors for different sensors (为不同的传感器分配不同的颜色)
colors = list(mcolors.CSS4_COLORS.values())

# MQTT client configuration (MQTT客户端配置)
client = mqtt.Client()

# MQTT message callback function (MQTT消息回调函数)
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    sensor_id = payload["device"]["id"]
    location = payload["device"]["location"]

    # Initialize data cache for new sensor ID (为新的传感器ID初始化数据缓存)
    if sensor_id not in data_cache:
        data_cache[sensor_id] = {
            'temperature': [],
            'humidity': [],
            'snow_depth': [],
            'wind_speed': []
        }
        sensor_info[sensor_id] = {'color': colors[len(sensor_info) % len(colors)], 'location': location}

    data = payload["environment"]
    # Append data to cache (向缓存中添加数据)
    data_cache[sensor_id]['temperature'].append(data["temperature"])
    data_cache[sensor_id]['humidity'].append(data["humidity"])
    data_cache[sensor_id]['snow_depth'].append(data["snow_depth"])
    data_cache[sensor_id]['wind_speed'].append(data["wind_speed"])

    update_sensor_info_display()

# Create Tkinter window (创建Tkinter窗口)
root = tk.Tk()
root.title("Ski Resort Environmental Monitoring Dashboard")

# Create a top bar for sensor information and control buttons (创建顶部传感器信息和控制按钮栏)
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)

sensor_info_frame = tk.Frame(top_frame)
sensor_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

control_frame = tk.Frame(top_frame)
control_frame.pack(side=tk.RIGHT, padx=5, pady=5)



# Function to update sensor information display (更新传感器信息显示的函数)
def update_sensor_info_display():
    for widget in sensor_info_frame.winfo_children():
        widget.destroy()

    for sensor_id, info in sensor_info.items():
        label = ttk.Label(sensor_info_frame, text=f"Sensor {sensor_id} (Location: {info['location']})",
                          background=info['color'])
        label.pack(side=tk.LEFT, padx=5, pady=5)

# Create Matplotlib charts (创建Matplotlib图表)
fig, axes = plt.subplots(4, 1, figsize=(10, 15))

# Adjust the subplots and the space at the top (调整子图和顶部空间)
fig.subplots_adjust(hspace=0.5, top=0.95)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True, pady=(20, 0))  # Add padding at the top (在顶部添加间距)

# Animation update function (动画更新函数)
def animate(i):
    titles = ["Temperature (°C)", "Humidity (%)", "Snow Depth (cm)", "Wind Speed (km/h)"]
    y_labels = ['temperature', 'humidity', 'snow_depth', 'wind_speed']

    for ax, title, y_label in zip(axes, titles, y_labels):
        ax.clear()
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel(title)

        for sensor_id, data in data_cache.items():
            ax.plot(data[y_label], label=f"Sensor {sensor_id}", color=sensor_info[sensor_id]['color'])

        ax.legend(loc="upper left")

ani = animation.FuncAnimation(fig, animate, interval=1000)

# Function to start receiving data (开始接收数据的函数)
def start_receiving_data():
    """Start receiving data from MQTT broker (开始从MQTT broker接收数据)"""
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    for topic, qos in MQTT_TOPICS:
        client.subscribe(topic)
    client.loop_start()

# Function to stop receiving data (停止接收数据的函数)
def stop_receiving_data():
    """Stop receiving data from MQTT broker (停止从MQTT broker接收数据)"""
    client.loop_stop()
    client.disconnect()

# Add control buttons at the top-right corner (在顶部右侧添加控制按钮)
start_button = ttk.Button(control_frame, text="Start Receiving Data", command=start_receiving_data)
start_button.pack(side=tk.LEFT)

stop_button = ttk.Button(control_frame, text="Stop Receiving Data", command=stop_receiving_data)
stop_button.pack(side=tk.LEFT)

# Set the closing behavior of the Tkinter window (设置Tkinter窗口的关闭行为)
def on_closing():
    client.disconnect()  # Ensure the MQTT loop is stopped (确保MQTT循环停止)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run Tkinter event loop (运行Tkinter事件循环)
root.mainloop()
