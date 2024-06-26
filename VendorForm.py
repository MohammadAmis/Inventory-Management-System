from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import sqlite3

class VendorForm(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('VendorForm.ui', self)
        self.btnVendorAdd.clicked.connect(self.add_vendor)
        self.btnVendorClear.clicked.connect(self.clearForm)
        self.btnAddItem.clicked.connect(lambda: self.itemList.setPlainText(self.itemList.toPlainText() + self.txtItem.text()+", "))


    def add_vendor(self):
        id_ = self.txtID.text()
        name = self.txtName.text()
        mobile = self.txtMobile.text()
        email = self.txtEmailId.text()
        address = self.txtAddress.text()
        product_list = self.itemList.toPlainText()

        try:
            connection = sqlite3.connect("InventoryManagement.db")
            cursor = connection.cursor()

            insert_query = "INSERT INTO Vendor(vendor_id, vendor_name, vendor_mobile_no, vendor_email_id, vendor_address, product_catalog) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_query, (id_, name, mobile, email, address, product_list))
            connection.commit()
            connection.close()

            self.close()  # Close the dialog after adding the vendor
        except sqlite3.Error as error:
            print("Vendor Error:", error)
            
    def clearForm(self):
        self.txtID.clear()
        self.txtName.clear()
        self.txtMobile.clear()
        self.txtEmailId.clear()
        self.txtAddress.clear()
        self.itemList.clear()



