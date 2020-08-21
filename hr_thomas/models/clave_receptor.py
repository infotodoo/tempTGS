from odoo import fields,models,api



class Todoo_ccnomina(models.Model):
    _name = 'clave'
    _rec_name = 'nombre_clave_receptor'
   
    nombre_clave_receptor=fields.Char()
    identificador=fields.Char()