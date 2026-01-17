_MODEL_REGISTRY: dict[str, object] = {}
registry = _MODEL_REGISTRY


def register_model(name: str, model: object) -> None:
    _MODEL_REGISTRY[name] = model


def get_model(name: str) -> object:
    if name not in _MODEL_REGISTRY:
        raise RuntimeError(
            f"RegistryError: Model '{name}' not registered. "
            "Ensure host app calls register_model(...) during startup."
        )
    return _MODEL_REGISTRY[name]
