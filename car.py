"""
@file car.py
@brief Defines the Car class for managing diagnostics and computing performance score.
"""

from typing import Optional
from diagnostic import Diagnostic

# Threshold constants
SCORE_THRESHOLD = 40
TEMP_BASELINE = 90


class Car:
    """
    @class Car
    @brief Represents a car with diagnostic data.
    """

    def __init__(self, car_id: str, diagnostic: Diagnostic) -> None:
        """
        @brief Constructor for Car class.
        @param car_id Car identifier (string).
        @param diagnostic Diagnostic object for the car.
        """
        self.car_id = car_id
        self.diagnostic = diagnostic

    def compute_score(self) -> Optional[float]:
        """
        @brief Computes the performance score for the car.
        @return Performance score as float (rounded to 1 decimal place), or None if diagnostics are invalid.
        """
        if not self.diagnostic.is_valid():
            return None
        rpm = self.diagnostic.rpm
        load = self.diagnostic.load
        temp = self.diagnostic.temp
        score = 100 - (rpm / 100 + load * 0.5 + (temp - TEMP_BASELINE) * 2)
        return round(score, 1)
