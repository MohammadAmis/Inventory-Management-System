from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QMenu
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sqlite3
from PyQt5.QtCore import Qt
from functools import partial

class InventoryPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Invenotory Page.ui', self)
        
        self.InventoryTableModel = QStandardItemModel()
        self.InventoryTableView.setModel(self.InventoryTableModel)
        self.txtBarcode.returnPressed.connect(self.load_product)
        headers = ["Barcode", "Product Name", "Retail Price", "Quantity", "Total"]
        self.InventoryTableModel.setHorizontalHeaderLabels(headers)
        self.InventoryTableView.setColumnWidth(0, 250)
        self.InventoryTableView.setColumnWidth(1, 350)
        self.InventoryTableView.setColumnWidth(2, 250)
        self.InventoryTableView.setColumnWidth(3, 250)
        self.InventoryTableView.setColumnWidth(4, 265)
        
        # TO DELETE ROW
        self.InventoryTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.InventoryTableView.customContextMenuRequested.connect(self.showContextMenuOnInventory)
        
        # TO UPDATE ROW
        self.InventoryTableModel.itemChanged.connect(self.handle_quantity_price)
        
        # TO UPDATE BALANCE
        self.txtPaidPrice.textChanged.connect(self.updateBalance)
        
        # TO PAY
        
        self.btnPay.clicked.connect(self.pay)
        


    def load_product(self):
        if self.InventoryTableModel.rowCount()==14:
            self.InventoryTableView.setColumnWidth(4, 250)
            # self.InventoryTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            
        barcode = self.txtBarcode.text()
        self.txtBarcode.clear()
        row = self.check_duplicate_barcode(barcode)
        if row is not None:
            current_quantity_item = self.InventoryTableModel.item(row, 3)
            current_quantity = int(current_quantity_item.text())
            new_quantity = current_quantity + 1
            self.InventoryTableModel.setItem(row, 3, QStandardItem(str(new_quantity)))
            
            retail_price_item = self.InventoryTableModel.item(row, 2)
            retail_price = float(retail_price_item.text())
            total_price = new_quantity * retail_price
            self.InventoryTableModel.setItem(row, 4, QStandardItem(str(total_price)))
            self.updateBalance()
        else:
            connection = sqlite3.connect("InventoryManagement.db")
            cursor = connection.cursor()
        
            cursor.execute("SELECT Barcode, Product_Name, Retail_Price FROM PRODUCT WHERE Barcode = ? AND Status = 'Available'", (barcode,))
            product = cursor.fetchone()
            connection.close()
        
            if product:                  
                barcode_item = QStandardItem(str(product[0]))
                product_name_item = QStandardItem(str(product[1]))
                retail_price_item = QStandardItem(str(product[2]))
                total_product_price = float(product[2])
                
                row = [barcode_item, product_name_item, retail_price_item, QStandardItem(str(1)), QStandardItem(str(total_product_price))]
                self.InventoryTableModel.appendRow(row)
                
                # Handling Billing Area
                self.txtTotalPrice.setText(str(total_product_price + float(self.txtTotalPrice.text())))
                self.txtBalancePrice.setText(str(total_product_price + float(self.txtBalancePrice.text())))
                self.txtNumberItems.setText(str(int(self.txtNumberItems.text())+1))
                            
            else:
                QMessageBox.warning(self, "Barcode", "Invalid Barcode OR Product Not Available")
            
    def check_duplicate_barcode(self, barcode):
        for row in range(self.InventoryTableModel.rowCount()):
            if barcode == self.InventoryTableModel.item(row, 0).text():
                return row
        return None
                
    def deleteProduct_from_Table(self, row):
        self.InventoryTableModel.removeRow(row)
    
    def showContextMenuOnInventory(self, position):
        index = self.InventoryTableView.indexAt(position)
        if index.isValid():
            row = index.row()
            menu = QMenu()
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(partial(self.deleteProduct_from_Table, row))
            menu.exec_(self.InventoryTableView.viewport().mapToGlobal(position))
    
    def calculate_total_price_quantity(self):
        total_price=0.0
        total_quantity=0
        paid=float(self.txtPaidPrice.text())
        for row in range(self.InventoryTableModel.rowCount()):
            total_price=total_price + float(self.InventoryTableModel.item(row, 4).text())
            total_quantity=total_quantity+int(self.InventoryTableModel.item(row,3).text())
            self.txtTotalPrice.setText(str(total_price))
            self.txtBalancePrice.setText(str(total_price-paid))
            self.txtNumberItems.setText(str(total_quantity))
            
            
            
    def handle_quantity_price(self, item):
        row = item.row()
        col = item.column()

        if col == 3:  # Only update total price if the quantity column is changed
            quantity_item = self.InventoryTableModel.item(row, 3)
            quantity_str = quantity_item.data(Qt.EditRole)
            price_item = self.InventoryTableModel.item(row, 2)
            price_str = price_item.data(Qt.EditRole)

            try:
                quantity = int(quantity_str)
                price = float(price_str)
                total_price = quantity * price
                self.InventoryTableModel.setItem(row, 4, QStandardItem(str(total_price)))
                                
            except ValueError:
                pass  # Handle invalid integer or float conversion if needed
            
        self.calculate_total_price_quantity()
        
    def updateBalance(self):
        try:
            
            paid=float(self.txtPaidPrice.text())
            total=float(self.txtTotalPrice.text())
            balance=total-paid
            self.txtBalancePrice.setText(str(balance))
        except ValueError:
            ...
        

    def pay(self):
        connection = sqlite3.connect("InventoryManagement.db")
        cursor = connection.cursor()
        try:
            for row in range(self.InventoryTableModel.rowCount()):
                barcode=self.InventoryTableModel.item(row, 0).text()
                quantity=self.InventoryTableModel.item(row, 3).text()
                
                cursor.execute("UPDATE PRODUCT SET Quantity = Quantity - ? where Barcode = ? ", (quantity,barcode,))
                connection.commit()
        except:
            ...
        finally:
            connection.close()
            QMessageBox.information(self,"Payment","Payment Success\nVisit Again")

if __name__ == "__main__": 
    import sys
    app = QApplication(sys.argv)
    window = InventoryPage()
    window.show()
    sys.exit(app.exec_())