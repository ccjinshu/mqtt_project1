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
    local simulator_id=$((RANDOM % 9000 + 1000))  # 生成一个100到999之间的随机数
    echo -e "${GREEN}Starting Data Simulator...${NC}"
    python3 ./data_simulator/simulator.py $simulator_id &
}

# 定义启动监控面板函数
start_dashboard() {
    echo -e "${GREEN}Starting Monitoring Dashboard...${NC}"
    python ./gui/main_window.py &
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
    echo -e "1) ${GREEN}Start Data Simulator${NC}"
    echo -e "2) ${GREEN}Start Monitoring Dashboard${NC}"
    echo -e "3) ${GREEN}Install Dependencies from requirements.txt${NC}"
    echo -e "4) Exit"
    read -p "Enter choice [1-4]: " choice
    return $choice
}

# 执行用户选择的操作
execute_choice() {
    case $1 in
        1)
            start_simulator
            ;;
        2)
            start_dashboard
            ;;
        3)
            install_requirements
            ;;
        4)
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
