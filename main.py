import json


print("hallo")

class Entity:

    def __init__(self, name):
        self.name = name


class Relation:
    """Der Name ist der Name der Relation, entity_left das Objekt der einen Entität, right das der anderen"""

    def __init__(self, name, entity_left, entity_right, cardi_left, card_right):
        self.name = name
        self.entity_left = entity_left
        self.entity_right = entity_right
        self.cardi_left = cardi_left
        self.card_right = card_right


# die JSON-Daten zu SQL konvertieren
def json_to_sql():
    sql_commands = ["CREATE DATABASE codenight;"]


# aus dem SQL die Datenbank erstellen (also Anfragen an das DBMS senden, damit dieses die Datenbank erstellt)
def sql_to_dbms():
    pass


# öffnet die Datei im Lese-Modus
with open("models/er-model.json", "r", encoding="utf-8") as file:
    er_model = json.load(file)
    print(er_model)
