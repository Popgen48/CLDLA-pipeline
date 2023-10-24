import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create labels
        self.label1 = QLabel(self)
        self.label1.setText('Keep sample:')
        self.label1.move(50, 50)

        self.label2 = QLabel(self)
        self.label2.setText('Remove sample:')
        self.label2.move(50, 100)

        # Create line edits
        self.line_edit1 = QLineEdit(self)
        self.line_edit1.move(150, 50)

        self.line_edit2 = QLineEdit(self)
        self.line_edit2.move(150, 100)

        # Create button
        self.button = QPushButton('Submit', self)
        self.button.move(150, 150)
        self.button.clicked.connect(self.submit)

    def submit(self):
        keep = self.line_edit1.text()
        remove = self.line_edit2.text()
        print(f'To-keep: {keep}, To-remove: {remove}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setGeometry(100, 100, 400, 200)
    window.setWindowTitle('cLDLA')
    window.show()
    sys.exit(app.exec_())
