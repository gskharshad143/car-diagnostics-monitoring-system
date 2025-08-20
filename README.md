# Car Diagnostics Monitoring System

## Introduction

The Car Diagnostics Monitoring System is a Python project designed to monitor and analyze key car diagnostics for multiple vehicles. It tracks metrics such as RPM, Engine Load, and Coolant Temperature, computes performance scores, and generates alerts for engine stress or sensor failures. The system is modular, beginner-friendly, and uses only the Python standard library.

## Project Structure

```
car.py
 diagnostic.py
 garage_monitor.py
 main.py
 test_main.py
 diagnostics.csv
```

- **car.py**: Defines the `Car` class for managing diagnostics and computing performance scores.
- **diagnostic.py**: Defines the `Diagnostic` class for validating and storing diagnostic readings.
- **garage_monitor.py**: Defines the `GarageMonitor` class for managing multiple cars and checking alerts.
- **main.py**: Main script for reading diagnostics from CSV, processing cars, and printing results.
- **test_main.py**: Pytest-based unit tests for all core functionality.
- **diagnostics.csv**: Sample input data for car diagnostics.

## Classes and Functions

### Diagnostic (diagnostic.py)
- **Fields:**
  - `rpm` (int): Engine RPM
  - `load` (float): Engine Load
  - `temp` (float): Coolant Temperature
- **Methods:**
  - `is_valid()`: Checks if all diagnostic values are present and valid.

### Car (car.py)
- **Fields:**
  - `car_id` (str): Car identifier (e.g., CAR001)
  - `diagnostic` (Diagnostic): Diagnostic object
- **Methods:**
  - `compute_score()`: Computes the car's performance score using the formula:
    ```python
    score = 100 - (rpm / 100 + load * 0.5 + (temp - 90) * 2)
    ```
    Returns score as a float (rounded to 1 decimal place).

### GarageMonitor (garage_monitor.py)
- **Fields:**
  - `csv_path` (str): Path to diagnostics CSV
  - `cars` (List[Car]): List of Car objects
- **Methods:**
  - `load_diagnostics()`: Loads diagnostics from CSV, groups by CarID, and creates Car objects.
  - `monitor()`: Prints each car's performance score and alerts in the required format.

### main.py
- Loads diagnostics from `diagnostics.csv`.
- Uses `GarageMonitor` to process all cars and print results.
- Example usage:
  ```python
  if __name__ == "__main__":
      main()
  ```

## Sample Input/Output

### Sample CSV Input (`diagnostics.csv`)
```csv
CarID,DiagnosticType,Value
CAR001,RPM,3200
CAR001,Engine Load,75
CAR001,Coolant Temperature,95
CAR002,RPM,4000
CAR002,Engine Load,90
CAR002,Coolant Temperature,110
```

### Example Console Output
```
Car: CAR001
Performance Score: 82.5
Alerts: None

Car: CAR002
Performance Score: 70.0
Alerts: Engine Stress Detected, High Coolant Temperature
```

## Testing

Unit tests are provided in `test_main.py` using pytest. Key scenarios tested:
- Severe engine stress alert when score < 40
- Sensor failure alert when a diagnostic is missing
- Garage average score calculation
- No alert on boundary score
- Exception raised for empty CSV

## How It Works

1. **Prepare diagnostics.csv** with car diagnostic data in the required format.
2. **Run main.py** to process the data and print results.
3. **Check alerts and scores** for each car in the console output.
4. **Run tests** with `pytest test_main.py` to validate all core logic.

## Notes
- Only Python standard library is used (no external dependencies).
- All code follows PEP8 and best practices.
- Output format is strictly controlled for clarity and consistency.

---

For any questions or improvements, feel free to update the code or add more test cases!
