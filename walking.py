import osmnx as ox
import networkx as nx

ox.config(log_console=True,
          use_cache=True)

G_walk = ox.graph_from_xml('map.osm')

orig_node = ox.nearest_nodes(G_walk, 18.5318803, -69.4860876)

dest_node = ox.nearest_nodes(G_walk, 18.6215826, 69.4937259)

route = nx.shortest_path(G_walk, orig_node, dest_node, weight='length')

fig, ax = ox.plot_graph_route(G_walk,
                              route,
                              node_size=0,
                              save=True,)