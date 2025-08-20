"""
@file garage_monitor.py
@brief GarageMonitor module for monitoring multiple cars.
"""

import csv
import threading
import time
from typing import List
from car import Car, SCORE_THRESHOLD
from diagnostic import Diagnostic


class GarageMonitor:
    """
    @class GarageMonitor
    @brief Monitors a fleet of cars using diagnostic data.
    """

    def __init__(self, csv_path: str) -> None:
        """
        @brief Constructor for GarageMonitor class.
        @param csv_path Path to diagnostics CSV file.
        """
        self.csv_path = csv_path
        self.cars: List[Car] = []
        self.lock = threading.Lock()

    def load_diagnostics(self) -> None:
        """
        @brief Loads diagnostics from a CSV file with validation and error handling.
        """
        car_dict = {}
        try:
            with open(self.csv_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    car_id = row.get('CarID')
                    dtype = row.get('DiagnosticType')
                    value = row.get('Value')
                    if not car_id or not dtype or value is None:
                        continue
                    if car_id not in car_dict:
                        car_dict[car_id] = {}
                    car_dict[car_id][dtype] = value
            for car_id, diags in car_dict.items():
                try:
                    rpm = int(diags.get('RPM')) if diags.get('RPM') is not None else None
                    load = float(diags.get('Engine Load')) if diags.get('Engine Load') is not None else None
                    temp = float(diags.get('Coolant Temperature')) if diags.get('Coolant Temperature') is not None else None
                    diagnostic = Diagnostic(rpm, load, temp)
                    car = Car(car_id, diagnostic)
                    self.cars.append(car)
                except Exception as e:
                    print(f"Error parsing car {car_id}: {e}")
            if not self.cars:
                raise Exception("No valid diagnostics found in CSV.")
        except FileNotFoundError:
            print(f"CSV file not found: {self.csv_path}")
            raise
        except Exception as e:
            print(f"Error reading CSV: {e}")
            raise

    def simulate_real_time_updates(self, update_count=5, delay=0.05):
        """
        @brief Simulates real-time updates to diagnostics for each car using threads.
        @param update_count Number of updates per car.
        @param delay Delay between updates in seconds.
        """
        threads = []
        for car in self.cars:
            t = threading.Thread(target=self._update_car_diagnostics, args=(car, update_count, delay))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def _update_car_diagnostics(self, car, update_count, delay):
        """
        @brief Internal method to update car diagnostics in a thread.
        @param car Car object to update.
        @param update_count Number of updates.
        @param delay Delay between updates in seconds.
        """
        import random
        for _ in range(update_count):
            with self.lock:
                # Simulate small random changes
                if car.diagnostic.rpm is not None:
                    car.diagnostic.rpm += random.randint(-10, 10)
                if car.diagnostic.load is not None:
                    car.diagnostic.load += random.uniform(-0.5, 0.5)
                if car.diagnostic.temp is not None:
                    car.diagnostic.temp += random.uniform(-0.2, 0.2)
            time.sleep(delay)

    def monitor(self) -> None:
        """
        @brief Prints each car's diagnostics in the required format. Uses lock for safe aggregation.
        """
        for car in self.cars:
            with self.lock:
                score = car.compute_score()
                alerts = []
                if score is None:
                    alerts.append("Sensor Failure Detected")
                else:
                    if score < SCORE_THRESHOLD:
                        alerts.append("Engine Stress Detected")
                    # Check for high coolant temperature
                    if car.diagnostic.temp is not None and car.diagnostic.temp > 105:
                        alerts.append("High Coolant Temperature")
                print(f"Car: {car.car_id}")
                print(f"Performance Score: {score:.1f}" if score is not None else "Performance Score: N/A")
                print(f"Alerts: {', '.join(alerts) if alerts else 'None'}\n")
