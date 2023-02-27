
import sys
import io
import osmnx as ox
import folium
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout,QPushButton, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine

"""
Folium in PyQt5
"""
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.resize(800, 720)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.view_zoom = 15

        # Cargar el grafo desde el archivo .osm
        G = ox.graph_from_xml('map.osm', simplify=False)

        # Obtener las coordenadas del centro del grafo
        location = (18.6259036, -69.4914634)
        m = folium.Map(
        	zoom_start=self.view_zoom,
        	location=location
        )

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView, stretch=7)
        
        # Contenedor para los textfields y el button.
        textFieldLayout = QVBoxLayout()
        
        src = QLineEdit(self)
        src.setPlaceholderText("Origen nodeID..")
        textFieldLayout.addWidget(src)
        
        dst = QLineEdit(self)
        dst.setPlaceholderText("Destino nodeID..")
        textFieldLayout.addWidget(dst)
        
        button = QPushButton("Encontrar ruta")
        button.clicked.connect(self.zoom)
        textFieldLayout.addWidget(button)
        
        layout.addLayout(textFieldLayout)
        
    def zoom(self):
        print(f"view_zoom {self.view_zoom}")
        self.view_zoom += 1
        location = (18.6259036, -69.4914634)
        m = folium.Map(
            zoom_start=self.view_zoom,
            location=location
        )
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 25px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')