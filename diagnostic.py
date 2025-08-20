
"""
@file diagnostic.py
@brief Diagnostic module for car engine diagnostics.
"""

from typing import Optional



class Diagnostic:
    """
    @class Diagnostic
    @brief Represents a set of engine diagnostic readings.
    """

    def __init__(self, rpm: Optional[int], load: Optional[float], temp: Optional[float]) -> None:
        """
        @brief Constructor for Diagnostic class.
        @param rpm Engine RPM value.
        @param load Engine Load value.
        @param temp Coolant Temperature value.
        """
        self.rpm = rpm
        self.load = load
        self.temp = temp

    def is_valid(self) -> bool:
        """
        @brief Checks if all diagnostic values are present and valid.
        @return True if all values are valid, False otherwise.
        """
        return (
            self.rpm is not None and self.rpm > 0 and
            self.load is not None and self.load >= 0 and
            self.temp is not None and self.temp > 0
        )
