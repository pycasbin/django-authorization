import importlib


def import_class(name):
    """Import class from string
    e.g. `package.module.ClassToImport` returns the `ClasToImport` class"""
    components = name.split(".")
    module_name = ".".join(components[:-1])
    class_name = components[-1]
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    return class_
