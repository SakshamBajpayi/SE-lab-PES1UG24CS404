import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# --- Initial starter test cases ---
def test_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True


# --- Additional test cases for >= 90% (100%) Line / Code Coverage ---
def test_extra_distance_fare_invalid_inputs():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("luxury", 10, "city", False)
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -2, "city", False)


def test_extra_distance_fare_city_subscriber():
    # mini included = 5 + 3 (subscriber) = 8; extra = 20 - 8 = 12 (<= 20); rate = 12
    assert extra_distance_fare("mini", 20, "city", True) == 144


def test_extra_distance_fare_outstation_long_trip():
    # sedan included = 8; extra = 35 - 8 = 27 (> 20); rate = 18 + 8 + 4 = 30
    assert extra_distance_fare("sedan", 35, "outstation", False) == 810


def test_seats_and_bags_wheelchair_and_over_capacity():
    assert seats_and_bags_ok(2, 0, True) is True
    assert seats_and_bags_ok(5, 1, False) is False
    assert seats_and_bags_ok(3, 3, False) is False


def test_pickup_status_all_outcomes():
    # scheduled + airport -> cutoff = 10 + 10 = 20
    assert pickup_status(22, True, True) == "on_time"
    # unscheduled + airport -> cutoff = 5 + 10 = 15; cutoff - 15 = 0
    assert pickup_status(5, False, True) == "delayed"
    assert pickup_status(-5, False, True) == "missed"
