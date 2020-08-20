# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Niyas Raphy(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import base64
import datetime
import json
import os
import re
import logging
import pytz
import requests
import werkzeug.utils
import werkzeug.wrappers
import urllib.request

from itertools import islice
from xml.etree import ElementTree as ET

import odoo
import odoo.modules.registry

from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.exceptions import Warning
from odoo.addons.web.controllers import main


_logger = logging.getLogger(__name__)

class Session(main.Session):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        ip_list = []
        company = request.env['res.company']._get_main_company()
        block = company.block_ips

        for ip in request.env['allowed.ips'].sudo().search([]):
            ip_list.append(ip.ip_address)

        if not ip_address in ip_list and block:
            return 'IP DO NOT ALLOWED {}'.format(ip_address)
        else:
            request.session.authenticate(db, login, password)
            return request.env['ir.http'].session_info()


# class Home(main.Home):

#     @http.route('/web/login', type='http', auth="public")
#     def web_login(self, redirect=None, **kw):
#         if request.httprequest.method == 'POST':
#             login_mail = request.params['login']
#             mail_validation = re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{0,10}", login_mail)
#             if mail_validation and len(mail_validation.group())==len(login_mail):
#                 return super(Home, self).web_login(redirect, **kw)
#             else:
#                 values = request.params.copy()
#                 values['error'] = _("Wrong login")
#                 response = request.render('web.login', values)
#                 response.headers['X-Frame-Options'] = 'DENY'
#                 return response
#         else:
#             return super(Home, self).web_login(redirect, **kw)
