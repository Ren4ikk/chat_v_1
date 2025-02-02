# клиент
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import socket
import threading
import sys

HOST = ('178.20.45.76', 20000)


class Client(QMainWindow):
    def setup_ui(self):
        self.resize(900, 600)

        # Центральный виджет
        self.central_wdg = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_wdg)

        # Сплиттер для списка чатов и окна сообщений
        self.splitter = QtWidgets.QSplitter(self.central_wdg)
        self.splitter.setGeometry(QtCore.QRect(10, 10, 880, 580))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        # Список всех чатов (не используется, но оставлен для будущих улучшений)
        self.chats_list = QtWidgets.QListView(self.splitter)

        # Виджет открытого чата
        self.opened_chat = QtWidgets.QWidget(self.splitter)
        self.opened_chat.setGeometry(QtCore.QRect(0, 0, 631, 441))

        self.opened_chat_Layout_wdg = QtWidgets.QWidget(self.opened_chat)
        self.opened_chat_Layout_wdg.setGeometry(QtCore.QRect(0, 0, 631, 441))

        self.opened_chat_Layout = QtWidgets.QVBoxLayout(self.opened_chat_Layout_wdg)
        self.opened_chat_Layout.setContentsMargins(0, 0, 0, 0)

        # Список сообщений чата
        self.opened_chat_messages_list = QtWidgets.QListWidget()
        self.opened_chat_Layout.addWidget(self.opened_chat_messages_list)

        # Виджет ввода сообщения
        self.messsage_Layout_wdg = QtWidgets.QWidget(self.opened_chat)
        self.messsage_Layout_wdg.setGeometry(QtCore.QRect(0, 460, 631, 89))

        self.messsage_Layout = QtWidgets.QHBoxLayout(self.messsage_Layout_wdg)
        self.messsage_Layout.setContentsMargins(0, 0, 0, 0)

        self.message = QtWidgets.QTextEdit()
        self.messsage_Layout.addWidget(self.message)

        self.send_msg_btn = QtWidgets.QPushButton()
        self.send_msg_btn.setText('Send')
        self.messsage_Layout.addWidget(self.send_msg_btn)

        self.create_client()
        self.connect_signals()

    def create_client(self):
        """Создание сокета и подключение к серверу"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(HOST)

        # Запуск потока для получения сообщений от сервера
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def connect_signals(self):
        self.send_msg_btn.clicked.connect(self.send_message)

    def send_message(self):
        """Отправка сообщения серверу"""
        message_text = self.message.toPlainText().strip()
        if message_text:
            self.client_socket.sendall(message_text.encode())
            self.opened_chat_messages_list.addItem(f"Вы: {message_text}")
            self.message.clear()

    def receive_messages(self):
        """Получение сообщений от сервера"""
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.opened_chat_messages_list.addItem(f"Другой клиент: {message}")
            except:
                break


app = QtWidgets.QApplication(sys.argv)
client_app = Client()
client_app.setup_ui()
client_app.show()
sys.exit(app.exec_())
