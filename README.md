# Temperature Monitoring Software and Controls

## Project Overview
This software project involves using a DHT22 sensor to monitor the temperature of heated copper-coated aluminum plate in low-cost heating mattress for operating rooms in the Dominican Republic. The aim is to ensure accurate temperature readings and to control the heating mattress using a Raspberry Pi 4.

## Physical Considerations
Understanding the thermal properties of the heating mattress and the materials involved is important for determining when to shut off the heating element.

### Key Concepts (WIP)

### Calculations
To determine when to shut off the heating:
- Define the **Temperature Threshold** (37°C ± 0.5°C)
- Measure the current temperature from the DHT22 sensor.
- If the measured contact temperature exceeds the threshold of 43°C, the heating will automatically shut off.

## Real-Time Data Output- Initial Development
The program will continuously display temperature readings in the terminal with an accuracy of ± 0.2°C.

### User Interaction
To allow the user to shut off heating from the terminal, the programs listen for a specific input command.

## UI/UX Design (WIP)
A monitor will display real-time temperature readings and provide controls for the user to adjust the temperature settings and turn off the heating.

### General Features
- **Real-Time Temperature Display**: Show current temperature and humidity readings.
- **Temperature Adjustment**: Allow users to set the desired temperature threshold via a simple interface.
- **Heating Control**: Provide buttons for users to turn the heating mattress on/off easily.

### Considerations
- Design should be user-friendly and accessible, especially for medical personnel.
- Use clear visuals and large buttons for ease of use.
-Implement a warning system to notify the healthcare team of potential hazards with the heating mattress.

## Conclusion
This software provides a robust framework for monitoring and controlling heating mattress for safety and usability in medical environments.

# Project Structure
Outline for organizing the program files and structure:

```plaintext
DHT22_Heating_Mattress_Project/
│
├── src/                    # Source code directory
│   ├── main.py             # Main script to run the program
│   ├── sensor.py           # Module for DHT22 sensor interactions
│   ├── relay.py            # Module for controlling the relay
│   ├── user_interface.py    # Module for terminal interactions
│   └── config.py           # Configuration settings (e.g., temperature thresholds)
│
├── data/                   # Data storage directory
│   ├── logs/               # Log files for temperature readings
│   └── historical_data/    # Historical data storage (if applicable)
│
├── tests/                  # Test directory for unit tests
│   ├── test_sensor.py      # Tests for sensor module
│   ├── test_relay.py       # Tests for relay control module
│   └── test_user_interface.py # Tests for user interface interactions
│
├── docs/                   # Documentation directory
│   ├── project_overview.md  # Overview of the project
│   ├── user_manual.md       # User manual for the software
│   └── technical_spec.md     # Technical specifications and details
│
├── requirements.txt         # List of required Python packages
└── README.md                # Project summary and setup instructions
```

## References
- [Adafruit DHT Sensor Library](https://github.com/adafruit/Adafruit_Python_DHT)
- [Raspberry Pi GPIO Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)