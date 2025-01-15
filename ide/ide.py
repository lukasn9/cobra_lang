from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QTreeView, QFileSystemModel, QSplitter, QToolBar)
from PySide6.QtGui import QColor, QFont, QIcon, QAction
from PySide6.QtCore import Qt, QDir
import sys

class CobraLangIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CobraLang IDE")
        self.setMinimumSize(1024, 768)
        self.setStyleSheet(self.load_theme())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder)
        toolbar.addAction(open_folder_action)
        
        new_file_action = QAction("New File", self)
        new_file_action.triggered.connect(self.new_file)
        toolbar.addAction(new_file_action)
        
        open_file_action = QAction("Open File", self)
        open_file_action.triggered.connect(self.open_file)
        toolbar.addAction(open_file_action)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.homePath())

        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(QDir.homePath()))
        self.file_tree.doubleClicked.connect(self.open_selected_file)

        splitter.addWidget(self.file_tree)

        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 12))
        splitter.addWidget(self.editor)

        splitter.setSizes([250, 750])

    def load_theme(self):
        return '''
            QMainWindow {
                background-color: #1e1b29;
            }
            QToolBar {
                background-color: #2b2840;
                border: none;
            }
            QTreeView {
                color: #f1f1f1;
                background-color: #2b2840;
            }
            QTextEdit {
                color: #f8f8f2;
                background-color: #322b42;
                border: none;
            }
            QToolButton {
                color: #f1f1f1;
            }
            QPushButton {
                color: #f1f1f1;
                background-color: #4b4161;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #66537a;
            }
        '''

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", QDir.homePath())
        if folder_path:
            self.file_tree.setRootIndex(self.file_model.index(folder_path))

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath(), "*.*")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            self.editor.setPlainText(content)

    def open_selected_file(self, index):
        file_path = self.file_model.filePath(index)
        if QDir(file_path).exists():
            return
        with open(file_path, 'r') as file:
            content = file.read()
        self.editor.setPlainText(content)

    def new_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "New File", QDir.homePath(), "*.*")
        if file_path:
            with open(file_path, 'w') as file:
                file.write("")
            self.open_file(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = CobraLangIDE()
    ide.show()
    sys.exit(app.exec())