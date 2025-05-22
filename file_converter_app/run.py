import os
import sys
import subprocess
import importlib.util

def check_requirements():
    """Check if all requirements are installed"""
    try:
        # Try to import PySide6 as a test
        import PySide6
        return True
    except ImportError:
        return False

def install_requirements():
    """Install requirements from requirements.txt"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def main():
    # Check if requirements are installed
    if not check_requirements():
        print("First time setup: Installing requirements...")
        install_requirements()
        print("Requirements installed successfully!")

    # Run the main application
    print("Starting the application...")
    from app.main import main as app_main
    app_main()

if __name__ == "__main__":
    main() 