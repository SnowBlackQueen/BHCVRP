import importlib

class FactoryLoader:

    @staticmethod
    def get_instance(class_name):
        try:
            module_name, class_name = class_name.rsplit('.', 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
        except (ModuleNotFoundError, AttributeError) as e:
            print("El nombre de la clase no existe en el classpath")
            raise e

        try:
            instance = cls()
        except TypeError as e:
            print("Ha ocurrido un error al invocar el constructor de la clase")
            raise e
        except AttributeError as e:
            print("Esta clase no tiene constructores disponibles")
            raise e

        return instance


