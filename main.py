import json


#print("hallo")

class Attribute:

    def __init__(self, name, type, primary):
        self.name = name
        self.type = type
        self.primary = primary


class Entity:

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes



class Relation:
    """Der Name ist der Name der Relation, entity_left das Objekt der einen Entität, right das der anderen"""

    def __init__(self, name):
        self.name = name
        self.entity_left = None
        self.entity_right = None
        self.cardi_left = None
        self.cardi_right = None

    def set_left(self, entity_left, cardi_left):
        self.entity_left = entity_left
        self.cardi_left = cardi_left

    def set_right(self, entity_right, cardi_right):
        self.entity_right = entity_right
        self.cardi_right = cardi_right

# die JSON-Daten zu SQL konvertieren
def json_to_sql(entities, relations):
    sql_commands = ["CREATE DATABASE codenight;"]
    for entity in entities:
        sql_commands += f"CREATE TABLE {entity}"
        sql_commands += "("
        for attribute in entity.attributes:
            sql_commands += f"{attribute.name} {attribute.type},"
        # dirty lol, das letzte unnötige Komma entfernen
        sql_commands[-1] = sql_commands[-1][:-1]

        # options and stuff
        sql_commands += ");"


# aus dem SQL die Datenbank erstellen (also Anfragen an das DBMS senden, damit dieses die Datenbank erstellt)
def sql_to_dbms():
    pass


def json_to_py(json):
    entities = []
    relations = []
    for entity in json["entities"]:
        attributes = []
        for attribute in entity["attributes"]:
            attributes.append(Attribute(attribute["name"], attribute["type"], attribute["is-primary-key"]))

        new_entity = Entity(entity["name"], attributes)
        for relation in entity["relations"]:
            exists = False
            for existing_relation in relations:
                if existing_relation.name == relation["name"]:
                    existing_relation.set_right(new_entity, relation["cardinality"]) 
                    exists = True
                    break
            if not exists:
                new_relation = Relation(relation["name"])
                new_relation.set_left(new_entity, relation["cardinality"])
                relations.append(new_relation)

        entities.append(new_entity)

    return entities, relations
            
            


# öffnet die Datei im Lese-Modus
with open("models/er-model.json", "r", encoding="utf-8") as file:
    er_model = json.load(file)
    print(er_model)
