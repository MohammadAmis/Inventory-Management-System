from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QTableView
from functools import partial
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QStandardItemModel
from Vendor_Controller import show_vendor_on_table,handleVendorCellChanged,showContextMenuOnVendor
from Purchase_Controller import handle_vendor_selection,load_vendor_names,addProduct_to_OrderTable
from Product_Controller import show_product_on_table,handleProductCellChanged,showContextMenuOnProduct


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)
        
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet("QPushButton:hover { color: #ffffff; }")
            
        self.btnDashboard.clicked.connect(partial(self.goto, 0, self.btnDashboard))
        self.btnVendor.clicked.connect(partial(self.goto, 1, self.btnVendor))
        self.btnPurchase.clicked.connect(partial(self.goto, 2, self.btnPurchase))
        self.btnProduct.clicked.connect(partial(self.goto, 3, self.btnProduct))
        
                        
        #------------------------- VENDOR START ---------------------------
        self.VendorTableModel = QStandardItemModel()
        self.VendorTableView.setModel(self.VendorTableModel)
        
        show_vendor_on_table(self)
        
        # TO UPDATE ROW
        self.VendorTableModel.itemChanged.connect(partial(handleVendorCellChanged, self)) 
        
        # TO ADD AND DELETE ROW
        self.VendorTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.VendorTableView.customContextMenuRequested.connect(partial(showContextMenuOnVendor,self))
        #------------------------- VENDOR END ---------------------------
        
        #------------------------- PURCHASE START ------------------------
        load_vendor_names(self)
        self.btnOrderProduct.clicked.connect(partial(addProduct_to_OrderTable,self))
        self.cmbVendorList.currentIndexChanged.connect(partial(handle_vendor_selection,self))
        
        self.table = QTableView()
        self.VendorProductModel = QStandardItemModel()
        self.VendorProductTable.setModel(self.VendorProductModel)
        self.table.setModel(self.VendorProductModel)
        
        self.table = QTableView()
        self.PurchseProductModel = QStandardItemModel()
        self.PurchaseTableView.setModel(self.PurchseProductModel)
        self.table.setModel(self.PurchseProductModel)
        
        
        # ------------------------ PRODUCT START
        self.ProductTableModel = QStandardItemModel()
        self.ProductTableView.setModel(self.ProductTableModel)
        show_product_on_table(self)
        
        # TO UPDATE ROW
        self.ProductTableModel.itemChanged.connect(partial(handleProductCellChanged, self)) 
        
        # TO DELETE ROW
        self.ProductTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ProductTableView.customContextMenuRequested.connect(partial(showContextMenuOnProduct,self))
        
        
        
    def goto(self, index, button):
        self.stackedWidget.setCurrentIndex(index)
        match(index):
            case 1:show_vendor_on_table(self)
            case 2:load_vendor_names(self)
            case 3:show_product_on_table(self)
                    
        
    
if __name__ == "__main__": 
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())