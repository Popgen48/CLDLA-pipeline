import sys
import yaml
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QGroupBox,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QAction,
    QMessageBox,
    QRadioButton,
    QButtonGroup
)


def is_float(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("cLDLA Parameters")
        self.setGeometry(100, 100, 800, 600)  # Adjust the window size as needed

        # Add a Help button to the title bar
        help_action = QAction("Help", self)
        help_action.setStatusTip("Show a basic help message")
        help_action.triggered.connect(self.show_help_message)
        self.menuBar().addAction(help_action)

        # Create the central widget and set it
        central_widget = MyWidget()
        self.setCentralWidget(central_widget)

    def show_help_message(self):
        # Function to display a basic help message
        help_message = "More information available at ..."
        QMessageBox.information(self, "Help", help_message)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        # Category 1
        groupbox1 = QGroupBox("General Parameters")
        g1_params = ["input", "out_dir", "window_size", "output_prefix", "email"]
        vbox1 = QVBoxLayout()
        self.category1_fields = {}  # Store references to widget labels and values)
        for i, l in enumerate([
            "Input file",
            "Output directory",
            "SNP window size",
            "Output prefix",
            "Email",
        ]):
            label = QLabel(l)
            edit = QLineEdit()
            vbox1.addWidget(label)
            vbox1.addWidget(edit)
            self.category1_fields[g1_params[i]] = edit
        groupbox1.setLayout(vbox1)

        # Category 2
        groupbox2 = QGroupBox("Filtering")
        g2_params = ["maf", "samples", "min_depth", "max_depth", "exclude_snps"]
        vbox2 = QVBoxLayout()
        self.category2_fields = {}
        for i, l in enumerate([
            "Minor Allele Frequency (0 to 1)",
            "Samples file",
            "Minimum depth",
            "Maximum depth",
            "SNP Ids to exclude",
        ]):
            label = QLabel(l)
            edit = QLineEdit()
            vbox2.addWidget(label)
            vbox2.addWidget(edit)
            self.category2_fields[g2_params[i]] = edit
        groupbox2.setLayout(vbox2)

        # Category 3
        groupbox3 = QGroupBox("Echidna Parameters")
        g3_params = ["param_file", "pheno_file", "pheno_cols", "perm_test", "num_phenos", "num_windows", "p_value", "chromosomes"]
        vbox3 = QVBoxLayout()
        self.category3_fields = {}
        for i, l in enumerate([
            "Parameter file",
            "Phenotype file",
            "Phenotype Columns",
            "Permutation Test (True/False)",
            "# random phenotypes",
            "# random windows",
            "p-value",
            "Chromosomes to include",
        ]):
            label = QLabel(l)
            edit = QLineEdit()
            vbox3.addWidget(label)
            vbox3.addWidget(edit)
            self.category3_fields[g3_params[i]] = edit
        groupbox3.setLayout(vbox3)

        # Category 4
        groupbox4 = QGroupBox("Phasing")
        g4_params = ["beagle_phasing", "fastphase_phasing", "no_phasing", "phase_params"]
        vbox4 = QVBoxLayout()
        self.category4_fields = {}
        for i, l in enumerate([
            "Beagle Phasing",
            "FastPHASE Phasing",
            "None",
            "Phasing Parameters",
        ]):
            if l != "Phasing Parameters":
                yes = QRadioButton(l)
                group = QButtonGroup()
                group.addButton(yes)
                vbox4.addWidget(yes)
                self.category4_fields[g4_params[i]] = yes
            else:
                label = QLabel(l)
                edit = QLineEdit()
                vbox4.addWidget(label)
                vbox4.addWidget(edit)
                self.category4_fields[g4_params[i]] = edit
        groupbox4.setLayout(vbox4)

        self.params = {
            **self.category1_fields,
            **self.category2_fields,
            **self.category3_fields,
            **self.category4_fields,
        }

        # Add the group boxes to the grid layout
        grid.addWidget(groupbox1, 0, 0)
        grid.addWidget(groupbox2, 0, 1)
        grid.addWidget(groupbox3, 1, 0)
        grid.addWidget(groupbox4, 0, 2)

        # Submit Button
        submit_button = QPushButton("Save")
        submit_button.clicked.connect(self.on_submit)

        # Load Button
        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_data)

        # File Dialog Field
        self.file_path_field = QLineEdit()
        self.file_path_field.setPlaceholderText("Enter .yml file path")

        load_layout = QHBoxLayout()
        load_layout.addWidget(load_button)
        load_layout.addWidget(self.file_path_field)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addLayout(load_layout)
        vbox.addWidget(submit_button)

        self.setLayout(vbox)
        self.setWindowTitle("cLDLA params")
        self.resize(800, 600)

    def load_data(self):
        # Function to handle the "Load" button click
        file_path = self.file_path_field.text()
        if file_path.endswith(".yml"):
            try:
                with open(file_path, "r") as yaml_file:
                    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                    self.populate_fields(data)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
        else:
            print("Please provide a valid .yml file path.")

    def populate_fields(self, data):
        # Function to populate the fields with loaded data
        for idx, field_value in data.items():
            self.params[idx].setText(field_value)

    def validate(self):
        # # Function to validate the input fields
        # if not self.params["SNP window size"].text().isdigit():
        #     QMessageBox.critical(self, "Error", "SNP window size must be an integer.")
        #     return False
        # if not int(self.params["SNP window size"].text()) > 0:
        #     QMessageBox.critical(
        #         self, "Error", "SNP window size must be greater than 0."
        #     )
        #     return False
        # if not is_float(self.params["Minor Allele Frequency (0 to 1)"].text()):
        #     QMessageBox.critical(
        #         self, "Error", "Minor Allele Frequency must be a float."
        #     )
        #     return False
        # if (
        #     0 >= float(self.params["Minor Allele Frequency (0 to 1)"].text())
        #     or float(self.params["Minor Allele Frequency (0 to 1)"].text()) >= 1
        # ):
        #     QMessageBox.critical(
        #         self, "Error", "Minor Allele Frequency must be between 0 and 1."
        #     )
        #     return False
        # if not self.params["Minimum depth"].text().isdigit():
        #     QMessageBox.critical(self, "Error", "Minimum depth must be an integer.")
        #     return False
        # if not int(self.params["Minimum depth"].text()) > 0:
        #     QMessageBox.critical(self, "Error", "Minimum depth must be greater than 0.")
        #     return False
        # if not self.params["Maximum depth"].text().isdigit():
        #     QMessageBox.critical(self, "Error", "Maximum depth must be an integer.")
        #     return False
        # if (not int(self.params["Maximum depth"].text()) > 0) or (
        #     int(self.params["Maximum depth"].text())
        #     < int(self.params["Minimum depth"].text())
        # ):
        #     QMessageBox.critical(
        #         self,
        #         "Error",
        #         "Maximum depth must be greater than 0 and the minimum depth.",
        #     )
        #     return False
        # if not self.params["# random phenotypes"].text().isdigit():
        #     QMessageBox.critical(
        #         self, "Error", "# random phenotypes must be an integer."
        #     )
        #     return False
        # if not self.params["# random windows"].text().isdigit():
        #     QMessageBox.critical(self, "Error", "# random windows must be an integer.")
        #     return False
        # if not is_float(self.params["p-value"].text()):
        #     QMessageBox.critical(self, "Error", "p-value must be a floating point.")
        #     return False
        
        # # Loop to check if file paths are valid
        # for i in [
        #     "Input file",
        #     "Output directory",
        #     "Samples file",
        #     "SNP Ids to exclude",
        #     "Parameter file",
        #     "Phenotype file",
        #     "Chromosomes to include",
        # ]:
        #     if not os.path.exists(self.params[i].text()):
        #         QMessageBox.critical(self, "Error", f"{i} file path is invalid.")
        #         return False
        
        # Check phasing
        if self.params["beagle_phasing"].isChecked():
            if self.params["fastphase_phasing"].isChecked():
                QMessageBox.critical(self, "Error", "Please select atmost one phasing method.")
                return False
            else:
                self.params["beagle_phasing"] = True
                self.params["fastphase_phasing"] = False
                self.params["no_phasing"] = False
                # check pahasing parameter file path
                if not os.path.exists(self.params["phase_params"].text()):
                    QMessageBox.critical(self, "Error", f"Phasing parameter file path is invalid.")
                    return False
                return True
        elif self.params["fastphase_phasing"].isChecked():
            self.params["beagle_phasing"] = False
            self.params["fastphase_phasing"] = True
            self.params["no_phasing"] = False
            # check pahasing parameter file path
            if not os.path.exists(self.params["phase_params"].text()):
                QMessageBox.critical(self, "Error", f"Phasing parameter file path is invalid.")
                return False
            return True
        elif self.params["no_phasing"].isChecked():
            self.params["beagle_phasing"] = False
            self.params["fastphase_phasing"] = False
            self.params["phase_params"] = QLineEdit('None')
            return True
        
            
            

    def on_submit(self):
        # Function to handle the "Submit" button click
        if not self.validate():
            return
        field_data = {}
        for label, value in self.params.items():
            print(label, value)
            if label == "beagle_phasing" or label == "fastphase_phasing":
                field_data[label] = value
            else:
                field_data[label] = value.text()

        # Save the dictionary to a YAML file
        output_file = f'{field_data["output_prefix"]}_parameters.yml'
        with open(output_file, "w") as yaml_file:
            yaml.dump(field_data, yaml_file, default_flow_style=False)
        print(f"Data saved to {output_file}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
