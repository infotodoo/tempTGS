# -*- coding: utf-8 -*-
# BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HrJob(models.Model):   
    _inherit = 'ir.actions.report'

    job_id = fields.Many2one('job.id', 'Puesto de Trabajo')
    reporte = fields.Many2one('ir.actions.report', string="Informes")
    company_id = fields.Many2many('res.company', string="Compañía")
    
    