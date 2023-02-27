import osmnx as ox
file = 'map.osm'
G = ox.graph_from_xml(file)

# define the colors to use for different edge types
hwy_colors = {'footway': 'skyblue',
              'residential': 'paleturquoise',
              'cycleway': 'orange',
              'service': 'sienna',
              'living street': 'lightgreen',
              'secondary': 'grey',
              'pedestrian': 'lightskyblue'}

# return edge IDs that do not match passed list of hwys
def find_edges(G, hwys):
    edges = []
    for u, v, k, data in G.edges(keys=True, data='highway'):
        check1 = isinstance(data, str) and data not in hwys
        check2 = isinstance(data, list) and all([d not in hwys for d in data])
        if check1 or check2:
            edges.append((u, v, k))
    return set(edges)

# first plot all edges that do not appear in hwy_colors's types
G_tmp = G.copy()
G_tmp.remove_edges_from(G.edges - find_edges(G, hwy_colors.keys()))
m = ox.plot_graph_folium(G_tmp, popup_attribute='highway', weight=5, color='black')

# then plot each edge type in hwy_colors one at a time
for hwy, color in hwy_colors.items():
    G_tmp = G.copy()
    G_tmp.remove_edges_from(find_edges(G_tmp, [hwy]))
    if G_tmp.edges:
        m = ox.plot_graph_folium(G_tmp,
                                 graph_map=m,
                                 popup_attribute='highway',
                                 weight=5,
                                 color=color)

m.save("omx.html")