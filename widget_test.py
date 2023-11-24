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

""" 
  해야할 것
  1. 맨 처음 col에 checkbox (✅) 추가
  2. 내 retake만 보는걸 기본 뷰로
  3. My Retake | All Retake view 선택 버튼 필요
  4. 기본 위젯 높이 조금 줄이기
  5. 각 col마다 width 지정해주기
  6. Img탭 이미지 띄우기 (클릭하면 더 크게 볼 수 있으면 좋겠음. modal 처럼)
  7. retake_v 부분 감독님 | 편집팀 그냥 이렇게 나누는게 좋을 것 같음.
  8. note 마우스 hover하면 전체 글 나오게
  9. retake 새로고침 버튼 필요
"""
