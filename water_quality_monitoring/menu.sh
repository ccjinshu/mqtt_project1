#!/bin/bash

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 定义Mosquitto操作函数
# ...（之前定义的Mosquitto操作函数）

# 定义启动数据仿真器函数
start_simulator() {
    local sensor_id=$((RANDOM % 9000 + 1000))  # 生成一个100到999之间的随机数
    echo -e "${GREEN}Starting Publisher (Water Quality Sensor Simulator)  ...${NC}"
    python3 ./publisher_sensor.py $sensor_id &
}

# 定义启动监控面板函数
start_dashboard_gui() {
    echo -e "${GREEN}Starting Monitoring Dashboard...${NC}"
    python ./subscriber_gui_dashboard.py &
}

# 定义启动监控面板函数
start_dashboard_console() {
    echo -e "${GREEN}Starting Monitoring Dashboard...${NC}"
    python ./subscriber_console.py &
}



# 定义安装依赖函数
install_requirements() {
    echo -e "${GREEN}Installing dependencies from requirements.txt...${NC}"
    # 假设requirements.txt位于脚本同级目录
    pip3 install -r requirements.txt
    echo -e "${GREEN}Dependencies installed.${NC}"
}


# 显示彩色菜单并获取用户选择
show_menu() {
    echo -e "${YELLOW}Choose an option:${NC}"
    echo -e "1) ${GREEN}Start Publisher (Water Quality Sensor Simulator) ${NC}"
    echo -e "2) ${GREEN}Start Subscriber GUI (Monitoring Dashboard) ${NC}"
    echo -e "3) ${GREEN}Start Subscriber Console (Monitoring Console) ${NC}"
    echo -e "4) ${GREEN}Install Dependencies from requirements.txt${NC}"
    echo -e "5) Exit"
    read -p "Enter choice [1-5]: " choice
    return $choice
}

# 执行用户选择的操作
execute_choice() {
    case $1 in
        1)
            start_simulator
            ;;
        2)
            start_dashboard_gui
            ;;
        3)
            start_dashboard_console
            ;;
        4)
            install_requirements
            ;;
        5)
            echo -e "${NC}Exiting..."
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice.${NC}"
            ;;
    esac
}

# 主循环
while true
do
    show_menu
    choice=$?
    execute_choice $choice
    echo "Press Enter to continue..."
    read
done
