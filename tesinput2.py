import telebot
import netifaces as ni
from webserver import app

# Token bot Telegram
TOKEN = "6943286641:AAGk9SKix3nTPLphMD2Bj_8Y6SGAdIgPdBk"

ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
ipaddr = ip


def botrun(time_end,jUser):
    print(time_end,jUser)

# def voting():


# Inisialisasi bot
bot = telebot.TeleBot(TOKEN)

# Menangani perintah /start
@bot.message_handler(commands=['startnew'])
def start(message):
    bot.reply_to(message, 'Halo! Silakan berikan informasi tentang acara kamu.')

@bot.message_handler(commands=['start'])
def startuser(message):
    bot.reply_to(message, 'Berikut Website Monitoring \nhttps://'+ipaddr+':5000\nSilakan menggunakan Menu Dibawah ini \nuntuk Voting.\n👇👇👇👇')

@bot.message_handler(commands=['naiksuhu'])
def startuser(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Suhu +1', callback_data='pilihan1'))
    markup.add(telebot.types.InlineKeyboardButton(text='Suhu -1', callback_data='pilihan2'))
    bot.send_message(message.chat.id, "Silakan pilih opsi:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'pilihan1':
        bot.send_message(call.message.chat.id, 'Suhu akan akan diproses')
    elif call.data == 'pilihan2':
        bot.send_message(call.message.chat.id, 'Suhu akan segera diproses')

# Menangani pesan yang berisi waktu selesai acara
@bot.message_handler(func=lambda message: True)
def end_time(message):
    bot.reply_to(message, f'Waktu selesai acara telah diset pada pukul {message.text}. Sekarang, berapa jumlah pengguna yang akan hadir?')
    global time_end
    time_end = message.text
    print(time_end)
    bot.register_next_step_handler(message, num_users)

# Menangani pesan yang berisi jumlah pengguna
def num_users(message):
    jUser = message.text
    print(jUser)
    bot.reply_to(message, f'Akan dihadiri oleh {message.text} pengguna.')
    botrun(time_end,jUser)

# Menjalankan bot
bot.polling()
app()
