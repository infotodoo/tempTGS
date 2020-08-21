from odoo.tests import HttpCase


class WebSuite(HttpCase):

    def test_ui_web(self):
        self.phantom_js('/web/tests?mod=inputmask_widget&failfast', "", "", login='admin', timeout=1800)
