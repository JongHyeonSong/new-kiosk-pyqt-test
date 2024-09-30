from PyQt5 import QtCore

def GlobalSignalProxy():
    global GlobalSignalProxy
    if not isinstance(GlobalSignalProxy, QtCore.QObject):
        class GlobalSignalProxy(QtCore.QObject):
            signal = QtCore.pyqtSignal(object)
        GlobalSignalProxy = GlobalSignalProxy()
    return GlobalSignalProxy