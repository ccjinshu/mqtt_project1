# subscriber_gui_dashboard.py
# Networking for Software Developer
# COMP216 Fall 2023 - Final Project
# Group : 4
# Group members:
#   Jin,Shu
#   Wang, Hui
#   Peng Gu, Peng
#   Cai,Ligeng
import time
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

# Constants (常量)
SENSOR_TIMEOUT = 5  # Time in seconds after which sensor is considered offline (传感器被认为掉线的时间，单位：秒)

# Data Cache (数据缓存)
data_cache = {}
sensor_info = {}  # Dictionary to store sensor information (存储传感器信息的字典)

# Assign different colors for different sensors (为不同的传感器分配不同的颜色)
colors = list(mcolors.CSS4_COLORS.values())

# MQTT client configuration (MQTT客户端配置)
client = mqtt.Client()

is_receiving_data = True

# MQTT message callback function (MQTT消息回调函数)
def on_message(client, userdata, msg):
    if   is_receiving_data == False: return
    # Decode JSON payload (解码JSON载荷)
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
    sensor_info[sensor_id]['is_online'] = True  # Set sensor status to online (将传感器状态设置为在线)
    sensor_info[sensor_id]['last_update'] = time.time()  # Update last update time (更新最后更新时间)
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



# Create a top bar for sensor information display using Treeview (使用Treeview创建顶部传感器信息显示栏)
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)

# Define columns for Treeview (为Treeview定义列)
columns = ('Sensor ID', 'Location', 'Status')

tree = ttk.Treeview(top_frame, columns=columns, show='headings', height=2)
tree.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
for col in columns:
    tree.heading(col, text=col)

# Create a scrollbar for the treeview (为treeview创建一个滚动条)
scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=tree.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)

top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_rowconfigure(0, weight=1)


# Function to update sensor information display (更新传感器信息显示的函数)
def update_sensor_info_display():
    for sensor_id, info in sensor_info.items():
        status = "Online" if info.get('is_online', False) else "Offline"
        color = "green" if status == "Online" else "gray"
        location = info['location']
        if tree.exists(sensor_id):
            tree.item(sensor_id, values=(sensor_id, location, status), tags=(color,))
        else:
            tree.insert('', 'end', iid=sensor_id, text="", values=(sensor_id, location, status), tags=(color,))

    tree.tag_configure('green', foreground='green')
    tree.tag_configure('gray', foreground='gray')

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

# Function to check sensors' online status (检查传感器在线状态的函数)
def check_sensors_status():
    current_time = time.time()
    for sensor_id, info in sensor_info.items():
        last_update = info.get('last_update', 0)
        if current_time - last_update > SENSOR_TIMEOUT:
            if info.get('is_online', False):
                info['is_online'] = False
                update_sensor_info_display()

    root.after(1000, check_sensors_status)  # Schedule to run this function again after 1 second (1秒后再次运行此函数)


# Function to start receiving data (开始接收数据的函数)
def start_receiving_data():
    """Start receiving data from MQTT broker (开始从MQTT broker接收数据)"""
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    for topic, qos in MQTT_TOPICS:
        client.subscribe(topic)
    client.loop_start()
    is_receiving_data = True  # Set the flag to start processing messages (设置标志以开始处理消息)

# Function to stop receiving data (停止接收数据的函数)
def stop_receiving_data():
    """Stop receiving data from MQTT broker (停止从MQTT broker接收数据)"""
    global is_receiving_data
    is_receiving_data = False  # Set the flag to stop processing messages (设置标志以停止处理消息)

    time.sleep(0.5) # 等待一小段时间，以确保所有消息都已处理完毕
    client.loop_stop()
    client.disconnect()

# Add control buttons on the right side (在右侧添加控制按钮)
control_frame = tk.Frame(top_frame)
control_frame.grid(row=0, column=1, sticky='ne', padx=0, pady=0)

start_button = ttk.Button(control_frame, text="Start Receiving Data", command=start_receiving_data)
start_button.grid(row=0, column=2, padx=5, pady=5)

stop_button = ttk.Button(control_frame, text="Stop Receiving Data", command=stop_receiving_data)
stop_button.grid(row=1, column=2, padx=5, pady=5)

# Set the closing behavior of the Tkinter window (设置Tkinter窗口的关闭行为)
def on_closing():
    stop_receiving_data()  # Ensure the MQTT loop is stopped (确保MQTT循环停止)
    root.destroy()

start_receiving_data()  # Start receiving data (开始接收数据)
root.protocol("WM_DELETE_WINDOW", on_closing)
# Run Tkinter event loop (运行Tkinter事件循环)
root.after(1000, check_sensors_status)  # Start checking sensors' status (开始检查传感器的状态)
root.mainloop()
