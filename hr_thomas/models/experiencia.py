# -*- coding: utf-8 -*-
# BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta



class HrResumeLine(models.Model):
    _inherit = 'hr.resume.line'

    rama_empresa_laboro = fields.Selection([('PÚBLICA', 'PÚBLICA'), ('PRIVADA', 'PRIVADA')])
    cargo_desempenado = fields.Many2one('cargo.desen')
    Tipo_de_Contrato = fields.Selection(
        [('CONTRATO FIJO', 'CONTRATO FIJO'), ('CONTRATO INDEFINIDO', 'CONTRATO INDEFINIDO'),
         ('INDEPENDIENTE', 'INDEPENDIENTE'), ('OBRA Y LABOR', 'OBRA Y LABOR'),
         ('PRESTACIÓN DE SERVICIOS', 'PRESTACIÓN DE SERVICIOS')])
    pais = fields.Many2one('res.country')
    actualmente_laborando = fields.Selection([('SI', 'SI'), ('NO', 'NO')])
    tiempo_laborando = fields.Char()
    applicant_id = fields.Many2one('hr.applicant', 'Aplicante')
    employee_id = fields.Many2one(required=False)
    total_days=fields.Integer(string="TOTAL DAYS")

    @api.onchange('date_start', 'date_end','total_days')
    def calculate_date(self):
        if self.date_start and self.date_end:
            d1=datetime.strptime(str(self.date_start),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.date_end),'%Y-%m-%d')
            d3=d2-d1
            self.total_days=str(d3.days)

   