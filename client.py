# Исправленный код клиента
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
import socket
import threading
import sys

HOST = ('178.20.45.76', 20000)


class Client(QMainWindow):
    new_message_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.resize(900, 600)

        # Центральный виджет
        self.central_wdg = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_wdg)

        # Сплиттер для списка чатов и окна сообщений
        self.splitter = QtWidgets.QSplitter(self.central_wdg)
        self.splitter.setGeometry(QtCore.QRect(10, 10, 880, 580))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        # Список всех чатов
        self.chats_list = QtWidgets.QListView(self.splitter)

        # Виджет открытого чата
        self.opened_chat = QtWidgets.QWidget(self.splitter)
        self.opened_chat_layout = QtWidgets.QVBoxLayout(self.opened_chat)
        self.opened_chat_layout.setContentsMargins(0, 0, 0, 0)

        # Область прокрутки для сообщений
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.addStretch(1)
        self.scroll_area.setWidget(self.messages_container)

        # Виджет для ввода сообщений
        self.message_layout = QtWidgets.QHBoxLayout()
        self.message_input = QtWidgets.QLineEdit()
        self.send_msg_btn = QtWidgets.QPushButton("Отправить")

        self.message_layout.addWidget(self.message_input)
        self.message_layout.addWidget(self.send_msg_btn)

        self.opened_chat_layout.addWidget(self.scroll_area)
        self.opened_chat_layout.addLayout(self.message_layout)

        # устанавливаем размеры по умочланию правой и левой частей сплиттера
        self.splitter.setSizes([200, 680])

        self.connect_signals()
        self.create_client()

    def connect_signals(self):
        self.new_message_signal.connect(self.show_message)
        self.send_msg_btn.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)

    def create_client(self):
        """Создание сокета и подключение к серверу"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(HOST)
            # Запуск потока для получения сообщений от сервера
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
        except Exception as e:
            self.show_message(f"Ошибка подключения к серверу: {e}", is_author=True)

    def send_message(self):
        """Отправка сообщения серверу"""
        message_text = self.message_input.text().strip()
        if message_text:
            try:
                self.client_socket.sendall(message_text.encode())
                self.show_message(message_text, is_author=True)
                self.message_input.clear()
            except Exception as e:
                self.show_message(f"Ошибка отправки сообщения: {e}", is_author=True)

    def receive_messages(self):
        """Получение сообщений от сервера"""
        buffer = ""  # Буфер для хранения данных, если сообщение пришло не полностью
        while True:
            try:
                data = self.client_socket.recv(1024).decode()  # Получаем данные от сервера (максимум 1024 байта)
                if not data:
                    break  # Если данных нет, значит соединение закрыто, выходим из цикла
                buffer += data  # Добавляем полученные данные в буфер

                while '\n' in buffer:  # Проверяем, есть ли завершенные сообщения (разделённые символом новой строки '\n')
                    message, buffer = buffer.split('\n', 1)
                    # Делим буфер на сообщение и остаток:
                    # message - полное сообщение до '\n'
                    # buffer - оставшиеся данные после '\n' (могут быть частью следующего сообщения)

                    self.new_message_signal.emit(message)
                    # Посылаем сигнал для отображения сообщения в интерфейсе
            except:
                self.new_message_signal.emit("Отключение от сервера.")
                # В случае ошибки соединения выводим сообщение об ошибке
                break

    def show_message(self, text, is_author=False):
        """Отображение сообщения в чате с выравниванием пузырьков"""

        # Создаём контейнер для каждого сообщения
        message_container = QtWidgets.QWidget()
        message_layout = QtWidgets.QHBoxLayout(message_container)
        message_layout.setContentsMargins(0, 0, 0, 0)

        # Создаём сам пузырёк сообщения
        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(400)
        message_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)

        # Стилизация сообщения
        if is_author:
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #DCF8C6;  /* Светло-зелёный фон для сообщений автора */
                    border: 1px solid #34B7F1;
                    border-radius: 10px;
                    padding: 8px;
                    margin: 5px;
                    font-size: 14px;
                }
            """)
            # Spacer слева для выравнивания вправо
            message_layout.addStretch()
            message_layout.addWidget(message_label)
        else:
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #FFFFFF;  /* Белый фон для сообщений собеседника */
                    border: 1px solid #34B7F1;
                    border-radius: 10px;
                    padding: 8px;
                    margin: 5px;
                    font-size: 14px;
                }
            """)
            # Spacer справа для выравнивания влево
            message_layout.addWidget(message_label)
            message_layout.addStretch()

        # Добавляем контейнер с сообщением в общий layout
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, message_container)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())


app = QtWidgets.QApplication(sys.argv)
client_app = Client()
client_app.show()
sys.exit(app.exec_())
