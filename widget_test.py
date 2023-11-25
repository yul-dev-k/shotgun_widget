import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from retake import Retake


class ShotGunRetakeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.col_title = ['✅', 'code', 'assigned', 'note', 'img', 'retake']
        self.show_my_retake = True
        self.initUI()
        self.setWindowTitle('Shotgun Retake Widget')
        self.setWindowIcon(QIcon('icons.png'))

    def initUI(self):
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        layout = QVBoxLayout()

        self.refresh_button = QPushButton('새로 고침', self)
        self.refresh_button.clicked.connect(self.refresh_data)
        self.refresh_button.setMaximumWidth(100)

        self.toggle_button = QPushButton('모든 리테이크 보기', self)
        self.toggle_button.clicked.connect(self.toggle_view)
        self.toggle_button.setMaximumWidth(150)

        hbox.addStretch(3)
        hbox.addWidget(self.refresh_button)
        hbox.addWidget(self.toggle_button)

        layout.addLayout(hbox)
        layout.addWidget(self.table())
        self.setLayout(layout)

        self.move(300, 300)
        self.setGeometry(300, 100, 570, 200)
        self.update()
        self.show()

    def all_retake_ui(self):
        return Retake().get_all_retake()

    def my_retake_ui(self):
        return Retake().get_my_retake()

    def toggle_view(self):
        self.show_my_retake = not self.show_my_retake
        self.update_table()
        self.update_toggle_button_text()

    def table(self):
        view = self.my_retake_ui() if self.show_my_retake else self.all_retake_ui()
        total_shot = len(view)
        self.checkboxes = []

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.col_title))
        self.table.setHorizontalHeaderLabels(self.col_title)
        self.table.setRowCount(total_shot)

        for row_idx, retake in enumerate(view):
            checkbox = QCheckBox()
            self.checkboxes.append(checkbox)
            self.table.setCellWidget(row_idx, 0, checkbox)
            self.table.setItem(row_idx, 1, QTableWidgetItem(retake['code']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(
                retake['assigned'][0]['name']))
            self.table.setItem(row_idx, 3, QTableWidgetItem(retake['note']))
            self.table.setItem(row_idx, 4, QTableWidgetItem(retake['img']))
            self.table.setItem(
                row_idx, 5, QTableWidgetItem(retake['retake_v']))

        self.table.setColumnWidth(0, 10)
        self.table.setColumnWidth(1, 130)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 50)

        return self.table

    def update_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        new_view = self.my_retake_ui() if self.show_my_retake else self.all_retake_ui()
        self.table.setRowCount(len(new_view))

        for row_idx, retake in enumerate(new_view):
            checkbox = QCheckBox()
            self.checkboxes.append(checkbox)
            self.table.setCellWidget(row_idx, 0, checkbox)
            self.table.setItem(row_idx, 1, QTableWidgetItem(retake['code']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(
                retake['assigned'][0]['name']))
            self.table.setItem(row_idx, 3, QTableWidgetItem(retake['note']))
            self.table.setItem(row_idx, 4, QTableWidgetItem(retake['img']))
            self.table.setItem(
                row_idx, 5, QTableWidgetItem(retake['retake_v']))

    def update_toggle_button_text(self):
        if self.show_my_retake:
            self.toggle_button.setText('모든 리테이크 보기')
        else:
            self.toggle_button.setText('내 리테이크 보기')

    def refresh_data(self):
        if self.show_my_retake:
            self.update_table_data(self.my_retake_ui())
        else:
            self.update_table_data(self.all_retake_ui())

        QMessageBox.information(self, '알림', '업데이트가 완료되었습니다.')

    def update_table_data(self, data):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setRowCount(len(data))

        for row_idx, retake in enumerate(data):
            checkbox = QCheckBox()
            self.checkboxes.append(checkbox)
            self.table.setCellWidget(row_idx, 0, checkbox)
            self.table.setItem(row_idx, 1, QTableWidgetItem(retake['code']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(
                retake['assigned'][0]['name']))
            self.table.setItem(row_idx, 3, QTableWidgetItem(retake['note']))
            self.table.setItem(row_idx, 4, QTableWidgetItem(retake['img']))
            self.table.setItem(
                row_idx, 5, QTableWidgetItem(retake['retake_v']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = ShotGunRetakeWidget()
    mywindow.show()
    sys.exit(app.exec_())


""" 
  해야할 것
  1. 맨 처음 col에 checkbox (✅) 추가 
  2. 내 retake만 보는걸 기본 뷰로 ✅
  3. My Retake | All Retake view 선택 버튼 필요 ✅
  4. 기본 위젯 높이 조금 줄이기 ✅
  5. 각 col마다 width 지정해주기 ✅
  6. Img탭 이미지 띄우기 (클릭하면 더 크게 볼 수 있으면 좋겠음. modal 처럼)
  7. retake_v 부분 감독님 | 편집팀 그냥 이렇게 나누는게 좋을 것 같음. ✅
  8. note 마우스 hover하면 전체 글 나오게
  9. retake 새로고침 버튼 필요 ✅
"""
