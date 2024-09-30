import sys
import os
def sum(self):
    return 'hi'



print("HIHI")
print(os.path.abspath("."))




def resource_path(relative_path):
    #  pyinstaller --noconfirm --onedir --console --add-data "./src/resources;resources/" src/app.py

    # """
    #     pyinstaller --noconfirm --onedir --console --add-data "C:\Users\user\Desktop\new-kiosk-pyqt5\resource;resource/"  "C:\Users\user\Desktop\new-kiosk-pyqt5\app.py"
    #     pyinstaller --noconfirm --onedir --console --add-data "./src/resource;resource/"  "app.py"
    # """

    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # os.path.abspath(".")
        base_path = os.path.join(os.getcwd(), "src")
    path = os.path.join(base_path, "resources", relative_path )

    # if win then replace all \\ to /
    if os.name == "nt":
        path = path.replace("\\", "/")
    return path

def server_url():
    url = os.environ.get("SERVER_URL")
    return url