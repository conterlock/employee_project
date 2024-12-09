# Employee Projects

## Descripción

El módulo **Employee Projects** permite gestionar los proyectos de los empleados dentro del sistema Odoo. Este módulo proporciona vistas y plantillas personalizadas para facilitar la administración de proyectos y la integración con el portal de empleados.

## Características

- Gestión de proyectos de empleados.
- Integración con el módulo de recursos humanos (`hr`).
- Plantillas personalizadas para el portal de empleados.
- Control de acceso basado en roles.

## Requisitos

- Odoo 16.0
- Módulos dependientes:
  - `base`
  - `hr`
  - `portal`

## Instalación

1. Clona este repositorio en tu directorio de addons de Odoo.
2. Reinicia el servidor de Odoo.
3. Activa el modo desarrollador en Odoo.
4. Ve a `Apps` y actualiza la lista de aplicaciones.
5. Busca `Employee Projects` e instala el módulo.

## Datos

El módulo incluye los siguientes archivos de datos:

- `views/employee_project.xml`: Vista de proyectos de empleados.
- `views/hr_employee.xml`: Vista de empleados.
- `views/portal_template.xml`: Plantillas del portal.
- `security/ir.model.access.csv`: Reglas de acceso.

## Activos

El módulo incluye los siguientes activos para el frontend:

- `employee_projects/static/src/js/employee_projects_portal.js`: Archivo JavaScript para el portal de proyectos de empleados.

## Autor

- Luis Millan

## Licencia

Este módulo está licenciado bajo LGPL-3.0. Para más detalles, consulta el archivo de licencia.
