from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QWidget,
                              QPushButton, QFileDialog, QTextEdit, QTreeView, QFileSystemModel, 
                              QSplitter, QToolBar, QLabel, QPlainTextEdit)
from PySide6.QtGui import QFont, QAction, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import Qt, QDir, QSize
import sys
import subprocess

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
        editor_layout.addWidget(self.editor)

        self.highlighter = SyntaxHighlighter()

        v_splitter.addWidget(editor_container)

        terminal_container = QWidget()
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        
        terminal_header = QLabel(" Terminal")
        terminal_header.setFont(QFont("Inter", 10))
        terminal_header.setContentsMargins(10, 5, 10, 5)
        terminal_layout.addWidget(terminal_header)
        
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont("JetBrains Mono", 11))
        self.terminal.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        terminal_layout.addWidget(self.terminal)
        
        v_splitter.addWidget(terminal_container)

        h_splitter.setSizes([250, 750])
        v_splitter.setSizes([600, 150])

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

            if file_path.endswith('.cl'):
                if self.highlighter:
                    self.highlighter.setDocument(self.editor.document())
            else:
                if self.highlighter:
                    self.highlighter.setDocument(None)
        except Exception as e:
            self.terminal.appendPlainText(f"Error opening file: {e}")

    def open_selected_file(self, index):
        file_path = self.file_model.filePath(index)
        if not QDir(file_path).exists():
            self.load_file(file_path)

    def new_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "New File", QDir.homePath(), "*.*")
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