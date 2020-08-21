# -*- coding: utf-8 -*-
#BY: LUIS FELIPE PATERNINA VITAL - TODOO SAS

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta


tallazapatos = [
    ('30', '30'),
    ('31', '31'),
    ('32', '32'),
    ('33', '33'),
    ('34', '34'),
    ('35', '35'),
    ('36', '36'),
    ('37', '37'),
    ('38', '38'),
    ('39', '39'),
    ('40', '40'),
    ('41', '41'),
    ('42', '42'),
    ('43', '43'),
    ('44', '44')
]

grupo_san = [    
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-')   
]

tipo_vivienda = [
    ('ARRENDADO', 'ARRENDADO'),
    ('COMUNITARIA', 'COMUNITARIA'),
    ('FAMILIAR', 'FAMILIAR'),
    ('PROPIA', 'PROPIA'),   
    ('OTRO', 'OTRO')   
]


class Todoo(models.Model):
    _inherit = 'hr.applicant'

    # Test--
    test_attach = fields.Binary('Test')
    # One2many
    formacion_line = fields.One2many('formacion','applicant_id','Formación')   
    hijos_Line = fields.One2many('hijo', 'applicant_id', 'Hijos')
    mascotas_line = fields.One2many('mascotas','applicant_id', 'Mascotas')
    idioma_line = fields.One2many('lenguage','applicant_id','Idiomas')
    #campos del grupo 1 page informacion general 
    name1 = fields.Char(string="Primer Apellido", tracking=True)
    name2 = fields.Char(string="Segundo Apellido", tracking=True)
    name3 = fields.Char(string="Primer Nombre", tracking=True)
    name4 = fields.Char(string="Segundo Nombre", tracking=True)
    nombre_aplicante=fields.Char(tracking=True)
    tratamiento = fields.Selection([('SR.', 'SR.'),('SRA.', 'SRA.')],tracking=True)
    name5 = fields.Many2one('res.country',tracking=True)
    nit = fields.Char(string='NIT', size=11, tracking=True)
    tipod=fields.Selection([('N.U.I.P', 'N.U.I.P'),('Cédula de Ciudadania', 'CÉDULA DE CIUDADANIA'),('Cédula de Extranjería', 'CÉDULA DE EXTRANJERÍA'), ('Tarjeta de Identidad', 'TARJETA DE IDENTIDAD'),('Pasaporte','PASAPORTE'),('NIT','NIT'),('Registro Civil','REGISTRO CIVIL'),('Visa','VISA'),('Antecedentes Disciplinarios','PERMISO ESPECIAL DE RESIDENCIA'),('RUT','RUT')],'Tipo de Identificación',tracking=True)
    ide=fields.Char(string="Número de Identificación")
    cide=fields.Char(string="Confirmar Número de Identificación")
    lugar_expedicion=fields.Many2one('res.city')
    ascenso=fields.Boolean(tracking=True)
    tratamiento_datos=fields.Boolean()
    description=fields.Text(invisible="True")
    emal_cc=fields.Char('Confirmar correo electrónico')
    #Campos de Dirección. tipo DIAN   
    direccion_dian=fields.Many2one('direccion',tracking=True)
    nombre_via_principla=fields.Char('Nombre Via Principal',tracking=True)
    via_generadora=fields.Char(tracking=True)
    Predio=fields.Char(tracking=True)
    complemento=fields.Char(tracking=True)
    dire_completo=fields.Char(tracking=True)
    #campos grupo 2 de la page informacion general
    name13 = fields.Char(string="Nombre Completo",tracking=True)    
    pais= fields.Many2one('res.country',tracking=True)
    namef = fields.Date(string="Fecha de Nacimiento")
    lugar_de_nacimiento=fields.Char()
    conf=fields.Date(string="Confirmar Fecha de Nacimiento")    
    dep=fields.Many2one('res.country.state', 'Departamento',tracking=True)
    city=fields.Many2one('res.city','Ciudad', tracking=True)
    barrio=fields.Char(string="Barrio de Residencia", tracking=True)     
    #tallas, pantalon, camisa, saco, zapatos
    tallap=fields.Selection([('XS', 'XS'),('S', 'S'),('M', 'M'), ('L', 'L'),('XL','XL'),('XXL','XXL')],'Talla Pantalón', tracking=True)
    tallac=fields.Selection([('XS', 'XS'),('S', 'S'),('M', 'M'), ('L', 'L'),('XL','XL'),('XXL','XXL')], 'Talla Camisa',tracking=True)
    tallas=fields.Selection([('XS', 'XS'),('S', 'S'),('M', 'M'), ('L', 'L'),('XL','XL'),('XXL','XXL')], 'Talla Saco',tracking=True)
    tallaz=fields.Selection(tallazapatos, 'Talla Zapatos', tracking=True)     
    #telefono,celular,correo,confirmar correo, idioma nativo, grupo sanguineo, genero. 
    tel=fields.Char(string="Télefono", tracking=True)
    cel=fields.Char(string="Celular", tracking=True)
    correo=fields.Char(string="Correo", tracking=True)
    ccorreo=fields.Char(string="Confirmar Correo")
    idioma=fields.Many2one('res.lang',tracking=True)
    grupo_san=fields.Selection(grupo_san,'Grupo Sanguíneo')
    genero=fields.Selection([('Masculino', 'MASCULINO'),('Femenino', 'FEMENINO')])
    renta=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)
    declara_renta=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
    #GRUPO: INFORMACION DE VIVIENDA.
    tipo_vivienda=fields.Selection(tipo_vivienda,tracking=True)    
    cual_tipo_vivienda=fields.Char(tracking=True)
    carac_vivienda=fields.Selection([('CASA', 'CASA'),('APARTAMENTO', 'APARTAMENTO'),('HABITACIÓN', 'HABITACIÓN'),('OTRO','OTRO')],'Caracteristicas de la Vivienda',tracking=True)
    cual_carc_vivienda=fields.Char(tracking=True)   
    zona_vivienda=fields.Selection([('RURAL', 'RURAL'),('URBANA', 'URBANA'),('SUB', 'SUB URBANA')],tracking=True)
    ser_energia_elec=fields.Selection([('Si', 'SI'),('No', 'NO')],'Cuenta con servicio de energía eléctrica',tracking=True)
    alcantarilla=fields.Selection([('Si', 'SI'),('No', 'NO')],'Cuenta con Servicio de Alcantarillado',tracking=True)
    acc=fields.Selection([('Si', 'SI'),('No', 'NO')],'Cuenta con Servicio de Acueducto',tracking=True)
    #GRUPO: INFORMACION DE VIVIENDA2
    basura=fields.Selection([('Si', 'SI'),('No', 'NO')],'Cuenta con servicio de recolección de basura',tracking=True)
    etnico=fields.Selection([('Mestizo', 'MESTIZO'),('Blanco', 'BLANCO'),('Afrocolombiano', 'AFROCOLOMBIANO'),('Indigena','INDIGENA'),('Gitano','GITANO')],'Grupo Etnico',tracking=True)
    estrato=fields.Selection([('1', '1'),('2', '2'),('3', '3'),('4','4'),('5','5'),('6','6')],tracking=True)
    gt=fields.Selection([('SI', 'SI'),('NO', 'NO')],'Cuenta con Servicio de Gas',tracking=True) 
    #campos: entidades del sistema de seguridad
    eps=fields.Many2one('res.partner','EPS',tracking=True)
    afp=fields.Many2one('res.partner','AFP',tracking=True)
    afc=fields.Many2one('res.partner','AFC',tracking=True)    
    #informacion parentesco
    nombre_completo=fields.Char(string="Nombre Completo",tracking=True)
    tel_contacto=fields.Char(string="Télefono",tracking=True)
    parentesco=fields.Selection([('ABUELO (A)', 'ABUELO (A)'),('AMIGO (A)', 'AMIGO (A)'),('ESPOSO (A)', 'ESPOSO (A)'),('HERMANO (A)','HERMANO (A)'),('PADRE','PADRE'),('MADRE','MADRE'),('SORBINO (A)','SOBRINO (A)'),('TIO (A)','TIO (A)'),('HIJO (A)','HIJO (A)'),('OTRO','OTRO')],tracking=True)
    Cual_Parentezco=fields.Char(tracking=True)
    via_principal_pariente = fields.Many2one('direccion',tracking=True)
    nombre_via_principal_pariente = fields.Char(tracking=True)
    via_generadora_pariente = fields.Char(tracking=True)
    Predio_pariente = fields.Char(tracking=True)
    complemento_pariente = fields.Char(tracking=True)
    direccion_contacto=fields.Char(string="Dirección del contacto",tracking=True)
    via_principal_con=fields.Many2one('direccion','Vía Principal',tracking=True)
    nombre_via_principal_cont=fields.Char('Nombre Vía Principal',tracking=True)
    via_generadora_con=fields.Char('Vía Generadora',tracking=True)
    predio_con=fields.Char('Predio',tracking=True)
    complemento_con=fields.Char(tracking=True)
    re=fields.Selection([('Si', 'SI'),('No', 'NO')],tracking=True)
    pe_eco=fields.Selection([('Si', 'SI'),('No', 'NO')],'Existen personas que dependan económicamente de usted',tracking=True)
    cab_familia=fields.Selection([('Si', 'SI'),('No', 'NO')],'Es cabeza de familia',tracking=True)
    num_personas = fields.Integer(tracking=True)
    num_personas_discapacitada = fields.Integer(tracking=True)
    no_personas_nucleo_familiar=fields.Integer('No. de personas del nucleo familiar',tracking=True)
    no_personas_estado_incapacidad=fields.Integer('No. Personas en Estado de Incapacidad',tracking=True)  
    #informacion de mascotas
    #num_mascotas=fields.Many2many('mascotas',tracking=True)
    #mascotas=fields.Integer(string="Numero de Mascotas",tracking=True)
    #tipo_mascotas=fields.Char(string="Tipo de Mascotas",tracking=True)
    #informacion de transporte
    lic_conducir=fields.Selection([('SI', 'SI'),('NO', 'NO')],'Licencia de Conducir',tracking=True)
    tipo_lic_conducir=fields.Selection([('A1', 'A1'),('A2', 'A2'),('B1', 'B1'),('B2','B2'),('B3','B3'),('C1', 'C1'),('C2','C2'),('C3','C3')],'Tipo de Licencia de Conducir',tracking=True)
    medio_transporte=fields.Selection([('BICICLETA', 'BICICLETA'),('CAMINANDO', 'CAMINANDO'),('CARRO', 'CARRO'),('MOTO','MOTO'),('PATINETA','PATINETA'),('TRANSPORTE COMPARTIDO', 'TRANSPORTE COMPARTIDO'),('TRANSPORTE PRIVADO(TAXI, UBER, BEAT)','TRANSPORTE PRIVADO(TAXI, UBER, BEAT)')],'Medio de transporte Principal',tracking=True)
    medio_transporte_sec=fields.Selection([('BICICLETA', 'BICICLETA'),('CAMINANDO', 'CAMINANDO'),('CARRO', 'CARRO'),('MOTO','MOTO'),('PATINETA','PATINETA'),('TRANSPORTE COMPARTIDO', 'TRANSPORTE COMPARTIDO'),('TRANSPORTE PRIVADO(TAXI, UBER, BEAT)','TRANSPORTE PRIVADO(TAXI, UBER, BEAT)')],'Medio de transporte secundario',tracking=True)
    Horas_trabajo=fields.Selection([('MENOS DE 30 MINUTOS', 'MENOS DE 30 MINUTOS'),('30 MINUTOS', '30 MINUTOS'),('1 HORA', '1 HORA'),('1.5 HORAS','1.5 HORAS'),('2 HORAS','2 HORAS'),('2.5 HORAS', '2.5 HORAS'),('3 HORAS','3 HORAS'),('3.5 HORAS','3.5 HORAS'),('4 HORAS','4 HORAS'),('4.5 HORAS','4.5 HORAS')],'Horas en llegar al trabajo',tracking=True)
    estudia_actualmente=fields.Selection([('Si', 'Si'),('No', 'No')],tracking=True)
    ano_graduacion=fields.Date(string="Año de Graduación",tracking=True)
    escolaridad=fields.Selection([('Primaria', 'PRIMARIA'),('Bachiller', 'BACHILLER'),('Curso o Seminario', 'CURSO O SEMINARIO'),('Técnica','TÉCNICA'),('Tecnológica','TECNOLÓGICA'),('Universitaria', 'UNIVERSITARIA'),('Especialización', 'ESPECIALIZACIÓN'),('Maestría','MAESTRÍA'),('Doctorado','DOCTORADO')],tracking=True)
    estado_civil=fields.Selection([('SOLTERO/A', 'SOLTERO/A'),('CASADO/A', 'CASADO/A'),('DIVORCIADO/A', 'DIVORCIADO/A'),('UNIÓN LIBRE','UNIÓN LIBRE'),('VIUDO/A','VIUDO/A')],tracking=True)

    #campos conyugue
    primer_apellido_conyugue=fields.Char(string="Primer Apellido del Cónyugue",tracking=True)
    segundo_apellido_conyugue=fields.Char(string="Segungo Apellido del Cónyugue",tracking=True)
    primer_nombre_conyugue=fields.Char(string="Primer Nombre del Cónyugue",tracking=True)
    segundo_nombre_conyugue=fields.Char(string="Segundo Nombre del Cónyugue",tracking=True)
    escolaridad_conyugue=fields.Selection([('Primaria', 'PRIMARIA'),('Bachiller', 'BACHILLER'),('Curso o Seminario', 'CURSO O SEMINARIO'),('Técnica','TÉCNICA'),('Tecnológica','TECNOLÓGICA'),('Universitaria', 'UNIVERSITARIA'),('Especialización', 'ESPECIALIZACIÓN'),('Maestría','MAESTRÍA'),('Doctorado','DOCTORADO')],tracking=True)
    genero_conyugue=fields.Selection([('Masculino', 'MASCULINO'),('Femenino', 'FEMENINO')])
    lugar_nacimiento_conyugue=fields.Many2one('res.city')
    pais_nacimiento_conyugue = fields.Many2one('res.country')
    fecha_conyugue = fields.Date()
    #informacion de hijos
    hijos=fields.Many2many('hijo',tracking=True)
    #campos relacionados traidos de la requisición
    requisicion=fields.Many2one('requisiciones',tracking=True)
    emp_aplica=fields.Char(string='Empresa', related='requisicion.company_id.name',tracking=True)
    cargo_aplica=fields.Char(string="Cargo al que Aplica", related="requisicion.cargo_solicitado.name",tracking=True)
    jefe=fields.Char(string="Jefe Inmediato", related="requisicion.jefe_inmediato.name",tracking=True)
    prueba=fields.Char()
    sede=fields.Char(string="Sede", related="requisicion.sede",tracking=True)
    departamento_req=fields.Many2one(related="requisicion.departamento")
    area_req=fields.Char(string="Área", related="requisicion.area")   
    turno_trabajo=fields.Selection(related="requisicion.turn",tracking=True)
    personal_cargo=fields.Selection(related="requisicion.personal_a_cargo",tracking=True)
    psicologo_req=fields.Many2one(related="requisicion.psicologo_req", string="Psicologo")
    reclutador_req=fields.Many2one(related="requisicion.reclutador_req", string="Reclutador")
    correo_psicologo=fields.Char(related="requisicion.correo_psicologo")
    ciudad_req = fields.Many2one(related="requisicion.res_city", string="Ciudad",tracking=True)
    #experiencia del aplicante
    resume=fields.Many2many('hr.resume.line',tracking=True)
    resume_line_ids = fields.One2many('hr.resume.line', 'applicant_id', string="Resumé lines",tracking=True)
    employee_skill_ids = fields.One2many('hr.employee.skill', 'employee_id', string="Skills",tracking=True) 
    #campos: Idiomas que habla el aplicante 
    otro_idioma=fields.Selection([('EN Ingles', 'EN Ingles'),('ES Español', 'ES Español'),('FR Francés', 'FR Francés'),('IT Italiano','IT Italiano')],tracking=True)
    porcent_dominio=fields.Integer(string="Porcentaje de Dominio",tracking=True)
    po=fields.Integer( related="porcent_dominio")
    Habla_un_Idioma_Diferente=fields.Selection([('Si', 'SI'),('No', 'NO')])
    lenguage=fields.Many2many('lenguage',tracking=True)
    #formacion academica
    formacion_academica=fields.Many2many('escolaridad',tracking=True)
    #escolaridad del solicitante
    escolaridad_solicitante=fields.Selection([('Primaria', 'PRIMARIA'),('Bachiller', 'BACHILLER'),('Curso o Seminario', 'CURSO O SEMINARIO'),('Técnica','TÉCNICA'),('Tecnológica','TECNOLÓGICA'),('Universitaria', 'UNIVERSITARIA'),('Especialización', 'ESPECIALIZACIÓN'),('Maestría','MAESTRÍA'),('Doctorado','DOCTORADO')],tracking=True)
    estudia_actualmente_solicitante=fields.Selection([('Si', 'SI'),('No', 'NO')])  
    #informacion especifica
    miedos=fields.Many2many('fobias',tracking=True)
    hobby=fields.Char(string="Hobby")
    nombre_hobby=fields.Many2many('hob',tracking=True)
    tiene_enfermedad=fields.Char(string="Tiene alguna enfermedad Importante",tracking=True)
    toma_medicamneto=fields.Char(string="Toma algun Medicamento",tracking=True)
    tiene_alergia=fields.Char(string="Tiene alguna Alergia")
    alergia=fields.Many2many('alergia')
    #campos tipo adjuntos (documentos personales)
    fotocopia_cedula=fields.Binary(tracking=True, copy=False)
    fotocopia_cedula_filename = fields.Char("File Name")
    cer_estudio=fields.Binary(tracking=True)
    cer_estudio_emp_filename = fields.Char("File Name")
    certi_laborales=fields.Binary(tracking=True)
    certi_laborales_emp_filename = fields.Char("File Name") 
    hv=fields.Binary(tracking=True)
    hv_filename = fields.Char("File Name")
    aceptacion_condiciones=fields.Binary(tracking=True)
    aceptacion_condiciones_emp_filename = fields.Char("File Name")
    libreta_militar=fields.Binary(tracking=True)
    libreta_militar_emp_filename = fields.Char("File Name")
    refrecnias_personales=fields.Binary(tracking=True)
    refrecnias_personales_emp_filename = fields.Char("File Name")
    verificacion_referencias=fields.Binary(tracking=True)
    verificacion_referencias_emp_filename = fields.Char("File Name")     
    certificado_cuenta_bancaria=fields.Binary(tracking=True)
    certificado_cuenta_bancaria_emp_filename = fields.Char("File Name")
    antecedentes_disciplinarios=fields.Binary(tracking=True)
    antecedentes_disciplinarios_emp_filename = fields.Char("File Name")
    validacion_antecedentes=fields.Binary(tracking=True)
    validacion_antecedentes_emp_filename = fields.Char("File Name")
    entrevista_jefe_inmediato=fields.Binary(tracking=True)
    entrevista_jefe_inmediato_emp_filename = fields.Char("File Name")
    fotografias=fields.Binary(tracking=True)
    fotografias_emp_filename = fields.Char("File Name")
    validacion_sarlaft=fields.Binary(tracking=True)
    validacion_sarlaft_emp_filename = fields.Char("File Name")
    TGS_Solidarios=fields.Binary(tracking=True)
    TGS_Solidarios_filename = fields.Char("File Name") 
    seguro_obligatorio_vigente = fields.Binary(tracking=True)
    seguro_obligatorio_vigente_filename = fields.Char("File Name")   
    estudio_seguridad=fields.Binary(tracking=True)
    estudio_seguridad_emp_filename = fields.Char("File Name")
    examendes_medicos=fields.Binary(tracking=True)
    examendes_medicos_emp_filename = fields.Char("File Name")
    poliza=fields.Binary(tracking=True)
    poliza_emp_filename = fields.Char("File Name")
    autorizacion_uso_correo=fields.Binary(tracking=True)
    autorizacion_uso_correo_emp_filename = fields.Char("File Name")
    licencia_conducir=fields.Binary(tracking=True)
    licencia_conducir_emp_filename = fields.Char("File Name")
    carta_propiedad_vehiculo=fields.Binary(tracking=True)
    carta_propiedad_vehiculo_emp_filename = fields.Char("File Name")
    autorizacion_propietario=fields.Binary(tracking=True)
    cer_runt=fields.Binary(tracking=True)
    cer_runt_emp_filename = fields.Char("File Name")
    seguro_obligatorio_vigente=fields.Binary(tracking=True)
    seguro_obligatorio_vigente_filename = fields.Char("File Name")
    revision_tecnico_mecanica=fields.Binary(tracking=True)
    revision_tecnico_mecanica_emp_filename = fields.Char("File Name")
    centro_induccion = fields.Binary(tracking=True)
    centro_induccion_emp_filename = fields.Char("File Name")
    certificacion_sena = fields.Binary(tracking=True)
    certificacion_senafile_name = fields.Char("File Name")
    caja_compensacion_sol=fields.Many2one('caja')    
    #campos: Razón de la Excepción
    formacion=fields.Boolean(tracking=True)
    experiencia=fields.Boolean(tracking=True)
    habilidades=fields.Boolean(tracking=True)
    educacion=fields.Boolean(tracking=True)
    fecha_compromiso=fields.Date(tracking=True)
    fecha_vencimiento=fields.Date(tracking=True)
    plan_accion=fields.Text(tracking=True)
    #ocultar campos
    email_from=fields.Char(invisible="True")
    email_cc=fields.Char(invisible="True")
    partner_phone=fields.Char(invisible="True")
    #employee_id    
    #campos de tiempos en etapas (ANS)
    tiempo_pre_seleccionado = fields.Float('Tiempo en Etapa Pre-Seleccionado',tracking=True)
    tiempo_entrevista_psicologica = fields.Float('Tiempo en Etapa Entrevista Psicológica',tracking=True)
    tiempo_entrevista_jefe_inmediato = fields.Float('Tiempo en Etapa Entrevista Jefe Inmediato',tracking=True)
    tiempo_estudio_seguridad = fields.Float('Tiempo en Etapa Estudio de Seguridad',tracking=True)
    tiempo_examen_medico = fields.Float('Tiempo en Etapa Exámen Médico',tracking=True)
    tiempo_referencias = fields.Float('Tiempo en Etapa Referecias',tracking=True)
    tiempo_contratacion = fields.Float('Tiempo en Etapa Contratación',tracking=True)
    tiempo_compensacion_beneficios = fields.Float('Tiempo en Etapa Compensación y Beneficios',tracking=True)
    tiempo_espera_por_cliente = fields.Float('Tiempo en Etapa Espera por el Cliente',tracking=True)
    tiempo_espera_por_candidato = fields.Float('Tiempo en Etapa Espera por el Candidato',tracking=True)
    tiempo_espera_por_tercero = fields.Float('Tiempo en Etapa Espera por el Tercero',tracking=True)
    tiempo_total = fields.Float('Tiempo Total del Proceso',tracking=True)
    #campos de hora y fechas
    tiempo_inicial=fields.Datetime('Fecha y hora de inicio',tracking=True, default= fields.Datetime().now())
    fecha_hora_pre_seleccionado = fields.Datetime('Fecha y hora Pre-Seleccionado', tracking=True, default= fields.Datetime().now())
    fecha_hora_entrevista_psicologica = fields.Datetime('Fecha y hora Entrevista Psicologica', tracking=True)
    fecha_hora_entrevista_jefe_inmediato = fields.Datetime('Fecha y hora Entrevista Jefe Inmediato', tracking=True)
    fecha_hora_estudio_seguridad = fields.Datetime('Fecha y hora Estudio Seguridad', tracking=True)
    fecha_hora_examen_medico = fields.Datetime('Fecha y hora Exámen Médico', tracking=True)
    fecha_hora_examen_referencias = fields.Datetime('Fecha y hora Referencias', tracking=True)
    fecha_hora_examen_contratacion = fields.Datetime('Fecha y hora Contratación', tracking=True)
    fecha_hora_compensacion_beneficios = fields.Datetime('Fecha y hora Compensación y Beneficios', tracking=True)
    fecha_hora_espera_por_cliente = fields.Datetime('Fecha y hora Espera Por Cliente', tracking=True)
    fecha_hora_espera_por_candidato = fields.Datetime('Fecha y hora Espera Por Candidato', tracking=True)
    fecha_hora_espera_por_tercero = fields.Datetime('Fecha y hora Espera Por Tercero', tracking=True)
    fecha_hora_reclutamiento = fields.Datetime('Fecha y hora En Reclutamiento', tracking=True)
    #Estados  
    estado_de_solicitud=fields.Char(related="stage_id.name")
    id_estado_de_solicitud=fields.Integer(related="stage_id.sequence")
    ide_requisicion = fields.Char(related="requisicion.name", string="Identificador de la Requisición")    
             
    @api.onchange('from_date', 'final_date','total_days')
    def calculate_date(self):
        if self.from_date and self.final_date:
            d1=datetime.strptime(str(self.from_date),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.final_date),'%Y-%m-%d')
            d3=d2-d1
            self.total_days=str(d3.days)      

    @api.constrains('nit')
    def _check_nit_size(self):
        pattern = "^\+?[0-9]*$" 
        for record in self:
            if record.nit and re.match(pattern, record.nit) is None:
                raise ValidationError(("NIT debe ser numerico"))

    #concatenación Dirección tipo DIAN
    @api.onchange('direccion_dian', 'nombre_via_principla', 'via_generadora', 'Predio', 'complemento')                  
    def _onchange_direccion_dian(self):
        self.dire_completo = "%s %s %s %s %s " % (
            self.direccion_dian.identificador if self.direccion_dian else "",           
            self.nombre_via_principla if self.nombre_via_principla else "",           
            self.via_generadora if self.via_generadora else "",           
            self.Predio if self.Predio else "",
            self.complemento if self.complemento else "")
    
    #concatenación Dirección persona caso de Emergencia
    @api.onchange('via_principal_con', 'nombre_via_principal_cont', 'via_generadora_con', 'predio_con', 'complemento_con')                  
    def _onchange_direccion_persona_caso_emergencia(self):
        self.direccion_contacto = "%s %s %s %s %s " % (
            self.via_principal_con.identificador if self.via_principal_con else "",           
            self.nombre_via_principal_cont if self.nombre_via_principal_cont else "",           
            self.via_generadora_con if self.via_generadora_con else "",           
            self.predio_con if self.predio_con else "",
            self.complemento_con if self.complemento_con else "")

    #concatenación asunto/solicitante
    @api.onchange('ide_requisicion','cargo_aplica', 'partner_name')                  
    def _onchange_asunto_solicitante(self):
        self.name = "[%s] %s / %s" % (
            self.ide_requisicion if self.ide_requisicion else "",
            self.cargo_aplica if self.cargo_aplica else "",          
            self.partner_name if self.partner_name else "")

    #concatenación: Nombre del aplicante
    @api.onchange('tratamiento','name3',   'name4',  'name1',  'name2')
    def _onchange_street(self):
        self.partner_name = "%s %s %s %s %s" % (
            self.tratamiento if self.tratamiento else "",
            self.name3 if self.name3 else "",        
          
            self.name4 if self.name4 else "",         
            
            self.name1 if self.name1 else "",
           
            self.name2 if self.name2 else "")

    # validar numero de identifiacion y confirmacion del mismo. 
    @api.constrains('ide', 'cide')
    def _check_some(self):
        for record in self:
            if record.ide != record.cide:
                raise ValidationError("Verificar su Número de Identificación : %s" % record.ide)

    #validar fecha de nacimiento
    @api.constrains('namef', 'conf')
    def _check_somethi(self):
        for record in self:
            if record.namef != record.conf:
                raise ValidationError("Verificar la confirmación de su fecha de nacimiento! : %s" % record.namef)
    
    #validar correo electronico
    @api.constrains('email_from', 'emal_cc')
    def _check_something(self):
        for record in self:
            if record.email_from != record.emal_cc:
                raise ValidationError("Verificar la confirmación de su Correo! : %s" % record.email_from)

    # en esta funcion pater hay que enviar tambien los cambios que guradan los nombres                       
    def create_employee_from_applicant(self):
        res = super(Todoo, self).create_employee_from_applicant()
        # res['main_road_name'] = self.nombre_via_principla
        employee_id = self.env['hr.employee'].browse(res['res_id'])
        vals = {
            'main_road': self.direccion_dian,
            'main_road_name': self.nombre_via_principla,
            'road_generator': self.via_generadora,
            'land': self.Predio,
            'complement': self.complemento,            
            'pants_size': self.tallap,
            'shirt_size': self.tallac,
            'coat_size': self.tallas,
            'shoes_size': self.tallaz,
            'identification_type': self.tipod,
            'identification_id': self.ide,
            'blood_group': self.grupo_san,
            'genero': self.genero,
            'property_type': self.tipo_vivienda,
            'property_type2': self.cual_tipo_vivienda,
            'property_characteristic': self.carac_vivienda,
            'property_characteristic2': self.cual_carc_vivienda,
            'property_zone': self.zona_vivienda,
            'energy_service': self.ser_energia_elec,
            'sewerage_service': self.alcantarilla,
            'aqueduct_service': self.acc,
            'gas_service': self.gt,
            'trash_service': self.basura,
            'etnic_group': self.etnico,
            'socioeconomical_state': self.estrato,
            'drive_license': self.lic_conducir,
            'license_type': self.tipo_lic_conducir,
            'main_transport': self.medio_transporte,
            'second_transport': self.medio_transporte_sec,
            'hour_to_arrive': self.Horas_trabajo,
            'first_name': self.name3,
            'second_name': self.name4,
            'third_name':self.name1,
            'fourth_name': self.name2,
            'civil_state': self.estado_civil,
            'fotocopia_cedula': self.fotocopia_cedula,
            'fotocopia_cedula_filename': self.fotocopia_cedula_filename, 
            'validacion_antecedentes_emp': self.validacion_antecedentes,
            'hv_emp': self.hv,
            'cer_estudio_emp': self.cer_estudio,
            'certi_laborales_emp': self.certi_laborales,
            'aceptacion_condiciones_emp': self.aceptacion_condiciones,
            'libreta_militar_emp': self.libreta_militar,
            'refrecnias_personales_emp': self.refrecnias_personales,
            'verificacion_referencias_emp': self.verificacion_referencias,
            'certificado_cuenta_bancaria_emp': self.certificado_cuenta_bancaria,
            'antecedentes_disciplinarios_emp': self.antecedentes_disciplinarios,
            'entrevista_jefe_inmediato_emp': self.entrevista_jefe_inmediato,
            'fotografias_emp': self.fotografias,
            'validacion_sarlaft_emp': self.validacion_sarlaft,
            'estudio_seguridad_emp': self.estudio_seguridad,
            'examendes_medicos_emp': self.examendes_medicos,
            'poliza_emp': self.poliza,
            'autorizacion_uso_correo_emp': self.autorizacion_uso_correo,
            'licencia_conducir_emp': self.licencia_conducir,
            'carta_propiedad_vehiculo_emp': self.carta_propiedad_vehiculo,
            'cer_runt_emp': self.cer_runt,
            'revision_tecnico_mecanica_emp': self.revision_tecnico_mecanica,
            'centro_induccion_emp': self.centro_induccion,
            'certificacion_sena_emp': self.certificacion_sena,
            'rent': self.renta,
            'afp_emp': self.afp,
            'afc_emp': self.afc,
            'eps_emp': self.eps,
            'first_last_name_parent': self.primer_apellido_conyugue,
            'second_last_name_parent': self.segundo_apellido_conyugue,
            'first_name_parent': self.primer_nombre_conyugue,
            'second_name_parent': self.segundo_nombre_conyugue,
            'gender_parent_emp': self.genero_conyugue,
            'depend_person': self.pe_eco,
            'head_family': self.cab_familia,
            'number_family': self.no_personas_nucleo_familiar,
            'number_person_discapacited': self.no_personas_estado_incapacidad,
            'full_name': self.nombre_completo,
            'Phone': self.tel_contacto,
            'relationship': self.parentesco,
            'what_relationship': self.Cual_Parentezco,
            'main_road_name_parent': self.nombre_via_principal_cont,
            'main_road_parent': self.direccion_dian,
            'road_generator_parent': self.via_generadora_con,
            'land_parent': self.predio_con,
            'complement_parent': self.complemento_con,        
            'nombre_hobby_emp': self.nombre_hobby,
            'miedos_emp': self.miedos,
            'alergia_emp':self.alergia,
            'escolaridad_emp': self.formacion_academica,
            'lenguage_emp': self.lenguage,
            'requisition_id': self.requisicion,
            'neighbordhood_residence': self.barrio,
            'tiene_enfermedad_emp': self.tiene_enfermedad,
            'toma_medicamneto_emp': self.toma_medicamneto,
            'city_residence': self.city,
            'state_residence': self.dep,
            'language': self.idioma,
            'mascotas_line_emp': self.mascotas_line,
            'hijos_line_emp': self.hijos_Line,           
            'telefono_del_empleado': self.partner_phone,
            'celular_del_empleado': self.partner_mobile,
            'correo_privado_del_empleado': self.email_from,
            'tratamiento_emp': self.tratamiento,
            'lugar_expedicion_id_emp': self.lugar_expedicion,
            'birthday': self.namef,
            'confirmation_date_of_birth': self.conf,
            'rent': self.declara_renta,
            'place_of_birth': self.lugar_de_nacimiento,
            'country_of_birth': self.pais,
            'country_born_parent_emp': self.pais_nacimiento_conyugue,
            'date_birth_parent_emp': self.fecha_conyugue,
            'escolaridad_solicitante_emp': self.escolaridad_solicitante,
            'estudia_actualmente_solicitante_emp': self.estudia_actualmente_solicitante,
            'idioma_line_emp': self.idioma_line,
            'country_id': self.pais,
            'escolaridad_conyugue_emp': self.escolaridad_conyugue,
            'born_place_parent_emp': self.lugar_nacimiento_conyugue,
            'formacion_line_emp': self.formacion_line,
            'resume_line_ids': self.resume_line_ids,
            'cer_estudio_emp_filename': self.cer_estudio_emp_filename,
            'certi_laborales_emp_filename': self.certi_laborales_emp_filename,
            'hv_emp_filename': self.hv_filename,
            'aceptacion_condiciones_emp_filename': self.aceptacion_condiciones_emp_filename,
            'libreta_militar_emp_filename': self.libreta_militar_emp_filename,
            'refrecnias_personales_emp_filename': self.refrecnias_personales_emp_filename,
            'verificacion_referencias_emp_filename': self.verificacion_referencias_emp_filename,
            'certificado_cuenta_bancaria_emp_filename': self.certificado_cuenta_bancaria_emp_filename,
            'antecedentes_disciplinarios_emp_filename': self.antecedentes_disciplinarios_emp_filename,
            'validacion_antecedentes_emp_filename': self.validacion_antecedentes_emp_filename,
            'entrevista_jefe_inmediato_emp_filename': self.entrevista_jefe_inmediato_emp_filename,
            'fotografias_emp_filename': self.fotografias_emp_filename,
            'validacion_sarlaft_emp_filename': self.validacion_sarlaft_emp_filename,           
            'estudio_seguridad_emp_filename': self.estudio_seguridad_emp_filename,
            'examendes_medicos_emp_filename': self.examendes_medicos_emp_filename,
            'poliza_emp_filename': self.poliza_emp_filename,
            'autorizacion_uso_correo_emp_filename': self.autorizacion_uso_correo_emp_filename,
            'licencia_conducir_emp_filename': self.licencia_conducir_emp_filename,
            'carta_propiedad_vehiculo_emp_filename': self.carta_propiedad_vehiculo_emp_filename,
            'cer_runt_emp_filename': self.cer_runt_emp_filename,
            'seguro_obligatorio_vigente': self.seguro_obligatorio_vigente,
            'seguro_obligatorio_vigente_filename': self.seguro_obligatorio_vigente_filename,
            'revision_tecnico_mecanica_emp_filename': self.revision_tecnico_mecanica_emp_filename,
            'centro_induccion_emp_filename': self.centro_induccion_emp_filename,
            'file_name': self.certificacion_senafile_name,
            'TGS_Solidarios': self.TGS_Solidarios,
            'TGS_Solidarios_filename': self.TGS_Solidarios_filename,
            'requisition_id': self.requisicion,
            'aplicante': self.partner_name,
            'complete_direction': self.dire_completo,
            'complete_direction_parent': self.direccion_contacto,
        }
        employee_id.write(vals)
        employee_id.action_req()
        return res


    #funcion para traer campos de la requisicion editables    
    @api.onchange('requisicion')
    def _onchange_requisicion(self):
      if self.requisicion:
         self.job_id =  self.requisicion.cargo_solicitado

    
    @api.onchange('nombre_via_principla','via_generadora','Predio','complemento')
    def _compute_address_thomas(self):        
        self.nombre_via_principla = self.nombre_via_principla.upper() if self.nombre_via_principla else False
        self.via_generadora = self.via_generadora.upper() if self.via_generadora else False
        self.Predio = self.Predio.upper() if self.Predio else False
        self.complemento = self.complemento.upper() if self.complemento else False

    @api.onchange('nombre_via_principal_cont','via_generadora_con','predio_con','complemento_con')
    def _compute_address_thomas(self):        
        self.nombre_via_principal_cont = self.nombre_via_principal_cont.upper() if self.nombre_via_principal_cont else False
        self.via_generadora_con = self.via_generadora_con.upper() if self.via_generadora_con else False
        self.predio_con = self.predio_con.upper() if self.predio_con else False
        self.complemento_con = self.complemento_con.upper() if self.complemento_con else False         

   #funcion para colocar nombre del conyugue en mayusculas. 
    @api.onchange('primer_apellido_conyugue','segundo_apellido_conyugue','primer_nombre_conyugue','segundo_nombre_conyugue')
    def _compute_maj_solicitante(self):
        self.primer_apellido_conyugue = self.primer_apellido_conyugue.upper() if self.primer_apellido_conyugue else False
        self.segundo_apellido_conyugue = self.segundo_apellido_conyugue.upper() if self.segundo_apellido_conyugue else False
        self.primer_nombre_conyugue = self.primer_nombre_conyugue.upper() if self.primer_nombre_conyugue else False
        self.segundo_nombre_conyugue = self.segundo_nombre_conyugue.upper() if self.segundo_nombre_conyugue else False

    @api.model
    def create(self, vals):
        res = super(Todoo, self).create(vals)
        if 'fotocopia_cedula' in vals and vals['fotocopia_cedula_filename']:
            dic = {
                'name': vals['fotocopia_cedula_filename'], 
                'datas': vals['fotocopia_cedula'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'cer_estudio'  in vals and vals['cer_estudio_emp_filename']:
            dic = {
                'name': vals['cer_estudio_emp_filename'],
                'datas': vals['cer_estudio'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

        if 'certi_laborales' in vals and vals['certi_laborales_emp_filename']:
            dic = {
                'name': vals['certi_laborales_emp_filename'],
                'datas': vals['certi_laborales'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'hv' in vals and vals['hv_filename']:
            dic = {
                'name': vals['hv_filename'],
                'datas': vals['hv'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

        if 'aceptacion_condiciones' in vals and vals['aceptacion_condiciones_emp_filename']:
            dic = {
                'name': vals['aceptacion_condiciones_emp_filename'],
                'datas': vals['aceptacion_condiciones'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)  

        if 'libreta_militar' in vals and vals['libreta_militar_emp_filename']:
            dic = {
                'name': vals['libreta_militar_emp_filename'],
                'datas': vals['libreta_militar'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'refrecnias_personales' in vals and vals['refrecnias_personales_emp_filename']:
            dic = {
                'name': vals['refrecnias_personales_emp_filename'],
                'datas': vals['refrecnias_personales'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'verificacion_referencias' in vals and vals['verificacion_referencias_emp_filename']:
            dic = {
                'name': vals['verificacion_referencias_emp_filename'],
                'datas': vals['verificacion_referencias'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

        if 'certificado_cuenta_bancaria' in vals and vals['certificado_cuenta_bancaria_emp_filename']:
            dic = {
                'name': vals['certificado_cuenta_bancaria_emp_filename'],
                'datas': vals['certificado_cuenta_bancaria'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'antecedentes_disciplinarios' in vals and vals['antecedentes_disciplinarios_emp_filename']:
            dic = {
                'name': vals['antecedentes_disciplinarios_emp_filename'],
                'datas': vals['antecedentes_disciplinarios'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'validacion_antecedentes' in vals and vals['validacion_antecedentes_emp_filename']:
            dic = {
                'name': vals['validacion_antecedentes_emp_filename'],
                'datas': vals['validacion_antecedentes'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

        if 'entrevista_jefe_inmediato' in vals and vals['entrevista_jefe_inmediato_emp_filename']:
            dic = {
                'name': vals['entrevista_jefe_inmediato_emp_filename'],
                'datas': vals['entrevista_jefe_inmediato'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'fotografias' in vals and vals['fotografias_emp_filename']:
            dic = {
                'name': vals['fotografias_emp_filename'],
                'datas': vals['fotografias'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'validacion_sarlaft' in vals and vals['validacion_sarlaft_emp_filename']:
            dic = {
                'name': vals['validacion_sarlaft_emp_filename'],
                'datas': vals['validacion_sarlaft'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

       

        if 'estudio_seguridad' in vals and vals['estudio_seguridad_emp_filename']:
            dic = {
                'name': vals['estudio_seguridad_emp_filename'],
                'datas': vals['estudio_seguridad'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'examendes_medicos' in vals and vals['examendes_medicos_emp_filename']:
            dic = {
                'name': vals['examendes_medicos_emp_filename'],
                'datas': vals['examendes_medicos'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

        if 'poliza' in vals and vals['poliza_emp_filename']:
            dic = {
                'name': vals['poliza_emp_filename'],
                'datas': vals['poliza'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)
        
        if 'autorizacion_uso_correo' in vals and vals['autorizacion_uso_correo_emp_filename']:
            dic = {
                'name': vals['autorizacion_uso_correo_emp_filename'],
                'datas': vals['autorizacion_uso_correo'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)
         
        if 'licencia_conducir' in vals and vals['licencia_conducir_emp_filename']:
            dic = {
                'name': vals['licencia_conducir_emp_filename'],
                'datas': vals['licencia_conducir'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 
         
        if 'carta_propiedad_vehiculo' in vals and vals['carta_propiedad_vehiculo_emp_filename']:
            dic = {
                'name': vals['carta_propiedad_vehiculo_emp_filename'],
                'datas': vals['carta_propiedad_vehiculo'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)
        
        if 'cer_runt' in vals and vals['cer_runt_emp_filename']:
            dic = {
                'name': vals['cer_runt_emp_filename'],
                'datas': vals['cer_runt'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

       

        if 'revision_tecnico_mecanica' in vals and vals['revision_tecnico_mecanica_emp_filename']:
            dic = {
                'name': vals['revision_tecnico_mecanica_emp_filename'],
                'datas': vals['revision_tecnico_mecanica'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 
        
        if 'certificacion_sena' in vals and vals['certificacion_senafile_name']:
            dic = {
                'name': vals['certificacion_senafile_name'],
                'datas': vals['certificacion_sena'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

        if 'centro_induccion' in vals and vals['centro_induccion_emp_filename']:
            dic = {
                'name': vals['centro_induccion_emp_filename'],
                'datas': vals['centro_induccion'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

        if 'seguro_obligatorio_vigente' in vals and vals['seguro_obligatorio_vigente_filename']:
            dic = {
                'name': vals['seguro_obligatorio_vigente_filename'],
                'datas': vals['seguro_obligatorio_vigente'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic) 

        if 'TGS_Solidarios' in vals and vals['TGS_Solidarios_filename']:
            dic = {
                'name': vals['TGS_Solidarios_filename'],
                'datas': vals['TGS_Solidarios'],
                'res_model': 'hr.applicant', 
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)             

         
            
        return res

    def write(self, vals):
        if 'stage_id' in vals:
            id_stage = self.env['hr.recruitment.stage'].browse(vals['stage_id'])
            if id_stage.sequence == 1:                
                vals.update(fecha_hora_pre_seleccionado=fields.Datetime().now())

            if id_stage.sequence == 2:               
                vals.update(fecha_hora_entrevista_psicologica=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_pre_seleccionado
                calc = calc.seconds/3600
                vals.update(tiempo_pre_seleccionado=calc)

            if id_stage.sequence == 3:               
                vals.update(fecha_hora_entrevista_jefe_inmediato=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_entrevista_psicologica
                calc = calc.seconds/3600
                vals.update(tiempo_entrevista_psicologica=calc)

            if id_stage.sequence == 4:               
                vals.update(fecha_hora_estudio_seguridad=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_entrevista_jefe_inmediato
                calc = calc.seconds/3600
                vals.update(tiempo_entrevista_jefe_inmediato=calc)

            if id_stage.sequence == 5:               
                vals.update(fecha_hora_examen_medico=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_estudio_seguridad
                calc = calc.seconds/3600
                vals.update(tiempo_estudio_seguridad=calc)

            if id_stage.sequence == 6:               
                vals.update(fecha_hora_examen_referencias=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_examen_medico
                calc = calc.seconds/3600
                vals.update(tiempo_examen_medico=calc)

            if id_stage.sequence == 7:               
                vals.update(fecha_hora_examen_contratacion=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_examen_referencias
                calc = calc.seconds/3600
                vals.update(tiempo_referencias=calc)

            if id_stage.sequence == 8:               
                vals.update(fecha_hora_compensacion_beneficios=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_examen_contratacion
                calc = calc.seconds/3600
                vals.update(tiempo_contratacion=calc)

            if id_stage.sequence == 9:               
                vals.update(fecha_hora_espera_por_cliente=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_compensacion_beneficios
                calc = calc.seconds/3600
                vals.update(tiempo_compensacion_beneficios=calc)

            if id_stage.sequence == 10:               
                vals.update(fecha_hora_espera_por_candidato=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_espera_por_cliente
                calc = calc.seconds/3600
                vals.update(tiempo_espera_por_cliente=calc)

            if id_stage.sequence == 11:               
                vals.update(fecha_hora_espera_por_tercero=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_espera_por_candidato
                calc = calc.seconds/3600
                vals.update(tiempo_espera_por_candidato=calc) 

            if id_stage.sequence == 12:               
                vals.update(fecha_hora_reclutamiento=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_espera_por_tercero
                calc2 = fields.Datetime.now() - self.fecha_hora_pre_seleccionado
                calc = calc.seconds/3600
                calc2 = calc2.seconds/3600
                vals.update(tiempo_espera_por_tercero=calc)
                vals.update(tiempo_total=calc2)                                         
                               
           
          
        return super(Todoo, self).write(vals)
        for record in self:
            if 'fotocopia_cedula' in vals and vals['fotocopia_cedula_filename']:
                dic = {
                    'name': vals['fotocopia_cedula_filename'],
                    'datas': vals['fotocopia_cedula'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'cer_estudio' in vals and vals['cer_estudio_emp_filename']:
                dic = {
                    'name': vals['cer_estudio_emp_filename'],
                    'datas': vals['cer_estudio'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'certi_laborales' in vals and vals['certi_laborales_emp_filename']:
                dic = {
                    'name': vals['certi_laborales_emp_filename'],
                    'datas': vals['certi_laborales'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)  

            if 'hv' in vals and vals['hv_filename']:
                dic = {
                    'name': vals['hv_filename'],
                    'datas': vals['hv'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'aceptacion_condiciones' in vals and vals['aceptacion_condiciones_emp_filename']:
                dic = {
                    'name': vals['aceptacion_condiciones_emp_filename'],
                    'datas': vals['aceptacion_condiciones'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'libreta_militar' in vals and vals['libreta_militar_emp_filename']:
                dic = {
                    'name': vals['libreta_militar_emp_filename'],
                    'datas': vals['libreta_militar'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'refrecnias_personales' in vals and vals['refrecnias_personales_emp_filename']:
                dic = {
                    'name': vals['refrecnias_personales_emp_filename'],
                    'datas': vals['refrecnias_personales'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'verificacion_referencias' in vals and vals['verificacion_referencias_emp_filename']:
                dic = {
                    'name': vals['verificacion_referencias_emp_filename'],
                    'datas': vals['verificacion_referencias'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'certificado_cuenta_bancaria' in vals and vals['certificado_cuenta_bancaria_emp_filename']:
                dic = {
                    'name': vals['certificado_cuenta_bancaria_emp_filename'],
                    'datas': vals['certificado_cuenta_bancaria'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic) 

            if 'antecedentes_disciplinarios' in vals and vals['antecedentes_disciplinarios_emp_filename']:
                dic = {
                    'name': vals['antecedentes_disciplinarios_emp_filename'],
                    'datas': vals['antecedentes_disciplinarios'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'validacion_antecedentes' in vals and vals['validacion_antecedentes_emp_filename']:
                dic = {
                    'name': vals['validacion_antecedentes_emp_filename'],
                    'datas': vals['validacion_antecedentes'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'entrevista_jefe_inmediato' in vals and vals['entrevista_jefe_inmediato_emp_filename']:
                dic = {
                    'name': vals['entrevista_jefe_inmediato_emp_filename'],
                    'datas': vals['entrevista_jefe_inmediato'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'fotografias' in vals and vals['fotografias_emp_filename']:
                dic = {
                    'name': vals['fotografias_emp_filename'],
                    'datas': vals['fotografias'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'validacion_sarlaft' in vals and vals['validacion_sarlaft_emp_filename']:
                dic = {
                    'name': vals['validacion_sarlaft_emp_filename'],
                    'datas': vals['validacion_sarlaft'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

           

            if 'estudio_seguridad' in vals and vals['validacion_sarlaft_emp_filename']:
                dic = {
                    'name': vals['estudio_seguridad_emp_filename'],
                    'datas': vals['estudio_seguridad'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'examendes_medicos' in vals and vals['examendes_medicos_emp_filename']:
                dic = {
                    'name': vals['examendes_medicos_emp_filename'],
                    'datas': vals['examendes_medicos'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'poliza'  in vals and vals['poliza_emp_filename']:
                dic = {
                    'name': vals['poliza_emp_filename'],
                    'datas': vals['poliza'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'autorizacion_uso_correo'  in vals and vals['autorizacion_uso_correo_emp_filename']:
                dic = {
                    'name': vals['autorizacion_uso_correo_emp_filename'],
                    'datas': vals['autorizacion_uso_correo'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic) 

            if 'licencia_conducir' in vals and vals['licencia_conducir_emp_filename']:
                dic = {
                    'name': vals['licencia_conducir_emp_filename'],
                    'datas': vals['licencia_conducir'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'carta_propiedad_vehiculo' in vals and vals['carta_propiedad_vehiculo_emp_filename']:
                dic = {
                    'name': vals['carta_propiedad_vehiculo_emp_filename'],
                    'datas': vals['carta_propiedad_vehiculo'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'cer_runt' in vals and vals['cer_runt_emp_filename']:
                dic = {
                    'name': vals['cer_runt_emp_filename'],
                    'datas': vals['cer_runt'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)  

          

            if 'revision_tecnico_mecanica' in vals and vals['revision_tecnico_mecanica_emp_filename']:
                dic = {
                    'name': vals['revision_tecnico_mecanica_emp_filename'],
                    'datas': vals['revision_tecnico_mecanica'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic) 

            if 'certificacion_sena' in vals and vals['certificacion_senafile_name']:
                dic = {
                    'name': vals['certificacion_senafile_name'],
                    'datas': vals['certificacion_sena'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic) 

            if 'centro_induccion' in vals and vals['centro_induccion_emp_filename']:
                dic = {
                    'name': vals['centro_induccion_emp_filename'],
                    'datas': vals['centro_induccion'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)
            
            if 'centro_induccion' in vals and vals['seguro_obligatorio_vigente_filename']:
                dic = {
                    'name': vals['seguro_obligatorio_vigente_filename'],
                    'datas': vals['seguro_obligatorio_vigente'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

           

            if 'TGS_Solidarios' in vals and vals['TGS_Solidarios_filename']:
                dic = {
                    'name': vals['TGS_Solidarios_filename'],
                    'datas': vals['TGS_Solidarios'],
                    'res_model': 'hr.applicant', 
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)    
        

        return res
