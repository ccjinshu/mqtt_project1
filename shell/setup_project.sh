#!/bin/bash

# 创建项目根目录
mkdir -p water_quality_monitoring

# 进入项目根目录
cd water_quality_monitoring

# 创建子目录
mkdir -p data_simulator mqtt_client gui utils

# 创建并写入 requirements.txt
echo "paho-mqtt\nmatplotlib\ntkinter" > requirements.txt

# 创建 data_simulator 模块
echo "# Data Simulator Module" > data_simulator/__init__.py
echo -e "\"\"\"\nData Simulator for Water Quality Monitoring\n\"\"\"\n\nimport random\nimport paho.mqtt.client as mqtt\nimport json\nimport time\n\nclass DataSimulator:\n    pass\n" > data_simulator/simulator.py

# 创建 mqtt_client 模块
echo "# MQTT Client Module" > mqtt_client/__init__.py
echo -e "\"\"\"\nMQTT Client for Water Quality Monitoring\n\"\"\"\n\nimport paho.mqtt.client as mqtt\n\nclass MQTTClient:\n    pass\n" > mqtt_client/client.py

# 创建 gui 模块
echo "# GUI Module" > gui/__init__.py
echo -e "\"\"\"\nGUI for Water Quality Monitoring\n\"\"\"\n\nimport tkinter as tk\nfrom matplotlib.backends.backend_tkagg import FigureCanvasTkAgg\nimport matplotlib.pyplot as plt\n\nclass MainWindow:\n    pass\n" > gui/main_window.py

# 创建 utils 模块
echo "# Utilities Module" > utils/__init__.py
echo -e "\"\"\"\nUtilities for Water Quality Monitoring\n\"\"\"\n\ndef save_data_to_csv(data, filename):\n    pass\n\ndef read_data_from_csv(filename):\n    pass\n" > utils/helpers.py

echo "Project structure and files created successfully."
