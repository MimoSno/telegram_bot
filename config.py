import sqlite3

TOKEN = '1831036657:AAFE-Ndi0H0NiNgkWQBo6e1w3wP55WPwgFI'

connect = sqlite3.connect('users.db')  # Подключение базы данных
cursor = connect.cursor()  # Взаимодействие с базой данных
