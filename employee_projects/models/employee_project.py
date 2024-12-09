# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EmployeeProject(models.Model):
    _name = "employee.project"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']
    _description = "Projects managed by and for employees"

    name = fields.Char(string="Project Name", required=True)
    description = fields.Text(string="Description")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)
    partner_id = fields.Many2one('res.partner', string="Partner", related='employee_id.user_partner_id')

    def get_portal_url(self):
        return '/my/employee/projects/%s' % self.id

    def _get_portal_return_action(self):
        return self.get_portal_url()

    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('employee_projects.employee_project_action_view')