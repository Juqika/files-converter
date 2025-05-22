import time
import os
from PySide6 import QtWidgets, QtCore, QtGui
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter

class FileConverter:
    def __init__(self, main_window):
        self.main_window = main_window
        self.status_log = self.main_window.status_log
        self.progress_bar = self.main_window.progress_bar
        self.file_list_widget = self.main_window.uploaded_files_list # Matches main_window.py
        self.output_format_combo = self.main_window.output_format_combo

    def start_conversion(self):
        selected_items = self.file_list_widget.selectedItems()

        if not selected_items:
            self.status_log.append("Error: No file selected for conversion.")
            QtWidgets.QMessageBox.warning(self.main_window, "Conversion Error", "Please select a file to convert.")
            return

        if len(selected_items) > 1:
            self.status_log.append("Error: Please select only one file for conversion.")
            QtWidgets.QMessageBox.warning(self.main_window, "Conversion Error", "Please select only a single file to convert.")
            return
            
        item = selected_items[0]
        input_file_path = item.data(QtCore.Qt.ItemDataRole.UserRole) # Get stored original path

        if not input_file_path or not os.path.exists(input_file_path):
            self.status_log.append(f"Error: Invalid or non-existent input file path for {item.text()}.")
            QtWidgets.QMessageBox.critical(self.main_window, "Conversion Error", f"The file {item.text()} could not be found or is invalid.")
            return

        selected_output_format = self.output_format_combo.currentText()
        
        invalid_formats = ["N/A", "--Select a single file for options--", "--No conversions available--", "--Select a file--", "--Unknown file type--", ""]
        if not selected_output_format or selected_output_format in invalid_formats :
            self.status_log.append("Error: No output format selected or format is invalid.")
            QtWidgets.QMessageBox.warning(self.main_window, "Conversion Error", "Please select a valid output format.")
            return

        base_name = os.path.splitext(os.path.basename(input_file_path))[0]
        extension = selected_output_format.lower()
        suggested_file_name = f"{base_name}_converted.{extension}"
        
        # Prepare filter string for QFileDialog
        filter_string = f"{selected_output_format} Files (*.{extension});;All Files (*)"

        output_file_path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self.main_window,
            "Save Converted File",
            suggested_file_name, # Default file name
            filter_string
        )

        if not output_file_path:
            self.status_log.append("Conversion cancelled by user.")
            return

        # Ensure the output file has the correct extension if user manually changed it or removed it
        if not output_file_path.lower().endswith(f".{extension}"):
            output_file_path += f".{extension}"
            
        self.perform_conversion(input_file_path, output_file_path, selected_output_format)

    def perform_conversion(self, input_file_path, output_file_path, output_format):
        input_filename = os.path.basename(input_file_path)
        output_filename = os.path.basename(output_file_path)

        self.status_log.append(f"Starting conversion of {input_filename} to {output_format.upper()}...")
        self.progress_bar.setValue(0)
        self.main_window.setDisabled(True) # Disable UI during conversion

        try:
            # Get file extension
            input_ext = os.path.splitext(input_file_path)[1].lower()
            
            # Handle image conversions
            if input_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']:
                self.convert_image(input_file_path, output_file_path, output_format)
            # Handle PDF conversions
            elif input_ext == '.pdf':
                self.convert_pdf(input_file_path, output_file_path, output_format)
            else:
                raise ValueError(f"Unsupported input file type: {input_ext}")

            self.status_log.append(f"Successfully converted {input_filename} to {output_filename}.")
            QtWidgets.QMessageBox.information(
                self.main_window,
                "Conversion Successful!",
                f"File '{input_filename}' was successfully converted and saved as '{output_filename}'."
            )

        except Exception as e:
            self.status_log.append(f"Error during conversion: {str(e)}")
            QtWidgets.QMessageBox.critical(
                self.main_window,
                "Conversion Error",
                f"An error occurred during conversion: {str(e)}"
            )
        finally:
            self.main_window.setDisabled(False)
            self.progress_bar.setValue(0) # Reset progress bar

    def convert_image(self, input_path, output_path, output_format):
        try:
            # Open the image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary (for PNG with transparency)
                if img.mode in ('RGBA', 'LA') and output_format.lower() in ('jpg', 'jpeg'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')

                # Handle JPEG format specifically
                if output_format.lower() in ('jpg', 'jpeg'):
                    # Save JPEG with quality setting
                    img.save(output_path, format='JPEG', quality=95)
                else:
                    # Save other formats
                    img.save(output_path, format=output_format.upper())
                
                self.progress_bar.setValue(100)

        except Exception as e:
            raise Exception(f"Image conversion failed: {str(e)}")

    def convert_pdf(self, input_path, output_path, output_format):
        try:
            if output_format.lower() == 'pdf':
                # PDF to PDF (optimize)
                reader = PdfReader(input_path)
                writer = PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                self.progress_bar.setValue(100)
            else:
                raise ValueError(f"Unsupported PDF conversion to {output_format}")

        except Exception as e:
            raise Exception(f"PDF conversion failed: {str(e)}")
