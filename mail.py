from __future__ import annotations

from abc import abstractmethod
from enum import Enum, auto
from typing import Final

MAX_PARCEL_VOLUME = 50
"""Maximum volume for a valid parcel, in liters."""

class DeliveryMode(Enum):
    NORMAL = auto()
    EXPRESS = auto()

    def __str__(self) -> str:
        match self:
            case DeliveryMode.NORMAL: return "normal"
            case DeliveryMode.EXPRESS: return "express"

class Format(Enum):
    A3 = auto()
    A4 = auto()
    A5 = auto()

    def __str__(self) -> str:
        return self.name

class Mail:
    weight_g: Final[int]
    """Weight in grams."""
    delivery_mode: Final[DeliveryMode]
    delivery_address: Final[str]

    def __init__(
        self,
        weight_g: int,
        delivery_mode: DeliveryMode,
        delivery_address: str
    ) -> None:
        self.weight_g = weight_g
        self.delivery_mode = delivery_mode
        self.delivery_address = delivery_address

    @property
    def weight_kg(self) -> float:
        """Weight in kilograms."""
        return self.weight_g / 1000.0

    def frank(self) -> float:
        """Computes the franking amount of the mail."""
        base = self.frank_normal()
        match self.delivery_mode:
            case DeliveryMode.NORMAL:
                return base
            case DeliveryMode.EXPRESS:
                return 2.0 * base

    @abstractmethod
    def frank_normal(self) -> float:
        """Computes the franking amount as if the mail used the normal delivery mode."""
        ...

    def is_valid(self) -> bool:
        """Tests whether this mail is valid.

        The default implementation checks that the delivery address is non-empty.
        Subclasses can add further restrictions.
        """
        return self.delivery_address != ""

    def general_info_str(self) -> str:
        """Returns a string with general info of this mail.

        Includes the weight (in g), the delivery mode and the delivery address.
        """
        return f"{self.weight_g} g, {self.delivery_mode}, pour '{self.delivery_address}'"

    def invalid_str_suffix(self) -> str:
        """Returns ' (invalide)' if this mail is invalid, and '' otherwise.

        Useful for the __str__ method of the subclasses."""
        if self.is_valid():
            return ""
        else:
            return " (invalide)"

class Letter(Mail):
    format: Final[Format]

    def __init__(
        self,
        weight_g: int,
        delivery_mode: DeliveryMode,
        delivery_address: str,
        format: Format
    ) -> None:
        super().__init__(weight_g, delivery_mode, delivery_address)
        self.format = format

    def __str__(self) -> str:
        return f"Lettre : {self.general_info_str()}, {self.format}{self.invalid_str_suffix()}"

    def frank_normal(self) -> float:
        match self.format:
            case Format.A5: base = 1.50
            case Format.A4: base = 2.50
            case Format.A3: base = 3.50
        return base + self.weight_kg

class Parcel(Mail):
    volume: Final[int]
    """Volume in liters."""

    def __init__(
        self,
        weight_g: int,
        delivery_mode: DeliveryMode,
        delivery_address: str,
        volume: int
    ) -> None:
        super().__init__(weight_g, delivery_mode, delivery_address)
        self.volume = volume

    def __str__(self) -> str:
        return f"Colis : {self.general_info_str()}, {self.volume} l{self.invalid_str_suffix()}"

    def frank_normal(self) -> float:
        return 0.25 * self.volume + self.weight_kg

    def is_valid(self) -> bool:
        """Tests whether this parcel is valid.

        In addition to the conditions enforced by Mail.is_valid, a parcel is
        valid only if its volume does not exceed MAX_PARCEL_VOLUME.
        """
        # On utilise `super().is_valid()` de la même façon qu'un `super().__init__()`.
        # Cela nous permet de réutiliser la définition héritée de Mail.
        # C'est intéressant ici car la spécification de Mail.is_valid() dit
        # bien que nous pouvons *ajouter* des restrictions, mais nous devons
        # avoir au moins toutes les restrictions héritées.
        return super().is_valid() and self.volume <= MAX_PARCEL_VOLUME

class Advertisement(Mail):
    # On n'a pas forcément besoin de __init__ ici, car elle serait identique à
    # la méthode héritée, et ne ferait rien d'autre qu'un appel à super.

    def frank_normal(self) -> float:
        return 5.0 * self.weight_kg

    def __str__(self) -> str:
        return f"Publicité : {self.general_info_str()}{self.invalid_str_suffix()}"

class Mailbox:
    # __mails, étant Final, pointera toujours sur la même instance de `list[Mail]`.
    # Cela n'empêche pas l'intérieur de cette instance de changer au cours du
    # temps, puisque `list` est une classe muable.
    __mails: Final[list[Mail]]

    def __init__(self) -> None:
        self.__mails = []

    def frank(self) -> float:
        """Total franking amount for all the valid mails in the mailbox.

        Invalid mails are ignored.
        """
        # On anticipe sur la semaine prochaine : un one-liner grâce aux list
        # comprehensions. Cela calcule littéralement "la somme de mail.frank()
        # pour tout mail dans self.__mails qui satisfait mail.is_valid()".
        return sum([mail.frank() for mail in self.__mails if mail.is_valid()])

    def invalid_mails(self) -> int:
        """Returns the count of invalid mails in the mailbox."""
        # Même idée : une petite list comprehension règle le problème en une ligne
        return len([mail for mail in self.__mails if not mail.is_valid()])

    def display(self) -> list[str]:
        return [str(mail) for mail in self.__mails]

    def __str__(self) -> str:
        return f"Boîte aux lettres: {self.__mails}"

    def add_mail(self, mail: Mail) -> None:
        self.__mails.append(mail)
