# subscriber_gui_dashboard.py
import threading
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
from datetime import datetime, timedelta

# ... 余下的代码 ...


# MQTT Configuration (MQTT配置)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [("sensor/data", 0)]  # Subscribed topics (订阅的主题)

SENSOR_TIMEOUT = 5  # Time in seconds after which sensor is considered offline (传感器被认为掉线的时间，单位：秒)
X_MAX_DISPLAY = 180  # Maximum number of data points to display (显示的最大数据点数)
# 图像刷新间隔
REFRESH_INTERVAL = 500  # Refresh interval in milliseconds (刷新间隔，单位：毫秒)


# Data Cache (数据缓存)
data_cache = {}
sensor_info = {}  # Dictionary to store sensor information (存储传感器信息的字典)
is_receiving_data = True  # Flag to control data reception (控制数据接收的标志)

msg_count = 0
# Assign different colors for different sensors (为不同的传感器分配不同的颜色)
colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'yellow','orangered', 'yellowgreen']
# colors = list(mcolors.cnames.keys()）
# Get a list of all available colors (获取所有可用颜色的列表)


#set the latest timestamp of '2000-01-01 00:00:00'
latest_timestamp = 946656000 # Latest timestamp received (最新接收到的时间戳)
def run_mqtt_client():
    client.loop_forever()


# MQTT message callback function (MQTT消息回调函数)
def on_message(client, userdata, msg):
    global is_receiving_data
    global msg_count
    global latest_timestamp
    if not is_receiving_data: # Ignore messages if not receiving data (如果不接收数据，则忽略消息)
        return

    if is_receiving_data:
        msg_count += 1
        # Update message count label (更新消息计数标签)
        msg_count_label.config(text=f"{msg_count} Messages Received")
        payload = json.loads(msg.payload.decode())
        sensor_id = payload["device"]["id"]
        location = payload["device"]["location"]
        timestamp = payload["environment"]["timestamp"]
        if(timestamp>latest_timestamp):
            latest_timestamp = timestamp
            #format the timestamp to date string
            str1= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(latest_timestamp))
            # print(str1)
        # Initialize data cache for new sensor ID (为新的传感器ID初始化数据缓存)
        if sensor_id not in data_cache:
            data_cache[sensor_id] = {
                'temperature': [],
                'humidity': [],
                'snow_depth': [],
                'wind_speed': []
            }
            #get a random   color
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
        sensor_info[sensor_id]['received_count'] = sensor_info[sensor_id]['received_count'] + 1 if 'received_count' in sensor_info[sensor_id] else 1
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
    # # client.on_message = on_message  # Assign on_message callback function (分配on_message回调函数)
    # client.loop_start()

    # Create and start the MQTT client thread (创建并启动MQTT客户端线程)
    mqtt_thread = threading.Thread(target=run_mqtt_client, daemon=True)
    mqtt_thread.start()

    # Update running status label (更新运行状态标签)
    status_label.config(text="Running...", foreground="green")

# Function to stop receiving data (停止接收数据的函数)
def stop_receiving_data():
    global is_receiving_data
    is_receiving_data = False

    # Disable stop button (禁用停止按钮)
    stop_button.config(state=tk.DISABLED)
    # Enable start button (启用开始按钮)
    start_button.config(state=tk.NORMAL)

    client.disconnect()
    #update running status label (更新运行状态标签)
    status_label.config(text="Stopped", foreground="red")




# MQTT client configuration (MQTT客户端配置)
client = mqtt.Client()
client.on_message = on_message

# Create Tkinter window (创建Tkinter窗口)
root = tk.Tk()
root.title("Ski Resort Environmental Monitoring Dashboard")

# Create frames for control and chart areas (为控制区和图表区创建框架)
control_frame = tk.Frame(root)
control_frame.grid(row=0, column=0, sticky="nsew")

chart_frame = tk.Frame(root)
chart_frame.grid(row=0, column=1, sticky="nsew",padx=0,pady=0)

# 配置行和列的权重
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)  # 增加控制区的列权重
root.grid_columnconfigure(1, weight=3)  # 增加图表区的列权重，这里的权重更大，因此图表区会获得更多空间



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
            ttk.Label(card_frame, text="", name=f"status_{sensor_id}").grid(row=3, column=0, sticky="w")
            ttk.Label(card_frame, text="", name=f"received_count_{sensor_id}").grid(row=2, column=0, sticky="w")
            sensor_frames[sensor_id] = card_frame


        # Update the status label (更新状态标签)
        received_count_label = card_frame.nametowidget(f"received_count_{sensor_id}")
        received_count_label.config(text=f"Received: {info['received_count']}")
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

fig.autofmt_xdate()  # Automatically format x-axis as dates (自动将x轴格式化为日期)


#ajust the space between subplots
plt.subplots_adjust(hspace=0.5,top=0.90,bottom=0.1)

# Add a big title at the top of the chart area (在图表区域的顶部添加一个大标题)
fig.suptitle('Ski Resort Environmental Monitoring Dashboard', fontsize=16)

# Create Tkinter canvas widget (创建Tkinter画布小部件)
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Animation update function (动画更新函数)
def animate(i):
    global latest_timestamp
    # Set the window of time you want to display (设置你想要显示的时间窗口)
    end_time = latest_timestamp == 0 and datetime.now() or datetime.fromtimestamp(latest_timestamp)
    start_time = end_time - timedelta(days=X_MAX_DISPLAY)  # 从当前时间回溯180天（半年）

    for ax, (y_label, title) in zip(axes, [('temperature', 'Temperature (°C)'), ('humidity', 'Humidity (%)'), ('snow_depth', 'Snow Depth (cm)'), ('wind_speed', 'Wind Speed (km/h)')]):
        ax.clear()

        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel(title)

        # Set the axis to handle date and time format (设置轴以处理日期和时间格式)
        # Format x-axis to show dates (格式化x轴显示日期)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        # Set x-axis to display the last six months (设置x轴显示最近六个月)
        ax.set_xlim([mdates.date2num(start_time), mdates.date2num(end_time)])

        for sensor_id, data in data_cache.items():
            if data[y_label]:
                times = [datetime.fromtimestamp(ts) for ts, _ in data[y_label]]
                values = [value for _, value in data[y_label]]
                ax.plot(times, values, label=f"Sensor {sensor_id}", color=sensor_info[sensor_id]['color'])

        ax.legend(loc="upper left")

ani = animation.FuncAnimation(fig, animate, interval=REFRESH_INTERVAL)

# Set the closing behavior of the Tkinter window (设置Tkinter窗口的关闭行为)
def on_closing():
    stop_receiving_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
start_receiving_data()
root.after(1000, update_sensor_info_display)  # Start the periodic update (开始周期性更新)

# Run Tkinter event loop (运行Tkinter事件循环)
root.mainloop()
