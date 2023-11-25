from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QCheckBox, QVBoxLayout, QWidget, QMessageBox, QComboBox, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
import numpy as np
import os


class ShotGunRetakeWidget(QTableWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Shotgun Retake Widget")

        self.data = self.filter_data(data)
        self.init_ui()

    def filter_data(self, data):
        return [
            item for item in data if item[1] and item[1].get("retake") and
            any(retake and retake.get("status") ==
                "rtks" for retake in item[1]["retake"].values())
        ]

    def init_ui(self):

        self.setColumnCount(10)
        self.setHorizontalHeaderLabels([
            "컷", "담당자", "Check", "Status", "Img", "Note",
            "Check", "Status", "Img", "Note"
        ])

        self.setRowCount(len(self.data))
        for i, item in enumerate(self.data):
            self.setItem(i, 0, QTableWidgetItem(item[0]["shot"]["shot_code"]))
            self.setItem(i, 1, QTableWidgetItem(
                item[0]["shot"]["shot_assignde"]))

            checkbox1 = QCheckBox()
            checkbox2 = QCheckBox()

            status_retake02 = item[1]["retake"]["retake02"]["status"] if item[1]["retake"]["retake02"] else None
            checkbox1.setEnabled(status_retake02 == "rtks")
            checkbox1.stateChanged.connect(
                lambda state, i=i, retake_type="retake02": self.checkbox_state_changed(state, i, retake_type))

            status_retake03 = item[1]["retake"]["retake03"]["status"] if item[1]["retake"]["retake03"] else None
            checkbox2.setEnabled(status_retake03 == "rtks")
            checkbox2.stateChanged.connect(
                lambda state, i=i, retake_type="retake03": self.checkbox_state_changed(state, i, retake_type))

            self.setCellWidget(i, 2, checkbox1)
            self.setCellWidget(i, 6, checkbox2)

            self.setItem(i, 3, QTableWidgetItem(
                str(status_retake02) if status_retake02 else ""))
            self.setItem(i, 4, QTableWidgetItem(
                self.ellipsis_text(str(item[1]["retake"]["retake02"]["image"])) if item[1]["retake"]["retake02"] else ""))
            self.setItem(i, 5, QTableWidgetItem(
                str(item[1]["retake"]["retake02"]["note"]) if item[1]["retake"]["retake02"] else ""))

            self.setItem(i, 7, QTableWidgetItem(
                str(status_retake03) if status_retake03 else ""))
            self.setItem(i, 8, QTableWidgetItem(
                self.ellipsis_text(str(item[1]["retake"]["retake03"]["image"])) if item[1]["retake"]["retake03"] else ""))
            self.setItem(i, 9, QTableWidgetItem(
                str(item[1]["retake"]["retake03"]["note"]) if item[1]["retake"]["retake03"] else ""))

            for j in range(self.columnCount()):
                item = self.item(i, j)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            self.resizeRowToContents(i)

        self.setColumnWidth(0, 120)
        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 30)
        self.setColumnWidth(3, 50)
        self.setColumnWidth(4, 50)
        self.setColumnWidth(5, 200)
        self.setColumnWidth(6, 30)
        self.setColumnWidth(7, 50)
        self.setColumnWidth(8, 50)
        self.setColumnWidth(9, 200)

    def create_combo_box(self):
        combo_box = QComboBox(self)
        combo_box.addItems(self.get_episode_files())
        combo_box.currentIndexChanged.connect(self.on_combo_box_change)

        return combo_box

    def on_combo_box_change(self, index):
        selected_file = self.get_episode_files()[index]
        # Load the selected file and update the UI
        print(f"Selected file: {selected_file}")
        # Add your code to update the UI with the data from the selected file

    @staticmethod
    def get_episode_files():
        folder_path = "DB"  # Change this to your actual folder path
        files = [file.split('.npy')[0] for file in os.listdir(
            folder_path) if file.endswith(".npy")]

        return files

    def checkbox_state_changed(self, state, row, retake_type):
        checkbox = self.cellWidget(row, 2 if retake_type == "retake02" else 6)

        if checkbox and checkbox.isChecked():
            reply = QMessageBox.warning(self, "Alert", f"'{retake_type}'의 상태를 'wfs'로 바꾸시겠습니까?",
                                        QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.No:
                checkbox.blockSignals(True)
                checkbox.setChecked(False)
                checkbox.blockSignals(False)
            if reply == QMessageBox.Yes:
                self.data[row][1]["retake"][retake_type]["status"] = "wfs"
                self.hide_row(row)

                print(f"현재 {row}열의 {retake_type}")
                print(self.data[row][1])

    def hide_row(self, row):
        self.setRowHidden(row, True)

    def ellipsis_text(self, text, max_len=50):
        if len(text) > max_len:
            return text[:max_len - 3] + "..."
        else:
            return text


def create_gui(data):
    app = QApplication([])
    window = QMainWindow()

    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)

    # Create the label and combo box layout
    combo_box_layout = QHBoxLayout()
    ep_label = QLabel("ep")
    combo_box_layout.addWidget(ep_label)
    combo_box_layout.addStretch()  # Add stretch to push combo box to the right

    widget = ShotGunRetakeWidget(data)
    combo_box = QComboBox()
    combo_box.addItems(widget.get_episode_files())
    combo_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    combo_box.currentIndexChanged.connect(widget.on_combo_box_change)
    combo_box_layout.addWidget(combo_box)

    main_layout.addLayout(combo_box_layout)

    # Create the table layout
    table_layout = QVBoxLayout()
    table_layout.addWidget(widget)

    main_layout.addLayout(table_layout)

    window.setCentralWidget(main_widget)
    window.show()
    app.exec_()


def get_retake_data(ep_num):
    return (np.load(f"DB/ep{ep_num}.npy", allow_pickle=True))


create_gui()
