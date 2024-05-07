import telebot
from telebot import types
import netifaces as ni
from webserver import app
import key
import schedule

# Token bot Telegram

TOKEN = key.TOKEN

# Inisialisasi dictionary untuk menyimpan suara pengguna
user_votes = {}
total_naik_votes = 0
total_turun_votes = 0

ipaddr = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

def botrun(time_end,jUser):
    print(time_end,jUser)

def voting():
    for user_id, vote_choice in user_votes.items():
        if vote_choice == 'Naik +1':
            total_naik_votes += 1
        elif vote_choice == 'Turun -1':
            total_turun_votes += 1
    print(f"Total suara 'naik': {total_naik_votes}")
    print(f"Total suara 'turun': {total_turun_votes}")


# Inisialisasi bot
bot = telebot.TeleBot(TOKEN)

# Menangani perintah /start
@bot.message_handler(commands=['startnew'])
def start(message):
    bot.reply_to(message, 'Halo! Silakan berikan informasi tentang acara kamu.')

@bot.message_handler(commands=['start'])
def startuser(message):
    bot.reply_to(message, 'Berikut Website Monitoring \nhttp://'+ipaddr+':5000\nSilakan menggunakan Menu Dibawah ini \nuntuk Voting.\n👇👇👇👇')

# Dekorator untuk menangani perintah `/vote`
@bot.message_handler(commands=['vote'])
def vote(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Periksa apakah pengguna sudah pernah memberikan suara
    if user_id in user_votes:
        bot.reply_to(message, "Anda sudah memberikan suara. Terima kasih!")
        return

    # Tampilkan opsi voting
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Naik +1', callback_data='vote_naik'), 
                 types.InlineKeyboardButton('Turun -1', callback_data='vote_turun'))

    # Kirim pesan dengan keyboard untuk memilih opsi
    bot.send_message(chat_id, "Bagaimana suhu akan diset?", reply_markup=keyboard)

    # Simpan ID pengguna dan pilihannya dalam dictionary
    user_votes[user_id] = None

# Dekorator untuk menangani balasan pesan voting
@bot.message_handler(func=lambda call: call.data in ['vote_naik', 'vote_turun'])
def process_vote(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    vote_choice = call.data.split('_')[1]

    # Perbarui dictionary dengan pilihan pengguna
    user_votes[user_id] = vote_choice

    # Berikan konfirmasi atas suara pengguna
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    bot.reply_to(message, f"Terima kasih atas suaranya! Anda memilih {vote_choice}.")


# Menangani pesan yang berisi waktu selesai acara
@bot.message_handler(func=lambda message: True)
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

# Menjalankan bot
schedule.every(10).seconds.do(voting)

# def run_telebot():
#     while True:
#         bot.polling()
        # schedule.run_pending()

while True:
    bot.polling()
    schedule.run_pending()