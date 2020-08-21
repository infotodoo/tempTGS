# -*- coding: utf-8 -*-
{
    'name': "Thomas hr",

    'summary': "Thomas hr",

    'description': "Thomas hr",

    'author': "Todoo SAS",
    'contributors': "Luis Paternina lp@todoo,co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '13.1.3',

    # any module necessary for this one to work correctly
    'depends': [
        'contacts',
        'hr_contract',
        'hr_skills',
        'hr_recruitment_survey',
        'base_address_city',
        'web',
               
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/rrhh_todoo_view.xml',
        'views/requisiciones.xml',
        'views/ciudades.xml',
        'views/unidades.xml',
        'views/direccion.xml',
        'views/fobias.xml',
        'views/hijo.xml',
        'views/job.xml',
        'views/formacion.xml',
        'views/activos.xml',
        'views/mascotas.xml',
        'views/alergia.xml',
        'views/lenguage.xml',
        'views/hob.xml',
        'views/employee.xml',
        'views/centro.xml',
        'views/contrato.xml',          
        'views/experiencia.xml',
        'views/escolaridad.xml',
        'views/titulo.xml',        
        'views/ccnomina.xml',
        'views/tipo_cotizante.xml',
        'views/clase_salario.xml',
        'views/division.xml',
        'views/area_personal.xml',       
        'views/cargo_desempenado.xml',
        'views/evaluacion_tiempos.xml',
        'views/res_partner.xml',
        'views/survey.xml',
        'views/reports.xml',
        'views/bancos.xml',
        'views/mask.xml',
        'views/eps.xml',
        'views/afp.xml',
        'views/afc.xml',
        'views/formacion_cargos.xml',
        'security/hr_requisition.xml',                
        'reports/report_contract.xml',
        'reports/report_minuta.xml',
        'reports/report_datos_personales.xml',
        'reports/report_memorando_presentacion.xml',
        'reports/report_fondo_solidario.xml',
        'reports/report_cuenta_bancaria.xml',
        'reports/report_certificacion_dependientes.xml',
        'reports/report_uso_correo.xml',
        'reports/report_situacion_militar.xml',
        'reports/report_autorizacion_derechos.xml',
        'reports/custom_header.xml',
        'reports/report_contrato_aprendizaje.xml',
        'reports/report_contrato_indefinido.xml',
        'reports/report_minuta_contrato_medio_tiempo.xml',
        'reports/report_contrato_obra_o_labor.xml',
        'reports/contrato_practicante.xml',
        'reports/report.xml',                    
        'data/requisicion_stage.xml',
        'data/applicant_stages.xml',
        'wizard/wizard_survey.xml',
        'wizard/wizard_print_survay.xml',
        'wizard/hr_employee.xml',
        
    ],
    # only loaded in demonstration mode.
    'qweb': ['static/src/xml/mask.xml'],
    'demo': [
        'demo/demo.xml',
    ],
}
