"""
Гуи для отображения диалога
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit, QPushButton, QHBoxLayout


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Чат с прокруткой')
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout(self)

        # Область прокрутки
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Контейнер для сообщений
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.addStretch(1)  # Чтобы сообщения сжимались к верху

        self.scroll_area.setWidget(self.messages_container)
        self.layout.addWidget(self.scroll_area)

        # Поле ввода и кнопка отправки
        self.input_layout = QHBoxLayout()
        self.message_input = QLineEdit(self)
        self.send_button = QPushButton("Отправить", self)
        self.send_button.clicked.connect(self.add_message)

        self.input_layout.addWidget(self.message_input)
        self.input_layout.addWidget(self.send_button)

        self.layout.addLayout(self.input_layout)

    def add_message(self):
        text = self.message_input.text().strip()
        if text:
            message_label = QLabel(text, self)
            message_label.setWordWrap(True)

            # Стилизация "пузыря" сообщения
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #DCF8C6;
                    border: 1px solid #34B7F1;
                    border-radius: 10px;
                    padding: 8px;
                    margin: 5px;
                    font-size: 14px;
                }
            """)

            # Добавляем сообщение и прокручиваем вниз
            self.messages_layout.insertWidget(self.messages_layout.count() - 1, message_label)
            self.message_input.clear()

            # Прокрутка к последнему сообщению
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
