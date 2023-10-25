import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QLabel, QLineEdit

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        # Category 1
        groupbox1 = QGroupBox('Category 1')
        vbox1 = QVBoxLayout()
        for _ in range(5):
            label = QLabel('Field:')
            edit = QLineEdit()
            vbox1.addWidget(label)
            vbox1.addWidget(edit)
        groupbox1.setLayout(vbox1)

        # Category 2
        groupbox2 = QGroupBox('Category 2')
        vbox2 = QVBoxLayout()
        for _ in range(5):
            label = QLabel('Field:')
            edit = QLineEdit()
            vbox2.addWidget(label)
            vbox2.addWidget(edit)
        groupbox2.setLayout(vbox2)

        # Category 3
        groupbox3 = QGroupBox('Category 3')
        vbox3 = QVBoxLayout()
        for _ in range(5):
            label = QLabel('Field:')
            edit = QLineEdit()
            vbox3.addWidget(label)
            vbox3.addWidget(edit)
        groupbox3.setLayout(vbox3)

        # Category 4
        groupbox4 = QGroupBox('Category 4')
        vbox4 = QVBoxLayout()
        for _ in range(5):
            label = QLabel('Field:')
            edit = QLineEdit()
            vbox4.addWidget(label)
            vbox4.addWidget(edit)
        groupbox4.setLayout(vbox4)

        # Add the group boxes to the grid layout
        grid.addWidget(groupbox1, 0, 0)
        grid.addWidget(groupbox2, 0, 1)
        grid.addWidget(groupbox3, 1, 0)
        grid.addWidget(groupbox4, 1, 1)

        self.setLayout(grid)
        self.setWindowTitle('cLDLA params')
        self.resize(750, 600)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    sys.exit(app.exec_())