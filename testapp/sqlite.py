import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3
print(sqlite3.version) # 모듈의 버전 2.6.0
print(sqlite3.sqlite_version) # sqlite의 버전
import asyncio

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.bt1 = QPushButton('Create Table1', self)
        self.bt1.clicked.connect(self.createTable1)

        self.bt2 = QPushButton('Create Table2', self)
        self.bt2.clicked.connect(self.createTable2)
        self.bt2.move(150, 150)

        self.move(1920*2, 0)
        self.setWindowTitle('Simple QTableWidget')
        self.show()

    def selectAll(self):
        con = sqlite3.connect('sql.sqlite')

    def slowQry(self):
        con = sqlite3.connect('sql.sqlite')

        slow_num = 4300001
        query = f'''
            WITH RECURSIVE delay(n) AS (
                SELECT 1
                UNION ALL
                SELECT n + 1 FROM delay WHERE n < {slow_num}  
            )
            SELECT * FROM delay WHERE n = {slow_num};
        '''
        print(query)
        return
        cursor = con.cursor()

        try:
            cursor.execute(query)

            for row in cursor.fetchall():
                print(row)

            con.commit()

        except sqlite3.OperationalError as e:
            print(e)

        con.close()


    def createTable1(self):

        self.slowQry()
        return
        con = sqlite3.connect('sql.sqlite')
        print(type(con))
                
        cursor = con.cursor()
        # cursor.execute("INSERT INTO alarm VALUES ('SUN', '12:25','교육학개론', 19230435, 0920, 0)")

        try:
            cursor.fetchall()
            # cursor.execute("SELECT * FROM alarm")
            con.commit()

            for row in cursor.execute('SELECT * FROM table1'):
                print(row)
                print(row[0])

            con.commit()
            con.close()
        except sqlite3.OperationalError as e:
            print(e)

        
    def createTable2(self):
        self.queryManaer.selectAll("select * from table", self.hook1)


class SqlManagerThread(QThread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()
        self.loop.run_forever()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())