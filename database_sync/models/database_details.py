# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    url = fields.Char("Url")
    db = fields.Char("Database")
    username = fields.Char("Username")
    password = fields.Char("Password")
    main_db = fields.Char("Main Database")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            url=params.get_param('database_sync.url'),
            db=params.get_param('database_sync.db'),
            username=params.get_param('database_sync.username'),
            password=params.get_param('database_sync.password'),
            main_db=params.get_param('database_sync.main_db'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("database_sync.url", self.url)
        self.env['ir.config_parameter'].sudo().set_param("database_sync.db", self.db)
        self.env['ir.config_parameter'].sudo().set_param("database_sync.username", self.username)
        self.env['ir.config_parameter'].sudo().set_param("database_sync.password", self.password)
        self.env['ir.config_parameter'].sudo().set_param("database_sync.main_db", self.main_db)
