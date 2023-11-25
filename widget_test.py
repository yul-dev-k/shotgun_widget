import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from retake import Retake


class ShotGunRetakeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.col_title = ['✅', '코드', '담당자', 'note', 'img', 'retake']
        self.show_my_retake = True
        self.row_height = 40
        self.col1_w, self.col2_w, self.col3_w, self.col4_w, self.col5_w, self.col6_w = [
            10, 130, 50, 200, 100, 50]
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

            note_item = QTableWidgetItem(retake['note'])
            self.table.setItem(row_idx, 3, note_item)

            self.table.setItem(row_idx, 4, QTableWidgetItem(retake['img']))
            self.table.setItem(
                row_idx, 5, QTableWidgetItem(retake['retake_v']))

            note_item.setToolTip(retake['note'])

            self.table.setRowHeight(row_idx, self.row_height)

        self.table.setColumnWidth(0, self.col1_w)
        self.table.setColumnWidth(1, self.col2_w)
        self.table.setColumnWidth(2, self.col3_w)
        self.table.setColumnWidth(3, self.col4_w)
        self.table.setColumnWidth(4, self.col5_w)
        self.table.setColumnWidth(5, self.col6_w)

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

            note_item = QTableWidgetItem(retake['note'])
            self.table.setItem(row_idx, 3, note_item)

            self.table.setItem(row_idx, 4, QTableWidgetItem(retake['img']))
            self.table.setItem(
                row_idx, 5, QTableWidgetItem(retake['retake_v']))

            note_item.setToolTip(retake['note'])

            self.table.setRowHeight(row_idx, self.row_height)

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

            note_item = QTableWidgetItem(retake['note'])
            self.table.setItem(row_idx, 3, note_item)

            self.table.setItem(row_idx, 4, QTableWidgetItem(retake['img']))
            self.table.setItem(
                row_idx, 5, QTableWidgetItem(retake['retake_v']))

            note_item.setToolTip(retake['note'])

            self.table.setRowHeight(row_idx, self.row_height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = ShotGunRetakeWidget()
    mywindow.show()
    sys.exit(app.exec_())
