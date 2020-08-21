# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
import subprocess

_logger = logging.getLogger(__name__)


class ConnectionSubprocess(models.TransientModel):
    _name = 'connection.subprocess'
    _description = 'Connection subprocess'

    @api.model
    def check_subprocess(self):
        def ask_port(port):
            command = "nc -vw 1 127.0.0.1 {}".format(port)
            try:
                process = subprocess.run([command], shell=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdout = process.stdout.decode("utf-8")
            except:
                _logger.error("\n\n\nDO NOT EXECUTE COMMAND\n\n\n")
            alarm = "\n\
                #################################################################################\n \
                ########################### PORT {} ###########################################\n \
                #################################################################################\n \
                #################################################################################\n".format(port)
            if 'succeeded' in stdout and process.returncode == 0:
                _logger.info("\n{}".format(stdout.split('\n')[-2]))
                return False
            else:
                _logger.error("{}\n{}\n{}".format(alarm,stdout,alarm))
                return True
        if ask_port('3636'):
            self.env['connection.ssh'].ssh_tunnel(flag=True,port='3636')
        # if ask_port('4646'):
        #     self.env['connection.ssh'].ssh_tunnel(flag=True,port='4646')
