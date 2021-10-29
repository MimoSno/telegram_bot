import sqlite3

TOKEN = 'Enter your Token Here'

connect = sqlite3.connect('users.db')  # Подключение базы данных
cursor = connect.cursor()  # Взаимодействие с базой данных
