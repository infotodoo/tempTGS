from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SuerveyInput(models.Model):
    _inherit = "survey.user_input"

    applicant_id = fields.Many2one('hr.applicant', 'Aplicante')


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    response_ids = fields.One2many('survey.user_input', 'applicant_id', 'Respuestas')



class WizardSurvey(models.TransientModel):
    _name = 'wizard.survey'
    _description = 'wizard Survey'


    def _default_applicantlt_job(self):
        ha = self.env['hr.applicant'].browse(self._context.get('active_id'))
        return ha

    def _default_job(self):
        ha = self.env['hr.applicant'].browse(self._context.get('active_id'))
        hj = ha.job_id
        return hj
    
    def _default_survey(self):
        ha = self.env['hr.applicant'].browse(self._context.get('active_id'))
        hj = ha.job_id
        ss = hj.surveys_id
        return ss

    applicant_id = fields.Many2one('hr.applicant', 'Aplicante', default=_default_applicantlt_job)
    job_id = fields.Many2one('hr.job','Puesto de Trabajo', default=_default_job)
    surveys_id = fields.Many2many('survey.survey', 'wizard_survey_rel','wizard_id','survey_id','Entrevistas', default=_default_survey)
    survey_id = fields.Many2one('survey.survey', 'Entrevista a Enviar') 
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null")

    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.survey_id._create_answer(partner=self.applicant_id.partner_id)
            response.applicant_id = self.applicant_id
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(survey_token=response.token).action_start_survey()


class WizardSurveyPrint(models.TransientModel):
    _name = 'wizard.survey.print'
    _description = 'Print Survey'

    def _default_applicant_id(self):
        ha = self.env['hr.applicant'].browse(self._context.get('active_id'))
        return ha
    
    def _default_input(self):
        ha = self.env['hr.applicant'].browse(self._context.get('active_id'))
        ui = ha.response_ids.ids
        return ui

    applicant_id = fields.Many2one('hr.applicant', 'Aplicante', default=_default_applicant_id)
    responses_ids = fields.Many2many('survey.user_input', 'wizard_input_rel','wizard_id','input_id','Respuestas', default=_default_input)
    response_id = fields.Many2one('survey.user_input', "Response")

    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        if not self.response_id:
            return self.response_id.survey_id.action_print_survey()
        else:
            response = self.response_id
            return self.response_id.survey_id.with_context(survey_token=response.token).action_print_survey()


