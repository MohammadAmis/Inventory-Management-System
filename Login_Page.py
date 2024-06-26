from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
import sqlite3
from Main_Window import MainWindow  # Importing MainWindow class from MainWindow.py

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Login_Page.ui', self)
        
        # Connect the btnLogin button to the authenticate function
        self.btnLogin.clicked.connect(self.authenticate)
        
    def authenticate(self):
        name = self.txtUserName.text().strip() # amis
        password = self.txtPassword.text().strip() # 12345678
        try:
            connection = sqlite3.connect("InventoryManagement.db")
            cursor = connection.cursor()
            
            query = "SELECT username, password, user_type FROM Login_Information WHERE username = ? AND password = ?"
            cursor.execute(query, (name, password))
            user = cursor.fetchone()
            connection.close()
            
            if user:
                # Close the LoginPage window
                self.close()
                # Open the MainWindow window
                main_window = MainWindow()
                main_window.show()
            else:
                QMessageBox.warning(None, "Login Failed", "Invalid username or password")         
                
        except sqlite3.Error as error:
            print("Error authenticating user:", error)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())
