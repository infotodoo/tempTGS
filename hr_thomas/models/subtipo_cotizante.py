from odoo import fields,models,api



class Todoo_subtipo_tipo_cotizante(models.Model):
    _name = 'subtipo.cotizante'
    _rec_name = 'nombre_sub_tipo_cotizante'
   
    nombre_sub_tipo_cotizante=fields.Char()
    