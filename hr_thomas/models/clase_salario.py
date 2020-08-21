from odoo import fields,models,api



class Todoo_subtipo_tipo_cotizante(models.Model):
    _name = 'clase.salario'
    _rec_name = 'clase_salario'
   
    clase_salario=fields.Char()
    