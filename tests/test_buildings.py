from pytest import approx
from buildings import *

def test_buildings() -> None:
    alice = Person("Alice")
    house = House(alice, living_area=50, garden_area=10)
    app_building = AppartmentBuilding(alice, [
        Appartment(30),
        Appartment(60),
    ])
    bob = Person("Bob")

    assert compute_taxes_for_building(house) == approx(295.0) == approx(LIVING_AREA_TAX_RATE*50 + GARDEN_AREA_TAX_RATE*10)
    assert compute_taxes_for_building(app_building) == approx(504.0) == approx(LIVING_AREA_TAX_RATE*90)
    assert compute_taxes(alice) == approx(295.0 + 504.0)

    assert compute_taxes(bob) == 0.0

    # Bob buys the appartment building from Alice
    app_building.owner = bob
    assert app_building in bob.owned_buildings
    assert app_building not in alice.owned_buildings
    assert compute_taxes(alice) == approx(295.0)
    assert compute_taxes(bob) == approx(504.0)
