import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import json

# MQTT配置
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [("water_quality/#", 0)] # 订阅所有水质相关主题

# 数据缓存
data_cache = {}

# MQTT消息回调函数
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    simulator_id = payload["simulator_id"]

    if simulator_id not in data_cache:
        data_cache[simulator_id] = {"water_temp": [], "co2_level": []}

    data_cache[simulator_id]["water_temp"].append(payload["water_temp"])
    data_cache[simulator_id]["co2_level"].append(payload["co2_level"])

    # 更新在线仿真器信息
    online_simulators_list = list(data_cache.keys())
    online_simulators.set(f"Online Simulators: {len(online_simulators_list)}\n{', '.join(online_simulators_list)}")

# MQTT客户端配置
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
for topic, qos in MQTT_TOPICS:
    client.subscribe(topic)

# Tkinter GUI设置
root = tk.Tk()
root.title("Water Quality Monitoring Dashboard")

# 设置窗口大小和居中
window_width = 800  # 设置窗口宽度
window_height = 600  # 设置窗口高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 添加在线仿真器指示器
online_simulators = tk.StringVar()
online_simulators.set("Online Simulators: 0\n")
online_simulators_label = tk.Label(root, textvariable=online_simulators)
online_simulators_label.pack()

fig, (ax1, ax2) = plt.subplots(2, 1)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# 增加曲线图之间的距离
plt.subplots_adjust(hspace=0.4)

# 动画更新函数
def animate(i):
    ax1.clear()
    ax2.clear()

    for simulator_id in data_cache:
        if data_cache[simulator_id]["water_temp"]:
            ax1.plot(data_cache[simulator_id]["water_temp"], label=f"{simulator_id} Water Temp")
            ax2.plot(data_cache[simulator_id]["co2_level"], label=f"{simulator_id} CO2 Level")

    ax1.set_title("Water Temperature (°C)")
    ax1.set_ylim(10, 25)  # 设置水温的Y轴范围
    ax2.set_title("CO2 Level (ppm)")
    ax2.set_ylim(300, 400)  # 设置二氧化碳的Y轴范围
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper left")

ani = animation.FuncAnimation(fig, animate, interval=1000)

# MQTT循环开始
def mqtt_loop():
    client.loop_start()

# MQTT循环结束
def on_closing():
    client.loop_stop()
    client.disconnect()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# 开始MQTT循环和Tkinter事件循环
mqtt_loop()
root.mainloop()
