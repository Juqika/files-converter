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
    DARK_STYLE = """ /* As defined in the previous response, based on the image */
    QMainWindow {
        background-color: #101010; 
        font-family: "Segoe UI", Arial, sans-serif; 
    }
    QGroupBox {
        background-color: rgba(40, 40, 40, 0.85); 
        border: 1px solid rgba(70, 70, 70, 0.9); 
        border-radius: 12px; 
        margin-top: 1ex;
        color: #E0E0E0; 
        padding: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 15px;
        padding: 0 5px 5px 5px; 
        color: #B0B0B0; 
        font-size: 14px;
        font-weight: bold;
    }
    QLabel {
        color: #D0D0D0; 
        background-color: transparent; 
    }
    QPushButton {
        background-color: rgba(55, 55, 55, 0.9); 
        color: #E0E0E0;
        border: 1px solid rgba(85, 85, 85, 0.9);
        padding: 10px 15px;
        border-radius: 8px; 
        font-size: 13px;
        font-weight: 500; 
    }
    QPushButton:hover {
        background-color: rgba(70, 70, 70, 0.95); 
        border-color: rgba(100, 100, 100, 0.95);
    }
    QPushButton:pressed {
        background-color: rgba(45, 45, 45, 0.9);
    }
    QPushButton#convertButton {
        background-color: rgba(0, 122, 204, 0.9); 
        color: white;
        font-weight: bold;
    }
    QPushButton#convertButton:hover {
        background-color: rgba(0, 100, 170, 0.95);
    }
    /* QPushButton#themeToggleButton styling can be removed as the button is removed */
    QComboBox {
        background-color: rgba(45, 45, 45, 0.9);
        color: #E0E0E0;
        border: 1px solid rgba(70, 70, 70, 0.9);
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 13px;
    }
    QComboBox::drop-down {
        border: none;
        width: 25px;
    }
    QComboBox QAbstractItemView {
        background-color: #1C1C1C; 
        color: #E0E0E0;
        selection-background-color: rgba(0, 122, 204, 0.7); 
        border: 1px solid #3A3A3A;
        border-radius: 6px;
        padding: 5px;
    }
    QListWidget {
        background-color: rgba(35, 35, 35, 0.85);
        color: #E0E0E0;
        border: 1px solid rgba(60, 60, 60, 0.9);
        border-radius: 10px;
        padding: 8px;
    }
    QListWidget::item {
        padding: 5px;
        border-radius: 4px; 
    }
    QListWidget::item:hover {
        background-color: rgba(70, 70, 70, 0.5);
    }
    QListWidget::item:selected {
        background-color: rgba(0, 122, 204, 0.6);
        color: white;
    }
    QProgressBar {
        border: 1px solid rgba(70, 70, 70, 0.9);
        border-radius: 8px;
        text-align: center;
        color: #E0E0E0;
        background-color: rgba(45, 45, 45, 0.9);
        font-size: 12px;
        height: 22px; 
    }
    QProgressBar::chunk {
        background-color: rgba(0, 122, 204, 0.8); 
        border-radius: 6px;
        margin: 1px;
    }
    DropGroupBox {
        background-color: rgba(30, 30, 30, 0.8); 
        border: 2px dashed rgba(80, 80, 80, 0.9);
        border-radius: 12px;
    }
    DropGroupBox QLabel {
        color: #A0A0A0;
        font-size: 14px;
        font-weight: normal;
    }
    * {
        font-family: "Segoe UI", Arial, sans-serif;
    }
    """

    # LIGHT_STYLE definition removed

    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Converter")
        self.resize(800, 600)
        # self.current_theme = "light" # Removed, dark is default

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Top Bar for Title and Theme Toggle --- REMOVED Theme Toggle
        top_bar_layout = QtWidgets.QHBoxLayout()
        # Title Label (already removed in previous steps)
        top_bar_layout.addStretch(1)
        # Theme Toggle Button - REMOVED
        # self.theme_toggle_button = QtWidgets.QPushButton("🌙")
        # self.theme_toggle_button.setFixedSize(40, 40)
        # self.theme_toggle_button.setObjectName("themeToggleButton")
        # self.theme_toggle_button.setToolTip("Toggle Dark/Light Mode")
        # self.theme_toggle_button.clicked.connect(self.toggle_theme)
        # top_bar_layout.addWidget(self.theme_toggle_button)
        main_layout.addLayout(top_bar_layout)

        # Subtitle Label (already removed in previous steps)

        # File Upload Area with drag-and-drop support
        self.upload_group_box = DropGroupBox("Drop Files Here or")
        # self.upload_group_box.setStyleSheet("QGroupBox { border: 2px dashed gray; margin-top: 1ex; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
        self.upload_group_box.setMinimumHeight(220) # Sizing consistency
        upload_layout = QtWidgets.QVBoxLayout(self.upload_group_box)
        upload_layout.setContentsMargins(20, 20, 20, 20) # Padding
        upload_layout.setSpacing(15) # Spacing between elements

        self.choose_files_button = QtWidgets.QPushButton(QtGui.QIcon.fromTheme("document-open"), "Choose Files") # Added icon
        self.choose_files_button.setIconSize(QtCore.QSize(20, 20))
        # self.choose_files_button.setStyleSheet("padding: 10px; font-size: 14px;") # Basic styling
        upload_layout.addWidget(self.choose_files_button, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        # drag_drop_label = QtWidgets.QLabel("Or drag and drop files here") # Removed, title of groupbox is enough
        # drag_drop_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # upload_layout.addWidget(drag_drop_label, 1, QtCore.Qt.AlignmentFlag.AlignCenter) # Center this label

        # Create QStackedWidget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.upload_group_box)

        # Uploaded Files List (will be added to a container)
        self.uploaded_files_list = DragDropListWidget()
        # self.uploaded_files_list.setStyleSheet("background-color: white; border: 1px solid #cccccc;") # Styling
        self.uploaded_files_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu) # Enable context menu
        self.uploaded_files_list.setSpacing(5) # Spacing between items

        # Create Container Widget for the File List View
        self.file_list_container_widget = QtWidgets.QWidget()
        self.file_list_container_widget.setMinimumHeight(220) # Sizing consistency
        file_list_layout = QtWidgets.QVBoxLayout(self.file_list_container_widget)
        file_list_layout.setContentsMargins(0, 0, 0, 0) # No margins for container, list has its own
        file_list_layout.setSpacing(10) # Spacing
        file_list_layout.addWidget(self.uploaded_files_list) # Add list to container layout

        self.clear_files_button = QtWidgets.QPushButton(QtGui.QIcon.fromTheme("edit-clear"), "Clear & Select New")
        self.clear_files_button.setIconSize(QtCore.QSize(18,18))
        # self.clear_files_button.setStyleSheet(""" 
        # ... (style removed, will be handled by global stylesheet)
        # """)
        file_list_layout.addWidget(self.clear_files_button) # Add button to container layout

        self.stacked_widget.addWidget(self.file_list_container_widget) # Add container to stacked widget

        # Add QStackedWidget to main layout
        main_layout.addWidget(self.stacked_widget)

        # Set initial widget to display
        self.stacked_widget.setCurrentWidget(self.upload_group_box)

        # --- Controls Layout (Output Format and Convert Button) ---
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.setSpacing(15)

        output_format_label = QtWidgets.QLabel("Output Format:")
        self.output_format_combo = QtWidgets.QComboBox()
        self.output_format_combo.addItems(["PNG", "JPG", "PDF", "WEBP", "ICO"]) # Added more items
        self.output_format_combo.setEnabled(False) # Initially disabled
        self.output_format_combo.setMinimumHeight(35) # Consistent height

        controls_layout.addWidget(output_format_label)
        controls_layout.addWidget(self.output_format_combo, 1) # Add stretch factor

        self.convert_button = QtWidgets.QPushButton(QtGui.QIcon.fromTheme("media-playback-start"), "Convert") # Made it an attribute
        self.convert_button.setObjectName("convertButton")
        self.convert_button.setIconSize(QtCore.QSize(20,20))
        self.convert_button.setMinimumHeight(40) # Taller convert button
        # self.convert_button.setStyleSheet(""" 
        # ... (style removed, will be handled by global stylesheet)
        # """)
        controls_layout.addWidget(self.convert_button, 0) # No stretch, fixed size preferred

        main_layout.addLayout(controls_layout)

        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True) # Make text visible
        self.progress_bar.setMinimumHeight(25)
        main_layout.addWidget(self.progress_bar)

        # Status Log REMOVED
        # self.status_log = QtWidgets.QTextEdit()
        # self.status_log.setReadOnly(True)
        # self.status_log.setPlaceholderText("Welcome! Select files to convert.")
        # main_layout.addWidget(self.status_log)

        # Instantiate FileHandler (ensure it's after UI elements it needs are created)
        self.file_handler = FileHandler(self)

        # Connect signals (theme toggle connection removed)
        self.upload_group_box.files_dropped.connect(self.handle_files_selected)
        self.choose_files_button.clicked.connect(self.trigger_file_dialog_and_process)
        self.clear_files_button.clicked.connect(self.show_upload_view)
        self.uploaded_files_list.customContextMenuRequested.connect(self.show_file_list_context_menu)

        self.apply_theme() # Apply dark theme by default

    # def toggle_theme(self): # REMOVED
    #     if self.current_theme == "light":
    #         self.current_theme = "dark"
    #         self.theme_toggle_button.setText("☀️")
    #     else:
    #         self.current_theme = "light"
    #         self.theme_toggle_button.setText("🌙")
    #     self.apply_theme(self.current_theme)

    def apply_theme(self): # Modified to only apply dark theme
        self.setStyleSheet(self.DARK_STYLE)
        # Potentially re-style child widgets if necessary or if they don't inherit

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
            # Log message REMOVED
            # self.status_log.append(f"Processed and displayed {len(file_paths)} file(s).")
        # else:
            # self.status_log.append("No files were selected or provided to display.") # Log message REMOVED

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
        # self.status_log.append("Ready to upload new files.") # Log message REMOVED

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
