from email import message
from turtle import done
import telebot
from telebot import types
import netifaces as ni
import key
from time import sleep
import threading
import re
import timeKU
from temp import get_suhu
from timeKU import set_off

# Inisialisasi bot
TOKEN = key.TOKEN
bot = telebot.TeleBot(TOKEN)

# Inisialisasi dictionary untuk menyimpan suara pengguna
user_votes = {}
voting_started = False
done_setting = False

ipaddr = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
# ipaddr = ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']

def botrun(time_end,jUser):
    print(time_end,jUser)

# Menangani perintah /start
@bot.message_handler(commands=['start'])
def startuser(message):
    bot.reply_to(message, 'Berikut Website Monitoring \nhttp://'+ipaddr+':5000\nSilakan menggunakan Menu Dibawah ini \nuntuk Voting.\n👇👇👇👇')

@bot.message_handler(commands=['adminsett'])
def start(message):
    global done_setting
    if done_setting == False:
        done_setting = True
        bot.reply_to(message, 'Halo! Silakan berikan informasi kapan acara selesai (Format penulisan jam 24 jam, misal 11:00 atau 13:44).')
    else :
        bot.reply_to(message, 'Anda Sudah menseting sebelumnya')

# Menangani pesan yang berisi waktu selesai acara
@bot.message_handler(func=lambda message: re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', message.text))
def end_time(message):
    global time_end
    bot.reply_to(message, f'Waktu selesai acara telah diset pada pukul {message.text}.\nAnda menyelsaikan Setting')
    time_end = message.text
    print(time_end)
    set_off(time_end)

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
        user_votes[user_id] = vote_choice
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"Anda mengganti ke - {vote_choice}.")
    else:
        user_votes[user_id] = vote_choice
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"Terima kasih atas suaranya! Anda memilih - {vote_choice}.")
        if not voting_started:
            voting_started = True
            threading.Thread(target=display_votes).start()

def display_votes():
    while True:
        sleep(30)
        up_votes = list(user_votes.values()).count('naik')
        down_votes = list(user_votes.values()).count('turun')
        timeKU.adjust_temp(up_votes,down_votes)
        print('votes naik = ',up_votes,'\nvotes turun = ',down_votes)
        send_notif(get_suhu(4))

def send_notif(suhu_now):
    global user_votes
    for user_id in user_votes.keys():
        bot.send_message(user_id, f"Suhu saat ini: {suhu_now}")

# Menjalankan bot
def run_telebot():
    bot.polling()