import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# --- Initial starter test cases ---
def test_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_seats_and_bags_ok():
    assert seats_and_bags_ok(2, 1, False) is True


# --- Comprehensive test cases for 100% Line and 100% Branch Coverage ---
def test_extra_distance_fare_unknown_cab_type():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 10, "city", False)


def test_extra_distance_fare_negative_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_extra_distance_fare_subscriber_non_suv_and_suv():
    # Subscriber with non-SUV gets +3 km included (5 + 3 = 8 km); extra = 10 - 8 = 2 km; city rate = 12
    assert extra_distance_fare("mini", 10, "city", True) == 24
    # Subscriber with SUV does not get +3 km bonus (included = 12 km); extra = 12 - 12 = 0 km
    assert extra_distance_fare("suv", 12, "city", True) == 0


def test_extra_distance_fare_city_over_20_km_extra():
    # Covers extra > 20 (True) with zone != "outstation" (False branch of line 21)
    # mini included = 5; extra = 30 - 5 = 25 (> 20); city rate = 12 + 8 = 20
    assert extra_distance_fare("mini", 30, "city", False) == 500


def test_extra_distance_fare_outstation_under_and_over_20_km_extra():
    # Outstation with extra <= 20: sedan included = 8; extra = 18 - 8 = 10; rate = 18
    assert extra_distance_fare("sedan", 18, "outstation", False) == 180
    # Outstation with extra > 20: sedan included = 8; extra = 30 - 8 = 22; rate = 18 + 8 + 4 = 30
    assert extra_distance_fare("sedan", 30, "outstation", False) == 660


def test_seats_and_bags_all_branches():
    # needs_wheelchair = True (<= 2 and > 2)
    assert seats_and_bags_ok(2, 1, True) is True
    assert seats_and_bags_ok(3, 1, True) is False
    # needs_wheelchair = False, passengers > 4 (True)
    assert seats_and_bags_ok(5, 1, False) is False
    # needs_wheelchair = False, passengers <= 4, bags > 2 (False return)
    assert seats_and_bags_ok(4, 3, False) is False


def test_pickup_status_all_branches():
    # is_scheduled = True (cutoff = 10), is_airport = True (+10 -> cutoff = 20)
    assert pickup_status(20, True, True) == "on_time"
    # is_scheduled = False (cutoff = 5), is_airport = False (cutoff stays 5)
    assert pickup_status(5, False, False) == "on_time"
    # delayed branch: cutoff - 15 <= minutes_early < cutoff (for cutoff = 5, range is -10 to 4)
    assert pickup_status(0, False, False) == "delayed"
    # missed branch: minutes_early < cutoff - 15 (for cutoff = 5, < -10)
    assert pickup_status(-11, False, False) == "missed"
