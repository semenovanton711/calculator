import sys
import random
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence

WORDS = ["дом", "окно", "забор", "собака", "дерево",
         "мама", "папа", "сестра", "брат", "машина"]


class SpeedTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_word = ""
        self.start_time = None
        self.test_active = False
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Скорость набора текста")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background-color: #2b2b2b;")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.word_label = QLabel("")
        self.word_label.setFont(QFont("Arial", 32))
        self.word_label.setStyleSheet("color: #6bff8a;")
        self.word_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.word_label)
        layout.addSpacing(50)

        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("background-color: #3c3c3c; color: white; font-size: 16px; padding: 8px;")
        self.input_field.returnPressed.connect(self.check)
        layout.addWidget(self.input_field)
        layout.addSpacing(20)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Старт")
        self.start_btn.setStyleSheet("background-color: #4c9aff; color: white; padding: 8px 20px;")
        self.start_btn.clicked.connect(self.start)

        reset_btn = QPushButton("Сброс")
        reset_btn.setStyleSheet("background-color: #ff6b6b; color: white; padding: 8px 20px;")
        reset_btn.clicked.connect(self.reset)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(reset_btn)
        layout.addLayout(btn_layout)
        layout.addSpacing(30)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #f0f0f0; font-size: 14px;")
        layout.addWidget(self.result_label)

        self.status_label = QLabel("Нажмите Старт")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.status_label)

        # Горячие клавиши
        self.start_btn.setShortcut("Ctrl+S")
        QShortcut("Esc", self, self.clear_input)

    def start(self):
        if self.test_active:
            return
        self.current_word = random.choice(WORDS)
        self.word_label.setText(self.current_word)
        self.input_field.clear()
        self.input_field.setEnabled(True)
        self.input_field.setFocus()
        self.start_time = time.time()
        self.test_active = True
        self.start_btn.setEnabled(False)
        self.status_label.setText(f"Введите: {self.current_word}")
        self.result_label.setText("")

    def check(self):
        if not self.test_active:
            QMessageBox.warning(self, "Ошибка", "Сначала нажмите Старт!")
            return

        user_input = self.input_field.text().strip()
        if not user_input:
            self.status_label.setText("Введите слово!")
            return

        elapsed = time.time() - self.start_time

        if user_input.lower() == self.current_word.lower():
            speed = int(len(self.current_word) / (elapsed / 60))
            self.result_label.setText(f"Скорость: {speed} знаков/мин")
            self.status_label.setText(f"Верно! Время: {elapsed:.1f} сек")
        else:
            self.status_label.setText(f"Ошибка! Было: {self.current_word}")

        self.test_active = False
        self.start_btn.setEnabled(True)

    def reset(self):
        self.test_active = False
        self.word_label.setText("")
        self.input_field.clear()
        self.input_field.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.result_label.setText("")
        self.status_label.setText("Сброшено. Нажмите Старт")

    def clear_input(self):
        self.input_field.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedTest()
    window.show()
    sys.exit(app.exec_())