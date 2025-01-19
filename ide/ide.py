from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QWidget,
                              QPushButton, QFileDialog, QTextEdit, QTreeView, QFileSystemModel, 
                              QSplitter, QToolBar, QLabel, QPlainTextEdit, QLineEdit, QDialog, QGridLayout, QLineEdit, QPushButton)
from PySide6.QtGui import QFont, QAction, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor
from PySide6.QtCore import Qt, QDir, QSize
import sys
import subprocess
import os

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = {}

        self.keywords = {
            "define": "#BD93F9",
            "give": "#BD93F9",
            "if": "#BD93F9",
            "else if": "#BD93F9",
            "otherwise": "#BD93F9",
            "loop while": "#BD93F9",
            "repeat": "#BD93F9",
            "class": "#BD93F9",
            "exit": "#BD93F9",
            "skip": "#BD93F9",
            "not": "#BD93F9",
            "within": "#BD93F9",
            "output": "#e7f3cb",
        }

        self.setup_highlighting_rules()
    
    def setup_highlighting_rules(self):
        for word, color in self.keywords.items():
            text_format = QTextCharFormat()
            text_format.setForeground(QColor(color))
            self.highlighting_rules[word] = text_format

    def highlightBlock(self, text):
        for word, format in self.highlighting_rules.items():
            index = text.find(word)
            while index >= 0:
                length = len(word)
                self.setFormat(index, length, format)
                index = text.find(word, index + length)

class Button(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(32)
        self.setFont(QFont("Inter", 9))

class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find")
        self.setModal(True)

        layout = QGridLayout()
        self.find_input = QLineEdit()
        self.replace_input = QLineEdit()
        self.find_button = QPushButton("Find")
        self.replace_button = QPushButton("Replace")
        self.replace_all_button = QPushButton("Replace All")

        layout.addWidget(QLabel("Find:"), 0, 0)
        layout.addWidget(self.find_input, 0, 1)
        layout.addWidget(QLabel("Replace:"), 1, 0)
        layout.addWidget(self.replace_input, 1, 1)
        layout.addWidget(self.find_button, 2, 0)
        layout.addWidget(self.replace_button, 2, 1)
        layout.addWidget(self.replace_all_button, 3, 1)
        self.setLayout(layout)

        self.find_button.clicked.connect(self.find_next)
        self.replace_button.clicked.connect(self.replace)
        self.replace_all_button.clicked.connect(self.replace_all)

        self.editor = parent.editor

    def find_next(self):
        search_text = self.find_input.text()
        if not search_text:
            return

        cursor = self.editor.textCursor()
        document = self.editor.document()
        cursor = document.find(search_text, cursor)

        if cursor.isNull():
            start_cursor = QTextCursor(document)
            cursor = document.find(search_text, start_cursor)

        if cursor.isNull():
            self.terminal.appendPlainText(f"'{search_text}' not found.")
        else:
            self.editor.setTextCursor(cursor)

    def replace(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_input.text())

    def replace_all(self):
        word = self.find_input.text()
        replace_text = self.replace_input.text()
        if not word:
            return
        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.Start)
        while True:
            cursor = self.editor.document().find(word, cursor)
            if cursor.isNull():
                break
            cursor.beginEditBlock()
            cursor.insertText(replace_text)
            cursor.endEditBlock()
        self.editor.setTextCursor(cursor)

class CobraLangIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CobraLang IDE")
        self.setMinimumSize(1024, 768)
        self.setStyleSheet(self.load_theme())

        app_font = QFont("Inter", 10)
        QApplication.setFont(app_font)

        self.current_file_path = None
        self.highlighter = None
        self.current_directory = os.getcwd()
        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        actions = [
            ("folder-outline", "Open Folder", self.open_folder),
            ("file-plus-outline", "New File", self.new_file),
            ("file-outline", "Open File", self.open_file),
            ("content-save-outline", "Save File", self.save_file, "Ctrl+S"),
            ("play-outline", "Run File", self.run_file, "Ctrl+R")
        ]
        
        for icon, text, slot, *shortcut in actions:
            action = QAction(text, self)
            action.triggered.connect(slot)
            if shortcut:
                action.setShortcut(QKeySequence(shortcut[0]))
            toolbar.addAction(action)

        h_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(h_splitter)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")
        
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(""))
        self.file_tree.setHidden(True)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setAnimated(True)
        self.file_tree.doubleClicked.connect(self.open_selected_file)

        for i in range(1, 4):
            self.file_tree.setColumnHidden(i, True)
            
        h_splitter.addWidget(self.file_tree)

        v_splitter = QSplitter(Qt.Vertical)
        h_splitter.addWidget(v_splitter)

        editor_container = QWidget()
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)

        self.filename_label = QLabel("No file opened")
        self.filename_label.setFont(QFont("Inter", 10))
        self.filename_label.setContentsMargins(10, 10, 10, 10)
        editor_layout.addWidget(self.filename_label)

        self.editor = QTextEdit()
        self.editor.setFont(QFont("JetBrains Mono", 12))
        self.editor.setLineWrapMode(QTextEdit.NoWrap)
        self.editor.setTabStopDistance(self.editor.fontMetrics().horizontalAdvance(" ") * 4)
        self.editor.setShortcutEnabled(True)
        self.editor.setFocusPolicy(Qt.StrongFocus)
        self.editor.setContextMenuPolicy(Qt.DefaultContextMenu)
        editor_layout.addWidget(self.editor)

        self.highlighter = SyntaxHighlighter()
        self.highlighter.setDocument(self.editor.document())

        v_splitter.addWidget(editor_container)

        terminal_container = QWidget()
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        
        terminal_header = QLabel(" Terminal")
        terminal_header.setFont(QFont("Inter", 10))
        terminal_header.setContentsMargins(10, 5, 10, 5)
        terminal_layout.addWidget(terminal_header)

        self.terminal_input = QLineEdit()
        self.terminal_input.setFont(QFont("JetBrains Mono", 11))
        self.terminal_input.returnPressed.connect(self.execute_command)
        terminal_layout.addWidget(self.terminal_input)

        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont("JetBrains Mono", 11))
        self.terminal.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        terminal_layout.addWidget(self.terminal)
        
        v_splitter.addWidget(terminal_container)

        h_splitter.setSizes([250, 750])
        v_splitter.setSizes([600, 150])

        self.editor.setFocus()

        find_replace_action = QAction("Find and Replace", self)
        find_replace_action.setShortcut(QKeySequence("Ctrl+H"))
        find_replace_action.triggered.connect(self.show_find_replace)
        self.addAction(find_replace_action)

    def show_find_replace(self):
        find_replace_dialog = FindReplaceDialog(self)
        find_replace_dialog.exec()

    def execute_command(self):
        command = self.terminal_input.text().strip()
        self.terminal_input.clear()
        if command:
            self.terminal.appendPlainText(f"> {command}")
            try:
                if command.startswith("cobra "):
                    filename = command.split(" ", 1)[1]
                    self.run_cobra(filename)
                elif command.startswith("cd "):
                    directory = command.split(" ", 1)[1]
                    os.chdir(directory)
                    self.current_directory = os.getcwd()
                    self.terminal.appendPlainText(f"Changed directory to: {self.current_directory}")
                elif command.startswith("mkdir "):
                    directory = command.split(" ", 1)[1]
                    os.mkdir(directory)
                    self.terminal.appendPlainText(f"Directory created: {directory}")
                elif command.startswith("rm "):
                    target = command.split(" ", 1)[1]
                    os.remove(target)
                    self.terminal.appendPlainText(f"Removed: {target}")
                elif command == "ls" or command == "dir":
                    contents = "\n".join(os.listdir(self.current_directory))
                    self.terminal.appendPlainText(contents)
                elif command == "pwd":
                    self.terminal.appendPlainText(self.current_directory)
                else:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    if result.stdout:
                        self.terminal.appendPlainText(result.stdout)
                    if result.stderr:
                        self.terminal.appendPlainText(f"Error: {result.stderr}")
            except Exception as e:
                self.terminal.appendPlainText(f"Error: {e}")

    def run_cobra(self, filename):
        try:
            if not os.path.isfile(filename):
                self.terminal.appendPlainText(f"Error: File '{filename}' not found")
                return
            self.terminal.appendPlainText(f"Running: {filename}")
            result = subprocess.run(["python3", "-m", "transl", filename], capture_output=True, text=True)
            if result.stdout:
                self.terminal.appendPlainText(result.stdout)
            if result.stderr:
                self.terminal.appendPlainText(f"Error: {result.stderr}")
        except Exception as e:
            self.terminal.appendPlainText(f"Error: {e}")

    def load_theme(self):
        return '''
            QMainWindow, QWidget {
                background-color: #1A1B26;
                color: #A9B1D6;
            }
            
            QToolBar {
                background-color: #1A1B26;
                border-bottom: 1px solid #2F3549;
                padding: 5px;
                spacing: 5px;
            }
            
            QToolBar QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 5px;
            }
            
            QToolBar QToolButton:hover {
                background-color: #2F3549;
            }
            
            QTreeView {
                background-color: #1A1B26;
                border: none;
                padding: 5px;
            }
            
            QTreeView::item {
                padding: 5px;
                border-radius: 4px;
            }
            
            QTreeView::item:hover {
                background-color: #2F3549;
            }
            
            QTreeView::item:selected {
                background-color: #3D59A1;
            }
            
            QTextEdit, QPlainTextEdit {
                background-color: #1A1B26;
                border: none;
                padding: 10px;
                selection-background-color: #3D59A1;
            }
            
            QLabel {
                color: #A9B1D6;
                background-color: #1F2335;
            }
            
            QSplitter::handle {
                background-color: #2F3549;
            }
            
            QSplitter::handle:horizontal {
                width: 1px;
            }
            
            QSplitter::handle:vertical {
                height: 1px;
            }
            
            QScrollBar:vertical {
                background-color: #1A1B26;
                width: 12px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background-color: #2F3549;
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #3D59A1;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            
            Button {
                background-color: #3D59A1;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                color: #FFFFFF;
            }
            
            Button:hover {
                background-color: #4B6BBF;
            }
            
            Button:pressed {
                background-color: #2F3549;
            }
        '''

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", QDir.homePath())
        if folder_path:
            self.file_tree.setRootIndex(self.file_model.index(folder_path))
            self.file_tree.setHidden(False)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath(), "*.*")
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            self.editor.setPlainText(content)
            self.current_file_path = file_path
            self.filename_label.setText(f" {file_path}")

            if self.highlighter:
                self.highlighter.setDocument(self.editor.document())
        except Exception as e:
            self.terminal.appendPlainText(f"Error opening file: {e}")

    def open_selected_file(self, index):
        file_path = self.file_model.filePath(index)
        if not QDir(file_path).exists():
            self.load_file(file_path)

    def new_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "New File", QDir.homePath(), ".cl")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write("")
                self.current_file_path = file_path
                self.filename_label.setText(f" {file_path}")
                self.editor.setPlainText("")
            except Exception as e:
                self.terminal.appendPlainText(f"Error creating file: {e}")

    def save_file(self):
        if not self.current_file_path:
            self.new_file()
            return
            
        try:
            with open(self.current_file_path, 'w') as file:
                file.write(self.editor.toPlainText())
            self.terminal.appendPlainText(f"File saved: {self.current_file_path}")
        except Exception as e:
            self.terminal.appendPlainText(f"Error saving file: {e}")

    def run_file(self):
        if not self.current_file_path:
            self.terminal.appendPlainText("Error: No file is currently open")
            return
            
        try:
            self.terminal.appendPlainText(f"\n--- Running {self.current_file_path} ---\n")
            result = subprocess.run(["python3", "-m", "transl", self.current_file_path], 
                                 capture_output=True, text=True)
            if result.stdout:
                self.terminal.appendPlainText(result.stdout)
            if result.stderr:
                self.terminal.appendPlainText(f"Error: {result.stderr}")
            self.terminal.appendPlainText("\n--- Execution completed ---\n")
        except Exception as e:
            self.terminal.appendPlainText(f"Error executing file: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = CobraLangIDE()
    ide.show()
    sys.exit(app.exec())