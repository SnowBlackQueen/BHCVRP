import json
import csv
import xml.etree.ElementTree as ET
from data.Problem import Problem
from data.ProblemType import ProblemType

class ExportResult:
    @staticmethod
    def to_txt(data, file_path):
        """Exporta los datos a un archivo TXT."""
        with open(file_path, "w") as file:
            file.write(data)

    @staticmethod
    def to_json(data, file_path):
        """Exporta los datos a un archivo JSON."""
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def to_csv(data, file_path):
        """Exporta los datos a un archivo CSV."""
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    @staticmethod
    def to_xml(data, file_path):
        """
        Exporta los datos a un archivo XML.
        :param data: Diccionario con los datos a exportar.
        :param file_path: Ruta del archivo XML.
        """
        # Crear el elemento raíz
        root = ET.Element("resultado")

        # Agregar heurística, costo y tiempo
        ET.SubElement(root, "heuristica").text = data["heuristic_type"]
        ET.SubElement(root, "costo_total").text = str(data["total_cost"])
        ET.SubElement(root, "tiempo_ejecucion").text = str(data["execution_time"])

        # Agregar rutas
        rutas_element = ET.SubElement(root, "rutas")
        if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
            for route in data["routes"]:
                ruta_element = ET.SubElement(rutas_element, "ruta", id=str(route["route_id"]))
                ET.SubElement(ruta_element, "paradas").text = ", ".join(map(str, route["bus_stops"]))
        else:
            for route in data["routes"]:
                ruta_element = ET.SubElement(rutas_element, "ruta", id=str(route["route_id"]))
                ET.SubElement(ruta_element, "clientes").text = ", ".join(map(str, route["customers"]))

        # Crear el árbol XML y guardar en un archivo
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)