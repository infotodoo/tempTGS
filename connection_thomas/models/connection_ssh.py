# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
from sshtunnel import SSHTunnelForwarder

_logger = logging.getLogger(__name__)


class ConnectionSsh(models.TransientModel):
    _name = 'connection.ssh'
    _description = 'Connection ssh'

    @api.model
    def ssh_tunnel(self, flag=False, port=False):
        ports = {'3636':389,'4646':636}
        def tunnel(local):
            remote_port = ports[local]
            connection_port = 1422 if local == '3636' else 1522
            local = int(local)
            server = SSHTunnelForwarder(
                ('54.39.127.106', connection_port),
                ssh_username="root",
                ssh_password="Soporte1",
                # set_keepalive = 60,
                local_bind_address=('0.0.0.0', local),
                remote_bind_address=('172.20.100.3', remote_port)
            )
            server.start()
            message = "Assigned local port %s" % server.local_bind_port
            _logger.info(message)
        if not flag:
            tunnel('3636')
            # tunnel('4646')
        else:
            tunnel(port)
