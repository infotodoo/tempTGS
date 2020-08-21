# -*- coding: utf-8 -*-
#BY: LUIS FELIPE PATERNINA VITAL - TODOO SAS

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta

class Todoo(models.Model):
    _inherit = 'hr.departure.wizard'

    