from odoo import fields,models,api



class Todoo_area_personal(models.Model):
    _name = 'area.personal'
    _rec_name = 'nombre_area_personal'
   
    nombre_area_personal=fields.Char()
    identificador=fields.Char()