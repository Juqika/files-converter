import os
import mimetypes
from PySide6 import QtWidgets, QtCore

class FileHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        # Ensure the file list widget name matches the one in main_window.py
        # In main_window.py, it's self.uploaded_files_list
        self.file_list_widget = self.main_window.uploaded_files_list
        self.output_format_combo = self.main_window.output_format_combo
        self.status_log = self.main_window.status_log

        # Connect signals
        self.file_list_widget.itemSelectionChanged.connect(self.handle_file_list_selection_change)

    def _get_human_readable_size(self, size_in_bytes):
        if size_in_bytes < 1024:
            return f"{size_in_bytes} B"
        elif size_in_bytes < 1024 * 1024:
            return f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 * 1024 * 1024:
            return f"{size_in_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"

    def _get_simplified_file_type(self, file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith("image/"):
                return f"{mime_type.split('/')[1].upper()} Image"
            elif mime_type == "application/pdf":
                return "PDF Document"
            elif mime_type == "text/plain":
                return "Text Document"
            # Add more specific types as needed
            return mime_type # Fallback to full MIME type
        else:
            ext = os.path.splitext(file_path)[1].lower()
            if ext:
                return f"{ext[1:].upper()} File" # e.g. ".PNG" -> "PNG File"
            return "Unknown Type"

    def open_file_dialog(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self.main_window,
            "Select Files to Convert",
            "",  # Start directory (empty means last used or default)
            "All Files (*);;Images (*.png *.jpg *.jpeg *.bmp *.webp);;Documents (*.pdf *.docx *.txt)" 
        )
        if file_paths:
            self.status_log.append(f"Selected {len(file_paths)} file(s).")
            self.process_selected_files(file_paths)
        else:
            self.status_log.append("No files selected.")

    def process_selected_files(self, file_paths):
        for file_path in file_paths:
            if not os.path.exists(file_path):
                self.status_log.append(f"Error: File not found - {file_path}")
                continue
            
            file_name = os.path.basename(file_path)
            file_size_bytes = os.path.getsize(file_path)
            file_size_str = self._get_human_readable_size(file_size_bytes)
            file_type_str = self._get_simplified_file_type(file_path) # Simplified type

            self.add_file_to_list(file_name, file_size_str, file_type_str, file_path)
        
        self.update_output_formats_for_selection() # Update based on current selection (or lack thereof)

    def add_file_to_list(self, file_name, file_size_str, file_type_str, original_path):
        display_text = f"{file_name} ({file_type_str}, {file_size_str})"
        item = QtWidgets.QListWidgetItem(display_text)
        item.setData(QtCore.Qt.ItemDataRole.UserRole, original_path) # Store full path
        # Store the simplified file type string for easier access later
        item.setData(QtCore.Qt.ItemDataRole.UserRole + 1, file_type_str) 
        self.file_list_widget.addItem(item)

    def get_output_formats(self, simplified_file_type):
        # This uses the simplified_file_type (e.g., "PNG Image", "PDF Document")
        if "Image" in simplified_file_type: # Covers PNG, JPG, BMP, WEBP etc.
            return ["PNG", "JPG", "BMP", "WebP"]
        elif "PDF Document" == simplified_file_type:
            return ["PDF (Optimize)", "DOCX", "TXT"]
        # Add more specific conversions here
        # e.g. "DOCX Document" -> ["PDF", "TXT"]
        else:
            return ["N/A"] # Default for unknown or unsupported types

    def update_output_formats_for_selection(self):
        selected_items = self.file_list_widget.selectedItems()
        self.output_format_combo.clear()

        if len(selected_items) == 1:
            item = selected_items[0]
            # Retrieve the stored simplified file type
            simplified_file_type = item.data(QtCore.Qt.ItemDataRole.UserRole + 1)
            
            if simplified_file_type:
                formats = self.get_output_formats(simplified_file_type)
                if formats and formats[0] != "N/A":
                    self.output_format_combo.addItems(formats)
                    self.output_format_combo.setEnabled(True)
                    self.status_log.append(f"Available output formats updated for {item.text().split(' (')[0]}.")
                else:
                    self.output_format_combo.addItem("--No conversions available--")
                    self.output_format_combo.setEnabled(False)
                    self.status_log.append(f"No conversion options for {item.text().split(' (')[0]}.")
            else: # Should not happen if data is stored correctly
                self.output_format_combo.addItem("--Unknown file type--")
                self.output_format_combo.setEnabled(False)
        elif len(selected_items) > 1:
            self.output_format_combo.addItem("--Select a single file for options--")
            self.output_format_combo.setEnabled(False)
            self.status_log.append("Select a single file to see conversion options.")
        else: # No items selected
            self.output_format_combo.addItem("--Select a file--")
            self.output_format_combo.setEnabled(False)
            # self.status_log.append("No file selected. Output options cleared.") # Can be noisy

    def handle_file_list_selection_change(self):
        self.update_output_formats_for_selection()

# Example of how to connect the button in main_window.py (for reference, not part of this file):
# from .logic.file_handler import FileHandler
# ...
# self.file_handler = FileHandler(self)
# self.choose_files_button.clicked.connect(self.file_handler.open_file_dialog)
# Note: The choose_files_button is not directly accessible from FileHandler.
# The main_window.py should connect its button to file_handler.open_file_dialog.
# The task was to connect itemSelectionChanged, which is done in __init__.

