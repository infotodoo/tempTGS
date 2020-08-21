from odoo import fields,models,api



class Todoo_ccnomina(models.Model):
    _name = 'ccnomina'
    _rec_name = 'nombre_ccnomina'
   
    nombre_ccnomina=fields.Char()
    identificador=fields.Char()
    
  