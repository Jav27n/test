# -*- coding: utf-8 -*-
# from odoo import http


# class MyHostel(http.Controller):
#     @http.route('/my_hostel/my_hostel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_hostel/my_hostel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_hostel.listing', {
#             'root': '/my_hostel/my_hostel',
#             'objects': http.request.env['my_hostel.my_hostel'].search([]),
#         })

#     @http.route('/my_hostel/my_hostel/objects/<model("my_hostel.my_hostel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_hostel.object', {
#             'object': obj
#         })

