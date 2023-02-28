"""
file: frontend.py
"""
import io
import osmnx as ox
import folium
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout,QPushButton, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from backend import Graph

class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Map routing')
        self.resize(800, 720)
        self._graph = Graph()
        self.view_zoom = 15
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        

        # Cargar el grafo desde el archivo .osm
        G = ox.graph_from_xml('map.osm', simplify=False)

        # Obtener las coordenadas del centro del grafo
        location = (18.6259036, -69.4914634)
        m = folium.Map(
        	zoom_start=self.view_zoom,
        	location=location
        )

        # save map data to data object
        self.update_map(m)
        self.webView = QWebEngineView()
        
        layout.addWidget(self.webView, stretch=7)
        
        # Contenedor para los textfields y el button.
        textFieldLayout = QVBoxLayout()
        
        self.src = QLineEdit(self)
        self.src.setPlaceholderText("Origen nodeID..")
        textFieldLayout.addWidget(self.src)
        
        self.dst = QLineEdit(self)
        self.dst.setPlaceholderText("Destino nodeID..")
        textFieldLayout.addWidget(self.dst)
        
        button = QPushButton("Encontrar ruta")
        button.clicked.connect(self.find_route)
        textFieldLayout.addWidget(button)
        
        layout.addLayout(textFieldLayout)
        
    def find_route(self):
        m = self._graph.generate_map(self.src.text(), self.dst.text())
        self.update_map(m)
        
    def update_map(self, m):
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())