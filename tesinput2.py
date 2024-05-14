from operator import call
import telebot
from telebot import types
import netifaces as ni
import key
from time import sleep
import threading
import re

# Inisialisasi bot
TOKEN = key.TOKEN
bot = telebot.TeleBot(TOKEN)

# Inisialisasi dictionary untuk menyimpan suara pengguna
user_votes = {}
voting_started = False

ipaddr = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

def botrun(time_end,jUser):
    print(time_end,jUser)

# Menangani perintah /start
@bot.message_handler(commands=['startnew'])
def start(message):
    bot.reply_to(message, 'Halo! Silakan berikan informasi tentang acara kamu.')

@bot.message_handler(commands=['start'])
def startuser(message):
    bot.reply_to(message, 'Berikut Website Monitoring \nhttp://'+ipaddr+':5000\nSilakan menggunakan Menu Dibawah ini \nuntuk Voting.\n👇👇👇👇')

# Menangani pesan yang berisi waktu selesai acara
@bot.message_handler(func=lambda message: re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', message.text))
def end_time(message):
    global time_end
    bot.reply_to(message, f'Waktu selesai acara telah diset pada pukul {message.text}. Sekarang, berapa jumlah pengguna yang akan hadir?')
    time_end = message.text
    print(time_end)
    bot.register_next_step_handler(message, num_users)

# Menangani pesan yang berisi jumlah pengguna
def num_users(message):
    jUser = message.text
    print(jUser)
    bot.reply_to(message, f'Akan dihadiri oleh {message.text} pengguna.')
    botrun(time_end,jUser)

def display_votes():
    while True:
        up_votes = list(user_votes.values()).count('naik')
        down_votes = list(user_votes.values()).count('turun')
        print(f"Hasil Voting: Naik - {up_votes}, Turun - {down_votes}")
        sleep(5)

def send_ir():
    up_votes = list(user_votes.values()).count('naik')
    down_votes = list(user_votes.values()).count('turun')



@bot.message_handler(commands=['vote'])
def vote_temperature(message):
    global voting_started
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('naik', callback_data='naik')
    itembtn2 = types.InlineKeyboardButton('turun', callback_data='turun')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Apakah suhu akan naik atau turun?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global voting_started
    user_id = call.message.chat.id
    vote_choice = call.data
    if user_id in user_votes:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, "Maaf, Anda sudah memilih sebelumnya.")
    else:
        user_votes[user_id] = vote_choice
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"Terima kasih atas suaranya! Anda memilih {vote_choice}.")
        if not voting_started:
            voting_started = True
            threading.Thread(target=display_votes).start()

# Menjalankan bot
def run_telebot():
    bot.polling()