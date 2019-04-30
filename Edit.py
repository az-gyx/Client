import sys,pymysql
from PyQt5.QtWidgets import *
from functools import partial
from PyQt5.Qt import QWidget
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame,QApplication,QDialog, QDialogButtonBox,
        QMessageBox,QVBoxLayout, QLineEdit,QTableWidgetItem,QTableWidget,QHBoxLayout)

class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("数据库列表")
        self.resize(1000,800)


        self.setWindowIcon(QtGui.QIcon('images/tubiao.ico'))




        db = pymysql.connect(host='127.0.0.1', port=3306, user='MSF', password='1024161X', db='videos',
                             charset='utf8', )
        cur = db.cursor()
        cur.execute("select name,url,mark from video")
        data = cur.fetchall()


        col_lst = [tup[0] for tup in cur.description]
        row = len(data)
        vol = len(data[0])


        self.MyTable = QTableWidget(row,vol)
        font = QtGui.QFont('微软雅黑',10)

        self.MyTable.horizontalHeader().setFont(font)
        self.MyTable.setHorizontalHeaderLabels(col_lst)
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.setFrameShape(QFrame.NoFrame)
        self.MyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MyTable.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')

        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.MyTable.setItem(i, j, data1)

        #编辑按钮
        self.qle = QLineEdit()
        buttonBox = QDialogButtonBox()
        #增删查改四个按钮
        addButton = buttonBox.addButton("&ADD",QDialogButtonBox.ActionRole)
        okButton = buttonBox.addButton("&OK",QDialogButtonBox.ActionRole)
        deleteButton = buttonBox.addButton("&DELETE",QDialogButtonBox.ActionRole)
        inquireButton = buttonBox.addButton("&QUERY",QDialogButtonBox.ActionRole)

        #设置按钮内字体样式
        addButton.setFont(font)
        okButton.setFont(font)
        deleteButton.setFont(font)
        inquireButton.setFont(font)

        #垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.qle)
        layout.addWidget(buttonBox)
        layout.addWidget(self.MyTable)
        self.setLayout(layout)

        addButton.clicked.connect(partial(self.add_data,cur,db))#插入实现
        okButton.clicked.connect(partial(self.up_data, cur, db,col_lst))#插入实现
        deleteButton.clicked.connect(partial(self.del_data,cur,db))#删除实现
        inquireButton.clicked.connect(partial(self.inq_data,db,cur))#查询实现

    # 添加空表格
    def add_data(self, cur, db):
        # 获取行数
        row = self.MyTable.rowCount()
        # 在末尾插入一空行
        self.MyTable.insertRow(row)

    # 插入数据
    def up_data(self, cur, db, col_lst):
        row_1 = self.MyTable.rowCount()

        value_lst = []
        for i in range(len(col_lst)):
            if (len(self.MyTable.item(row_1 - 1, i).text()) == 0):
                value_lst.append(None)
            else:
                value_lst.append(self.MyTable.item(row_1 - 1, i).text())
        print(value_lst)

        tup_va_lst = []
        for cl, va in zip(col_lst, value_lst):
            tup_va_lst.append((cl, va))

        # 插入语句
        cur.execute("INSERT INTO video(name,url,mark) VALUES (%s,%s,%s)", value_lst)

        db.commit()


    # 删除
    def del_data(self, cur, db):
        # 是否删除的对话框
        reply = QMessageBox.question(self, 'Message', 'Are you sure to delete it ?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 当前行
            row_2 = self.MyTable.currentRow()
            del_d = self.MyTable.item(row_2, 0).text()

            # 在数据库删除数据
            cur.execute("DELETE FROM video WHERE name = '" + del_d + "'")
            db.commit()
            # 删除表格
            self.MyTable.removeRow(row_2)

    # 查询
    def inq_data(self, db,cur):
        txt = self.qle.text()
        # 模糊查询
        if len(txt) != 0:
            cur.execute(
                "SELECT name,url,mark FROM video WHERE name LIKE '%" + txt + "%' or mark LIKE '%" + txt + "%'")  #
            # CONCAT(
            # 'f_id','f_area','f_place','f_AQI','f_AQItype','f_PM25per1h'),concat(concat('%','#txt'),'%')

            data_x = cur.fetchall()

            self.MyTable.clearContents()

            row_4 = len(data_x)
            vol_1 = len(cur.description)

            # 查询到的更新带表格当中
            for i_x in range(row_4):
                for j_y in range(vol_1):
                    temp_data_1 = data_x[i_x][j_y]  # 临时记录，不能直接插入表格
                    data_1 = QTableWidgetItem(str(temp_data_1))  # 转换后可插入表格
                    self.MyTable.setItem(i_x, j_y, data_1)

        # 空输入返回原先数据表格
        else:
            self.MyTable.clearContents()
            cur.execute("SELECT name,url,mark FROM video")
            data_y = cur.fetchall()

            row_5 = len(data_y)
            vol_1 = len(cur.description)

            for i_x_1 in range(row_5):
                for j_y_1 in range(vol_1):
                    temp_data_2 = data_y[i_x_1][j_y_1]  # 临时记录，不能直接插入表格
                    data_2 = QTableWidgetItem(str(temp_data_2))  # 转换后可插入表格
                    self.MyTable.setItem(i_x_1, j_y_1, data_2)



if __name__=='__main__':
    app = QApplication(sys.argv)
    example = Table()
    example.show()
    sys.exit(app.exec_())