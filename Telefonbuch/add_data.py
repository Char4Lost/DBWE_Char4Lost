from app import db, Person, app  # Importiere db, Person und app aus deiner app.py

# Hier kannst du die zu hinzufügenden Personen definieren
personen_daten = [
    Person(name='Denis Hefti', adresse='Kirchweg 20a, 8180 Bülach', telefonnummer='044 586 95 55'),
    Person(name='Jack Shepard', adresse='Inselstrasse 4, 8000 Zürich', telefonnummer='044 865 32 54'),
    Person(name='Rocco Nardone', adresse='Einbahnstrasse 67, 9565 St. Gallen', telefonnummer='044 476 62 14'),
    Person(name='Thomas Seebacher', adresse='Seestrasse 78, 5767 Beinwil am See', telefonnummer='056 265 88 84'),
    Person(name='John Lock', adresse='Inselstrasse 3, 8001 Zürich', telefonnummer='056 396 54 66')
]

# Füge die Personen zur Datenbank hinzu
def add_personen():
    with app.app_context():  # Startet den Application-Context
        db.session.bulk_save_objects(personen_daten)
        db.session.commit()
        print("Personen wurden zur Datenbank hinzugefügt!")

# Die Funktion ausführen
if __name__ == '__main__':
    add_personen()
