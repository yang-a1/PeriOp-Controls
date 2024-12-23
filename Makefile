# Python interpreter (adjust this if you use a different version)
PYTHON = python3

# Main application file for the executable
APP_SCRIPT = app.py

# The files for your old and new sensor code
OLD_SENSOR_SCRIPT = temperature_sensor.py
NEW_SENSOR_RELAY_SCRIPT = temperature_sensor_relay.py

# The virtual environment directory (if you're using one)
VENV_DIR = venv

# The name of the executable
APP_EXE = dist/app.exe

# Default target
all: run_app_exe

# Create a virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Build the executable using pyinstaller
build_exe:
	@echo "Building executable for app.py..."
	$(VENV_DIR)/bin/pip install pyinstaller
	$(VENV_DIR)/bin/pyinstaller --onefile $(APP_SCRIPT)

# Run the executable
run_app_exe: $(APP_EXE)
	@echo "Running the app executable..."
	./$(APP_EXE)

# Run the old temperature sensor code
run_old_sensor:
	@echo "Running old temperature sensor script..."
	$(VENV_DIR)/bin/python $(OLD_SENSOR_SCRIPT)

# Run the new temperature sensor relay code
run_new_sensor:
	@echo "Running new temperature sensor relay script..."
	$(VENV_DIR)/bin/python $(NEW_SENSOR_RELAY_SCRIPT)

# Install dependencies (useful for setting up the environment without making a new venv)
install_requirements:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

# Clean up virtual environment and build artifacts
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -rf dist build __pycache__ *.spec

# Lint the code (if you have pylint installed and a .pylintrc file)
lint:
	@echo "Running linter..."
	$(VENV_DIR)/bin/python -m pylint $(OLD_SENSOR_SCRIPT) $(NEW_SENSOR_RELAY_SCRIPT) $(APP_SCRIPT)

# Help command to display options
help:
	@echo "Makefile commands:"
	@echo "  setup                - Set up virtual environment and install dependencies"
	@echo "  build_exe            - Build an executable for app.py"
	@echo "  run_app_exe          - Run the app executable"
	@echo "  run_old_sensor       - Run the old temperature sensor script"
	@echo "  run_new_sensor       - Run the new temperature sensor relay script"
	@echo "  install_requirements - Install dependencies from requirements.txt"
	@echo "  clean                - Remove the virtual environment and build artifacts"
	@echo "  lint                 - Run linter on the scripts"
	@echo "  help                 - Show this help message"

# Ensure the executable depends on app.py
$(APP_EXE): $(APP_SCRIPT)
	@$(MAKE) build_exe