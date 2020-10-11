import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMessageBox

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

    def __init__(self):
        super().__init__()

        self.accountList = []
        self.maxAccountLen = 5

        self.layout = QVBoxLayout()
        self.indexLayout = QGridLayout()
        self.elementLayout = QGridLayout()

        self.initUI()
        # self.init_settings()
        self.init_signals()

    def initUI(self):

        self.init_index_layout()
        self.layout.addLayout(self.indexLayout)
        self.layout.addLayout(self.elementLayout)

        self.setLayout(self.layout)

    def init_settings(self):
        size = self.sizeHint()
        self.setFixedWidth(size.width())

    def init_signals(self):

        indexCheckBox = self.indexLayout.itemAtPosition(0, 0).widget()
        indexCheckBox.stateChanged.connect(self.onStateChanged)

    def init_index_layout(self):
        self.indexLayout.addWidget(QCheckBox(), 0, 0)
        self.indexLayout.addWidget(QLabel('번호'), 0, 1)
        self.indexLayout.addWidget(QLabel('계정'), 0, 2)
        self.indexLayout.addWidget(QLabel('비밀번호'), 0, 3)
        self.indexLayout.addWidget(QLabel('검증'), 0, 4)

    def make_connection(self, obj):

        if type(obj).__name__ == 'AccountInput':
            obj.send_account.connect(self.onAccountSent)
        elif type(obj).__name__ == 'Buttons':
            obj.validationButton.clicked.connect(self.onValidationClicked)

    @pyqtSlot()
    def onValidationClicked(self):

        accounts = []
        row = len(self.accountList)
        col = len(self.accountList[0])

        for pos in range(row):

            items = [self.elementLayout.itemAtPosition(
                pos, idx).widget() for idx in range(col)]

            if items[0].checkState() == Qt.Checked:
                id = items[1].text()
                passwd = items[2].text()
                accounts.append((id, passwd))

    @pyqtSlot()
    def onStateChanged(self):
        indexCheckBox = self.indexLayout.itemAtPosition(0, 0).widget()
        indexState = indexCheckBox.checkState()

        accounts = self.accountList

        for idx in range(len(accounts)):
            checkBox = self.elementLayout.itemAtPosition(idx, 0).widget()
            checkBox.setChecked(indexState)

    @pyqtSlot(tuple)
    def onAccountSent(self, account):

        if self.maxAccountLen > len(self.accountList):

            id = account[0]
            passwd = account[1]
            num = len(self.accountList)

            elem = (QCheckBox(), QLabel(str(num+1)), QLabel(str(id)),
                    QLabel(str(passwd)), QLabel(self.VALID[False]))
            self.accountList.append(elem)

            pos = 0
            for e in elem:
                self.elementLayout.addWidget(e, num, pos)
                pos += 1
        else:
            title = "Information"
            text = "최대 {}개의 계정만 추가 하실 수 있습니다.".format(self.maxAccountLen)
            reply = QMessageBox.warning(self, title, text)


class Buttons(QWidget):

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
        self.buttons = Buttons()

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
