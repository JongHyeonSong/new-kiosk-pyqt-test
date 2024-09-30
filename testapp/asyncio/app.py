import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from testapp.asyncio.managers import SqlManager
from managers import *
import json
# from testapp.asyncio.chatWidget import ChatWidget
from chatWidget import ChatWidget
from qPu import MyQpush

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.sqlManager = SqlManager()
        self.apiManager = ApiManager()

    def initUI(self):
        self.move(1920 *2, 0)
        self.resize(500,500)
        self.setWindowTitle('Asyncio')

        self.btn1 = QPushButton('query', self)
        self.btn2 = QPushButton('apiaa', self)


        self.layout = QVBoxLayout()

        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.btn2)

        self.setLayout(self.layout)

        self.chatWidget = ChatWidget()
        print(self.chatWidget)
        self.layout.addWidget(self.chatWidget)



        p1 = MyQpush()
        p2 = MyQpush()
        self.layout.addWidget(p1)
        self.layout.addWidget(p2)

        p1.clicked.connect(lambda x:print('p1'))
        p2.clicked.connect(lambda x:print('p2'))

        self.btn2.move(150, 150)
        self.btn1.clicked.connect(self.query)
        self.btn2.clicked.connect(self.api)
        self.show()
    
    def query(self):
        sql = "select * from table1fw where namffe='name1'"
        # sql = "select * from table1 where name='name1'"

        slow_num = 4300001
        query = f'''
            WITH RECURSIVE delay(n) AS (
                SELECT 1
                UNION ALL
                SELECT n + 1 FROM delay WHERE n < {slow_num}  
            )
            SELECT * FROM delay WHERE n = {slow_num};
        '''
        self.sqlManager.select_list(query, lambda x: print('go', x))

    def api(self):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        # url = "http://sjhtest.musicen.com/ping/delay/1"
        # url = "http://sjhtest.musicen.com/ping/delayErr/0"
        self.apiManager.get_request(url, lambda x: print('goo', x))


        print('api')
    def api2(self):
        url = "http://sjhtest.musicen.com/ping/same/1"

        # dict = {
        #     "method": "POST",
        #     "headers": { "content-type": "application/json" },
        #     "body": json.dumps({ "a": 1, "b": 2 }),
        # }
        dict = json.dumps({ "a": 1, "b": 2 })

        self.apiManager.post_request_json(
            url=url,
            cb= lambda x: print('goo', x) ,
            data = { "a": 1, "b": 2 },
         )

     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWidget()
    sys.exit(app.exec_())