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
import urllib.request
from ipaddress import ip_address, ip_network

from odoo import models, fields, http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def block_ips(self):
        company = request.env["res.company"]._get_main_company()
        block = company.block_ips
        if block:
            user_ip_address = request.httprequest.environ["REMOTE_ADDR"]
            ip_list = []
            ip_networks = []

            for ip in request.env["allowed.ips"].sudo().search([]):
                if not ip.network:
                    ip_list.append(ip.ip_address)
                elif ip.network:
                    ip_networks.append(ip_network(ip.ip_address))

            if not user_ip_address in ip_list and block:
                if ip_networks:
                    user_ip_address = ip_address(user_ip_address)
                    for network in ip_networks:
                        if user_ip_address in network:
                            _logger.error(
                                f"\nAllowed IP in network: {user_ip_address}, {network}"
                            )
                            return False
                        else:
                            _logger.error(
                                f"\nDo not allowed IP in network: {user_ip_address}, {network}"
                            )
                _logger.error(f"\nDo not allowed IP: {user_ip_address}")
                # Template from https://www.w3schools.com/css/css_templates.asp
                if not company.redirect_to:
                    url = "https://www.google.com"
                else:
                    url = company.redirect_to
                return """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <title>Redirect</title>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                        * {
                        box-sizing: border-box;
                        font-family: Arial, Helvetica, sans-serif;
                        }

                        body {
                        background-color: #ddd;
                        margin: 0;
                        font-family: Arial, Helvetica, sans-serif;
                        }
                        .button {
                                display: inline-block;
                                padding: 10px 20px;
                                text-align: center;
                                text-decoration: none;
                                color: #ffffff;
                                background-color: #7aa8b7;
                                border-radius: 6px;
                                outline: none;
                            }
                        /* Style the top navigation bar */
                        .topnav {
                        overflow: hidden;
                        background-color: #333;
                        }

                        /* Style the topnav links */
                        .topnav a {
                        float: left;
                        display: block;
                        color: #f2f2f2;
                        text-align: center;
                        padding: 14px 16px;
                        text-decoration: none;
                        }

                        /* Change color on hover */
                        .topnav a:hover {
                        background-color: #ddd;
                        color: black;
                        }

                        /* Style the content */
                        .content {
                        background-color: #ddd;
                        padding: 10px;
                        height: 200px; /* Should be removed. Only for demonstration */
                        }
                        </style>
                        </head>
                        <body>

                        <div class="topnav">
                        <a href="%s">Home</a>
                        </div>

                        <div class="content">
                        <center>
                        <h2>Go to our website</h2>
                        <a class="button" href="%s">Click here</a>
                        </center>
                        </div>
                        </body>
                        </html>""" % (
                    url,
                    url,
                )
            else:
                return False
        else:
            return block

    @classmethod
    def _dispatch(cls):
        # add signup token or login to the session if given
        block = request.env["ir.http"].block_ips()
        if block:
            _logger.error(f"\nDispatch Fail function: {cls}")
            return block
        return super(Http, cls)._dispatch()


class AllowedIPs(models.Model):
    _name = "allowed.ips"
    _description = "Allowes IPS"

    network = fields.Boolean(
        "Network",
        default=False,
        help="\
        Format for network mask",
    )
    ip_address = fields.Char(string="Allowed IP")
    name = fields.Char("Name")
