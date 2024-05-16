import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton,QMainWindow, QTableWidget \
    ,QTableWidgetItem,QDialog,QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        search = QAction("Search",self)
        edit_menu_item.addAction(search)
        search.triggered.connect(self.search)


        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID","Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math","Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Phone Number")
        layout.addWidget(self.mobile_number)

        submit = QPushButton("Register")
        layout.addWidget(submit)
        submit.clicked.connect(self.add_students)

        self.setLayout(layout)

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.setLayout(layout)

        submit = QPushButton("Search")
        layout.addWidget(submit)
        submit.clicked.connect(self.search)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = mainwindow.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            mainwindow.table.item(item.row(),1 ).setSelected(True)
        cursor.close()
        connection.close()


    def add_students(self):
        name = self.student_name.text()
        course = self.course_name.currentText()
        mobile = self.mobile_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,course, mobile) VALUES(?, ?, ?)",(name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        mainwindow.load_data()

app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
mainwindow.load_data()
sys.exit(app.exec())