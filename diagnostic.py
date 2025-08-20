"""
Diagnostic module for car engine diagnostics.
"""

from typing import Optional


class Diagnostic:
    """Represents a set of engine diagnostic readings."""

    def __init__(self, rpm: Optional[int], load: Optional[float], temp: Optional[float]) -> None:
        self.rpm = rpm
        self.load = load
        self.temp = temp

    def is_valid(self) -> bool:
        """Checks if all diagnostic values are present and valid."""
        return (
            self.rpm is not None and self.rpm > 0 and
            self.load is not None and self.load >= 0 and
            self.temp is not None and self.temp > 0
        )
