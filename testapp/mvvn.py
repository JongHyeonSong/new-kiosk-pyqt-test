import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import aiohttp

class AsyncAPIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Async API Call with PyQt5')

        # Create widgets
        self.button = QPushButton('Make API Call', self)
        self.result_label = QLabel('Result will appear here', self)

        # Connect button click to the handler
        self.button.clicked.connect(self.on_button_clicked)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setGeometry(300, 300, 300, 200)

    def on_button_clicked(self):
        # Create a task for the async function
        asyncio.create_task(self.fetch_data())

    async def fetch_data(self):
        url = 'http://sjhtest.musicen.com/ping/delay/1'  # Replace with your API endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                result = str(data)  # Process your response as needed
                # Schedule the UI update in the PyQt event loop
                self.update_ui(result)

    def update_ui(self, result):
        # Update the label with the result
        self.result_label.setText(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Get the PyQt event loop
    loop = asyncio.get_event_loop()

    # Ensure the PyQt event loop and asyncio event loop are running together
    asyncio.ensure_future(loop.run_in_executor(None, app.exec_))
    
    mainWin = AsyncAPIApp()
    mainWin.show()
    
    sys.exit(app.exec_())
