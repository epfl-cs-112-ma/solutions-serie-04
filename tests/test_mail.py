from mail import *

def test_letter() -> None:
    letter = Letter(180, DeliveryMode.NORMAL, "dest", Format.A5)
    assert letter.frank() == 1.68 == (1.50 + 180/1000)
    assert letter.is_valid()
    assert str(letter) == "Lettre : 180 g, normal, pour 'dest', A5"

    letter = Letter(240, DeliveryMode.EXPRESS, "", Format.A4)
    assert letter.frank() == 5.48 == 2 * (2.50 + 240/1000)
    assert not letter.is_valid()
    assert str(letter) == "Lettre : 240 g, express, pour '', A4 (invalide)"

def test_parcel() -> None:
    parcel = Parcel(1800, DeliveryMode.NORMAL, "dest", volume=2)
    assert parcel.frank() == 2.30 == 0.25*2 + 1800/1000
    assert parcel.is_valid()
    assert str(parcel) == "Colis : 1800 g, normal, pour 'dest', 2 l"

    parcel = Parcel(1800, DeliveryMode.NORMAL, "", volume=2)
    assert parcel.frank() == 2.30 == 0.25*2 + 1800/1000
    assert not parcel.is_valid()
    assert str(parcel) == "Colis : 1800 g, normal, pour '', 2 l (invalide)"

    parcel = Parcel(15000, DeliveryMode.EXPRESS, "dest", volume=200)
    assert parcel.frank() == 130.00 == 2 * (0.25*200 + 15000/1000)
    assert not parcel.is_valid()
    assert str(parcel) == "Colis : 15000 g, express, pour 'dest', 200 l (invalide)"

def test_advertisement() -> None:
    advertisement = Advertisement(200, DeliveryMode.NORMAL, "dest")
    assert advertisement.frank() == 1.0 == (5 * 200/1000)
    assert advertisement.is_valid()
    assert str(advertisement) == "Publicité : 200 g, normal, pour 'dest'"

    advertisement = Advertisement(240, DeliveryMode.EXPRESS, "")
    assert advertisement.frank() == 2.4 == 2 * (5 * 240/1000)
    assert not advertisement.is_valid()
    assert str(advertisement) == "Publicité : 240 g, express, pour '' (invalide)"

def test_mailbox() -> None:
    mailbox = Mailbox()
    mailbox.add_mail(Letter(180, DeliveryMode.NORMAL, "dest", Format.A5))
    mailbox.add_mail(Letter(240, DeliveryMode.EXPRESS, "", Format.A4))
    mailbox.add_mail(Parcel(1800, DeliveryMode.NORMAL, "dest", volume=2))
    mailbox.add_mail(Parcel(1800, DeliveryMode.NORMAL, "", volume=2))
    mailbox.add_mail(Parcel(15000, DeliveryMode.EXPRESS, "dest", volume=200))
    mailbox.add_mail(Advertisement(200, DeliveryMode.NORMAL, "dest"))
    mailbox.add_mail(Advertisement(240, DeliveryMode.EXPRESS, ""))

    assert mailbox.frank() == (1.68 + 2.30 + 1.0)
    assert mailbox.invalid_mails() == 4

    assert mailbox.display() == [
        "Lettre : 180 g, normal, pour 'dest', A5",
        "Lettre : 240 g, express, pour '', A4 (invalide)",
        "Colis : 1800 g, normal, pour 'dest', 2 l",
        "Colis : 1800 g, normal, pour '', 2 l (invalide)",
        "Colis : 15000 g, express, pour 'dest', 200 l (invalide)",
        "Publicité : 200 g, normal, pour 'dest'",
        "Publicité : 240 g, express, pour '' (invalide)",
    ]
