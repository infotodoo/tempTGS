from odoo import fields,models,api



class Todoo_beneficio_sap(models.Model):
    _name = 'beneficio'
    _rec_name = 'nombre_beneficio'
   
    nombre_beneficio=fields.Char()
    identificador=fields.Char()
    