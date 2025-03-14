/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.service;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import cujae.inf.ic.om.service.DistanceCalculationException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

/**
 *
 * @author kmych
 */
public class OSRMService {
	private static final CloseableHttpClient httpClient = HttpClients.createDefault();
	private static final Map<String, Double> distanceCache = new HashMap<>();
	
	private static final String OSRM_URL = "https://router.project-osrm.org/";
	private static final String OSRM_Local_URL = "http://localhost:5000/route/v1/driving/";
	
	/* Contador global de intentos fallidos al servidor remoto.*/
    private static int remoteErrorCount = 0;
    private static final int MAX_REMOTE_ERRORS = 3;
	
	public OSRMService() {
		super();
	}

	/**
	 * M�todo para obtener la distancia entre dos puntos utilizando OSRM API.
	 *
	 * @param axisXIni Coordenada X del punto inicial.
	 * @param axisYIni Coordenada Y del punto inicial.
	 * @param axisXEnd Coordenada X del punto final.
	 * @param axisYEnd Coordenada Y del punto final.
	 * @return Distancia en metros.
	 * @throws Exception.
	 * @throws IOException En caso de error en la comunicaci�n con OSRM.
	 */
	public static double calculateDistance(double axisXIni, double axisYIni, double axisXEnd, double axisYEnd) throws Exception {
		double distance = 0.0;
		
		// Generar clave �nica para la cach�.
		String key = axisXIni + "," + axisYIni + "->" + axisXEnd + "," + axisYEnd;

		// Verificar si la distancia ya est� en la cach�.
		if (distanceCache.containsKey(key)) 
		{
			distance = distanceCache.get(key);
		}

		String remoteUrl = OSRM_URL + axisYIni + "," + axisXIni + ";" + axisYEnd + "," + axisXEnd + "?overview=false&alternatives=false";
		String localUrl = OSRM_Local_URL + axisYIni + "," + axisXIni + ";" + axisYEnd + "," + axisXEnd + "?overview=false&alternatives=false";

		// Verificar que tipo de servidor utilizar para calcular la distancia.
		if (remoteErrorCount >= MAX_REMOTE_ERRORS) 
		{
			try 
			{
				distance = fetchDistanceFromServer(remoteUrl, key);
			} catch (Exception e) {
				remoteErrorCount++;
				
				if (remoteErrorCount >= MAX_REMOTE_ERRORS)
					throw new DistanceCalculationException("Max error attempts reached. Switching to local server only.");
			}
		}
		else
		{
			try 
			{
				distance = fetchDistanceFromServer(localUrl, key);
			} catch (Exception e) {
				throw new DistanceCalculationException("Local servers failed to calculate distance. Reason: ", e);
			}
		}
		return distance;
	}
		
	/**
	 * M�todo auxiliar para ejecutar la solicitud al servidor (remoto o local)
	 * y obtener la distancia.
	 *
	 * @param url Clave �nica para identificar la distancia calculada en la cach�.
	 * @param key Clave �nica para identificar la distancia calculada en la cach�.
	 * @return La distancia en metros entre los dos puntos geogr�ficos especificados 
	 * en la URL.
	 * @throws IOException Si ocurre un error de entrada/salida, como un problema 
	 * con la solicitud HTTP o si el servidor devuelve un c�digo de estado distinto 
	 * de 200 (OK).
	 */
	private static double fetchDistanceFromServer(String url, String key) throws IOException {
		HttpGet request = new HttpGet(url);

		try (CloseableHttpResponse response = httpClient.execute(request)) 
		{
			int statusCode = response.getStatusLine().getStatusCode();
		    String responseBody = EntityUtils.toString(response.getEntity());
			
			if (statusCode != 200) 
				throw new IOException("OSRM API returned status code: " + statusCode + " for URL: " + url);

			double distance = parseDistanceFromResponse(responseBody);

			// Pausa para evitar rate limiting
			//Thread.sleep(1);                //Farthest-First demora 0.2 mins en ejecutarse correctamente 1 vez
			//Thread.sleep(2);                //Farthest-First demora 0.3 mins en ejecutarse correctamente 1 vez
			//Thread.sleep(5);                //Farthest-First demora 0.6 mins en ejecutarse correctamente 1 vez
			//Thread.sleep(10)                //Farthest-First demora 1.3 mins en ejecutarse correctamente 1 vez
			//Thread.sleep(100);              //Farthest-First demora 9.3 mins en ejecutarse correctamente 1 vez
			//Thread.sleep(1000);
			
			// Guardar en cach� la distancia calculada
			distanceCache.put(key, distance);
			return distance;
		}
	}

	/**
	 * M�todo auxiliar para parsear la distancia desde la respuesta de OSRM.
	 *
	 * @param responseBody Respuesta JSON de OSRM.
	 * @return Distancia en metros.
	 */
	private static double parseDistanceFromResponse(String responseBody) {
		// Parsear la respuesta JSON.
		JsonObject jsonResponse = JsonParser.parseString(responseBody).getAsJsonObject();

		// Validar la estructura del JSON.
		if (!jsonResponse.has("routes") || jsonResponse.getAsJsonArray("routes").size() == 0) 
			throw new IllegalStateException("No routes found in OSRM API response: " + responseBody);
		
		// Extraer la distancia.
		JsonArray routes = jsonResponse.getAsJsonArray("routes");
		JsonObject firstRoute = routes.get(0).getAsJsonObject();

		// Verificar si la distancia est� presente.
		if (!firstRoute.has("distance")) 
			throw new IllegalStateException("Distance not found in the first route of OSRM API response: " + responseBody);
		
		return Math.floor((firstRoute.get("distance").getAsDouble() * 0.001) * 100) / 100.0;
	}
	
	/**
     * M�todo para limpiar la cach� de distancias.
     */
    public static void clearDistanceCache() {
    	System.out.println("---------------------------------------------");
    	System.out.println("CLEARING DISTANCE CACHE WITH: " + distanceCache.size() + " ENTRIES");
        distanceCache.clear();
        
    }
}
