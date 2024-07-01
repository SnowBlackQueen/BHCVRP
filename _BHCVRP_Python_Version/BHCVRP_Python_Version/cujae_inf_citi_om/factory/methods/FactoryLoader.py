import importlib

class FactoryLoader:

    @staticmethod
    def get_instance(class_name):
        try:
            # Separa el nombre del módulo y el nombre de la clase
            module_path, class_name = class_name.rsplit('.', 1)
            # Importa el módulo dinámicamente
            module = importlib.import_module(module_path)
            # Obtiene la clase del módulo importado
            cls = getattr(module, class_name)
            # Crea una instancia de la clase
            instance = cls()
            return instance
        except Exception as e:
            print(f"Error al crear la instancia de {class_name}: {e}")
            return None

'''def get_instance(class_name):
        try:
            module_name, class_name = class_name.rsplit('.', 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            instance = cls()
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

        return instance'''

