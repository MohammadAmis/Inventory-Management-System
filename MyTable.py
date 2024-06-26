from PyQt5.QtGui import QStandardItem
import sqlite3
from PyQt5.QtWidgets import QMenu, QMessageBox,QDialog
from VendorForm import VendorForm
from functools import partial

vendor_table={
    0:"vendor_id",
    1:"vendor_name",
    2:"vendor_mobile_no",
    3:"vendor_email_id",
    4:"vendor_address",
    5:"product_catalog",
}

def show_vendor_on_table(self):
        try:
            connection = sqlite3.connect("InventoryManagement.db")
            cursor = connection.cursor()
            
            fetch_query="SELECT * FROM VENDOR"
            cursor.execute(fetch_query)
            vendor_details=cursor.fetchall()
            
        except Exception as ex:
            print(ex)
            
        self.model.clear()
        for vendor in vendor_details:
            self.model.appendRow([
                QStandardItem(str(vendor[0])),  # vendor_id
                QStandardItem(vendor[1]),  # vendor_name
                QStandardItem(vendor[2]),  # vendor_mobile_no
                QStandardItem(vendor[3]),  # vendor_email_id
                QStandardItem(vendor[4]),  # vendor_address
                QStandardItem(vendor[5])   # product_catalog
            ])
            
            
def addVendor_to_DB(self):
        id_ = self.txtID.text()
        name = self.txtName.text()
        mobile = self.txtMobile.text()
        email = self.txtEmailId.text()
        address = self.txtAddress.text()
        product_list = self.itemList.toPlainText()
        
        try:
            connection = sqlite3.connect("InventoryManagement.db")
            cursor = connection.cursor()
            
            insert_query="INSERT into Vendor(vendor_id,vendor_name,vendor_mobile_no,vendor_email_id,vendor_address,product_catalog) VALUES(?,?,?,?,?,?)"
            cursor.execute(insert_query,(id_,name,mobile,email,address,product_list))
            connection.commit()
            connection.close()
            
        except sqlite3.Error as error:
            print("Vendor Error :", error)
        
        show_vendor_on_table(self)
        

def handleCellChanged(self, item):
    row = item.row()
    col = item.column()
    value = item.text()
    id_item = self.model.item(row, 0)  # Assuming ID is in the first column
    id_value = id_item.text()
    
    # Update the database with the new value using parameterized query
    try:
        connection = sqlite3.connect("InventoryManagement.db")
        cursor = connection.cursor()
        cursor.execute(f"UPDATE Vendor SET {vendor_table[col]} = ? WHERE vendor_id = ?", (value, id_value))
        connection.commit()
        connection.close()
        print("Database updated successfully.")
    except sqlite3.Error as update_error:
        print("Update Error:", update_error)


def deleteVendor_from_DB(self, row):
    id_item = self.model.item(row, 0)  # Assuming ID is in the first column
    if id_item is None:
        QMessageBox.warning(self,"Error","Select Row")
        return
    else:
        id_value = id_item.text()
    
    try:
        connection = sqlite3.connect("InventoryManagement.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Vendor WHERE vendor_id = ?", (id_value,))
        connection.commit()
        connection.close()
        print("Row deleted from database successfully.")
    except sqlite3.Error as delete_error:
        print("Delete Error:", delete_error)

    # Remove the row from the table view after deleting from the database
    self.model.removeRow(row)
    
    
def openAddVendorForm():
        add_form = VendorForm()
        result = add_form.exec_()
        if result == QDialog.Accepted:
            # Data was saved, update the table view
            # show_vendor_on_table()   
            print("Vendor Added") 
        else:
            print("Vendor Not Added")
    
def showContextMenu(self, position):
        row = self.VendorTableView.indexAt(position).row()
        menu = QMenu()  
        delete_action = menu.addAction("Delete Vendor")
        delete_action.triggered.connect(partial(deleteVendor_from_DB,self,row))
        add_record = menu.addAction("Add Vendor")
        add_record.triggered.connect(openAddVendorForm)
        menu.exec_(self.VendorTableView.viewport().mapToGlobal(position))
