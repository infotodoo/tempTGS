# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Applicant(models.Model):
    _inherit = "hr.applicant"

    def create_employee_from_applicant(self):
        res = super(Applicant, self).create_employee_from_applicant()
        if res.get('res_id', False) or self.emp_id:
            employee_id = self.env['hr.employee'].browse(res.get('res_id')) or self.emp_id
            employee_id.applicant_categ_ids = [(6, 0, self.categ_ids.ids)]
            employee_id.applicant_type_id = self.type_id
            employee_id.applicant_medium_id = self.medium_id
            employee_id.applicant_source_id = self.source_id
            employee_id.applicant_job_id = self.job_id
            employee_id.applicant_salary_proposed_extra = self.salary_proposed_extra
            employee_id.applicant_salary_expected_extra = self.salary_expected_extra
            employee_id.applicant_salary_proposed = self.salary_proposed
            employee_id.applicant_salary_expected = self.salary_expected
            employee_id.applicant_availability = self.availability
            # for attachment in self.attachment_ids:
            #     emp_attachment_id = attachment.copy()
            #     emp_attachment_id.write({'res_model':'hr.employee','res_id':self.emp_id.id or res.get('res_id', False)})
        return res