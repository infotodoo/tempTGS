from odoo import fields,models,api



class Todoo_ccnomina(models.Model):
    _name = 'division'
    _rec_name = 'nombre_division'
   
    nombre_division=fields.Char()
    identificador=fields.Char()