#!/bin/bash

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 定义操作函数
check_status() {
    echo -e "${YELLOW}Checking Mosquitto MQTT Broker status...${NC}"
    brew services list | grep mosquitto
}

start_mosquitto() {
    echo -e "${GREEN}Starting Mosquitto MQTT Broker...${NC}"
    brew services start mosquitto
}

stop_mosquitto() {
    echo -e "${RED}Stopping Mosquitto MQTT Broker...${NC}"
    brew services stop mosquitto
}

restart_mosquitto() {
    echo -e "${YELLOW}Restarting Mosquitto MQTT Broker...${NC}"
    brew services restart mosquitto
}

install_mosquitto() {
    echo -e "${GREEN}Installing Mosquitto MQTT Broker...${NC}"
    brew install mosquitto
}

uninstall_mosquitto() {
    echo -e "${RED}Uninstalling Mosquitto MQTT Broker...${NC}"
    brew uninstall mosquitto
}

reinstall_mosquitto() {
    echo -e "${YELLOW}Reinstalling Mosquitto MQTT Broker...${NC}"
    brew reinstall mosquitto
}

# 显示彩色菜单并获取用户选择
show_menu() {
    echo -e "${YELLOW}Choose an option:${NC}"
    echo -e "1) ${YELLOW}Check Mosquitto Status${NC}"
    echo -e "2) ${GREEN}Start Mosquitto${NC}"
    echo -e "3) ${RED}Stop Mosquitto${NC}"
    echo -e "4) ${YELLOW}Restart Mosquitto${NC}"
    echo -e "5) ${GREEN}Install Mosquitto${NC}"
    echo -e "6) ${RED}Uninstall Mosquitto${NC}"
    echo -e "7) ${YELLOW}Reinstall Mosquitto${NC}"
    echo -e "8) Exit"
    read -p "Enter choice [1-8]: " choice
    return $choice
}

# 执行用户选择的操作
execute_choice() {
    case $1 in
        1)
            check_status
            ;;
        2)
            start_mosquitto
            ;;
        3)
            stop_mosquitto
            ;;
        4)
            restart_mosquitto
            ;;
        5)
            install_mosquitto
            ;;
        6)
            uninstall_mosquitto
            ;;
        7)
            reinstall_mosquitto
            ;;
        8)
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
