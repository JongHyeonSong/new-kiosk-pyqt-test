import sys
import os

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import util

import shutil
from util.globalSignal import GlobalSignalProxy

class MediaWidget(QVideoWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # self.setAspectRatioMode(Qt.IgnoreAspectRatio)

        self.initMediaPlayer()

    def initMediaPlayer(self):
        self.mediaIter = self.medialFilePathGenerator()
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChanged)

        self.mediaPlayer.setVideoOutput(self)
        self.mediaPlayer.setMuted(True)
        self.playNextMedia()

    def relseVideoAndCopyMediaAAA(self):
        self.releaseResources()
        self.copyMedia()
        self.playNextMedia(reloadMediaIter=True)

    def releaseResources(self):
        """Stop the player and release resources."""
        self.mediaPlayer.stop()   # Stop the current video
        self.mediaPlayer.setMedia(QMediaContent())  # Release media resource   

    def copyMedia(self):
        remoteFolder = util.resource_path("test")
        targetFolder = util.resource_path("media")

        # remove all files in media and copy all files in remoteFolder to media
        for file in os.listdir(targetFolder):
            os.remove(os.path.join(targetFolder, file))
        for file in os.listdir(remoteFolder):
            shutil.copy(os.path.join(remoteFolder, file), targetFolder)

    def playNextMedia(self, reloadMediaIter=False):
        if reloadMediaIter:
            self.mediaIter = self.medialFilePathGenerator()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(next(self.mediaIter))))
        self.mediaPlayer.play() 

    def medialFilePathGenerator(self):
        mediaFolder = util.resource_path("media")
        print('mediaFolder', mediaFolder)

        mp4_files = [f for f in os.listdir(mediaFolder) if f.lower().endswith('.mp4')]
        # mp4_files.sort()  # 파일 이름 순으로 정렬

        if len(mp4_files) == 0:
            return 

        while True:
            for file in mp4_files:
                full_path = os.path.join(mediaFolder, file)
                yield full_path
                
    # 영상 상태 변경 이벤트 처리
    def handleMediaStatusChanged(self, status):
        # 2 -> 6 -> 7 -> 3 ->6
        # print(QMediaPlayer.MediaStatus.UnknownMediaStatus) #0
        # print(QMediaPlayer.MediaStatus.NoMedia) #1
        # print(QMediaPlayer.MediaStatus.LoadingMedia) #2
        # print(QMediaPlayer.MediaStatus.LoadedMedia) #3
        # print(QMediaPlayer.MediaStatus.StalledMedia) #4
        # print(QMediaPlayer.MediaStatus.BufferingMedia) #5
        # print(QMediaPlayer.MediaStatus.BufferedMedia) #6
        # print(QMediaPlayer.MediaStatus.EndOfMedia) #7
        # print(QMediaPlayer.MediaStatus.InvalidMedia) #8


        # 어떤 이유로든지 파일 IO가 깨지면 다시 재생하기
        if(status == QMediaPlayer.InvalidMedia):
            self.mediaIter = self.medialFilePathGenerator()
            self.playNextMedia()

        if status == QMediaPlayer.EndOfMedia:
            self.playNextMedia()
            # self.mediaPlayer.setPosition(0)
            # self.mediaPlayer.play()
