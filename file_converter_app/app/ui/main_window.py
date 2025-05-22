import sys
from PySide6 import QtWidgets, QtGui, QtCore
from app.ui.drag_drop_list_widget import DragDropListWidget

class DropGroupBox(QtWidgets.QGroupBox):
    files_dropped = QtCore.Signal(list)

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_paths = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_paths.append(url.toLocalFile())
            if file_paths:
                self.files_dropped.emit(file_paths)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Converter")
        self.resize(800, 600)

        # Main widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        # Title Label
        title_label = QtWidgets.QLabel("File Converter")
        title_font = QtGui.QFont()
        title_font.setBold(True)
        title_font.setPointSize(24)
        title_label.setFont(title_font)
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle Label
        subtitle_label = QtWidgets.QLabel("Easily convert files from one format to another")
        subtitle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # File Upload Area with drag-and-drop support
        self.upload_group_box = DropGroupBox("Upload Files")
        self.upload_group_box.setStyleSheet("QGroupBox { border: 2px dashed gray; margin-top: 1ex; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
        upload_layout = QtWidgets.QVBoxLayout(self.upload_group_box)

        self.choose_files_button = QtWidgets.QPushButton("Choose Files") # Made it an attribute
        upload_layout.addWidget(self.choose_files_button)

        drag_drop_label = QtWidgets.QLabel("Or drag and drop files here")
        drag_drop_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        upload_layout.addWidget(drag_drop_label)
        
        main_layout.addWidget(self.upload_group_box)

        # Uploaded Files List with drag-and-drop support
        self.uploaded_files_list = DragDropListWidget()
        main_layout.addWidget(self.uploaded_files_list)

        # Output Format Selector
        output_format_layout = QtWidgets.QHBoxLayout()
        output_format_label = QtWidgets.QLabel("Output Format:")
        self.output_format_combo = QtWidgets.QComboBox()
        self.output_format_combo.addItems(["PNG", "JPG", "PDF"]) # Placeholder items
        self.output_format_combo.setEnabled(False) # Initially disabled
        output_format_layout.addWidget(output_format_label)
        output_format_layout.addWidget(self.output_format_combo)
        main_layout.addLayout(output_format_layout)

        # Convert Button
        self.convert_button = QtWidgets.QPushButton("Convert") # Made it an attribute
        self.convert_button.setObjectName("convertButton")
        self.convert_button.setStyleSheet("""
            QPushButton#convertButton {
                background-color: #4CAF50; /* Green */
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton#convertButton:hover {
                background-color: #45a049;
            }
        """)
        main_layout.addWidget(self.convert_button)

        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # Status Log
        self.status_log = QtWidgets.QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.setPlaceholderText("Welcome! Select files to convert.")
        main_layout.addWidget(self.status_log)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
