import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QLabel, QLineEdit, QPushButton

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

        # Submit Button
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.on_submit)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(submit_button)

        self.setLayout(vbox)
        self.setWindowTitle('cLDLA params')
        self.resize(760, 600)
        self.show()

    def on_submit(self):
        # Function to handle the "Submit" button click
        # Create a dictionary of field name and field value
        field_data = {}
        for category in (groupbox1, groupbox2, groupbox3, groupbox4):
            for widget in category.findChildren(QLineEdit):
                field_name = widget.text()
                field_value = widget.text()
                field_data[field_name] = field_value

        # Save the dictionary to a JSON file
        with open('parameters.json', 'w') as json_file:
            json.dump(field_data, json_file, indent=4)
        print("Data saved to parameters.json")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    sys.exit(app.exec_())
