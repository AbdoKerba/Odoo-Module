{
    'name': 'Library',
    'version': '1.0',
    'summary': 'Library Management',
    'depends': ['base', 'sale_management', 'account', 'mail'],
    'data': [
        'security/book_security_groups.xml',
        'security/ir.model.access.csv',
        'data/book_view.xml',
        'data/author_view.xml',
        'data/sale_order_inherit_view.xml',
        'data/book_sequence.xml',
        'data/book_history_view.xml',
        'data/account_inherit_view.xml',
        'wizards/book_state_view.xml',
        'report/book_template.xml'
             ],
    'assets': {
        'web.assets_backend': ['library/static/src/css/book.css'],
        'web.report_assets_common': ['library/static/src/css/fonts.css']
    },
    'application': True
}