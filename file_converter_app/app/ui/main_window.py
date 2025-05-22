import sys
from PySide6 import QtWidgets, QtGui, QtCore
from app.ui.drag_drop_list_widget import DragDropListWidget
from app.logic.file_handler import FileHandler # Added import

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
        self.upload_group_box.setMinimumHeight(200) # Sizing consistency
        upload_layout = QtWidgets.QVBoxLayout(self.upload_group_box)
        upload_layout.setContentsMargins(15, 15, 15, 15) # Padding
        upload_layout.setSpacing(10) # Spacing between elements

        self.choose_files_button = QtWidgets.QPushButton("Choose Files") # Made it an attribute
        self.choose_files_button.setStyleSheet("padding: 8px;") # Basic styling
        upload_layout.addWidget(self.choose_files_button, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        drag_drop_label = QtWidgets.QLabel("Or drag and drop files here")
        drag_drop_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        upload_layout.addWidget(drag_drop_label, 1, QtCore.Qt.AlignmentFlag.AlignCenter) # Center this label

        # Create QStackedWidget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.upload_group_box)

        # Uploaded Files List (will be added to a container)
        self.uploaded_files_list = DragDropListWidget()
        self.uploaded_files_list.setStyleSheet("background-color: white; border: 1px solid #cccccc;") # Styling
        self.uploaded_files_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu) # Enable context menu

        # Create Container Widget for the File List View
        self.file_list_container_widget = QtWidgets.QWidget()
        self.file_list_container_widget.setMinimumHeight(200) # Sizing consistency
        file_list_layout = QtWidgets.QVBoxLayout(self.file_list_container_widget)
        file_list_layout.setContentsMargins(10, 10, 10, 10) # Padding
        file_list_layout.setSpacing(10) # Spacing
        file_list_layout.addWidget(self.uploaded_files_list) # Add list to container layout

        self.clear_files_button = QtWidgets.QPushButton("Clear Files & Select New")
        self.clear_files_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0; /* Light gray */
                color: black;
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #d0d0d0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        file_list_layout.addWidget(self.clear_files_button) # Add button to container layout

        self.stacked_widget.addWidget(self.file_list_container_widget) # Add container to stacked widget

        # Add QStackedWidget to main layout
        main_layout.addWidget(self.stacked_widget)

        # Set initial widget to display
        self.stacked_widget.setCurrentWidget(self.upload_group_box)

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

        # Instantiate FileHandler (ensure it's after UI elements it needs are created)
        self.file_handler = FileHandler(self)

        # Connect signals
        self.upload_group_box.files_dropped.connect(self.handle_files_selected)
        self.choose_files_button.clicked.connect(self.trigger_file_dialog_and_process)
        self.clear_files_button.clicked.connect(self.show_upload_view) # Connect clear button
        self.uploaded_files_list.customContextMenuRequested.connect(self.show_file_list_context_menu) # Connect context menu signal

    def show_file_list_context_menu(self, position):
        item = self.uploaded_files_list.itemAt(position)
        if item:
            menu = QtWidgets.QMenu(self)
            remove_action = menu.addAction("Remove File")
            
            # Show the menu and get the chosen action
            action = menu.exec(self.uploaded_files_list.mapToGlobal(position))
            
            if action == remove_action:
                row = self.uploaded_files_list.row(item)
                self.file_handler.remove_file_at_row(row) # Call FileHandler method

    def handle_files_selected(self, file_paths):
        if file_paths: # Ensure there are files to process
            self.file_handler.process_selected_files(file_paths)
            self.stacked_widget.setCurrentWidget(self.file_list_container_widget) # Switch to container
            # Log message after switching view and processing
            self.status_log.append(f"Processed and displayed {len(file_paths)} file(s).")
        else:
            self.status_log.append("No files were selected or provided to display.")

    def trigger_file_dialog_and_process(self):
        returned_file_paths = self.file_handler.open_file_dialog()
        # open_file_dialog now returns a list (empty if cancelled)
        # It no longer calls process_selected_files directly
        if returned_file_paths: # Check if the list is not empty
            self.handle_files_selected(returned_file_paths)
        # If empty, open_file_dialog in FileHandler already logs "No files selected via dialog."

    def show_upload_view(self):
        self.file_handler.clear_all_files() # Call FileHandler method
        self.stacked_widget.setCurrentWidget(self.upload_group_box)
        self.status_log.append("Ready to upload new files.") # Update status

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
