"""
file: main.py
"""
import sys
import frontend
from frontend import Map

if __name__ == '__main__':
    app = frontend.QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 25px;
        }
    ''')
    
    map = Map()
    map.show()
    
    app.exec()
