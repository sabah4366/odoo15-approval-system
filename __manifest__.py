{
    'name': 'Inv Approval system',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Manage Deliver Order approvals',
    'description': """
        This module adds an approval workflow for delivery orders.
    """,
    'sequence': -500,
    'author': 'Sabah',
    'website': 'https://www.example.com',
    'depends': ['base','account','stock','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_date.xml',
        'data/sequence_data.xml',
        'view/stock_picking_inherit.xml',
        'view/invoicing_menu.xml',
        'view/stock_picking_type.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
