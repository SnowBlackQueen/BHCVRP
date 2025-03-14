import requests
import time
from typing import Dict, Tuple

class OSRMService:
    # URLs de los servidores OSRM (remoto y local)
    OSRM_URL = "https://router.project-osrm.org/"
    OSRM_LOCAL_URL = "http://localhost:5000/route/v1/driving/"

    # Caché para almacenar distancias ya calculadas
    distance_cache: Dict[str, float] = {}

    # Contador de errores en el servidor remoto
    remote_error_count: int = 0
    MAX_REMOTE_ERRORS: int = 3

    def __init__(self):
        pass

    def calculate_distance(self, axis_x_ini, axis_y_ini, axis_x_end, axis_y_end):
        """
        Calcula la distancia entre dos puntos utilizando OSRM API.

        :param axis_x_ini: Coordenada X del punto inicial.
        :param axis_y_ini: Coordenada Y del punto inicial.
        :param axis_x_end: Coordenada X del punto final.
        :param axis_y_end: Coordenada Y del punto final.
        :return: Distancia en metros.
        :raises Exception: Si ocurre un error al calcular la distancia.
        """
        distance = 0.0

        # Generar clave única para la caché
        key = f"{axis_x_ini},{axis_y_ini}->{axis_x_end},{axis_y_end}"

        # Verificar si la distancia ya está en la caché
        if key in self.distance_cache:
            distance = self.distance_cache[key]
            return distance

        # Construir las URLs para el servidor remoto y local
        remote_url = f"{self.OSRM_URL}{axis_y_ini},{axis_x_ini};{axis_y_end},{axis_x_end}?overview=false&alternatives=false"
        local_url = f"{self.OSRM_LOCAL_URL}{axis_y_ini},{axis_x_ini};{axis_y_end},{axis_x_end}?overview=false&alternatives=false"

        # Verificar qué tipo de servidor utilizar
        if self.remote_error_count >= self.MAX_REMOTE_ERRORS:
            try:
                distance = self._fetch_distance_from_server(remote_url, key)
            except Exception as e:
                self.remote_error_count += 1

                if self.remote_error_count >= self.MAX_REMOTE_ERRORS:
                    raise Exception("Max error attempts reached. Switching to local server only.") from e
        else:
            try:
                distance = self._fetch_distance_from_server(local_url, key)
            except Exception as e:
                raise Exception("Local servers failed to calculate distance.") from e

        return distance

    def _fetch_distance_from_server(self, url: str, key: str) -> float:
        """
        Realiza una solicitud al servidor OSRM (remoto o local) y obtiene la distancia.

        :param url: URL del servidor OSRM.
        :param key: Clave única para almacenar la distancia en la caché.
        :return: Distancia en metros.
        :raises Exception: Si ocurre un error en la solicitud HTTP o en el servidor.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción si el código de estado no es 200

            # Parsear la respuesta JSON
            distance = self._parse_distance_from_response(response.json())

            # Guardar en caché la distancia calculada
            self.distance_cache[key] = distance

            # Pausa para evitar rate limiting (opcional)
            time.sleep(1)

            return distance
        except requests.RequestException as e:
            raise Exception(f"Error fetching distance from OSRM server: {e}") from e

    def _parse_distance_from_response(self, response: dict) -> float:
        """
        Parsea la distancia desde la respuesta JSON de OSRM.

        :param response: Respuesta JSON de OSRM.
        :return: Distancia en metros.
        :raises Exception: Si la respuesta no tiene la estructura esperada.
        """
        if "routes" not in response or len(response["routes"]) == 0:
            raise Exception("No routes found in OSRM API response.")

        first_route = response["routes"][0]
        if "distance" not in first_route:
            raise Exception("Distance not found in the first route of OSRM API response.")

        # Redondear la distancia a 2 decimales (opcional)
        distance = round(first_route["distance"], 2)
        return distance

    def clear_distance_cache(self) -> None:
        """
        Limpia la caché de distancias.
        """
        print(f"Clearing distance cache with {len(self.distance_cache)} entries.")
        self.distance_cache.clear()