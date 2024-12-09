
{
    "name": "Employee Projects",
    "version": "16.0.1.0.0",
    "author": "Luis Millan",
    'category': 'Human Resources/Employees',
    'license': 'LGPL-3',
    "depends": ["base","hr","portal"],
    "data": [
        'views/employee_project.xml',
        'views/hr_employee.xml',
        'views/portal_template.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_frontend': [
            'employee_projects/static/src/js/employee_projects_portal.js',
        ]
    },
    "installable": True,
    "application": True,
}
