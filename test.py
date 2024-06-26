from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)
        
        # Load the custom widget
        self.custom_widget = loadUi('ProductTempelate.ui', QWidget(self))
        
        # Set up the layout
        self.layout = QHBoxLayout()
        
        self.layout.addWidget(self.custom_widget)
        
        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
