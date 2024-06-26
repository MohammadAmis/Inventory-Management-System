from PyQt5.QtGui import  QStandardItem
from PyQt5.QtCore import Qt
import sqlite3
from Receipts import create_receipt_and_send_email
from random import randrange

def load_vendor_names(self):
    
        self.cmbVendorList.clear()
        connection = sqlite3.connect("InventoryManagement.db")
        cursor = connection.cursor()
        cursor.execute("SELECT vendor_name FROM VENDOR")
        vendors = cursor.fetchall()
        for vendor in vendors:
            self.cmbVendorList.addItem(vendor[0])
            
        connection.close()


def handle_vendor_selection(self):
        selected_vendor = self.cmbVendorList.currentText()
        load_vendor_products(self,selected_vendor)
        

def load_vendor_products(self, vendor_name):
    self.VendorProductModel.clear()
    
    connection = sqlite3.connect("InventoryManagement.db")
    cursor = connection.cursor()
    cursor.execute("SELECT product_catalog FROM vendor WHERE vendor_name=?", (vendor_name,))
    products = cursor.fetchone()
    if products:
        product_catalog = products[0].split(',')  # Assuming product_catalog is a comma-separated string
        
        for product_name in product_catalog:
            item_name = QStandardItem(product_name.strip())  # Strip whitespace characters from the product name
            item_quantity = QStandardItem('1')  # Default quantity of one
            item_name.setCheckable(True)  # Make the item checkable if needed
            item_name.setCheckState(Qt.Unchecked)  # Set the initial check state if needed
            self.VendorProductModel.appendRow([item_name, item_quantity])
    
    self.VendorProductModel.setHorizontalHeaderLabels(["Product Name","Quantity"])
    self.VendorProductTable.setColumnWidth(0, 250)
    self.VendorProductTable.setColumnWidth(1, 100)

    
    total_height = self.VendorProductModel.rowCount() * self.VendorProductTable.rowHeight(0)  # Assuming all rows have the same height
    self.VendorProductTable.setFixedHeight(total_height+40)
    
    self.btnOrderProduct.move(160, 240+total_height)

    connection.close()
        
        
def addProduct_to_OrderTable(self):
    vendor_name = self.cmbVendorList.currentText()
    try:
        connection = sqlite3.connect("InventoryManagement.db")
        cursor = connection.cursor()
        
        fetch_query = f"SELECT * FROM VENDOR WHERE vendor_name = '{vendor_name}'"  # Fetch vendor details
        cursor.execute(fetch_query)
        vendor_details = cursor.fetchone()
        
        if vendor_details is None:
            raise ValueError("Vendor not found")

    except Exception as ex:
        print(ex)
        return
    
    vendor_id = str(vendor_details[0])  # vendor_id
    vendor_email_id = vendor_details[3]  # vendor_email_id
    
    insert_query = """INSERT INTO PRODUCT (Vendor_ID, Vendor_Name, Product_Name, Barcode, Quantity) VALUES (?, ?, ?, ?, ?)"""
    update_query = """UPDATE PRODUCT SET Quantity = Quantity + ? WHERE Vendor_ID = ? AND Product_Name = ?"""
    
    checked_rows = []
    for row in range(self.VendorProductModel.rowCount()):  # Total rows
        item = self.VendorProductModel.item(row, 0)  # Assuming the checkable column is at index 0
        if item and item.checkState() == Qt.Checked:
            product_name = self.VendorProductModel.item(row, 0).text()  # Assuming product name is in the second column
            barcode = str(randrange(100000, 999999))
            quantity = self.VendorProductModel.item(row, 1).text()  # Assuming quantity is in the third column

            # Check if the product already exists
            cursor.execute("SELECT Quantity FROM PRODUCT WHERE Vendor_ID = ? AND Product_Name = ?", (vendor_id, product_name))
            existing_product = cursor.fetchone()
            
            if existing_product:
                # Update the quantity if the product exists
                cursor.execute(update_query, (quantity, vendor_id, product_name))
            else:
                # Insert new product if it does not exist
                cursor.execute(insert_query, (vendor_id, vendor_name, product_name, barcode, quantity))
            
            row_data = [vendor_id, vendor_name, product_name, barcode, quantity]
            checked_rows.append(row_data)
            connection.commit()

    for row_data in checked_rows:
        items = [QStandardItem(item) for item in row_data]
        self.PurchseProductModel.appendRow(items)
    
    self.VendorProductModel.clear()
    self.btnOrderProduct.move(160, 240)
    connection.close()
    
    # Invoke to create receipt
    notes = "Thank you for your business!"
    # create_receipt_and_send_email(vendor_name, checked_rows, notes, vendor_email_id)
