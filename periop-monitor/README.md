## PeriOp Monitor

A Tkinter-based GUI application for monitoring perioperative temperature data in real time. Includes a digital temperature display, toggle buttons, monitor mode navigation, and a status panel.

## Installation

1. Clone the repo:
- `git clone <your_repo>`
- `cd periop-monitor`
2. Install dependencies:
- `pip install -r requirements.txt`

## Requirements

- Python 3.8+
- `pip` (Python package installer)
- Linux/macOS/Windows with GUI support

## Running the App

From the project root:
- Use `python3 main.py` to run the app.

Make sure you're in the environment where the dependencies are installed.

## Folder Structure

``` 
periop-monitor/
├── assets/ # Images for display and buttons
├── app.py # Main application script
├── temperature_sensor_backend.py
├── utils/
│ └── temperature_utils.py
├── HomeScreen.py # Home screen UI logic
├── MonitorModeScreen.py # Monitor mode screen UI
├── requirements.txt
└── README.md 
```

## Key Modules

- `HomeScreen.py`: Controls the main temperature display, toggle buttons, and event handling.
- `MonitorModeScreen.py`: Stub or secondary screen for expansion.
- `temperature_sensor_backend.py`: Gets real-time temperature values from a sensor or mock.
- `update_temperature_display()`: Digit-by-digit rendering with fallbacks like --.-C.

## Adding New Screens

To add a new screen:
1. Create a new file (e.g., `HelpScreen.py`) subclassing `tk.Frame`.
2. Instantiate and store it in `PeriOpApp.__init__()`.
3. Use `show_screen()` to navigate to it.