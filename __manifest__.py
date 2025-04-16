{
    'name': 'Customer Filter Wizard',
    'version': '1.0',
    'depends': ['base', 'sale', 'account'],
    'data': [
        'views/customer_report_line_views.xml',  # prima le viste dei modelli
        'views/customer_date_wizard_views.xml',  # poi il wizard
    ],
    'installable': True,
    'application': False,
}
