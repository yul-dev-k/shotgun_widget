import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from retake import Retake


class ShotGunRetakeWidget(QWidget):
    def __init__(self):
        super().__init__()
        all_retake = Retake().get_all_retake()
        self.col_title = ['code', 'assigned', 'note', 'img', 'retake']
        self.initUI(all_retake, self.col_title)
        self.setWindowTitle('Shotgun Retake Widget')
        self.setWindowIcon(QIcon('icons.png'))

    def initUI(self, all_retake, col_title):
        total_shot = len(all_retake)
        self.table = QTableWidget()
        self.table.setColumnCount(len(col_title))
        self.table.setHorizontalHeaderLabels(col_title)
        self.table.setRowCount(total_shot)

        for idx, retake in enumerate(all_retake):

            self.table.setItem(idx, 0, QTableWidgetItem(retake['code']))
            self.table.setItem(idx, 1, QTableWidgetItem(
                retake['assigned'][0]['name']))
            self.table.setItem(idx, 2, QTableWidgetItem(retake['note']))
            self.table.setItem(idx, 3, QTableWidgetItem(retake['img']))
            self.table.setItem(idx, 4, QTableWidgetItem(retake['retake_v']))

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.move(300, 300)
        self.setGeometry(300, 100, 600, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = ShotGunRetakeWidget()
    mywindow.show()
    app.exec_()
