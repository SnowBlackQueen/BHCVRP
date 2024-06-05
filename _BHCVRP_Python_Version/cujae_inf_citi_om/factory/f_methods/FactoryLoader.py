import sys
import traceback

class FactoryLoader:
    @staticmethod
    def get_instance(class_name):
        try:
            class_obj = __import__(class_name)
            instance = class_obj()
            return instance
        except ClassNotFoundError as e:
            print("The class name does not exist in the classpath")
            traceback.print_exc(file=sys.stdout)
        except (InstantiationError, IllegalAccessError) as e:
            print("An error occurred when invoking the class constructor")
            traceback.print_exc(file=sys.stdout)
        except Exception as e:
            print("This class does not have available constructors")
            traceback.print_exc(file=sys.stdout)
        return None

