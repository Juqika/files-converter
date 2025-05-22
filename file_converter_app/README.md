# File Converter Application

A desktop application built with Python and PySide6 to convert files from one format to another.

## Features (Current - Initial Setup)

*   Basic UI structure for file conversion.
*   File selection (single/multiple).
*   Automatic detection of file type (basic, based on extension/mimetype).
*   Dynamic update of available output formats based on selected file type (placeholder).
*   Placeholder for file conversion logic with progress simulation.
*   "Save As" dialog for converted files.
*   Status messages and progress bar.

## Project Structure

```
file_converter_app/
├── app/
│   ├── __init__.py
│   ├── main.py             # Main application entry point
│   ├── logic/
│   │   ├── __init__.py
│   │   ├── converter.py    # Conversion logic
│   │   └── file_handler.py # File selection and processing logic
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_window.py  # Main application window UI
│   └── utils/
│       └── __init__.py     # Utility functions (currently empty)
├── assets/                 # For icons, images (currently empty)
├── tests/                  # For unit tests (currently empty)
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Getting Started

### Prerequisites

*   Python 3.7+
*   pip (Python package installer)

### Installation

1.  **Clone the repository (or download the source code):**
    ```bash
    # git clone <repository_url>
    # cd file_converter_app
    ```
    (If not using git, simply navigate to the `file_converter_app` directory).

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

```bash
python app/main.py
```

## Future Enhancements (Planned from Issue)

*   Implement actual file conversion for various types (images, documents, audio, video).
*   Full drag-and-drop support for file uploads.
*   Batch processing capabilities with individual file controls (delete, specific output format).
*   Dark mode toggle.
*   Persistent settings.
*   Robust error handling for unsupported files and conversion failures.
*   Detailed item view in the file list (size, type, output format controls per file).
```
