from reportlab.lib.pagesizes import  letter #letter , A4 , legal, tabloid
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from random import randrange
from Email import Sending_Receipt_Using_Email
from PyQt5.QtWidgets import QMessageBox

def create_receipt_and_send_email(vendor_name,checked_rows,notes,email_id):
    
    receipt_no = randrange(100000, 999999)
    current_date = datetime.now().strftime('%Y-%m-%d')

    filename = f"OrderReceipt/{vendor_name}_{receipt_no}_{current_date}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    table_data = [["Product Name", "Quantity"],]
    for order in checked_rows: table_data.append([order[3], order[4]])

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
    
    
    styles1 = getSampleStyleSheet()
    right_top_style = styles1["Normal"]
    right_top_style.alignment = 0
    bill_info = Paragraph(f"""<br/><br/><b>From :{'&nbsp;' * 99} </b>Bill Number: {receipt_no}<br/>
                          Name: Mohammad Amis {'&nbsp;' * 70} Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                          <br/>Mobile: 8052757464<br/>Email: mugeeraamis@gmail.com"<br/><br/>
                          """, right_top_style)
    
    story.append(shop_para)
    story.append(bill_info)
    story.append(table)
    story.append(Spacer(1, 20))  # Add space
    
    notes_para = Paragraph(f"<b>Notes:</b><br/>{notes}", styles['BodyText'])
    story.append(notes_para)

    # Build the PDF
    doc.build(story)
    
    reply = QMessageBox.question(None, 'Confirmation', 'Do you want to send the email?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        Sending_Receipt_Using_Email(email_id,f"C:\\Users\\Lenovo\\Desktop\\Inventory Management System\\{filename}")
    else:
        print("Email sending cancelled.")
    