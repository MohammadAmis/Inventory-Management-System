from reportlab.lib.pagesizes import letter  # letter, A4, legal, tabloid
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from random import randrange
from PyQt5.QtWidgets import QMessageBox,QApplication
from Email import Sending_Receipt_Using_Email
import sys

def create_receipt_and_send_email(vendor_name, checked_rows, notes, email_id, save_amount):
    receipt_no = randrange(100000, 999999)
    current_date = datetime.now().strftime('%Y-%m-%d')

    filename = f"OrderReceipt/{vendor_name}_{receipt_no}_{current_date}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Table data
    table_data = [["Product Name", "Price", "Quantity", "Total"]]
    total_amount = 0
    
    for order in checked_rows:
        product_name = order[3]
        price = float(order[4])
        quantity = int(order[5])
        total = price * quantity
        table_data.append([product_name, price, quantity, total])
        total_amount += total

    table = Table(table_data)

    style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('SIZE', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ])

    table.setStyle(style)

    story = []

    styles = getSampleStyleSheet()
    center_top_style = styles["Normal"]
    center_top_style.alignment = 1
    shop_info = f"<h1><b>Inventory Management System</b></h1><br/>Saboo Siddik Polytechnic Road, Mumbai, Maharashtra"
    shop_para = Paragraph(shop_info, center_top_style)
    
    right_top_style = styles["Normal"]
    right_top_style.alignment = 2
    bill_info = Paragraph(f"""<br/><br/><b>From :{'&nbsp;' * 99} </b>Bill Number: {receipt_no}<br/>
                          Name: Mohammad Amis {'&nbsp;' * 70} Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                          <br/>Mobile: 8052757464<br/>Email: mugeeraamis@gmail.com"<br/><br/>
                          """, right_top_style)
    
    story.append(shop_para)
    story.append(bill_info)
    story.append(table)
    story.append(Spacer(1, 20))  # Add space
    
    total_para = Paragraph(f"<b>Total Amount:</b> {total_amount}", styles['BodyText'])
    save_para = Paragraph(f"<b>Save Amount:</b> {save_amount}", styles['BodyText'])
    story.append(total_para)
    story.append(save_para)
    
    notes_para = Paragraph(f"<b>Notes:</b><br/>{notes}", styles['BodyText'])
    story.append(notes_para)

    # Build the PDF
    doc.build(story)
    
    reply = QMessageBox.question(None, 'Confirmation', 'Do you want to send the email?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        Sending_Receipt_Using_Email(email_id, f"C:\\Users\\Lenovo\\Desktop\\Inventory Management System\\{filename}")
    else:
        print("Email sending cancelled.")

# Function to extract data from QTableWidget
def extract_data_from_table(table_widget):
    row_count = table_widget.rowCount()
    column_count = table_widget.columnCount()
    table_data = []

    for row in range(row_count):
        row_data = []
        for column in range(column_count):
            item = table_widget.item(row, column)
            text = item.text() if item else ""
            row_data.append(text)
        table_data.append(row_data)
    
    return table_data

# Example PyQt5 application to demonstrate the functionality
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Example data and settings
    vendor_name = "Example Vendor"
    checked_rows = [
        ["", "", "", "Product A", "100", "2"],
        ["", "", "", "Product B", "150", "1"],
    ]
    notes = "These are example notes."
    email_id = "example@example.com"
    save_amount = 50  # Example save amount
    
    create_receipt_and_send_email(vendor_name, checked_rows, notes, email_id, save_amount)
    
    sys.exit(app.exec_())
