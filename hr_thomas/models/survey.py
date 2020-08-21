# -*- coding: utf-8 -*-
#BY: LUIS FELIPE PATERNINA VITAL - TODOO SAS

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta

class Todoo(models.Model):
    _inherit = 'survey.survey'

    manejo_interno = fields.Boolean(string="Manejo Interno")


class Todoo2(models.Model):
    _inherit = 'survey.user_input'

    candidato = fields.Many2one('hr.applicant', string="Candidato")