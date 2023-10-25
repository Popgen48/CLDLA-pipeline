import sys
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QMainWindow, QAction, QMessageBox

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('cLDLA Parameters')
        self.setGeometry(100, 100, 800, 600)  # Adjust the window size as needed

        # Add a Help button to the title bar
        help_action = QAction('Help', self)
        help_action.setStatusTip('Show a basic help message')
        help_action.triggered.connect(self.show_help_message)
        self.menuBar().addAction(help_action)

        # Create the central widget and set it
        central_widget = MyWidget()
        self.setCentralWidget(central_widget)

    def show_help_message(self):
        # Function to display a basic help message
        help_message = "More information available at ..."
        QMessageBox.information(self, 'Help', help_message)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        # Category 1
        groupbox1 = QGroupBox('Category 1')
        vbox1 = QVBoxLayout()
        self.category1_fields = []  # Store references to widget labels and values)
        for i in ['C1 F1', 'C1 F2', 'C1 F3', 'C1 F4', 'C1 F5']:
            label = QLabel(i)
            edit = QLineEdit()
            vbox1.addWidget(label)
            vbox1.addWidget(edit)
            self.category1_fields.append((label.text(), edit))
        groupbox1.setLayout(vbox1)

        # Category 2
        groupbox2 = QGroupBox('Category 2')
        vbox2 = QVBoxLayout()
        self.category2_fields = []
        for i in ['C2 F1', 'C2 F2', 'C2 F3', 'C2 F4', 'C2 F5']:
            label = QLabel(i)
            edit = QLineEdit()
            vbox2.addWidget(label)
            vbox2.addWidget(edit)
            self.category2_fields.append((label.text(), edit))
        groupbox2.setLayout(vbox2)

        # Category 3
        groupbox3 = QGroupBox('Category 3')
        vbox3 = QVBoxLayout()
        self.category3_fields = []
        for i in ['C3 F1', 'C3 F2', 'C3 F3', 'C3 F4', 'C3 F5']:
            label = QLabel(i)
            edit = QLineEdit()
            vbox3.addWidget(label)
            vbox3.addWidget(edit)
            self.category3_fields.append((label.text(), edit))
        groupbox3.setLayout(vbox3)

        # Category 4
        groupbox4 = QGroupBox('Category 4')
        vbox4 = QVBoxLayout()
        self.category4_fields = []  
        for i in ['C4 F1', 'C4 F2', 'C4 F3', 'C4 F4', 'C4 F5']:
            label = QLabel(i)
            edit = QLineEdit()
            vbox4.addWidget(label)
            vbox4.addWidget(edit)
            self.category4_fields.append((label.text(),edit))
        groupbox4.setLayout(vbox4)
        
        # Add the group boxes to the grid layout
        grid.addWidget(groupbox1, 0, 0)
        grid.addWidget(groupbox2, 0, 1)
        grid.addWidget(groupbox3, 1, 0)
        grid.addWidget(groupbox4, 1, 1)

        # Submit Button
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.on_submit)

        # Load Button
        load_button = QPushButton('Load')
        load_button.clicked.connect(self.load_data)

        # File Dialog Field
        self.file_path_field = QLineEdit()
        self.file_path_field.setPlaceholderText('Enter .yml file path')

        load_layout = QHBoxLayout()
        load_layout.addWidget(load_button)
        load_layout.addWidget(self.file_path_field)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addLayout(load_layout)
        vbox.addWidget(submit_button)

        self.setLayout(vbox)
        self.setWindowTitle('cLDLA params')
        self.resize(800, 600)

    def load_data(self):
        # Function to handle the "Load" button click
        file_path = self.file_path_field.text()
        if file_path.endswith('.yml'):
            try:
                with open(file_path, 'r') as yaml_file:
                    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                    self.populate_fields(data)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
        else:
            print("Please provide a valid .yml file path.")

    def populate_fields(self, data):
        # Function to populate the fields with loaded data
        for idx, field_value in enumerate(data.values()):
            if idx < len(self.category1_fields):
                self.category1_fields[idx].setText(str(field_value))
            elif idx < 2 * len(self.category1_fields):
                self.category2_fields[idx - len(self.category1_fields)].setText(str(field_value))
            elif idx < 3 * len(self.category1_fields):
                self.category3_fields[idx - 2 * len(self.category1_fields)].setText(str(field_value))
            else:
                self.category4_fields[idx - 3 * len(self.category1_fields)].setText(str(field_value))

    def on_submit(self):
        # Function to handle the "Submit" button click
        field_data = {}
        for label, value in self.category1_fields + self.category2_fields + self.category3_fields + self.category4_fields:
            field_data[label] = value.text()

        # Save the dictionary to a YAML file
        with open('parameters.yml', 'w') as yaml_file:
            yaml.dump(field_data, yaml_file, default_flow_style=False)
        print("Data saved to parameters.yml")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
