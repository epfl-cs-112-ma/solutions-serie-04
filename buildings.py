from __future__ import annotations

from abc import abstractmethod
from enum import Enum, auto
from typing import Final

# Remarque générale : nous ne modélisons pas du tout les "nombres de pièces" ni les
# tailles de balcons. En effet, nous n'en avons pas besoin pour calculer les impôts.
# Il faut toujours penser à nos *besoins*, et ne pas modéliser de choses inutiles.

LIVING_AREA_TAX_RATE = 5.6
GARDEN_AREA_TAX_RATE = 1.5

class Person:
    full_name: Final[str]

    # Le design n'est pas super ici. Il faudrait *s'assurer* que les codes
    # utilisateur de cette classe ne peuvent pas modifier `owned_buildings`.
    # Mais il faut que `Building` puisse le faire.
    owned_buildings: Final[list[Building]]
    """List of the buildings owned by this person.

    Users of the class should not modify this list.
    """

    def __init__(self, full_name: str) -> None:
        self.full_name = full_name
        self.owned_buildings = []

class Building:
    __owner: Person

    def __init__(self, initial_owner: Person) -> None:
        self.__owner = initial_owner
        initial_owner.owned_buildings.append(self)

    @property
    def owner(self) -> Person:
        return self.__owner

    @owner.setter
    def owner(self, new_owner: Person) -> None:
        self.__owner.owned_buildings.remove(self)
        self.__owner = new_owner
        new_owner.owned_buildings.append(self)

    # On n'en a pas parlé, mais on peut faire des propriétés abstraites.

    @property
    @abstractmethod
    def living_area(self) -> int:
        ...

    @property
    @abstractmethod
    def garden_area(self) -> int:
        ...

class House(Building):
    __living_area: Final[int]
    """Living area in m²."""
    __garden_area: Final[int]
    """Garden area in m²."""

    def __init__(self, initial_owner: Person, living_area: int, garden_area: int) -> None:
        super().__init__(initial_owner)
        self.__living_area = living_area
        self.__garden_area = garden_area

    @property
    def living_area(self) -> int:
        return self.__living_area

    @property
    def garden_area(self) -> int:
        return self.__garden_area

class Appartment:
    living_area: Final[int]
    """Living area in m²."""

    def __init__(self, living_area: int):
        self.living_area = living_area

class AppartmentBuilding(Building):
    __appartments: Final[list[Appartment]]

    def __init__(self, initial_owner: Person, appartments: list[Appartment]) -> None:
        super().__init__(initial_owner)
        self.__appartments = appartments.copy() # so no one can modify it after the fact

    @property
    def living_area(self) -> int:
        return sum([appartment.living_area for appartment in self.__appartments])

    @property
    def garden_area(self) -> int:
        """Buildings do not have gardens in this town, so the gargen area is always 0."""
        return 0

# Nous déclarons les fonctions de calcul des taxes comme fonctions globales.
# On pourrait aussi les déclarer dans les classes Building et Person.
# Notre raisonnement ici est que les taxes ne sont pas une propriété intrinsèque
# des personnes et des bâtiments. C'est le système de taxation, externe à ces
# classes, qui s'en occupe.
#
# En fait, on aurait même pu faire une `class TaxesCalculator` qui prennet les
# deux taux de taxation en paramètres du constructeur. Dans ce cas, ces
# fonctions auraient naturellement été des méthodes de cette classe.

def compute_taxes_for_building(building: Building) -> float:
    """Computes the taxes applicable to one building."""
    living_area_taxes = LIVING_AREA_TAX_RATE * building.living_area
    garden_taxes = GARDEN_AREA_TAX_RATE * building.garden_area
    return living_area_taxes + garden_taxes

def compute_taxes(person: Person) -> float:
    """Computes the taxes applicable to all the buildings owned by a person."""
    return sum([compute_taxes_for_building(building) for building in person.owned_buildings])
