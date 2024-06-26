from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QMenu, QMessageBox
from functools import partial
import sqlite3

Product_Table = {
    0: "Vendor_ID",
    1: "Vendor_Name",
    2: "Product_Name",
    3: "Barcode",
    4: "Cost",
    5: "Retail_Price",
    6: "Quantity",
    7: "Reorder_Level",
    8: "Description",
    9: "Status"
}

def show_product_on_table(self):
    try:
        with sqlite3.connect("InventoryManagement.db") as connection:
            cursor = connection.cursor()
            self.ProductTableModel.clear()
            
            fetch_query = "SELECT * FROM PRODUCT"
            cursor.execute(fetch_query)
            product_details = cursor.fetchall()
            
            self.ProductTableModel.setHorizontalHeaderLabels(["Vendor ID", "Vendor Name", "Product Name", "Barcode", "Cost", "Retail Price", "Quantity", "Reorder Level", "Description", "Status"])

            for product in product_details:
                if product:
                    row = [
                        QStandardItem(str(product[0])),  # Vendor ID
                        QStandardItem(str(product[1])),  # Vendor Name
                        QStandardItem(str(product[2])),  # Product Name
                        QStandardItem(str(product[3])),  # Barcode
                        QStandardItem(str(product[4])),  # Cost
                        QStandardItem(str(product[5])),  # Retail Price
                        QStandardItem(str(product[6])),  # Quantity
                        QStandardItem(str(product[7])),  # Reorder Level
                        QStandardItem(str(product[8])),  # Description
                        QStandardItem(str(product[9]))   # Status
                    ]
                    self.ProductTableModel.appendRow(row)
                else:
                    print("Incomplete product details:", product)
    except sqlite3.Error as ex:
        print("Error fetching product details:", ex)
    finally:
        self.ProductTableView.setColumnWidth(0, 150)  # Vendor ID
        self.ProductTableView.setColumnWidth(1, 300)  # Vendor Name
        self.ProductTableView.setColumnWidth(2, 150)  # Product Name
        self.ProductTableView.setColumnWidth(3, 120)  # Barcode
        self.ProductTableView.setColumnWidth(4, 120)  # Cost
        self.ProductTableView.setColumnWidth(5, 125)  # Retail Price
        self.ProductTableView.setColumnWidth(6, 125)  # Quantity
        self.ProductTableView.setColumnWidth(7, 125)  # Reorder Level
        self.ProductTableView.setColumnWidth(8, 425)  # Description
        self.ProductTableView.setColumnWidth(9, 125)  # Status

def deleteProduct_from_DB(self, row):
    barcode_item = self.ProductTableModel.item(row, 3)  # Assuming Barcode is in the fourth column
    if barcode_item is None:
        QMessageBox.warning(self, "Error", "Select Any Record")
        return
    else:
        barcode_value = barcode_item.text()
    
    try:
        with sqlite3.connect("InventoryManagement.db") as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Product WHERE Barcode = ?", (barcode_value,))
            connection.commit()
            print("Row deleted from database successfully.")
    except sqlite3.Error as delete_error:
        print("Delete Error:", delete_error)

    # Remove the row from the table view after deleting from the database
    self.ProductTableModel.removeRow(row)

def handleProductCellChanged(self, item):
    row = item.row()
    col = item.column()
    value = item.text()
    barcode_item = self.ProductTableModel.item(row, 3)  # Assuming Barcode is in the fourth column
    barcode_value = barcode_item.text()
    
    # Update the database with the new value using parameterized query
    try:
        with sqlite3.connect("InventoryManagement.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE Product SET {Product_Table[col]} = ? WHERE Barcode = ?", (value, barcode_value))
            connection.commit()
            print("Database updated successfully.")
    except sqlite3.Error as update_error:
        print("Update Error:", update_error)

def showContextMenuOnProduct(self, position):
    row = self.VendorTableView.indexAt(position).row()
    menu = QMenu()
    delete_action = menu.addAction("Delete Vendor")
    delete_action.triggered.connect(partial(deleteProduct_from_DB, self, row))
    # add_record = menu.addAction("Add Vendor")
    # add_record.triggered.connect(partial(openAddVendorForm, self))
    menu.exec_(self.VendorTableView.viewport().mapToGlobal(position))
