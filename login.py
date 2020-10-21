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
        self.initUI()

    def initUI(self):
        txt = '계정관리'
        self.setText(txt)
        font = self.font()
        font.setPointSize(15)
        self.setFont(font)


class AccountInput(QWidget):

    send_account = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()

        self.inputID = QLineEdit()
        self.inputPasswd = QLineEdit()
        self.btn = QPushButton()

        self.init_txt()
        self.init_settings()
        self.init_signals()
        self.initUI()

    def init_txt(self):
        txt = '추가'
        self.btn.setText(txt)

    def init_settings(self):
        self.btn.setEnabled(False)

    def init_signals(self):
        self.btn.clicked.connect(self.onClicked)

        self.inputID.returnPressed.connect(self.onClicked)
        self.inputPasswd.returnPressed.connect(self.onClicked)

        self.inputID.textChanged[str].connect(self.onTextChanged)
        self.inputPasswd.textChanged[str].connect(self.onTextChanged)

    def initUI(self):
        layout = QHBoxLayout()
        layout.addWidget(self.inputID)
        layout.addWidget(self.inputPasswd)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    @pyqtSlot()
    def onTextChanged(self):
        id = self.inputID.text()
        passwd = self.inputPasswd.text()

        if id and passwd:
            self.btn.setEnabled(True)

    @pyqtSlot()
    def onClicked(self):

        id = self.inputID.text()
        passwd = self.inputPasswd.text()

        if id and passwd:
            self.btn.setEnabled(False)
            self.inputID.clear()
            self.inputPasswd.clear()
            self.send_account.emit((id, passwd))


class AccountList(QWidget):

    VALID = {True: 'O', False: 'X'}
    horizontalHeader = ['체크', '아이디', '비밀번호', '검증']

    def __init__(self):
        super().__init__()

        self.accountList = []
        self.maxAccountLen = 5

        self.layout = QVBoxLayout()
        self.tableList = QTableWidget()

        self.initUI()

    def initUI(self):
        self.layout.addWidget(self.tableList)
        self.table_setting()
        self.setLayout(self.layout)

    def table_setting(self):
        self.tableList.showGrid()
        self.tableList.setColumnCount(len(self.horizontalHeader))
        self.tableList.setHorizontalHeaderLabels(self.horizontalHeader)
        self.tableList.alternatingRowColors()

        for idx in range(len(self.horizontalHeader)):
            self.tableList.setColumnWidth(idx, 70)

    def make_connection(self, obj):

        if type(obj).__name__ == 'AccountInput':
            obj.send_account.connect(self.onAccountSent)

        elif type(obj).__name__ == 'ValidationButtons':
            validationStartButton = obj.validationButton
            validationStartButton.clicked.connect(
                self.onValidationStartClicked)

    def add_item(self, account):
        row = self.tableList.rowCount()
        self.tableList.insertRow(row)

        chkbox = QTableWidgetItem()
        chkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chkbox.setCheckState(Qt.Unchecked)
        self.tableList.setItem(row, 0, chkbox)
        self.tableList.setItem(row, 1, MyTableWidgetItem(account[0]))
        self.tableList.setItem(row, 2, QTableWidgetItem(account[1]))
        self.tableList.setItem(
            row, 3, QTableWidgetItem(self.VALID[False]))

    def __get_checked_items(self):
        t = self.tableList

        checkedItems = [(t.item(row, 1).text(), t.item(row, 2).text())
                        for row in range(t.rowCount()) if t.item(row, 0).checkState() == Qt.Checked]

        return checkedItems

    @pyqtSlot(tuple)
    def onAccountSent(self, account):

        if self.maxAccountLen > len(self.accountList):

            self.accountList.append(account)
            self.add_item(account)

        else:
            title = "Information"
            text = "최대 {}개의 계정만 추가 하실 수 있습니다.".format(self.maxAccountLen)
            reply = QMessageBox.warning(self, title, text)

    @pyqtSlot()
    def onValidationStartClicked(self):

        items = self.__get_checked_items()
        print(items)


class MyTableWidgetItem(QTableWidgetItem):

    def __init__(self, arg):
        super().__init__(arg)
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)


class ValidationButtons(QWidget):

    def __init__(self):
        super().__init__()

        self.validationButton = QPushButton()
        self.deleteButton = QPushButton()

        self.initUI()

    def initUI(self):

        self.validationButton.setText('검증 시작')
        self.deleteButton.setText('선택 삭제')

        layout = QHBoxLayout()
        layout.addWidget(self.validationButton)
        layout.addWidget(self.deleteButton)

        self.setLayout(layout)


class Login(QWidget):

    def __init__(self):
        super().__init__()
        self.label = Title()
        self.account_input = AccountInput()
        self.account_list = AccountList()
        self.buttons = ValidationButtons()

        self.init_settings()
        self.initUI()

    def init_settings(self):
        self.account_list.make_connection(self.account_input)
        self.account_list.make_connection(self.buttons)

    def initUI(self):
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
