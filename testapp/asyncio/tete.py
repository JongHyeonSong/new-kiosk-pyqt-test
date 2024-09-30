import sys
import requests
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget

class ApiWorker(QObject):
    result_ready = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        """This function will be executed in a separate thread."""
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.result_ready.emit(response.text)  # Emit the API response text
            else:
                self.result_ready.emit(f"Error: {response.status_code}")
        except Exception as e:
            self.result_ready.emit(f"Exception: {str(e)}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up UI
        self.label = QLabel("Press the button to start API request", self)
        self.button = QPushButton("Make API Request", self)
        self.button.clicked.connect(self.start_api_request)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Create a reusable thread
        self.thread = QThread()
        self.worker = None

    def start_api_request(self):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        self.label.setText("Making API request...")

        # If a worker is already assigned to the thread, delete it
        if self.worker is not None:
            self.worker.deleteLater()

        # Create a new worker object
        self.worker = ApiWorker(url)
        
        # Move the worker to the reusable thread
        self.worker.moveToThread(self.thread)
        
        # Disconnect the previous signal connection if it exists
        try:
            self.thread.started.disconnect()
            self.worker.result_ready.disconnect()
        except TypeError:
            pass  # No previous connections, so just continue
        
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.result_ready.connect(self.on_result)
        
        # Start the thread only if it's not already running
        if not self.thread.isRunning():
            self.thread.start()

    def on_result(self, result):
        print("GGO")
        """Handle the result from the API request."""
        self.label.setText(result)
        
        # After result is received, stop the thread if there are no more tasks
        self.thread.quit()
        self.thread.wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
