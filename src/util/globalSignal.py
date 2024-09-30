from PyQt5 import QtCore

def GlobalSignalProxy():
    global GlobalSignalProxy
    if not isinstance(GlobalSignalProxy, QtCore.QObject):
        class GlobalSignalProxy(QtCore.QObject):
            signal = QtCore.pyqtSignal(object)
            changeBottomStackSignal = QtCore.pyqtSignal(int)
            webLinkSignal = QtCore.pyqtSignal(str)
        GlobalSignalProxy = GlobalSignalProxy()
    return GlobalSignalProxy