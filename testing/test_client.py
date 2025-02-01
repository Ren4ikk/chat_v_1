import socket
from client_gui import Client
from PyQt5 import QtWidgets
import sys


# открываем приложение
app = QtWidgets.QApplication(sys.argv)
client_app = Client()
client_app.setup_ui()
client_app.show()

HOST = ('178.20.45.76', 20_000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# от созданного клиентского сокета коннектимся к созданному серверу
client.connect(HOST)

# метод recv поможет нам получить какие-то данные от сервера
# 1024 это размер временного буфера для хранения двоичного значения (данных от сервера) в количестве байт
msg = client.recv(1024)
client_app.opened_chat_messages_list.addItem(msg.decode('utf-8'))

sys.exit(app.exec_())
