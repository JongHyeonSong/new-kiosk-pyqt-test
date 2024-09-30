# PySide에서의 스레드 구현
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QThread, SIGNAL
import time

class Worker(QThread):
    def __init__(self, proc):
        super().__init__()
        self.proc = proc

    def run(self):
        count = 0
        for i in range(0, 100):
            count += 1
            # windoww 클래스에서 넘겨받은 함수를 수신부로 지정하고 값을 송신한다.
            self.emit(SIGNAL(self.proc(count)))
            time.sleep(1)

class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        # 스레드 클래수에 수신 함수를 넘겨준다.
        self.worker = Worker(self.proc)
        self.worker.start()

    def proc(self, count):
        print(count)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()

    myWindow.show()
    sys.exit(app.exec())