
#Luis Felipe Paternina Vital - Todoo SAS
from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta

class Todoo(models.Model):
    _inherit = 'hr.recruitment.stage'

    active = fields.Boolean('active', default=True)
