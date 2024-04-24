import importlib


def import_class(name):
    """Import class from string
    e.g. `package.module.ClassToImport` returns the `ClassToImport` class"""
    components = name.split(".")
    module_name = ".".join(components[:-1])
    class_name = components[-1]
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
