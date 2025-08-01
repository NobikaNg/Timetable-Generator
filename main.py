import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath('src'))

from src.ui.ui_display import whole_ui_display

if __name__ == "__main__":
    whole_ui_display()
