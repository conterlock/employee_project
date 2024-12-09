# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager

import logging
logger = logging.getLogger(__name__)

class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        EmployeeProjects = request.env['employee.project'].sudo()
        if 'employee_projetc_count' in counters:
            values['employee_projetc_count'] = EmployeeProjects.search_count(self._prepare_employee_projects_domain(partner))
        return values

    def _prepare_employee_projects_domain(self, partner):
        return [
            ('partner_id', '=', [partner.id])
        ]
    
    def _get_employee_projects_searchbar_sortings(self):
        return {
            'date_start': {'label': _('Start Date'), 'project': 'date_start desc'},
            'date_end': {'label': _('End Date'), 'project': 'date_start desc'},
            'name': {'label': _('Name'), 'project': 'name desc'},
        }

    def _prepare_employee_projects_portal_rendering_values(self, page=1, date_begin=None, date_end=None, sortby=None, **kwargs):
        EmployeeProjects = request.env['employee.project'].sudo()
        if not sortby:
            sortby = 'date_start'
        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()
        url = "/my/employee/projects"
        domain = self._prepare_employee_projects_domain(partner)
        searchbar_sortings = self._get_employee_projects_searchbar_sortings()
        sort_projects = searchbar_sortings[sortby]['project']
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        pager_values = portal_pager(
            url=url,
            total=EmployeeProjects.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
        )
        employee_projects = EmployeeProjects.search(domain, order=sort_projects, limit=self._items_per_page, offset=pager_values['offset'])
        values.update({
            'date': date_begin,
            'employee_projects': employee_projects.sudo(),
            'page_name': 'employeeProjects',
            'pager': pager_values,
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return values

    @http.route(['/my/employee/projects', '/my/employee/projects/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_employee_projects(self, **kwargs):
        values = self._prepare_employee_projects_portal_rendering_values(**kwargs)
        request.session['my_employee_projects_history'] = []
        return request.render("employee_projects.portal_my_employee_projects", values)
    
    @http.route(['/my/employee/projects/<int:project_id>'], type='http', auth="public", website=True)
    def portal_employee_project_page(self, project_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            project_sudo = self._document_check_access('employee.project', project_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        backend_url = f'/web#model={project_sudo._name}'\
                    f'&id={project_sudo.id}'\
                    f'&action={project_sudo._get_portal_return_action().id}'\
                    f'&view_type=form'
        values = {
            'employee_project': project_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': project_sudo.company_id,
        }
        return request.render('employee_projects.employee_project_portal_template', values)
    
    @http.route(['/my/EmployeeProjects/newProject'], type='http', auth="public", methods=['POST'], website=True)
    def portal_new_employee_project(self, access_token=None, **kwargs):
        request.env['employee.project'].sudo().create({
            'name': kwargs.get('projectName'),
            'date_start': kwargs.get('projectStartDate'),
            'date_end': kwargs.get('projectEndDate'),
            'description': kwargs.get('description'),
            'partner_id': request.env.user.partner_id.id,
            'employee_id': request.env.user.employee_id.id
        })
        return request.redirect('/my/employee/projects')