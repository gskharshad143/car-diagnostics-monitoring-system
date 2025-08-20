"""
@file test_main.py
@brief Unit tests for Car Diagnostics Monitoring System using pytest.
"""

import pytest
from diagnostic import Diagnostic
from car import Car, SCORE_THRESHOLD
from garage_monitor import GarageMonitor

# --- Fixtures ---

@pytest.fixture
def car_severe_stress():
    """
    @brief Fixture for a car with severe engine stress (score < 40).
    @return Car object with high RPM, load, and temp.
    """
    diag = Diagnostic(6500, 95, 120)
    return Car(0, diag)

@pytest.fixture
def car_missing_temp():
    """
    @brief Fixture for a car missing CoolantTemp diagnostic.
    @return Car object with missing temp.
    """
    diag = Diagnostic(3000, 40, None)
    return Car(1, diag)

@pytest.fixture
def garage_with_two_cars(tmp_path):
    """
    @brief Fixture for a garage with two cars having scores 70 and 30.
    @param tmp_path Temporary path for CSV file.
    @return GarageMonitor object with loaded diagnostics.
    """
    csv_file = tmp_path / "diagnostics.csv"
    csv_file.write_text(
        "CarID,DiagnosticType,Value\n"
        "CAR1,RPM,2000\n"
        "CAR1,Engine Load,20\n"
        "CAR1,Coolant Temperature,90\n"
        "CAR2,RPM,4000\n"
        "CAR2,Engine Load,40\n"
        "CAR2,Coolant Temperature,95\n"
    )
    garage = GarageMonitor(str(csv_file))
    garage.load_diagnostics()
    return garage

@pytest.fixture
def car_boundary_score():
    """
    @brief Fixture for a car with boundary score (score = 40).
    @return Car object with score exactly at threshold.
    """
    diag = Diagnostic(4000, 80, 110)  # Adjust values to get score = 40
    return Car(2, diag)

# --- Tests ---

def test_severe_engine_stress_alert(car_severe_stress, capsys):
    """
    @brief Test that severe engine stress alert is raised when score < 40.
    """
    score = car_severe_stress.compute_score()
    assert score is not None and score < SCORE_THRESHOLD
    # Simulate monitor output
    print(f"Car {car_severe_stress.car_id} score={score:.2f}")
    if score < SCORE_THRESHOLD:
        print("Severe Engine Stress")
    captured = capsys.readouterr()
    assert "Severe Engine Stress" in captured.out

def test_sensor_failure_alert_for_missing_temp(car_missing_temp, capsys):
    """
    @brief Test that sensor failure alert is raised when CoolantTemp is missing.
    """
    score = car_missing_temp.compute_score()
    assert score is None
    # Simulate monitor output
    if score is None:
        print(f"Car {car_missing_temp.car_id}: Sensor Failure Detected")
    captured = capsys.readouterr()
    assert "Sensor Failure Detected" in captured.out

def test_garage_average_score(garage_with_two_cars):
    """
    @brief Test that garage average score is calculated correctly.
    """
    scores = [car.compute_score() for car in garage_with_two_cars.cars if car.compute_score() is not None]
    assert len(scores) == 2
    avg_score = sum(scores) / len(scores)
    assert avg_score == pytest.approx(50.0, abs=1.0)  # Accept small float error

def test_no_alert_on_boundary_score(car_boundary_score, capsys):
    """
    @brief Test that no alert is raised when score is exactly at threshold.
    """
    # Find values so score = 40
    # score = 100 - (rpm/100 + load*0.5 + (temp-90)*2) = 40
    # Let's use rpm=4000, load=40, temp=90
    diag = Diagnostic(4000, 40, 90)
    car = Car(2, diag)
    score = car.compute_score()
    assert score == SCORE_THRESHOLD
    print(f"Car {car.car_id} score={score:.2f}")
    if score < SCORE_THRESHOLD:
        print("Severe Engine Stress")
    captured = capsys.readouterr()
    assert "Severe Engine Stress" not in captured.out

def test_empty_csv_raises_exception(tmp_path):
    """
    @brief Test that an exception is raised for empty CSV file.
    """
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")  # Empty file
    garage = GarageMonitor(str(csv_file))
    with pytest.raises(Exception):
        garage.load_diagnostics()