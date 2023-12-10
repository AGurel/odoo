{
    'name': 'Teklif Sihirbazı',
    'version': '1.0',
    'category': "Sales",
    'author': 'Abdurrahman GÜREL',
    'depends': ['product', 'mail'],
    'summary': 'Quotation, Sales Orders, Delivery & Invoicing Control',
    'description': """
Manage sales quotations and orders
==================================

This module makes the link between the sales and warehouses management applications.

Preferences
-----------
* Shipping: Choice of delivery at once or partial delivery
* Invoicing: choose how invoices will be paid
* Incoterms: International Commercial terms

""",
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/teklif.xml',
    ]
}