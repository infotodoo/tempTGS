# -*- coding: utf-8 -*-
# from odoo import http


# class ConnectionThomas(http.Controller):
#     @http.route('/connection_thomas/connection_thomas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/connection_thomas/connection_thomas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('connection_thomas.listing', {
#             'root': '/connection_thomas/connection_thomas',
#             'objects': http.request.env['connection_thomas.connection_thomas'].search([]),
#         })

#     @http.route('/connection_thomas/connection_thomas/objects/<model("connection_thomas.connection_thomas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('connection_thomas.object', {
#             'object': obj
#         })
