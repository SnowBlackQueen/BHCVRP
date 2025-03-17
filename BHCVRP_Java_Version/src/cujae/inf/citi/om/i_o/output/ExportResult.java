/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.i_o.output;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import org.json.JSONObject;
import java.util.List;
import java.util.Map;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

/**
 *
 * @author kmych
 */
public class ExportResult {

    public static void toTxt(String data, String filePath) throws IOException {
        try (FileWriter file = new FileWriter(filePath)) {
            file.write(data);
        }
    }

    public static void toJson(Map<String, Object> data, String filePath) throws IOException {
        JSONObject jsonObject = new JSONObject(data);
        try (FileWriter file = new FileWriter(filePath)) {
            file.write(jsonObject.toString(4)); // Indentación de 4 espacios
        }
    }

    public static void toCsv(ArrayList<ArrayList<String>> data, String filePath) throws IOException {
        try (FileWriter file = new FileWriter(filePath)) {
            for (List<String> row : data) {
                file.write(String.join(",", row) + "\n");
            }
        }
    }

    public static void toXml(Map<String, Object> data, String filePath) throws ParserConfigurationException, IOException, Exception {
        DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
        DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
        Document doc = docBuilder.newDocument();

        // Crear el elemento raíz
        Element rootElement = doc.createElement("resultado");
        doc.appendChild(rootElement);

        // Agregar heurística, costo y tiempo
        Element heuristicElement = doc.createElement("heuristica");
        heuristicElement.appendChild(doc.createTextNode((String) data.get("heuristic_type")));
        rootElement.appendChild(heuristicElement);

        Element costElement = doc.createElement("costo_total");
        costElement.appendChild(doc.createTextNode(String.valueOf(data.get("total_cost"))));
        rootElement.appendChild(costElement);

        Element timeElement = doc.createElement("tiempo_ejecucion");
        timeElement.appendChild(doc.createTextNode(String.valueOf(data.get("execution_time"))));
        rootElement.appendChild(timeElement);

        // Agregar rutas
        Element routesElement = doc.createElement("rutas");
        rootElement.appendChild(routesElement);

        List<Map<String, Object>> routes = (List<Map<String, Object>>) data.get("routes");
        for (Map<String, Object> route : routes) {
            Element routeElement = doc.createElement("ruta");
            routeElement.setAttribute("id", String.valueOf(route.get("route_id")));
            routesElement.appendChild(routeElement);

            Element customersElement = doc.createElement("clientes");
            customersElement.appendChild(doc.createTextNode(String.join(", ", (List<String>) route.get("customers"))));
            routeElement.appendChild(customersElement);
        }

        // Escribir el contenido en un archivo XML
        TransformerFactory transformerFactory = TransformerFactory.newInstance();
        Transformer transformer = transformerFactory.newTransformer();
        DOMSource source = new DOMSource(doc);
        StreamResult result = new StreamResult(new FileWriter(filePath));
        transformer.transform(source, result);
    }
}