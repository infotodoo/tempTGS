# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ValidationMail(models.Model):
    _inherit = 'res.users'

    signup_request = fields.Boolean(default=False)

    @api.model
    def create(self, vals_list):
        """ Creating self-registration users"""
        if 'groups_id' in vals_list:
            portal_group_id = self.env.ref("base.group_portal").id
            if portal_group_id in vals_list.get('groups_id')[0][2]:
                vals_list.update({'active': False})
                vals_list.update({'signup_request': True})
        res = super(ValidationMail, self).create(vals_list)
        return res

    @api.onchange('active')
    @api.constrains('active')
    def set_active(self):
        if self.active:
            self.action_reset_password()
            self.signup_request = False


class HrApplicantForm(models.Model):
    _inherit = 'hr.applicant'

    created_user = fields.Char()


class FindSurveys(models.Model):
    _inherit = 'hr.job'

    def find_surveys(self, id):
        obj = self.env['hr.applicant'].with_user(1).browse(id).job_id
        data_to_send = []
        for data in obj.surveys_id:
            survey_data = data.read()[0]
            keys = ['id', 'title']
            surveys = {x: survey_data[x] for x in keys}
            data_to_send.append((surveys))
        return data_to_send


class HrCargos(models.Model):
    _inherit = 'hr.job'

    def fetch_cargo_details(self, id):
        obj = self.env['hr.job'].with_user(1).browse(id)
        caros_data = obj.read()[0]

        formacion = []
        if obj.formacion_esp:
            for elements in obj.formacion_esp:
                formacion_rec = elements.read()[0]
                keys = ['id', 'formacion_especifica', 'certificado_academico', 'prueba_tecnica',
                        'certificado_laboral_funciones']
                formacion_data = {x: formacion_rec[x] for x in keys}
                formacion.append(formacion_data)

        activos = []
        if obj.activos_line:
            for elements in obj.activos_line:
                activos_rec = elements.read()[0]
                keys = ['id', 'categoria', 'activo_cargo']
                activos_data = {x: activos_rec[x] for x in keys}
                activos.append((activos_data))
        keys = ['name', 'company_id', 'tht', 'unidad_organizativa', 'jefe_inmediato_apl', 'procesos_servicios_per',
                'tiene_personal_cargo', 'cargo1', 'tipo_relacion1', 'cargo2', 'tipo_relacion2', 'cargo3',
                'tipo_relacion3', 'cargo4', 'tipo_relacion4', 'nivel_primario_educativo_minimo',
                'nombre_programa_carrera', 'nivel_secundario_educativo', 'nombre_programa',
                'requiere_tarjeta_profesional', 'objetivo_cargo', 'aplica', 'minimo', 'maximo', 'que_hace',
                'como_lo_hace', 'deberes', 'responsabilidades', 'nivel_autoridad', 'description', 'general',
                'especifica_cargos_similares']

        cargos_data_return = {x: caros_data[x] for x in keys}
        cargos_list = {}
        cargos_list.update({'formacion': formacion})
        cargos_list.update({'activos': activos})
        cargos_list.update({'cargos': cargos_data_return})
        return cargos_list

    def fetch_cargo_state(self, id):
        obj = self.env['hr.job'].with_user(1).browse(id)
        return obj.state


class FormactionJs(models.Model):
    _inherit = 'formacion'

    def unlink_formacion(self, id):
        obj = self.env['formacion'].with_user(1).browse(id)
        unlink_status = obj.unlink()
        return unlink_status


class FormactionCargosJs(models.Model):
    _inherit = 'formacion.cargos'

    def unlink_formacion_cargos(self, id):
        obj = self.env['formacion.cargos'].with_user(1).browse(id)
        unlink_status = obj.unlink()
        return unlink_status


class ActivosJs(models.Model):
    _inherit = 'activos'

    def unlink_activos(self, id):
        obj = self.env['activos'].with_user(1).browse(id)
        unlink_status = obj.unlink()
        return unlink_status


class CentrJs(models.Model):
    _inherit = 'centro'

    def fetch_centro_details(self, id):
        obj = self.env['centro'].with_user(1).browse(id)
        return obj.centro_costo


class CompanyChange(models.Model):
    _inherit = 'res.company'

    def change_company(self, id):
        obj = self.env['res.company'].with_user(1).browse(id)
        return obj.read()


class CertificatesCompany(models.Model):
    _name = 'company.certificates'

    name = fields.Char()
    tratamiento_datos_pdf = fields.Binary(string="Tratamiento de Datos", tracking=True, attachment=True)
    tratamiento_datos_pdf_filename = fields.Char("File name")
    homologacion_pdf = fields.Binary(string="Homologación", tracking=True, attachment=True)
    homologacion_pdf_filename = fields.Char("File name")

    def write(self, vals):
        self.ensure_one()
        attachment = self.env['ir.attachment'].sudo()
        if vals.get('tratamiento_datos_pdf'):
            attachment.search([('res_field', '=', 'tratamiento_datos_pdf')]).unlink()
            dic = {
                'name': vals.get('tratamiento_datos_pdf_filename') or self.tratamiento_datos_pdf_filename,
                'datas': vals.get('tratamiento_datos_pdf'),
                'res_field': 'tratamiento_datos_pdf',
                'res_id': self.id
            }
            attachment.create(dic)
        if vals.get('homologacion_pdf'):
            attachment.search([('res_field', '=', 'homologacion_pdf')]).unlink()
            dic = {
                'name': vals.get('homologacion_pdf_filename') or self.homologacion_pdf_filename,
                'datas': vals.get('homologacion_pdf'),
                'res_field': 'homologacion_pdf',
                'res_id': self.id
            }
            attachment.create(dic)
        return super(CertificatesCompany, self).write(vals)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def fetch_job_details(self, id):
        obj = self.env['hr.employee'].with_user(1).browse(id)
        return obj.job_id.display_name


class PortalSurvey(models.TransientModel):
    _inherit = 'wizard.survey'

    def action_start_survey_portal(self, survey, record):
        application = self.env['hr.applicant'].with_user(1).browse(record)
        user = int(application.created_user)
        user_obj = self.env['res.users'].browse(user)
        survey_id = self.env['survey.survey'].browse(survey)
        response = survey_id._create_answer(partner=user_obj)
        response.applicant_id = application.id
        obj = self.env['wizard.survey']
        values = {
            'applicant_id': application.id,
            'job_id': application.job_id.id,
            'survey_id': survey_id.id,
            'response_id': response.id
        }
        obj.with_user(1).create(values)
        trail = "?answer_token=%s" % response.token if response.token else ""
        return survey_id.public_url + trail


class WebsiteRequisicion(models.Model):
    _inherit = 'requisiciones'

    @api.model
    def create(self, vals):
        res = super(WebsiteRequisicion, self).create(vals)
        # composer = self.env['mail.compose.message'].with_user(self.user_employee).with_context({
        #     'default_composition_mode': 'comment',
        #     'default_model': 'mail.test.simple',
        #     'default_res_id': self.test_record.id,
        #     'default_template_id': self.email_template.id,
        # }).create({'subject': 'Forget me subject', 'body': 'Dummy body'})
        partner_id = self.env['hr.employee'].with_user(1).browse(res.aprobador_nivel1.id)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        ## FIX ME: cyfer_method(res.id)
        link = base_url + '/requisicion/%s' % (res.id)
        mail = self.env['mail.mail'].create({
            'subject': _('Requisicion Approval: %s') % res.name,
            'email_from': self.env.company.email,
            'email_to': partner_id.work_email,
            'body_html': "Dear" + partner_id.name + ", </br> Here is the link of requisicion for you to review with reference.</br>"
                         + link,
        })
        try:
            mail.send_mail()
        except:
            pass
        return res

    def requisicion_approval(self, requisicion_id, user_id, action):
        record = self.env['requisiciones'].with_user(1).browse(requisicion_id)
        base_url = self.env['ir.config_parameter'].with_user(1).get_param('web.base.url')
        approver1 = record.aprobador_nivel1.user_id.id
        approver2 = record.aprobador_nivel2.user_id.id
        approver3 = record.aprobador_nivel3.user_id.id
        if action == 1:
            if record.stage_id.name == 'PRIMERA APROBACION' and approver1:
                if approver1 == user_id:
                    self.send_requisicion_approval(record, record.aprobador_nivel2, base_url)
                    record.stage_id = 8
                return base_url
            if record.stage_id.name == 'SEGUNDA APROBACION' and approver2:
                if approver2 == user_id:
                    self.send_requisicion_approval(record, record.aprobador_nivel3, base_url)
                    record.stage_id = 9
                return base_url
            if record.stage_id.name == 'TERCERA APROBACION' and approver3:
                if approver3 == user_id:
                    record.stage_id = 1
                return base_url
        if action == 0:
            if user_id in [approver1, approver2, approver3]:
                employee = self.env['hr.employee'].with_user(1).search([('user_id', '=', user_id)])
                base_url = self.env['ir.config_parameter'].with_user(1).get_param('web.base.url')
                mail = self.env['mail.mail'].sudo().create({
                    'subject': _('Requisicion Approval: %s') % record.name,
                    'email_from': self.env.company.email,
                    'email_to': record.solicitante.work_email,
                    'body_html': "Dear" + record.solicitante.name + ", </br> The requisicione has been rejected by " +
                                 employee.name + " .</br>"
                })
                try:
                    mail.send_mail()
                except:
                    pass
                record.stage_id = 10
            return base_url
        return base_url

    def send_requisicion_approval(self, record, partner, base_url):
        link = base_url + '/requisicion/%s' % (record.id)
        mail = self.env['mail.mail'].sudo().create({
            'subject': _('Requisicion Approval: %s') % record.name,
            'email_from': self.env.company.email,
            'email_to': partner.work_email,
            'body_html': "Dear" + partner.name + ", </br> Here is the link of requisicion for you to review with reference.</br>"
                         + link,
        })
        try:
            mail.send_mail()
        except:
            pass
