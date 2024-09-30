from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import sys
import os
import signal


class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        # Create top bar
        self.topBar = QWidget(self)
        self.topBar.setFixedHeight(40)
        self.topBar.setStyleSheet("background-color: #444;")
        self.topBarLayout = QHBoxLayout(self.topBar)
        self.topBarLayout.setContentsMargins(0, 0, 0, 0)

        # Create X button
        self.closeButton = QPushButton("X", self.topBar)
        self.closeButton.setFixedSize(40, 40)
        self.closeButton.setStyleSheet("background-color: red; color: white; border: none;")
        self.closeButton.clicked.connect(self.close)
        self.topBarLayout.addWidget(self.closeButton, alignment=Qt.AlignRight)

        # Create play/pause button
        self.playPauseButton = QPushButton("Play", self)
        self.playPauseButton.setFixedSize(100, 40)
        self.playPauseButton.setStyleSheet("background-color: #444; color: white;")
        self.playPauseButton.clicked.connect(self.playPause)

        # Create volume slider
        self.volumeSlider = QSlider(Qt.Horizontal, self)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setFixedWidth(200)
        self.volumeSlider.setStyleSheet("background-color: #444;")
        self.volumeSlider.valueChanged.connect(self.setVolume)

        videoItem = QGraphicsVideoItem()
        self.videoItem = videoItem  # Store reference for resizing
        scene = QGraphicsScene(self)
        scene.addItem(videoItem)
        self.graphicsView = QGraphicsView(scene)

        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.topBar)
        self.layout.addWidget(self.graphicsView)
        self.layout.addWidget(self.playPauseButton, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.volumeSlider, alignment=Qt.AlignLeft)
        self.setLayout(self.layout)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(videoItem)
        self.mediaPlayer.stateChanged.connect(self.handleStateChanged)
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChanged)
        self.isPlaying = False

        self.startPos = None

    def playPause(self):
        if self.isPlaying:
            self.mediaPlayer.pause()
            self.playPauseButton.setText("Play")
        else:
            self.mediaPlayer.play()
            self.playPauseButton.setText("Pause")
        self.isPlaying = not self.isPlaying

    def setVolume(self, value):
        self.mediaPlayer.setVolume(value)

    def load(self):
        # local = QUrl.fromLocalFile('./vi.mp4')
        # local = QUrl.fromLocalFile('./static/vi.mp4')
        local = QUrl.fromLocalFile(self.resource_path("vi.mp4"))
        # self.resource_path("")
        # local = QUrl.fromLocalFile()
        media = QMediaContent(local)
        self.mediaPlayer.setMedia(media)

    def handleStateChanged(self, state):
        if state == QMediaPlayer.StoppedState:
            self.mediaPlayer.play()

    def handleMediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.mediaPlayer.setPosition(0)
            self.mediaPlayer.play()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_L:
            self.load()
            self.mediaPlayer.play()
        elif e.key() == Qt.Key_P:
            self.mediaPlayer.play()
        elif e.key() == Qt.Key_Q:
            self.close()
        else:
            return

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 40:
            self.startPos = event.globalPos()
            self.clickPos = self.mapToParent(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.startPos:
            self.move(self.pos() + event.globalPos() - self.startPos)
            self.startPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.startPos = None

    def resizeEvent(self, event):
        self.videoItem.setSize(QSizeF(self.width(), self.height() - 80))
        super(VideoPlayer, self).resizeEvent(event)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path,"static", relative_path )




def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

# signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGINT, signal_handler)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    player.load()
    player.mediaPlayer.play()

    print(player.resource_path(""))
    print(player.resource_path("vi.mp4"))
    sys.exit(app.exec_())
