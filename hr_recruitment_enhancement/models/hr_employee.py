# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    applicant_categ_ids = fields.Many2many('hr.applicant.category', string="Tags")
    applicant_type_id = fields.Many2one('hr.recruitment.degree', "Degree")
    applicant_medium_id = fields.Many2one('utm.medium', string='Medium')
    applicant_source_id = fields.Many2one('utm.source', "Source", ondelete='cascade')
    applicant_job_id = fields.Many2one('hr.job', string="Applied Job")
    applicant_salary_proposed_extra = fields.Char("Proposed Salary Extra",
                                        help="Salary Proposed by the Organisation, extra advantages")
    applicant_salary_expected_extra = fields.Char("Expected Salary Extra", help="Salary Expected by Applicant, extra advantages")
    applicant_salary_proposed = fields.Float("Proposed Salary", group_operator="avg", help="Salary Proposed by the Organisation")
    applicant_salary_expected = fields.Float("Expected Salary", group_operator="avg", help="Salary Expected by Applicant")
    applicant_availability = fields.Date("Availability",
                               help="The date at which the applicant will be available to start working")
