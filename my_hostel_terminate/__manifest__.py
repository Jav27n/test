# -*- coding: utf-8 -*-
{
    'name': "hostel terminate",

    'summary': "My Hostel Extension",

    'description': """
My Hostel Extension 
    """,

    'author': "HSxTECH",
    'website': "https://www.hsxtech.net",
    'category': 'Hostel',
    'version': '18.0.0.1',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'my_hostel'],

    'data': [
        'views/hostel_room.xml',
        'views/hostel_room_category.xml',
    ],

    'application': True,
    'license': 'LGPL-3'
}

