import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
import PyQt6.QtGui as QtGui

from processor.grab import pull

class FetchWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal(bytes)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def run(self):
        response, _ = pull.pull_raw(self.url)
        self.finished.emit(response)

class Home(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.draw_tab_strip()
        self.thread = QtCore.QThread()
        self.thread.start()

    def load_url(self):
        url = self.search_bar.text()
        if url:
            self.content_view.setText("Loading...")
            self.worker = FetchWorker(url)
            self.worker.moveToThread(self.thread)
            self.worker.finished.connect(self.display_response)
            self.worker.start()

    def display_response(self, response):
        self.content_view.setText(response.decode("utf-8", errors="ignore"))

    def go_home(self):
        self.search_bar.setText("")
        self.content_view.setText("")

    def draw_tab_strip(self):
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        left_bar = QtWidgets.QWidget()
        left_bar.setFixedWidth(200)
        left_bar.setStyleSheet("background-color: #2b2b2b;")
        
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setStyleSheet("background-color: #3c3c3c; color: white;")
        self.search_bar.returnPressed.connect(self.load_url)

        self.back_button = QtWidgets.QPushButton("^")
        self.back_button.setStyleSheet("background-color: #3c3c3c; color: white;")

        self.refresh_button = QtWidgets.QPushButton("↻")
        self.refresh_button.setStyleSheet("background-color: #3c3c3c; color: white;")

        self.forward_button = QtWidgets.QPushButton(">")
        self.forward_button.setStyleSheet("background-color: #3c3c3c; color: white;")


        self.tab_bar = QtWidgets.QListWidget()
        self.tab_bar.setLayout(QtWidgets.QVBoxLayout())
        self.tab_bar.layout().addWidget(self.search_bar)
        self.tab_bar.layout().addWidget(self.back_button)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.tab_bar)
        self.button_strip = QtWidgets.QHBoxLayout()
        self.button_strip.addWidget(self.back_button)
        self.button_strip.addWidget(self.refresh_button)
        self.button_strip.addWidget(self.forward_button)
        left_layout.addLayout(self.button_strip)
        left_bar.setLayout(left_layout)

        self.content_view = QtWidgets.QTextEdit()
        self.content_view.setStyleSheet("background-color: #1a1a1a; color: white;")
        self.content_view.setReadOnly(True)

        main_layout.addWidget(left_bar)
        main_layout.addWidget(self.content_view)

        return main_layout

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    home = Home()
    home.show()
    app.exec()
