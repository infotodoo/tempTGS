import base64
import logging
import time
import datetime
import io
import os
import mimetypes

import werkzeug
import ast

from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError
from werkzeug.exceptions import NotFound
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

_logger = logging.getLogger(__name__)


class WebsiteLogin(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                data = request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))])
                qcontext["error"] = _("Esperando la validación de su cuenta. Se enviará a su cuenta de correo")

            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")
        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        request.env.cr.commit()  # as authenticate will use its own cursor we need to commit the current transaction


class EditJob(WebsiteForm):

    @http.route(['/applied_jobs'], type='http', csrf=False, auth='user', website=True)
    def show_applied_jobs(self, **kwargs):
        """ Show Applied Jobs"""
        user = request.env.uid
        countries = request.env['res.country'].sudo().search([])
        cities = request.env['res.city'].sudo().search([])
        cargo_desen_rec = request.env['cargo.desen'].sudo().search([])
        titulo_rec = request.env['titulo'].sudo().search([])
        eps_rec = request.env['res.partner'].sudo().search([('tipo', '=', 'EPS')])
        afp_rec = request.env['res.partner'].sudo().search([('tipo', '=', 'AFP')])
        afc_rec = request.env['res.partner'].sudo().search([('tipo', '=', 'AFC')])

        # Many2one in development document, but actually one2many
        fobias_rec = request.env['fobias'].sudo().search([])
        hob_rec = request.env['hob'].sudo().search([])
        alergia_rec = request.env['alergia'].sudo().search([])
        direccion_recs = request.env['direccion'].sudo().search([])
        applied_jobs = request.env['hr.applicant'].sudo().search([('created_user', '=', user)])
        return request.render('website_login.applied_job', {'records': applied_jobs,
                                                            'countries': countries,
                                                            'cities': cities,
                                                            'direccion_recs': direccion_recs,
                                                            'cargo_desen_rec': cargo_desen_rec,
                                                            'titulo_rec': titulo_rec,
                                                            'eps_rec': eps_rec,
                                                            'afp_rec': afp_rec,
                                                            'afc_rec': afc_rec,
                                                            'fobias_rec': fobias_rec,
                                                            'hob_rec': hob_rec,
                                                            'alergia_rec': alergia_rec})

    @http.route(['/requisiciones'], type='http', csrf=False, auth='user', website=True)
    def add_requisicions(self, **kwargs):
        """ add requisicions"""
        company = request.env.company
        date_today = datetime.date.today()
        companies = request.env['res.company'].sudo().search([])
        centro = request.env['centro'].sudo().search([('company_id', '=', request.env.company.id)])
        unidades = request.env['unidades'].sudo().search([('company_id', '=', request.env.company.id)])
        nivel1_rec = request.env['hr.employee'].sudo().search([('company_id', '=', request.env.company.id)])
        nivel2_rec = request.env['hr.employee'].sudo().search(
            [('aprobador_ninel2', '=', True), ('company_id', '=', request.env.company.id)])
        nivel3_rec = request.env['hr.employee'].sudo().search(
            [('aprobador_ninel3', '=', True), ('company_id', '=', request.env.company.id)])
        jobs = request.env['hr.job'].sudo().search([('company_id', '=', request.env.company.id)])
        employees = request.env['hr.employee'].sudo().search([('company_id', '=', request.env.company.id)])
        cities = request.env['res.city'].sudo().search([])
        calendars = request.env['resource.calendar'].sudo().search([('company_id', '=', request.env.company.id)])

        return request.render('website_login.website_requisicions', {'employees': employees,
                                                                     'company_current': company,
                                                                     'centro': centro,
                                                                     'today': date_today,
                                                                     'companies': companies,
                                                                     'jobs': jobs,
                                                                     'cities': cities,
                                                                     'unidades': unidades,
                                                                     'calendars': calendars,
                                                                     'nivel1_rec': nivel1_rec,
                                                                     'nivel2_rec': nivel2_rec,
                                                                     'nivel3_rec': nivel3_rec})

    @http.route(['/cargos_add'], type='http', csrf=False, auth='user', website=True)
    def add_cargos(self, **kwargs):
        """ add Cargos"""
        companies = request.env['res.company'].sudo().search([])
        company = request.env.company
        unidades = request.env['unidades'].sudo().search([])
        employees = request.env['hr.employee'].sudo().search([('company_id', '=', request.env.company.id)])
        jobs = request.env['hr.job'].sudo().search([('company_id', '=', request.env.company.id)])
        certificates = request.env.ref('website_login.company_certificate').id
        homologacion = request.env['ir.attachment'].search(
            [('res_field', '=', 'homologacion_pdf'), ('res_id', '=', certificates)])
        return request.render('website_login.cargos_add', {'companies': companies,
                                                           'company_current': company,
                                                           'unidades': unidades,
                                                           'homologacion': homologacion,
                                                           'employees': employees,
                                                           'jobs': jobs})

    @http.route(['/create_cargos'], type='http', csrf=False, auth='user', website=True)
    def apply_cargos(self, **kwargs):
        " Apply Cargos"
        if kwargs:
            for key in kwargs.keys():
                _logger.info("SHOW {}: {}".format(key, kwargs.get(key)))
        obj = request.env['hr.job']
        del kwargs['no_of_formacion_especifica']
        del kwargs['no_of_activos_cargo']
        # Job Formacion
        remove_formacion_ids = []
        if kwargs['formacion_especifica_to_remove'] != '':
            remove_formacion_ids = ast.literal_eval(kwargs['formacion_especifica_to_remove'])
            remove_formacion_ids = [int(s) for s in remove_formacion_ids]
        del kwargs['formacion_especifica_to_remove']

        formacion_line_record = ''
        formacion_line = kwargs.get('formacion_esp')
        if formacion_line:
            formacion_line_record = ast.literal_eval(formacion_line)
        del kwargs['formacion_especifica']
        if 'certificado_academico' in kwargs:
            del kwargs['certificado_academico']
        del kwargs['prueba_tecnica']
        del kwargs['certificado_laboral_funciones']
        del kwargs['formacion_esp']

        # Job Activos
        remove_activos_ids = []
        if kwargs['activos_cargo_to_remove'] != '':
            remove_activos_ids = ast.literal_eval(kwargs['activos_cargo_to_remove'])
            remove_activos_ids = [int(s) for s in remove_activos_ids]
        del kwargs['activos_cargo_to_remove']
        activos_line_record = ''
        activos_line = kwargs.get('activos_line')
        if activos_line != '':
            activos_line_record = ast.literal_eval(activos_line)
        del kwargs['categoria']
        del kwargs['activo_cargo']
        del kwargs['activos_line']
        if kwargs['minimo'] != '':
            kwargs['minimo'] = float(kwargs['minimo'])
        if kwargs['maximo']:
            kwargs['maximo'] = float(kwargs['maximo'])

        #  Create
        get_operation = kwargs['edit_cargo_id']
        activos_obj = request.env['activos']
        formacion_obj = request.env['formacion.cargos']
        record = ''
        if get_operation == '':
            del kwargs['edit_cargo_id']
            record = obj.sudo().create(kwargs)
            if activos_line_record != '':
                for elements in activos_line_record:
                    if elements['id'] in remove_activos_ids:
                        continue
                    del elements['id']
                    elements['job_id'] = record.id
                    activos_obj.sudo().create(elements)
            if formacion_line_record != '':
                for elements in formacion_line_record:
                    if elements['id'] in remove_formacion_ids:
                        continue
                    del elements['id']
                    elements['job_id'] = record.id
                    formacion_obj.sudo().create(elements)
            record.write({'name':record.name})
        else:
            record_id = int(get_operation)
            if kwargs['company_id']:
                kwargs['company_id'] = int(kwargs['company_id'])
            else:
                kwargs['company_id'] = False
            if kwargs['cargo1']:
                kwargs['cargo1'] = int(kwargs['cargo1'])
            else:
                kwargs['cargo1'] = False
            if kwargs['cargo2']:
                kwargs['cargo2'] = int(kwargs['cargo2'])
            else:
                kwargs['cargo2'] = False
            if kwargs['cargo3']:
                kwargs['cargo3'] = int(kwargs['cargo3'])
            else:
                kwargs['cargo3'] = False
            if kwargs['cargo4']:
                kwargs['cargo4'] = int(kwargs['cargo4'])
            else:
                kwargs['cargo4'] = False
            if kwargs['jefe_inmediato_apl'] == '':
                del kwargs['jefe_inmediato_apl']
            if 'jefe_inmediato_apl' in kwargs:
                kwargs['jefe_inmediato_apl'] = int(kwargs['jefe_inmediato_apl'])
            if 'modificacion' in kwargs:
                kwargs['modificacion'] = True
            if 'eliminacion' in kwargs:
                kwargs['eliminacion'] = True
            del kwargs['edit_cargo_id']
            kwargs['company_id'] = int(kwargs['company_id'])
            get_record = request.env['hr.job'].sudo().browse(record_id)
            record = get_record.sudo().write(kwargs)
            if activos_line_record != '':
                for elements in activos_line_record:
                    if elements['id'] in remove_activos_ids:
                        continue
                    del elements['id']
                    elements['job_id'] = get_record.id
                    activos_obj.sudo().create(elements)
            if formacion_line_record != '':
                for elements in formacion_line_record:
                    if elements['id'] in remove_formacion_ids:
                        continue
                    del elements['id']
                    elements['job_id'] = get_record.id
                    formacion_obj.sudo().create(elements)
            _logger.error("SHOW RECORD: {}".format(get_record.activos_line if get_record.activos_line else get_record))
            get_record.write({'write_date': datetime.datetime.now()})
        return request.redirect('/cargos_add')

    @http.route('/edited_applied_job', type='http', csrf=True, auth="public", methods=['POST'], website=True,
                save_session=True)
    def edit_applied_job(self, **kwargs):
        """ Edit Applied Job"""
        record_id = int(kwargs.get('job_name'))
        kwargs['direccion_dian'] = int(kwargs['direccion_dian'])
        kwargs['via_principal_con'] = int(kwargs['via_principal_con'])
        obj = request.env['hr.applicant'].sudo().browse(record_id)
        if obj:
            if 'job_name' in kwargs:
                del kwargs['job_name']
            # Mascotas
            del kwargs['no_of_mascotas']
            remove_mascotas_ids = []
            if kwargs['mascotas_to_remove'] != '':
                remove_mascotas_ids = ast.literal_eval(kwargs['mascotas_to_remove'])
                remove_mascotas_ids = [int(s) for s in remove_mascotas_ids]
            del kwargs['mascotas_to_remove']
            mascotas_lines = kwargs.get('mascotas_lines')
            if mascotas_lines != '[]' and mascotas_lines != '':
                mascotas_records = ast.literal_eval(mascotas_lines)
                mascotas = request.env['mascotas']
                for elements in mascotas_records:
                    if elements['id'] in remove_mascotas_ids:
                        continue
                    del elements['id']
                    elements['numero_mascota'] = int(elements['numero_mascota'])
                    elements['applicant_id'] = obj.id
                    print(elements, "elementsssss")
                    mascotas.sudo().create(elements)
            del kwargs['tipo_mascota']
            del kwargs['numero_mascota']
            del kwargs['mascotas_lines']

            # Hijos
            del kwargs['no_of_hijos']
            remove_hijos_ids = []
            if kwargs['hijos_to_remove'] != '':
                remove_hijos_ids = ast.literal_eval(kwargs['hijos_to_remove'])
                remove_hijos_ids = [int(s) for s in remove_hijos_ids]
            del kwargs['hijos_to_remove']
            hijos_line = kwargs.get('hijos_Line')
            if hijos_line != '[]' and hijos_line != '':
                hijos_record = ast.literal_eval(hijos_line)
                hijo = request.env['hijo']
                for elements in hijos_record:
                    if elements['id'] in remove_hijos_ids:
                        continue
                    del elements['id']
                    elements['identificacion'] = int(elements['identificacion'])
                    elements['nacionalidad'] = int(elements['nacionalidad'])
                    elements['pais_nacimiento'] = int(elements['pais_nacimiento'])
                    elements['fecha_nac_hijo'] = datetime.datetime.strptime(elements['fecha_nac_hijo'],
                                                                            '%Y-%m-%d').date()
                    elements['applicant_id'] = obj.id
                    hijo.sudo().create(elements)

            hijo_keys = ['nombre_hijo', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'identificacion',
                         'nivel_escolaridad_hijo', 'ocupacion_hijo', 'fecha_nac_hijo', 'genero_hijo', 'grupo_sanguineo',
                         'nacionalidad', 'pais_nacimiento', 'hijastro', 'hijos_Line']
            for keys in hijo_keys:
                del kwargs[keys]

            # Resume lines
            del kwargs['no_of_resume_line']
            remove_resume_line_ids = []
            if kwargs['resume_line_to_remove'] != '':
                remove_resume_line_ids = ast.literal_eval(kwargs['resume_line_to_remove'])
                remove_resume_line_ids = [int(s) for s in remove_resume_line_ids]
            del kwargs['resume_line_to_remove']
            resume_line_ids = kwargs.get('resume_line_ids')
            if resume_line_ids != '[]' and resume_line_ids != '':
                resume_line_record = ast.literal_eval(resume_line_ids)
                resume_line = request.env['hr.resume.line']
                for elements in resume_line_record:
                    if elements['id'] in remove_resume_line_ids:
                        continue
                    del elements['id']
                    elements['cargo_desempenado'] = int(elements['cargo_desempenado'])
                    elements['pais'] = int(elements['pais'])
                    elements['date_start'] = datetime.datetime.strptime(elements['date_start'], '%Y-%m-%d').date()
                    elements['date_end'] = datetime.datetime.strptime(elements['date_end'], '%Y-%m-%d').date()
                    elements['applicant_id'] = obj.id
                    resume_line.sudo().create(elements)
            resume_line_keys = ['name', 'rama_empresa_laboro', 'cargo_desempenado', 'Tipo_de_Contrato',
                                'pais', 'actualmente_laborando', 'date_start', 'date_end',
                                'resume_line_ids']
            for keys in resume_line_keys:
                del kwargs[keys]

            # Formación
            del kwargs['no_of_formacion_line']
            remove_formacion_line_ids = []
            if kwargs['formacion_line_to_remove'] != '':
                remove_formacion_line_ids = ast.literal_eval(kwargs['formacion_line_to_remove'])
                remove_formacion_line_ids = [int(s) for s in remove_formacion_line_ids]
            del kwargs['formacion_line_to_remove']
            formacion_line = kwargs.get('formacion_line')
            if formacion_line != '[]' and formacion_line != '':
                formacion_line_record = ast.literal_eval(formacion_line)
                formacion = request.env['formacion']
                for elements in formacion_line_record:
                    if elements['id'] in remove_formacion_line_ids:
                        continue
                    del elements['id']
                    if elements['fecha_graduacion'] == '':
                        del elements['fecha_graduacion']
                    else:
                        elements['fecha_graduacion'] = datetime.datetime.strptime(elements['fecha_graduacion'],
                                                                                  '%Y-%m-%d').date()
                    elements['titulo_obtenido'] = int(elements['titulo_obtenido'])
                    elements['pais_donde_estudio'] = int(elements['pais_donde_estudio'])
                    elements['tiempo_estudio'] = int(elements['tiempo_estudio'])
                    elements['applicant_id'] = obj.id
                    formacion.sudo().create(elements)
            formacion_keys = ['formacion', 'estudia_actualmente_for', 'nombre_institucion', 'titulo_obtenido',
                              'clase_titulo', 'estado_formacion', 'pais_donde_estudio', 'tiempo_estudio',
                              'periocidad_estudio', 'fecha_graduacion', 'formacion_line']
            for keys in formacion_keys:
                del kwargs[keys]

            # Idiomas
            del kwargs['no_of_idioma']
            remove_idioma_ids = []
            if kwargs['idioma_to_remove'] != '':
                remove_idioma_ids = ast.literal_eval(kwargs['idioma_to_remove'])
                remove_idioma_ids = [int(s) for s in remove_idioma_ids]
            del kwargs['idioma_to_remove']
            idioma_line = kwargs.get('idioma_line')
            if idioma_line != '[]' and idioma_line != '':
                idioma_line_record = ast.literal_eval(idioma_line)
                idioma = request.env['lenguage']
                for elements in idioma_line_record:
                    if elements['id'] in remove_idioma_ids:
                        continue
                    del elements['id']
                    elements['porcent_dominio'] = int(elements['porcent_dominio'])
                    elements['applicant_id'] = obj.id
                    idioma.sudo().create(elements)
            del kwargs['idioma_line']
            del kwargs['nombre']
            del kwargs['porcent_dominio']

            # Medios
            del kwargs['no_of_fobia']
            remove_fobia_ids = []
            if kwargs['fobia_to_remove'] != '':
                remove_fobia_ids = ast.literal_eval(kwargs['fobia_to_remove'])
                remove_fobia_ids = [int(s) for s in remove_fobia_ids]
            del kwargs['fobia_to_remove']
            miedos_line = kwargs.get('miedos_line')
            if miedos_line:
                miedos_line_record = ast.literal_eval(miedos_line)
                for elements in miedos_line_record:
                    if elements['id'] in remove_fobia_ids:
                        continue
                    del elements['id']
                    elements['name'] = int(elements['name'])
                    rec = request.env['fobias'].sudo().browse(elements['name'])
                    obj.miedos |= rec
            del kwargs['miedos_line']
            del kwargs['miedos']

            # Hobby
            del kwargs['no_of_hobby']
            remove_hobby_ids = []
            if kwargs['hobby_to_remove'] != '':
                remove_hobby_ids = ast.literal_eval(kwargs['hobby_to_remove'])
                remove_hobby_ids = [int(s) for s in remove_hobby_ids]
            del kwargs['hobby_to_remove']
            hobby_line = kwargs.get('hobby_line')
            if hobby_line:
                hobby_line_record = ast.literal_eval(hobby_line)
                for elements in hobby_line_record:
                    if elements['id'] in remove_hobby_ids:
                        continue
                    del elements['id']
                    elements['nombre'] = int(elements['nombre'])
                    rec = request.env['hob'].sudo().browse(elements['nombre'])
                    obj.nombre_hobby |= rec

            del kwargs['hobby_line']
            del kwargs['nombre_hobby']

            # Fobia
            del kwargs['no_of_alergia']
            remove_alergia_ids = []
            if kwargs['alergia_to_remove'] != '':
                remove_alergia_ids = ast.literal_eval(kwargs['alergia_to_remove'])
                remove_alergia_ids = [int(s) for s in remove_alergia_ids]
            del kwargs['alergia_to_remove']
            alergia_line = kwargs.get('alergia_line')
            if alergia_line:
                alergia_line_record = ast.literal_eval(alergia_line)
                for elements in alergia_line_record:
                    if elements['id'] in remove_alergia_ids:
                        continue
                    del elements['id']
                    elements['Nombre'] = int(elements['Nombre'])
                    rec = request.env['alergia'].sudo().browse(elements['Nombre'])
                    obj.alergia |= rec
            del kwargs['alergia_line']
            del kwargs['alergia']

            if kwargs['estado_civil'] != 'CASADO/A' and kwargs['estado_civil'] != 'UNIÓN LIBRE':
                estardo_keys = ['primer_apellido_conyugue', 'segundo_apellido_conyugue', 'primer_nombre_conyugue',
                                'segundo_nombre_conyugue', 'escolaridad_conyugue', 'genero_conyugue',
                                'lugar_nacimiento_conyugue', 'pais_nacimiento_conyugue', 'fecha_conyugue']
                for keys in estardo_keys:
                    del kwargs[keys]

            if kwargs['no_personas_nucleo_familiar'] != '':
                kwargs['no_personas_nucleo_familiar'] = int(kwargs['no_personas_nucleo_familiar'])
            if kwargs['no_personas_estado_incapacidad'] != '':
                kwargs['no_personas_estado_incapacidad'] = int(kwargs['no_personas_estado_incapacidad'])
            if kwargs['eps'] != '':
                kwargs['eps'] = int(kwargs['eps'])
            if kwargs['afp'] != '':
                kwargs['afp'] = int(kwargs['afp'])
            if kwargs['afc'] != '':
                kwargs['afc'] = int(kwargs['afc'])
            document_datas = []
            document_keys = ['aceptacion_condiciones', 'libreta_militar', 'refrecnias_personales',
                             'verificacion_referencias', 'certificado_cuenta_bancaria', 'antecedentes_disciplinarios',
                             'validacion_antecedentes', 'entrevista_jefe_inmediato', 'fotografias',
                             'validacion_sarlaft', 'estudio_seguridad', 'examendes_medicos', 'poliza',
                             'autorizacion_uso_correo', 'licencia_conducir', 'carta_propiedad_vehiculo', 'cer_runt',
                             'seguro_obligatorio_vigente', 'revision_tecnico_mecanica', 'centro_induccion',
                             'certificacion_sena']
            for keys in document_keys:
                document_datas.append(kwargs[keys])
                del kwargs[keys]

            document_records = []
            for records in document_datas:
                attachment_value = {}
                if records != '':
                    attachment_value = {
                        'name': records.filename,
                        'datas': base64.encodestring(records.read()),
                    }
                else:
                    attachment_value = {
                        'name': '',
                        'datas': '',
                    }
                document_records.append(attachment_value)
            vals = {
                'aceptacion_condiciones': document_records[0]['datas'],
                'aceptacion_condiciones_emp_filename': document_records[0]['name'],
                'libreta_militar': document_records[1]['datas'],
                'libreta_militar_emp_filename': document_records[1]['name'],
                'refrecnias_personales': document_records[2]['datas'],
                'refrecnias_personales_emp_filename': document_records[2]['name'],
                'verificacion_referencias': document_records[3]['datas'],
                'verificacion_referencias_emp_filename': document_records[3]['name'],
                'certificado_cuenta_bancaria': document_records[4]['datas'],
                'certificado_cuenta_bancaria_emp_filename': document_records[4]['name'],
                'antecedentes_disciplinarios': document_records[5]['datas'],
                'antecedentes_disciplinarios_emp_filename': document_records[5]['name'],
                'validacion_antecedentes': document_records[6]['datas'],
                'validacion_antecedentes_emp_filename': document_records[6]['name'],
                'entrevista_jefe_inmediato': document_records[7]['datas'],
                'entrevista_jefe_inmediato_emp_filename': document_records[7]['name'],
                'fotografias': document_records[8]['datas'],
                'fotografias_emp_filename': document_records[8]['name'],
                'validacion_sarlaft': document_records[9]['datas'],
                'validacion_sarlaft_emp_filename': document_records[9]['name'],
                'estudio_seguridad': document_records[10]['datas'],
                'estudio_seguridad_emp_filename': document_records[10]['name'],
                'examendes_medicos': document_records[11]['datas'],
                'examendes_medicos_emp_filename': document_records[11]['name'],
                'poliza': document_records[12]['datas'],
                'poliza_emp_filename': document_records[12]['name'],
                'autorizacion_uso_correo': document_records[13]['datas'],
                'autorizacion_uso_correo_emp_filename': document_records[13]['name'],
                'licencia_conducir': document_records[14]['datas'],
                'licencia_conducir_emp_filename': document_records[14]['name'],
                'carta_propiedad_vehiculo': document_records[15]['datas'],
                'carta_propiedad_vehiculo_emp_filename': document_records[15]['name'],
                'cer_runt': document_records[16]['datas'],
                'cer_runt_emp_filename': document_records[16]['name'],
                'seguro_obligatorio_vigente': document_records[17]['datas'],
                'seguro_obligatorio_vigente_filename': document_records[17]['name'],
                'revision_tecnico_mecanica': document_records[18]['datas'],
                'revision_tecnico_mecanica_emp_filename': document_records[18]['name'],
                'centro_induccion': document_records[19]['datas'],
                'centro_induccion_emp_filename': document_records[19]['name'],
                'certificacion_sena': document_records[20]['datas'],
                'certificacion_senafile_name': document_records[20]['name'],
            }
            kwargs.update(vals)
            obj.sudo().write(kwargs)
        return request.redirect('/job-thank-you')


class ApplyJob(WebsiteHrRecruitment):

    @http.route('''/jobs/apply/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''',
                type='http', auth="public", website=True)
    def jobs_apply(self, job, **kwargs):
        if not job.can_access_from_current_website():
            raise NotFound()
        city = request.env['res.city'].sudo().search([])
        country = request.env['res.country'].sudo().search([])
        state = request.env['res.country.state'].sudo().search([])
        language = request.env['res.lang'].sudo().search([])
        requisicion_stage = request.env['requisicion.stage'].sudo().search([('name', '=', 'ABIERTA')]).id
        requisicion = request.env['requisiciones'].sudo().search(
            [('company_id', '=', request.env.company.id), ('stage_id', '=', requisicion_stage),
             ('cargo_solicitado', '=', job.id)])
        error = {}
        default = {}
        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')

        certificates = request.env.ref('website_login.company_certificate').id
        tratamiento_datos = request.env['ir.attachment'].search(
            [('res_field', '=', 'tratamiento_datos_pdf'), ('res_id', '=', certificates)])

        return request.render("website_hr_recruitment.apply", {
            'cities': city,
            'tratamiento_datos': tratamiento_datos,
            'countries': country,
            'states': state,
            'requisicions': requisicion,
            'lang_records': language,
            'job': job,
            'error': error,
            'default': default,
        })

    @http.route(['/job_apply'], type='http', csrf=False, auth='user', methods=['POST'], website=True)
    def apply_for_jobs(self, **kwargs):
        """ Apply For Jobs"""
        attachments = []
        keys_to_remove = ['fotocopia_cedula', 'cer_estudio', 'hv', 'certi_laborales']
        names = ['name1', 'name2', 'name3', 'name4']
        for name in names:
            kwargs[name] = kwargs[name].upper()
        for key in keys_to_remove:
            attachments.append(kwargs[key])
            del kwargs[key]
        requisicion_id = int(kwargs['requisicion'])
        applied_requisicion = request.env['requisiciones'].sudo().browse(requisicion_id)
        department_id = int(kwargs['department_id']) if kwargs['department_id'] else False
        job_id = int(kwargs['job_id']) if kwargs['job_id'] else False
        postion_name = applied_requisicion.cargo_solicitado.name if applied_requisicion.cargo_solicitado else ''
        kwargs.update(
            {'name': '[' + applied_requisicion.name + ']' + postion_name + ' / ' + kwargs['tratamiento'] + ' ' + kwargs[
                'name3'] + ' ' + kwargs['name4'] + ' ' + kwargs['name1'] + ' ' + kwargs['name2'],
             'job_id': job_id,
             'department_id': department_id,
             'requisicion': int(kwargs['requisicion']),
             'partner_name': kwargs['tratamiento'] + ' ' + kwargs['name3'] + ' ' + kwargs['name4'] + ' ' +
                             kwargs['name1'] + ' ' + kwargs['name2']})
        obj = request.env['hr.applicant']
        record = obj.create(kwargs)
        attachment_records = []
        for records in attachments:
            attachment_value = {
                'name': records.filename,
                'datas': base64.encodestring(records.read()),
            }
            attachment_records.append(attachment_value)
        vals = {
            'fotocopia_cedula_filename': attachment_records[0]['name'],
            'fotocopia_cedula': attachment_records[0]['datas'],
            'cer_estudio_emp_filename': attachment_records[1]['name'],
            'cer_estudio': attachment_records[1]['datas'],
            'hv_filename': attachment_records[2]['name'],
            'hv': attachment_records[2]['datas'],
            'certi_laborales_emp_filename': attachment_records[0]['name'],
            'certi_laborales': attachment_records[3]['datas'],
        }
        record.sudo().write(vals)

        surveys = request.env['hr.job'].browse(record.job_id.id).surveys_id
        entrevista = surveys.filtered(lambda l: l.manejo_interno is False)
        values = {'entrevista_rec': entrevista,
                  'record_id': record.id,
                  'user': record.created_user}
        return request.render('website_login.entrevista_template', values)

    @http.route(['/attachment/download'], type='http', auth='user')
    def download_attachment(self, attachment_id):
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "type", "mimetype"]
        )
        if attachment:
            attachment = attachment[0]
        else:
            return request.not_found()
        if attachment["datas"]:
            data = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
            extension = os.path.splitext(attachment["name"] or '')[1]
            extension = extension if extension else mimetypes.guess_extension(attachment["mimetype"] or '')
            filename = attachment['name']
            filename = filename if os.path.splitext(filename)[1] else filename + extension
            return http.send_file(data, filename=filename, as_attachment=True)
        else:
            return request.not_found()

    @http.route(['/create_requisicion'], type='http', csrf=False, auth='user', methods=['POST'], website=True)
    def create_requisicion(self, **kwargs):
        """ Create Requisicion"""
        attachment = ''
        req_keys = ['solicitante', 'emp', 'aprobador_nivel1', 'aprobador_nivel2', 'aprobador_nivel3', 'jefe_inmediato',
                    'catidad_vacantes', 'res_city', 'un_organizativa', 'centro_de_costo', 'horari']

        for k in req_keys:
            kwargs[k] = int(kwargs[k])
        if kwargs['docuemnto_ref'] != '':
            attachment = kwargs['docuemnto_ref']
            del kwargs['docuemnto_ref']
        obj = request.env['requisiciones']
        del kwargs['centro_costo']
        record = obj.sudo().create(kwargs)
        obj.env.cr.commit()
        if attachment:
            attachment_value = {
                'name': attachment.filename,
                'datas': base64.encodestring(attachment.read()),
                'res_model': 'requisiciones',
                'res_id': record.id,
            }
            created_document = request.env['ir.attachment'].sudo().create(attachment_value)
            record.docuemnto_ref = created_document.datas
        return request.render('website_login.thankyou_requisicion', {'requisicion_name': record.name})

    @http.route(['/requcision/<int:requisicion_id>'], type='http', csrf=False, auth='user', website=True)
    def approve_requisicion(self, requisicion_id, **kwargs):
        obj = request.env['requisiciones'].sudo().browse(requisicion_id)
        approver1 = obj.aprobador_nivel1.user_id.id
        approver2 = obj.aprobador_nivel2.user_id.id
        approver3 = obj.aprobador_nivel3.user_id.id
        user = request.env.uid
        if user in [approver1, approver2, approver3]:
            company = request.env.company
            document = request.env['ir.attachment'].sudo().search(
                [('res_model', '=', 'requisiciones'), ('res_id', '=', requisicion_id)])
            return request.render('website_login.requision_approve', {'requisicion': obj,
                                                                      'document': document,
                                                                      'company_current': company,
                                                                      'user': user,
                                                                      'requisicion_id': requisicion_id})
