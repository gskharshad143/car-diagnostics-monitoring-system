
"""
@file main.py
@brief Main script for reading diagnostics from CSV and processing cars.

Example CSV format:
CarID,DiagnosticType,Value
CAR001,RPM,3200
CAR001,Engine Load,75
CAR001,Coolant Temperature,95
CAR002,RPM,4000
CAR002,Engine Load,90
CAR002,Coolant Temperature,110

Expected Output Format:
Car: CAR001
Performance Score: 82.5
Alerts: None

Car: CAR002
Performance Score: 70.0
Alerts: Engine Stress Detected, High Coolant Temperature
"""


import time
from garage_monitor import GarageMonitor

def main() -> None:
    """
    @brief Runs the garage monitor in both single-threaded and multi-threaded modes.
    """
    monitor = GarageMonitor('diagnostics.csv')
    monitor.load_diagnostics()

    print("--- Single-threaded Execution ---")
    start = time.time()
    monitor.monitor()
    single_threaded_time = time.time() - start
    print(f"Single-threaded execution time: {single_threaded_time:.4f} seconds\n")

    # Reload diagnostics for fair comparison
    monitor = GarageMonitor('diagnostics.csv')
    monitor.load_diagnostics()
    print("--- Multi-threaded Execution ---")
    start = time.time()
    monitor.simulate_real_time_updates(update_count=10, delay=0.01)
    monitor.monitor()
    multi_threaded_time = time.time() - start
    print(f"Multi-threaded execution time: {multi_threaded_time:.4f} seconds\n")

if __name__ == "__main__":
    main()
