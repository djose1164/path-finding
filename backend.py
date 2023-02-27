import xml.etree.ElementTree as ET
from math import sin, cos, sqrt, atan2, radians
import heapq
import folium

# Función para calcular la distancia entre dos puntos dadas sus coordenadas latitud y longitud
def distance(lat1, lon1, lat2, lon2):
    R = 6373.0 # Radio de la Tierra en km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Parsear el archivo XML
tree = ET.parse("map.osm")
root = tree.getroot()

# Crear una lista de adyacencia de los nodos y sus nodos adyacentes con sus distancias
adj_list = {}
nodes_dict = {}
for node in root.findall("./node"):
    node_id = node.attrib["id"]
    nodes_dict[node_id] = {
        "lat": float(node.attrib["lat"]),
        "lon": float(node.attrib["lon"])
    }
for way in root.findall("./way"):
    # Obtener los nodos que forman el way
    nodes = [node.attrib["ref"] for node in way.findall("./nd")]
    # Agregar las conexiones a la lista de adyacencia
    for i, node in enumerate(nodes):
        if i > 0:
            dist = distance(
                nodes_dict[node]["lat"], nodes_dict[node]["lon"],
                nodes_dict[nodes[i-1]]["lat"], nodes_dict[nodes[i-1]]["lon"]
            )
            adj_list.setdefault(node, []).append((nodes[i-1], dist))
        if i < len(nodes)-1:
            dist = distance(
                nodes_dict[node]["lat"], nodes_dict[node]["lon"],
                nodes_dict[nodes[i+1]]["lat"], nodes_dict[nodes[i+1]]["lon"]
            )
            adj_list.setdefault(node, []).append((nodes[i+1], dist))

# Implementación del algoritmo UCS
def ucs(graph, start, goal):
    visited = set()
    queue = [(0, start, [])]
    heapq.heapify(queue)
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [node]
            if node == goal:
                return path
            for neighbor, distance in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + distance, neighbor, path))
    return []


def get_optimal_route(start_node, goal_node):
    # Buscamos la ruta más óptima entre los nodos de inicio y final
    # Devuelve una lista con los nodos transitorios
    print(adj_list)
    return ucs(adj_list, start_node, goal_node)

def get_coordinates(node_id):
    return nodes_dict[node_id]["lat"], nodes_dict[node_id]["lon"]

def generate_map(start_node, goal_node, zoom_start=15):
    # Obtenemos la ruta óptima y sus coordenadas
    path = get_optimal_route(start_node, goal_node)
    path_coords = [get_coordinates(node) for node in path]

    # Configuración del mapa
    folium_map = folium.Map(location=path_coords[0], zoom_start=15)

    # Marcador del inicio
    folium.Marker(location=path_coords[0], icon=folium.Icon(color="green")).add_to(folium_map)

    # Marcador del fin
    folium.Marker(location=path_coords[-1], icon=folium.Icon(color="red")).add_to(folium_map)

    # Dibujar la ruta en el mapa
    folium.PolyLine(locations=path_coords, color="blue").add_to(folium_map)

    # Mostrar el mapa
    return folium_map

if __name__ == "__main__":
    # Definimos los nodos de inicio y final
    start_node = input("Ingrese el primer nodo: ")
    goal_node = input("Ingrese el segundo nodo: ")

    path = get_optimal_route(start_node, goal_node)
    # Imprimimos la ruta encontrada
    if not path:
        print(f"No se encontró ruta entre {start_node} y {goal_node}")
    else:
        print(f"Ruta encontrada: {' -> '.join(path)}")