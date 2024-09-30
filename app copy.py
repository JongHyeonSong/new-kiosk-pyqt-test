import sys
import signal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QMainWindow, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QSize, QDir

import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebView and MP4 Player")
        # alway top
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint |  Qt.WindowStaysOnTopHint)

        # Set initial size to half of the screen size
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(screen.width() // 2, screen.height() // 2)

        # Create a central widget and set layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Create a horizontal layout for the top bar
        top_bar_layout = QHBoxLayout()

        # Create a URL input line edit
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL and press Enter")
        self.url_input.returnPressed.connect(self.load_url)

        # Create a close button
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(QSize(30, 30))
        self.close_button.clicked.connect(self.close)

        # Add URL input and close button to the top bar layout
        top_bar_layout.addWidget(self.url_input)
        top_bar_layout.addWidget(self.close_button)

        # Create a WebView
        self.webview = QWebEngineView()

        # Create a video player
        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)

        # Create a button to play the MP4 file
        self.play_button = QPushButton("Play MP4")
        self.play_button.clicked.connect(self.play_mp4)

        # Add widgets to the layout
        layout.addLayout(top_bar_layout)
        layout.addWidget(self.webview)
        layout.addWidget(self.video_widget)
        layout.addWidget(self.play_button)


        self.setCentralWidget(central_widget)

    def load_url(self):
        url = self.url_input.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.webview.setUrl(QUrl(url))

    def play_mp4(self):
        # mp4_file = __name__ + './vi.mp4'  # Replace with your MP4 file path
        mp4_file = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'  # Replace with your MP4 file path
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(mp4_file)))
        self.media_player.play()
        # filePathf = QDir.currentPath()
        # m_player = new QMediaPlayer(this)
        # m_playlist = new QMediaPlaylist(m_player)

        # m_player->setPlaylist(m_playlist)
        # m_playlist->addMedia(QUrl::fromLocalFile(filePath + "/sound/HH.wav"));

        # m_player->play();

signal.signal(signal.SIGINT, signal.SIG_DFL)


mp4_file = os.getcwd() + '\\vi.mp4'  # Replace with your MP4 file path
print(mp4_file)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
# window.raise_()
window.activateWindow()
sys.exit(app.exec_())
