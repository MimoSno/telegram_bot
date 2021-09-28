
import sqlite3
import time
import telebot

from config import TOKEN, connect, cursor

bot=telebot.TeleBot(TOKEN)

from multiprocessing import *
pool = Pool(20)


def executor(fu):
    def run(*a,**kw):
        pool.apply_async(fu, a, kw, lambda result: pass, lambda error: raise error)
    return run

@bot.message_handler(commands=['start'])
@executor
def send_welcome(message):
    time.sleep(5)
    bot.reply_to(message, "Howdy, how are you doing?")

bot.polling()
