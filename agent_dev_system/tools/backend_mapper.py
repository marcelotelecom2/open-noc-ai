from pathlib import Path
from pprint import pprint


BASE_PATH = Path("backend/app")


def list_entities():
    models_path = BASE_PATH / "models"
    return [
        f.stem
        for f in models_path.glob("*.py")
        if f.is_file() and f.name != "__init__.py"
    ]


def check_layer(entity: str):
    return {
        "model": (BASE_PATH / "models" / f"{entity}.py").exists(),
        "schema": (BASE_PATH / "schemas" / f"{entity}.py").exists(),
        "crud": (BASE_PATH / "crud" / f"{entity}.py").exists(),
        "endpoint": any((BASE_PATH / "api/v1/endpoints").glob(f"{entity}s.py")),
    }


def is_complete(layers: dict):
    return all(layers.values())


def map_backend():
    entities = list_entities()

    mapping = {}

    for entity in entities:
        mapping[entity] = check_layer(entity)

    return mapping


def classify_backend():
    mapping = map_backend()

    complete_entities = {
        entity: layers
        for entity, layers in mapping.items()
        if is_complete(layers)
    }

    incomplete_entities = {
        entity: layers
        for entity, layers in mapping.items()
        if not is_complete(layers)
    }

    return {
        "complete_entities": complete_entities,
        "incomplete_entities": incomplete_entities,
    }


def select_reference_entity(preferred: str = "site"):
    classified = classify_backend()
    complete_entities = classified["complete_entities"]

    if preferred in complete_entities:
        return preferred

    if complete_entities:
        return next(iter(complete_entities.keys()))

    return None


if __name__ == "__main__":
    pprint(classify_backend())
    print("\nReference entity:")
    print(select_reference_entity())