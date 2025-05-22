import sys
from PySide6.QtWidgets import QApplication

# Relative imports based on the project structure
# main.py is in file_converter_app/app/
from app.ui.main_window import MainWindow
from app.logic.file_handler import FileHandler
from app.logic.converter import FileConverter

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_win = MainWindow()

    # Instantiate handlers/controllers
    file_handler = FileHandler(main_win)
    file_converter = FileConverter(main_win)

    # Connect signals to slots
    # These connections rely on choose_files_button and convert_button 
    # being attributes of the MainWindow instance, which was addressed by modifying main_window.py.
    
    try:
        main_win.choose_files_button.clicked.connect(file_handler.open_file_dialog)
        main_win.convert_button.clicked.connect(file_converter.start_conversion)
        main_win.uploaded_files_list.files_dropped.connect(file_handler.process_selected_files)
        main_win.upload_group_box.files_dropped.connect(file_handler.process_selected_files)
    except AttributeError as e:
        print(f"Error connecting signals in main.py: {e}. "
              f"This indicates that 'choose_files_button' or 'convert_button' "
              f"might still not be correctly defined as attributes in 'main_window.py'. "
              f"Please ensure they are defined as 'self.choose_files_button' etc. in 'main_window.py'.", file=sys.stderr)
        # Exit if essential connections cannot be made, as the app won't be functional.
        sys.exit(1) 

    # The file_list_widget.itemSelectionChanged signal is connected 
    # in FileHandler.__init__ (verified in previous steps).
    # e.g., self.file_list_widget.itemSelectionChanged.connect(self.handle_file_list_selection_change)

    main_win.show()
    sys.exit(app.exec())
