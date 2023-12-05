# subscriber_gui_dashboard.py

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import matplotlib.colors as mcolors  # 导入matplotlib的颜色模块
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# ... 余下的代码 ...


# MQTT Configuration (MQTT配置)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [("sensor/data", 0)]  # Subscribed topics (订阅的主题)

# Data Cache (数据缓存)
data_cache = {}
sensor_info = {}  # Dictionary to store sensor information (存储传感器信息的字典)
is_receiving_data = True  # Flag to control data reception (控制数据接收的标志)
SENSOR_TIMEOUT = 5  # Time in seconds after which sensor is considered offline (传感器被认为掉线的时间，单位：秒)

msg_count = 0
# Assign different colors for different sensors (为不同的传感器分配不同的颜色)
colors = list(mcolors.CSS4_COLORS.values())

# MQTT client configuration (MQTT客户端配置)
client = mqtt.Client()

# MQTT message callback function (MQTT消息回调函数)
def on_message(client, userdata, msg):
    global is_receiving_data
    global msg_count
    if is_receiving_data:
        msg_count += 1
        # Update message count label (更新消息计数标签)
        msg_count_label.config(text=f"{msg_count} Messages Received")
        payload = json.loads(msg.payload.decode())
        sensor_id = payload["device"]["id"]
        location = payload["device"]["location"]
        timestamp = payload["environment"]["timestamp"]

        # Initialize data cache for new sensor ID (为新的传感器ID初始化数据缓存)
        if sensor_id not in data_cache:
            data_cache[sensor_id] = {
                'temperature': [],
                'humidity': [],
                'snow_depth': [],
                'wind_speed': []
            }
            sensor_info[sensor_id] = {
                'color': colors[len(sensor_info) % len(colors)],
                'location': location,
                'last_update': time.time(),
                'is_online': True
            }

        # Append data to cache (向缓存中添加数据)
        data = payload["environment"]
        data_cache[sensor_id]['temperature'].append((timestamp, data["temperature"]))
        data_cache[sensor_id]['humidity'].append((timestamp, data["humidity"]))
        data_cache[sensor_id]['snow_depth'].append((timestamp, data["snow_depth"]))
        data_cache[sensor_id]['wind_speed'].append((timestamp, data["wind_speed"]))
        sensor_info[sensor_id]['last_update'] = time.time()
        sensor_info[sensor_id]['is_online'] = True
        update_sensor_info_display()

# Function to start receiving data (开始接收数据的函数)
def start_receiving_data():
    #Disable start button (禁用开始按钮)
    start_button.config(state=tk.DISABLED)
    # Enable stop button (启用停止按钮)
    stop_button.config(state=tk.NORMAL)
    global is_receiving_data
    is_receiving_data = True
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    for topic, qos in MQTT_TOPICS:
        client.subscribe(topic)
    client.on_message = on_message
    client.loop_start()
    # Update running status label (更新运行状态标签)
    status_label.config(text="Running...", foreground="green")

# Function to stop receiving data (停止接收数据的函数)
def stop_receiving_data():
    # Disable stop button (禁用停止按钮)
    stop_button.config(state=tk.DISABLED)
    # Enable start button (启用开始按钮)
    start_button.config(state=tk.NORMAL)
    global is_receiving_data
    is_receiving_data = False

    #wait for the last message to be processed
    time.sleep(1)
    client.loop_stop()
    client.disconnect()
    #update running status label (更新运行状态标签)
    status_label.config(text="Stopped", foreground="red")

# Create Tkinter window (创建Tkinter窗口)
root = tk.Tk()
root.title("Ski Resort Environmental Monitoring Dashboard")

# Create frames for control and chart areas (为控制区和图表区创建框架)
control_frame = tk.Frame(root)
control_frame.grid(row=0, column=0, sticky="nsew")

chart_frame = tk.Frame(root)
chart_frame.grid(row=0, column=1, sticky="nsew")

# Add running status label (添加运行状态标签)
status_label = ttk.Label(control_frame, text="Running...", font=("Arial", 12), foreground="green")
status_label.grid(row=0, column=0, padx=5, pady=5)

online_count_label = ttk.Label(control_frame, text="", font=("Arial", 12))
online_count_label.grid(row=1, column=0, padx=5, pady=5)


# Add msg count label (添加消息计数标签)
msg_count_label = ttk.Label(control_frame, text="", font=("Arial", 12))
msg_count_label.grid(row=2, column=0, padx=5, pady=5)

# Add separator (添加分隔符)
separator = ttk.Separator(control_frame, orient="horizontal")
separator.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

# Add control buttons (添加控制按钮)
start_button = ttk.Button(control_frame, text="Start Receiving Data", command=start_receiving_data)
start_button.grid(row=4, column=0, padx=5, pady=5)

stop_button = ttk.Button(control_frame, text="Stop Receiving Data", command=stop_receiving_data)
stop_button.grid(row=5, column=0, padx=5, pady=5)

# Add separator (添加分隔符)
separator = ttk.Separator(control_frame, orient="horizontal")
separator.grid(row=6, column=0, sticky="ew", padx=5, pady=5)

# Function to create sensor cards (创建传感器卡片的函数)
# 全局字典来存储传感器卡片的引用
sensor_frames = {}
def create_sensor_cards():
    row_index = 7 + len(sensor_frames)
    for sensor_id, info in sensor_info.items():
        # Check if the frame for this sensor already exists (检查这个传感器的框架是否已经存在)
        if sensor_id in sensor_frames:
            card_frame = sensor_frames[sensor_id]
        else:
            # Create new frame for the sensor (为传感器创建新的框架)
            card_frame = ttk.Frame(control_frame, borderwidth=2, relief="groove")
            card_frame.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")
            ttk.Label(card_frame, text=f"Sensor ID: {sensor_id}").grid(row=0, column=0, sticky="w")
            ttk.Label(card_frame, text=f"Location: {info['location']}").grid(row=1, column=0, sticky="w")
            ttk.Label(card_frame, text="", name=f"status_{sensor_id}").grid(row=2, column=0, sticky="w")
            sensor_frames[sensor_id] = card_frame


        # Update the status label (更新状态标签)
        status_label = card_frame.nametowidget(f"status_{sensor_id}")
        status_text = "Online" if info['is_online'] else "Offline"
        status_color = "green" if info['is_online'] else "red"
        status_label.config(text=f"Status: {status_text}", foreground=status_color)


# Function to update sensor information display (更新传感器信息显示的函数)
def update_sensor_info_display():
    current_time = time.time()
    online_sensors = 0
    for sensor_id, info in sensor_info.items():
        last_update = info.get('last_update', 0)
        if current_time - last_update < SENSOR_TIMEOUT:
            info['is_online'] = True
            online_sensors += 1
        else:
            info['is_online'] = False

    online_count_label.config(text=f"{online_sensors} Online Sensors")
    create_sensor_cards()

# Create Matplotlib charts (创建Matplotlib图表)
fig, axes = plt.subplots(4, 1, figsize=(10, 15))

#ajust the space between subplots
plt.subplots_adjust(hspace=0.5)

# Create Tkinter canvas widget (创建Tkinter画布小部件)
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Animation update function (动画更新函数)
def animate(i):
    for ax, (y_label, title) in zip(axes, [('temperature', 'Temperature (°C)'), ('humidity', 'Humidity (%)'), ('snow_depth', 'Snow Depth (cm)'), ('wind_speed', 'Wind Speed (km/h)')]):
        ax.clear()
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel(title)

        # Set the axis to handle date and time format (设置轴以处理日期和时间格式)
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

        for sensor_id, data in data_cache.items():
            if data[y_label]:
                times = [datetime.fromtimestamp(ts) for ts, _ in data[y_label]]
                values = [value for _, value in data[y_label]]
                ax.plot(times, values, label=f"Sensor {sensor_id}", color=sensor_info[sensor_id]['color'])

        ax.legend(loc="upper left")

ani = animation.FuncAnimation(fig, animate, interval=1000)

# Set the closing behavior of the Tkinter window (设置Tkinter窗口的关闭行为)
def on_closing():
    stop_receiving_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
start_receiving_data()
# Run Tkinter event loop (运行Tkinter事件循环)
root.mainloop()
