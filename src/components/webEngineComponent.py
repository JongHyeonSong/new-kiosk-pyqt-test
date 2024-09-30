import os

from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class WebEngineComponent(QWebEngineView):
    def __init__(self, initUrl = "https://soland.co.kr", parent=None):
        super().__init__(parent)
        self.initUrl = initUrl
        self.setPage(self.getWebPage())

    def getWebPage(self):
        self.webPage = CustomWebEnginePage()

        # 콘솔 받기 window.console.log("heoolo !!"); --> (0, 'heoolo !!', 130, 'http://127.0.0.1:8080/scheme.html')
        # web_page.javaScriptConsoleMessage = lambda *li: print(li)
        self.webPage.javaScriptConsoleMessage = self.handleConsoleMessage

        if(os.getenv("DISABLE_WEB_CACHE") == "Y"):
            self.webPage.profile().setHttpCacheType(QWebEngineProfile.NoCache)
        
        # scheme 처리
        self.webPage.customUrlSignal.connect(lambda: self.close())
        self.setPage(self.webPage)

        # self.webEngineView.setUrl(QUrl(url))  # Replace with your URL
        self.replaceUrl(self.initUrl)
        return self.webPage
    
    def replaceUrl(self, url: str):
        # 처음 webview의 url값은 "" 공백이다 None이 아니라
        
        currFullUrl = self.url().url()
        # print('gogo',url)
        # print('gogo',self.url().host())
        # print('gogo',self.url().url())
        if (currFullUrl != "" and currFullUrl == url):
            # print("같음")
            pass
        else:
            # print("다름")
            self.load(QUrl(url))  # Replace with your URL
    
    def handleConsoleMessage(self, level, message, lineNumber, sourceID):
        # print(f"Console: {message} (line: {lineNumber}, source: {sourceID})")
        pass

class CustomWebEnginePage(QWebEnginePage):
    customUrlSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # 짓시등 getUserMedia() 같은거 할때 호출된다
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
        # location.href = "closewebview://?";
        print(url.toString()) # 전체 URL 
        print(url.url()) # 전체 URL
        print(url.scheme()) # 프로토콜
        print(url.host()) # 호스트도메인

        if(url.scheme() == "closewebview"):
            self.view().close() #일단 웹뷰엔진을 먼저 끄고고
            self.customUrlSignal.emit()  # 시그널을 부모한테 날려서 Dialog 끄기
            return False  # Prevent the navigation

        if url.scheme() == 'scheme':
            fullUrl = url.toString()
            print(fullUrl)
            myQuery = url.query() #closeme=true&a=1&b=2
            parsedQuery = dict() if not myQuery else dict(myQuery.split('=') for myQuery in myQuery.split('&'))
            print(parsedQuery)

            if(parsedQuery.get("closeWebview") == "Y"):
                # isInst = isinstance(self.view(), WebViewDialog) 이코드 어디쓸지모르겠음 false나옴
                self.view().close() #일단 웹뷰엔진을 먼저 끄고고
                self.customUrlSignal.emit()  # 시그널을 부모한테 날려서 Dialog 끄기
                return False  # Prevent the navigation
        return super().acceptNavigationRequest(url, _type, isMainFrame)


