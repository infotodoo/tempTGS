from odoo import fields,models,api



class RequisionStage(models.Model):
    _name = 'requisicion.stage'
    _order='sequence'

    name=fields.Char("Stage Name")
    sequence=fields.Integer("sequence", default=1)

   
  