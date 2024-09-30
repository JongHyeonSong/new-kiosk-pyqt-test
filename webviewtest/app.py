import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QUrl, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from PyQt5.Qt import *
import debugpy
import time

class VideoCaptureThread(QThread):
    frame_changed = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(0)  # Open the first camera
        # check camera is possible
        print(self.capture.isOpened())
        print(self.capture.isOpened())
        # if not self.capture.isOpened():
        #     print("Cannot open camera")
        #     exit()
        self.running = True

    def run(self):
        # debugpy.debug_this_thread()
        print(123123)
        while self.running:
            print(3333333333331231233)

            try:
                ret, frame = self.capture.read()
                # time.sleep(0.3)
                # QTest.qWait(5000)
                if not ret:
                    continue
                self.frame_changed.emit(frame)
                
                # 
            except Exception as e:
                print(e) 
    def stop(self):
        self.capture.release()
        self.quit()

    def restart(self):
        print(123123)
        self.stop()
        self.capture = cv2.VideoCapture(0)
        self.running = True
        self.start()

class CustomWebEnginePage(QWebEnginePage):
    custom_url_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)
    def onFeaturePermissionRequested(self, url, feature):
        if feature in (QWebEnginePage.MediaAudioCapture,
                       QWebEnginePage.MediaVideoCapture,
                       QWebEnginePage.MediaAudioVideoCapture):
            self.setFeaturePermission(
                url, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            self.setFeaturePermission(
                url, feature, QWebEnginePage.PermissionDeniedByUser)

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if url.scheme() == 'scheme':
            fullUrl = url.toString()
            myQuery = url.query() #closeme=true&a=1&b=2
            parsedQuery = dict() if not myQuery else dict(myQuery.split('=') for myQuery in myQuery.split('&'))
            print(parsedQuery)

            if(parsedQuery.get("closeWebview") == "Y"):

                isInst = isinstance(self.view(), WebViewDialog)
                print(isInst)
                self.custom_url_signal.emit()  # Emit the signal


                if isInst:
                    print("WO22")

                    self.view().close()
                return False  # Prevent the navigation
        return super().acceptNavigationRequest(url, _type, isMainFrame)

class WebViewDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebView")
        self.setGeometry(100, 100, 1024, 768)

        self.web_view = QWebEngineView()
        self.web_page = CustomWebEnginePage(self)

        self.web_page.custom_url_signal.connect(self.closeDialog)
        
        self.web_view.setPage(self.web_page)
        self.web_view.setUrl(QUrl("http://127.0.0.1:5500/webviewtest/index.html"))  # Replace with your URL

        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def closeDialog(self):
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Feed")
        self.setGeometry(100, 100, 640, 480)

        self.video_frame = QLabel()
        self.open_webview_button = QPushButton("Open Web View")
        self.open_webview_button2 = QPushButton("Open Web View2")

        self.enable_cam = QPushButton("enable cam")
        self.disable_cam = QPushButton("disable cam")

        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        layout.addWidget(self.open_webview_button)
        layout.addWidget(self.open_webview_button2)
        layout.addWidget(self.enable_cam)
        layout.addWidget(self.disable_cam)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.capture_thread = VideoCaptureThread()
        self.capture_thread.frame_changed.connect(self.update_frame)
        self.capture_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.open_webview_button.clicked.connect(self.open_web_view)
        self.open_webview_button.clicked.connect(self.deall)

        self.enable_cam.clicked.connect(self.enable_cam_hook)
        self.disable_cam.clicked.connect(self.disable_cam_hook)
    def enable_cam_hook(self):
        print(1)
    def disable_cam_hook(self):
        print(2)
    def deall(self):
        if self.webview:
            self.webview.closeDialog()
        else:
            print("no webview")
    def update_frame(self, frame=None):
        if frame is None:
            return
        
        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to QImage
        height, width, channels = frame.shape
        bytes_per_line = channels * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Update QLabel with the QImage
        self.video_frame.setPixmap(QPixmap.fromImage(q_image))

    def open_web_view(self):
        self.capture_thread.stop()  # Release the camera
        self.webview = WebViewDialog()

        self.webview.finished.connect(self.webview_dialog_closed)
        self.webview.exec_()
        print("IM CLOSED")

    @pyqtSlot()
    def webview_dialog_closed(self):
        print("IM CLOSED")
        self.capture_thread.restart()  # Restart the camera feed

    # def webview_dialog_closed(self):
    #     # restart the camera
    #     a=3
    def closeEvent(self, event):
        self.capture_thread.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
