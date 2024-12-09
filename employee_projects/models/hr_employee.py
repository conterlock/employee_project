# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    total_projects = fields.Integer(string="Total Projects", compute="_compute_total_projects")

    def _compute_total_projects(self):
        for record in self:
            record.total_projects = self.env['employee.project'].search_count([('employee_id', '=', record.id)])

