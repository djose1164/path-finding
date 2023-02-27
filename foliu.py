import osmnx as ox
import folium

# Cargar el grafo desde el archivo .osm
G = ox.graph_from_xml('map.osm', simplify=False)

# Obtener las coordenadas del centro del grafo
center = ox.graph_to_gdfs(G, edges=False).unary_union.centroid.coords[0]

# Crear un mapa con folium centrado en las coordenadas del grafo
m = folium.Map(location=center[::-1], zoom_start=12)



# Mostrar el mapa
m.save("index.html")
