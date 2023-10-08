from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QLineEdit,
                             QPushButton,
                             QLabel,
                             QGridLayout,
                             QVBoxLayout,
                             QHBoxLayout,
                             QWidget,
                             QSpacerItem,
                             QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyInstaller.utils.hooks import collect_data_files
import subprocess
import os

ICON = "Fortran_logo.ico"
datas = collect_data_files('icons')
datas += [(ICON, '.')]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fortran Build Tool")
        self.setMaximumSize(800, 600)

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Path to Fortran file (/path/to/your/folder)")
        self.command_edit = QLineEdit()
        self.command_edit.setText("gfortran -o")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter your program name here")
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("Enter your Fortran filename ('hello_world.f90')")

        self.programs_combobox = QComboBox()

        self.build_button = QPushButton()
        self.build_button.setText("Build")
        self.run_button = QPushButton()
        self.run_button.setDisabled(True)
        self.run_button.setText("Run")

        self.output_label = QLabel()
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_label.hide()
        self.errors_label = QLabel()
        self.errors_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errors_label.hide()

        self.path_edit.textChanged.connect(self.loadPrograms)
        self.build_button.clicked.connect(self.build)
        self.run_button.clicked.connect(self.runProgram)

        self.initGUI()
        self.show()

    def initGUI(self):
        grid_layout = QGridLayout()
        vertical_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        path_label = QLabel()
        path_label.setText("File path:")
        command_label = QLabel()
        command_label.setText("Command:")
        name_label = QLabel()
        name_label.setText("Program name:")
        file_label = QLabel()
        file_label.setText("Fortran file name:")

        button_spacer_left = QSpacerItem(30, 0)
        button_spacer_right = QSpacerItem(30, 0)
        button_layout.addItem(button_spacer_left)
        button_layout.addWidget(self.build_button)
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.programs_combobox)
        button_layout.addItem(button_spacer_right)

        grid_layout.addWidget(path_label, 0, 0, 1, 1)
        grid_layout.addWidget(self.path_edit, 0, 1, 1, 2)
        grid_layout.addWidget(command_label, 1, 0, 1, 1)
        grid_layout.addWidget(self.command_edit, 1, 1, 1, 2)
        grid_layout.addWidget(name_label, 2, 0, 1, 1)
        grid_layout.addWidget(self.name_edit, 2, 1, 1, 2)
        grid_layout.addWidget(file_label, 3, 0, 1, 1)
        grid_layout.addWidget(self.file_edit, 3, 1, 1, 2)
        grid_layout.addLayout(button_layout, 4, 0, 1, 3)
        grid_layout.addWidget(self.output_label, 5, 0, 1, 3)
        grid_layout.addWidget(self.errors_label, 6, 0, 1, 3)
        grid_layout.setColumnStretch(1, 1)

        spacer_top = QSpacerItem(400, 0)
        spacer_bottom = QSpacerItem(400, 0)
        vertical_layout.addItem(spacer_top)
        vertical_layout.addLayout(grid_layout)
        vertical_layout.addItem(spacer_bottom)

        central_widget = QWidget()
        central_widget.setLayout(vertical_layout)
        self.setCentralWidget(central_widget)

    def build(self):
        self.output_label.hide()
        self.output_label.hide()
        path = self.path_edit.text()
        compile_command = self.command_edit.text()
        program_name = self.name_edit.text()
        file_name = self.file_edit.text()
        command = f'cd {path} & {compile_command} {program_name} {file_name}'
        process = subprocess.run(command, capture_output=True, shell=True)
        output = process.stdout.decode('utf-8')
        errors = process.stderr.decode('utf-8')
        self.showOutputAndErrors(output, errors)
        self.loadPrograms()

    def showOutputAndErrors(self, output: str, errors: str):
        if not output and not errors:
            self.output_label.setText(f"Program '{self.name_edit.text()}' created!")
            if self.errors_label.isVisible():
                self.errors_label.hide()
            if self.output_label.isHidden():
                self.output_label.show()
        else:
            if output:
                self.output_label.setText("Output\n" + output)
                if self.output_label.isHidden():
                    self.output_label.show()
            if errors:
                self.errors_label.setText("Errors\n" + errors)
                if self.errors_label.isHidden():
                    self.errors_label.show()

    def loadPrograms(self):
        self.programs_combobox.clear()
        matching_files = []
        try:
            folder_path = self.path_edit.text()
            matching_files = [filename for filename in os.listdir(folder_path) if filename.endswith('.exe')]
        except FileNotFoundError:
            pass
        finally:
            self.programs_combobox.addItems(matching_files)
            self.run_button.setDisabled(not bool(matching_files))

    def runProgram(self):
        path = self.path_edit.text()
        cmdline = self.programs_combobox.currentText()
        subprocess.call("start cmd /K " + cmdline, cwd=path, shell=True)


if __name__ == "__main__":
    app = QApplication([])
    app_icon = QIcon(f"icons/Fortran_logo.ico")  # Replace with the path to your icon
    app.setWindowIcon(app_icon)
    window = MainWindow()
    app.exec()
