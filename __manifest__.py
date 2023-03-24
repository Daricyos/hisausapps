{
    'name': 'Hisausapps',

    'author': 'Kodershop',
    'website': 'https://kodershop.com/',

    'category': 'E-commerce',
    'license': 'OPL-1',
    'version': '16.0.0.0.0',

    'depends': ['base',
                ],

    'data': [
        'security/ir.model.access.csv',

        'views/menu_views.xml',
        'views/ks_key_views.xml',
        'views/ruling_views.xml',
    ],
    'installable': True,
    'application': True,

    'images': [
        'static/description/icon.png',
    ],
}
