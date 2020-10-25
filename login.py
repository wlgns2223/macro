import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal


class Title(QLabel):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        txt = '계정관리'
        self.setText(txt)
        font = self.font()
        font.setPointSize(15)
        self.setFont(font)


class AccountInput(QWidget):

    send_account = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()

        self.input_id = QLineEdit()
        self.input_passwd = QLineEdit()
        self.btn = QPushButton()

        self.init_txt()
        self.init_settings()
        self.init_signals()
        self.init_UI()

    def init_txt(self):
        txt = '추가'
        self.btn.setText(txt)

    def init_settings(self):
        self.btn.setEnabled(False)

    def init_signals(self):
        self.btn.clicked.connect(self.on_id_return_clicked)

        self.input_id.returnPressed.connect(self.on_id_return_clicked)
        self.input_passwd.returnPressed.connect(self.on_id_return_clicked)

        self.input_id.textChanged[str].connect(self.on_text_changed)
        self.input_passwd.textChanged[str].connect(self.on_text_changed)

    def init_UI(self):
        layout = QHBoxLayout()
        layout.addWidget(self.input_id)
        layout.addWidget(self.input_passwd)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    @pyqtSlot()
    def on_text_changed(self):
        id = self.input_id.text()
        passwd = self.input_passwd.text()

        if id and passwd:
            self.btn.setEnabled(True)

    @pyqtSlot()
    def on_id_return_clicked(self):

        id = self.input_id.text()
        passwd = self.input_passwd.text()

        if id and passwd:
            self.btn.setEnabled(False)
            self.input_id.clear()
            self.input_passwd.clear()
            self.send_account.emit((id, passwd))


class AccountList(QWidget):

    VALID = {True: 'O', False: 'X'}
    horizontal_header = ['체크', '아이디', '비밀번호', '검증']

    def __init__(self):
        super().__init__()

        self.account_list = []
        self.max_account_len = 5

        self.layout = QVBoxLayout()
        self.table_list = QTableWidget()

        self.init_UI()

    def init_UI(self):
        self.layout.addWidget(self.table_list)
        self.table_setting()
        self.setLayout(self.layout)

    def table_setting(self):
        self.table_list.showGrid()
        self.table_list.setColumnCount(len(self.horizontal_header))
        self.table_list.setHorizontalHeaderLabels(self.horizontal_header)
        self.table_list.alternatingRowColors()
        self.table_list.setMouseTracking(True)

        for idx in range(len(self.horizontal_header)):
            self.table_list.setColumnWidth(idx, 70)

    def make_connection(self, obj):

        if type(obj).__name__ == 'AccountInput':
            obj.send_account.connect(self.onAccountSent)

        elif type(obj).__name__ == 'ValidationButtons':
            validation_button = obj.validation_button
            delete_button = obj.delete_button

            validation_button.clicked.connect(
                self.on_validation_button_clicked)

            delete_button.clicked.connect(self.on_delete_button_clicked)

    def __make_checkbox(self):

        checkbox = QTableWidgetItem()
        checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        checkbox.setCheckState(Qt.Unchecked)

        return checkbox

    def add_item(self, account):
        row = self.table_list.rowCount()
        self.table_list.insertRow(row)

        chkbox = self.__make_checkbox()

        self.table_list.setItem(
            row, 0, chkbox)

        self.table_list.setItem(
            row, 1, MyTableWidgetItem(account[0]))

        self.table_list.setItem(
            row, 2, MyTableWidgetItem(account[1]))

        self.table_list.setItem(
            row, 3, MyTableWidgetItem(self.VALID[False]))

        qitem = (self.table_list.item(row, 1), self.table_list.item(row, 2))

        for idx in range(2):
            self.__set_table_item_tooptip(qitem[idx], account[idx])

    def __set_table_item_tooptip(self, qitem, account):
        qitem.setToolTip(account)

    def __get_checked_items(self):
        t = self.table_list

        checkedItems = [(t.item(row, 1).text(), t.item(row, 2).text())
                        for row in range(t.rowCount()) if t.item(row, 0).checkState() == Qt.Checked]

        return checkedItems

    @pyqtSlot()
    def on_delete_button_clicked(self):

        qtable = self.table_list
        row = []

        for index in range(qtable.rowCount()):
            if qtable.item(index, 0).checkState() == Qt.Checked:
                row.append(index)

        row = tuple(row)

        for index in sorted(row, reverse=True):
            qtable.removeRow(index)
            del self.account_list[index]

    @pyqtSlot(tuple)
    def onAccountSent(self, account):

        if self.max_account_len > len(self.account_list):

            self.account_list.append(account)
            self.add_item(account)

        else:
            title = "Information"
            text = "최대 {}개의 계정만 추가 하실 수 있습니다.".format(self.max_account_len)
            reply = QMessageBox.warning(self, title, text)

    @pyqtSlot()
    def on_validation_button_clicked(self):

        items = self.__get_checked_items()
        print(items)


class MyTableWidgetItem(QTableWidgetItem):

    def __init__(self, arg):
        super().__init__(arg)
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)


class ValidationButtons(QWidget):

    def __init__(self):
        super().__init__()

        self.validation_button = QPushButton()
        self.delete_button = QPushButton()

        self.init_UI()

    def init_UI(self):

        self.validation_button.setText('검증 시작')
        self.delete_button.setText('선택 삭제')

        layout = QHBoxLayout()
        layout.addWidget(self.validation_button)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)


class Login(QWidget):

    def __init__(self):
        super().__init__()
        self.label = Title()
        self.account_input = AccountInput()
        self.account_list = AccountList()
        self.buttons = ValidationButtons()

        self.init_settings()
        self.init_UI()

    def init_settings(self):
        self.account_list.make_connection(self.account_input)
        self.account_list.make_connection(self.buttons)

    def init_UI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.account_input)
        layout.addWidget(self.account_list)
        layout.addWidget(self.buttons)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())
