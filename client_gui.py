from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Client(QMainWindow):
    def setup_ui(self):
        self.resize(900, 600)
        # self.setFixedSize(900, 600)  # Фиксируем размер окна

        # центральный виджет
        self.central_wdg = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_wdg)

        # Сплиттер, который разделяет список чата (справа) и
        # открытый чат (открыйтый диалог, поле для ввода сообщений и кнопка отправки сообщения))
        self.splitter = QtWidgets.QSplitter(self.central_wdg)
        self.splitter.setGeometry(QtCore.QRect(10, 10, 880, 580))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        # Список всех чатов
        self.chats_list = QtWidgets.QListView(self.splitter)

        # Открытый (конректный) чат
        self.opened_chat = QtWidgets.QWidget(self.splitter)
        self.opened_chat.setGeometry(QtCore.QRect(0, 0, 631, 441))


        # Виджет открытого диалога
        self.opened_chat_Layout_wdg = QtWidgets.QWidget(self.opened_chat)
        self.opened_chat_Layout_wdg.setGeometry(QtCore.QRect(0, 0, 631, 441))

        self.opened_chat_Layout = QtWidgets.QVBoxLayout(self.opened_chat_Layout_wdg)
        self.opened_chat_Layout.setContentsMargins(0, 0, 0, 0)

        # Все сообщения чата
        self.opened_chat_messages_list = QtWidgets.QListWidget()
        self.opened_chat_Layout.addWidget(self.opened_chat_messages_list)

        # Виджет (печатаемого) сообщения (поле для ввода сообщения, кнопка отправки)
        self.messsage_Layout_wdg = QtWidgets.QWidget(self.opened_chat)
        self.messsage_Layout_wdg.setGeometry(QtCore.QRect(0, 460, 631, 89))

        self.messsage_Layout = QtWidgets.QHBoxLayout(self.messsage_Layout_wdg)
        self.messsage_Layout.setContentsMargins(0, 0, 0, 0)

        self.message = QtWidgets.QTextEdit()
        self.messsage_Layout.addWidget(self.message)

        self.send_msg_btn = QtWidgets.QPushButton()
        self.send_msg_btn.setText('Send')
        self.messsage_Layout.addWidget(self.send_msg_btn)

        self.conncet_signals()

        # self.retranslateUi(MainWindow)

    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "Chat Application"))
    #     self.send_msg_btn.setText(_translate("MainWindow", "Send"))

    def conncet_signals(self):
        self.send_msg_btn.clicked.connect(self.send_message)

    def send_message(self):
        message_text = self.message.toPlainText().strip()
        if message_text:
            self.opened_chat_messages_list.addItem(message_text)
            self.message.clear()


