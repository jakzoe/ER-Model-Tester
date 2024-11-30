import json


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


def is_one_to_one(entity, relations):
    cardi_left = get_cardi(entity, relations)
    _, cardi_right = get_relation_entity(entity, relations)
    return cardi_left == cardi_right == "1"


def is_one_to_n(entity, relations):
    cardi_left = get_cardi(entity, relations)
    _, cardi_right = get_relation_entity(entity, relations)
    return cardi_left == "1" and cardi_right == "n"


def is_n_to_one(entity, relations):
    cardi_left = get_cardi(entity, relations)
    _, cardi_right = get_relation_entity(entity, relations)
    return cardi_left == "n" and cardi_right == "1"


def is_n_to_n(entity, relations):
    cardi_left = get_cardi(entity, relations)
    _, cardi_right = get_relation_entity(entity, relations)
    return cardi_left == "n" and cardi_right == "n"


def get_cardi(entity, relations):
    for relation in relations:
        if relation.entity_left is entity:
            return relation.cardi_left
    return None


def get_relation_entity(entity, relations):
    for relation in relations:
        if relation.entity_left is entity:
            return relation.entity_right, relation.cardi_right
    return None, None


def get_primary_key(entity):
    if entity is None:
        return None, None
    for attribute in entity.attributes:
        if attribute.primary:
            return attribute.name, attribute.type
    raise RuntimeError("not possible...")


# die JSON-Daten zu SQL konvertieren
def py_to_sql(entities, relations):
    print()
    print()
    sql_commands = [["CREATE DATABASE codenight;"]]
    post_sql_commands = []
    new_relation_right = []
    for entity in entities:
        sql_command = []

        primary_name, primary_type = get_primary_key(entity)

        relation_entity, relation_cardi = get_relation_entity(entity, relations)
        relation_primary_name, relation_primary_type = get_primary_key(relation_entity)

        sql_command.append(f"CREATE TABLE {entity.name}")
        sql_command.append("(")
        # Attribute hinzufügen
        for attribute in entity.attributes:
            sql_command.append(
                f"{attribute.name} {attribute.type} {'PRIMARY KEY' if attribute.primary else ''},"
            )

        if relation_entity is not None:
            # relationships hinzufügen. UNIQUE wenn one to one, kein UNIQUE wenn one to many
            if is_one_to_one(entity, relations) or is_one_to_n(entity, relations):
                sql_command.append(
                    f"{relation_primary_name} {relation_primary_type} {'UNIQUE' if is_one_to_one(entity, relations) else ''},"
                )
                post_sql_commands.append(
                    f"ALTER TABLE {entity.name} FOREIGN KEY ({relation_primary_name}) REFERENCES {relation_entity.name}({relation_primary_name});"
                )
            elif is_n_to_one(entity, relations):
                new_relation_right.append([relation_entity.name, entity.name, primary_name])

        for existing_relation in new_relation_right:
            if entity.name == existing_relation[0]:
                sql_command.append(f"FOREIGN KEY ({existing_relation[2]}) REFERENCES {existing_relation[1]}({existing_relation[2]}),")
                new_relation_right.remove(existing_relation)

        # dirty lol, das letzte unnötige Komma entfernen
        sql_command[-1] = sql_command[-1][:-1]

        # options and stuff
        sql_command.append(");")
        sql_commands.append(sql_command)

        # linking table erstellen
        if is_n_to_n(entity, relations):
            sql_command = []
            sql_command.append(f"CREATE TABLE {entity.name}_{relation_entity.name}")
            sql_command.append("(")

            sql_command.append(f"{primary_name} {primary_type},")
            sql_command.append(f"{relation_primary_name} {relation_primary_type},")

            sql_command.append(
                (f"PRIMARY KEY ({primary_name}, {relation_primary_name}),")
            )
            sql_command.append(
                f"FOREIGN KEY ({primary_name}) REFERENCES {entity.name}({primary_name}),"
            )
            post_sql_commands.append(
                f"ALTER TABLE {entity.name} FOREIGN KEY ({relation_primary_name}) REFERENCES {relation_entity.name}({relation_primary_name});"
            )

            sql_command[-1] = sql_command[-1][:-1]
            # options and stuff
            sql_command.append(");")
            sql_commands.append(sql_command)

        # break

    for command in sql_commands:
        for line in command:
            print(line)

    for line in post_sql_commands:
        print(line)


# aus dem SQL die Datenbank erstellen (also Anfragen an das DBMS senden, damit dieses die Datenbank erstellt)
def sql_to_dbms():
    pass


def json_to_py(json):
    entities = []
    relations = []
    for entity in json["entities"]:
        attributes = []
        for attribute in entity["attributes"]:
            attributes.append(
                Attribute(
                    attribute["name"], attribute["type"], attribute["is-primary-key"]
                )
            )

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
with open("models/er-model-v4.json", "r", encoding="utf-8") as file:
    er_model = json.load(file)
    print(er_model)
    entities, relations = json_to_py(er_model)
    py_to_sql(entities, relations)
