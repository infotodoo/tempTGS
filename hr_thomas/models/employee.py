# -*- coding: utf-8 -*-
# BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields, models, api, exceptions
import re
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta

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
    _inherit = 'hr.employee'

    #principal
    company_id= fields.Many2one('res.company',tracking=True)
    first_name= fields.Char('Primer Nombre',required=False,  tracking=True)
    second_name = fields.Char('Segundo Nombre',tracking=True)
    third_name = fields.Char('Primer Apellido',required=False,tracking=True)
    fourth_name = fields.Char('Segundo Apellido',tracking=True)
    requisition_id = fields.Many2one('requisiciones','Requisiciones',tracking=True)
    aplicante=fields.Char('Aplicante')
    candidate = fields.Char('Candidado',related='requisition_id.solicitante.name',tracking=True)
    ciudad_requi = fields.Many2one('res.city',string="Ciudad",tracking=True)
    sede_requi = fields.Char(string="Sede",tracking=True)
    area_requi = fields.Char(string="Area",tracking=True)
    tratamiento_emp = fields.Selection([('SR.','SR.'),('SRA.','SRA.')],'Tratamiento', tracking=True)
    unidad_organizativa_requi = fields.Many2one('unidades', tracking=True)

    centro_costo_empleado = fields.Many2one('centro', string="Centro de Costo", tracking=True)


    centro_de_costo_requisicion = fields.Many2one('centro',string="Número del Centro de Costo",tracking=True)

    nombre_centro_costo_requi = fields.Char(related="centro_de_costo_requisicion.centro_costo",string="Nombre del Centro de Costo",tracking=True)
    porcentaje_nivel_de_riesgo = fields.Selection(related="requisition_id.nivel_riesgo", tracking=True)
    nivel_de_riesgo = fields.Selection(related="requisition_id.nivel_riesgo_arl", tracking=True)
    manejo_vacaciones_req = fields.Selection([('L-V', 'L-V'),('L-S', 'L-S')],string="Manejo de Vacaciones",tracking=True)
    manejo_incapacidades_req = fields.Selection([('PAGAR AL 66.66%', 'PAGAR AL 66.66%'),('PAGAR AL 100%', 'PAGAR AL 100%')],string="Manejo de Incapacidades",tracking=True)
    pacto_convencion = fields.Selection([('PACTO COLECTIVO', 'PACTO COLECTIVO'),('CONVENCIÓN COLECTIVA DE TRABAJO', 'CONVENCIÓN COLECTIVA DE TRABAJO'),('NO APLICA','NO APLICA')],string="Pacto/Convención",tracking=True)
    #Private Information
    applicant_id = fields.Many2one('hr.applicant',tracking=True)
    formacion_line_emp = fields.One2many('formacion','employee_id','Formación')

    #employee_id One2many
    idioma_line_emp = fields.One2many('lenguage','employee_id','Idiomas')
    mascotas_line_emp = fields.One2many('mascotas','employee_id', 'Mascotas')
    hijos_line_empleado = fields.One2many('hijo','employee_id', 'Hijos')
    activos_line = fields.One2many('activos', 'employee_id', 'Activos')
    #1 grupo
    confirmation_date_of_birth = fields.Date('Confirmacion Fecha de Nacimiento',tracking=True)
    state_residence = fields.Many2one('res.country.state','Departamento',tracking=True)
    city_residence = fields.Many2one('res.city', 'Ciudad de Residencia',tracking=True)
    neighbordhood_residence = fields.Char('Barrio de residencia',tracking=True)
    identification_type = fields.Selection([('N.U.I.P', 'N.U.I.P'),('Cédula de Ciudadania', 'CÉDULA DE CIUDADANIA'),('Cédula de Extranjería', 'CÉDULA DE EXTRANJERÍA'), ('Tarjeta de Identidad', 'TARJETA DE IDENTIDAD'),('Pasaporte','PASAPORTE'),('NIT','NIT'),('Registro Civil','REGISTRO CIVIL'),('Visa','VISA'),('Antecedentes Disciplinarios','PERMISO ESPECIAL DE RESIDENCIA'),('RUT','RUT')],'Tipo de Identificación',tracking=True)
    lugar_expedicion_id_emp=fields.Many2one('res.city','Lugar de Expedición',tracking=True)
    country_of_birth =  fields.Many2one('res.country','País de Nacimiento')
    identifiction_id = fields.Char(string="Identificación")
    # identification_number = fields.Char('Numero de identificación',tracking=True)
    #2 grupo
    pants_size = fields.Selection([('XS', 'XS'),('S', 'S'),('M', 'M'), ('L', 'L'),('XL','XL'),('XXL','XXL')],'Talla Pantalon',tracking=True)
    shirt_size = fields.Selection([('XS', 'XS'),('S', 'S'),('M', 'M'), ('L', 'L'),('XL','XL'),('XXL','XXL')],'Talla Camisa',tracking=True)
    coat_size = fields.Selection([('XS', 'XS'),('S', 'S'),('M', 'M'), ('L', 'L'),('XL','XL'),('XXL','XXL')],'Talla Saco',tracking=True)
    shoes_size = fields.Selection(tallazapatos,'Talla Zapatos',tracking=True)
    #3 grupo
    confirmation_email = fields.Char('Confirmación del correo',tracking=True)
    language = fields.Many2one('res.lang','Idioma Nativo',tracking=True)
    blood_group = fields.Selection(grupo_san,'Grupo Sanguíneo',tracking=True)
    genero = fields.Selection([('Masculino', 'MASCULINO'),('Femenino', 'FEMENINO')])
    rent = fields.Selection([('SI', 'SI'),('NO', 'NO')],'Declara usted Renta?',tracking=True)
    #4 grupo dirección de residencia
    main_road = fields.Many2one('direccion','Vía principal',tracking=True)
    main_road_name = fields.Char('Nombre Vía Principal',tracking=True)
    road_generator = fields.Char('Via Generadora',tracking=True)
    land = fields.Char('Predio',tracking=True)
    complement = fields.Char('Complemento',tracking=True)
    complete_direction = fields.Char('Dirección Completa',tracking=True)
    #información de vivienda
    property_type = fields.Selection(tipo_vivienda,'Tipo de Vivienda',tracking=True)
    property_type2 = fields.Char('¿Cuál tipo de vivienda?',tracking=True)
    property_characteristic = fields.Selection([('CASA', 'CASA'),('APARTAMENTO', 'APARTAMENTO'),('HABITACIÓN', 'HABITACIÓN'),('OTRO','OTRO')],'Caracteristicas de la Vivienda',tracking=True)
    property_characteristic2 = fields.Char('¿Cúal Caracteristica de Vivienda?',tracking=True)
    property_zone = fields.Selection([('RURAL', 'RURAL'),('URBANA', 'URBANA'),('SUB', 'SUB URBANA')],'Zona de la Vivienda',tracking=True)
    energy_service = fields.Selection([('Si', 'SI'),('No', 'NO')],'Cuenta con servicio de Energia eléctrica?',tracking=True)
    sewerage_service = fields.Selection([('Si', 'SI'),('No', 'NO')],'Cuenta con servicio de alcantarillado?',tracking=True)
    aqueduct_service = fields.Selection([('Si', 'SI'),('No', 'NO')],'Cuenta con servicio de acueducto?',tracking=True)
    #5 grupo
    gas_service = fields.Selection([('SI', 'SI'),('NO', 'NO')],'Cuenta con servicio de Gas Natural?',tracking=True)
    trash_service = fields.Selection([('Si', 'SI'),('No', 'NO')],'Cuenta con servicio de Recolección de Basura?',tracking=True)
    etnic_group = fields.Selection([('Mestizo', 'MESTIZO'),('Blanco', 'BLANCO'),('Afrocolombiano', 'AFROCOLOMBIANO'),('Indigena','INDIGENA'),('Gitano','GITANO')],'Grupo Étnico',tracking=True)
    socioeconomical_state = fields.Selection([('1', 'ESTRATO 1'),('2', 'ESTRATO 2'),('3', 'ESTRATO 3'),('4','ESTRATO 4'),('5','ESTRATO 5'),('6','ESTRATO 6')],'Estrato Socioeconómico',tracking=True)

    #6 grupo persona en caso de emergencia//
    full_name = fields.Char('Nombre Completo',tracking=True)
    Phone = fields.Char('Telefono',tracking=True)

    relationship = fields.Selection([('ABUELO (A)', 'ABUELO (A)'),('AMIGO (A)', 'AMIGO (A)'),('ESPOSO (A)', 'ESPOSO (A)'),('HERMANO (A)','HERMANO (A)'),('PADRE','PADRE'),('MADRE','MADRE'),('SORBINO (A)','SOBRINO (A)'),('TIO (A)','TIO (A)'),('HIJO (A)','HIJO (A)'),('OTRO','OTRO')],tracking=True)


    what_relationship = fields.Char('Cuál parentesco?',tracking=True)
    #dirección
    main_road_parent = fields.Many2one('direccion','Vía Principal',tracking=True)
    main_road_name_parent = fields.Char('Nombre Vía Principal',tracking=True)
    road_generator_parent = fields.Char('Via Generadora',tracking=True)
    land_parent = fields.Char('Predio',tracking=True)
    complement_parent = fields.Char('Complemento',tracking=True)
    complete_direction_parent = fields.Char('Dirección Completa del Conyugue',tracking=True)
    #7 grupo
    depend_person = fields.Selection([('Si', 'SI'),('No', 'NO')],'Existen personas que dependan económicamente de usted?',tracking=True)
    head_family = fields.Selection([('Si', 'SI'),('No', 'NO')],'Es cabeza de familia?',tracking=True)
    number_family = fields.Integer('Número de personas del núcleo familiar',tracking=True)
    number_person_discapacited = fields.Integer('Número de personas en estado de discapacidad',tracking=True)

    #9 grupo
    drive_license = fields.Selection([('SI', 'SI'),('NO', 'NO')],'Tiene Licencia para conducir?',tracking=True)
    license_type = fields.Selection([('A1', 'A1'),('A2', 'A2'),('B1', 'B1'),('B2','B2'),('B3','B3'),('C1', 'C1'),('C2','C2'),('C3','C3')],'Tipo de Licencia',tracking=True)
    main_transport = fields.Selection([('BICICLETA', 'BICICLETA'),('CAMINANDO', 'CAMINANDO'),('CARRO', 'CARRO'),('MOTO','MOTO'),('PATINETA','PATINETA'),('TRANSPORTE COMPARTIDO', 'TRANSPORTE COMPARTIDO'),('TRANSPORTE PRIVADO(TAXI, UBER, BEAT)','TRANSPORTE PRIVADO(TAXI, UBER, BEAT)')],'Medio de Transporte Principal',tracking=True)
    second_transport = fields.Selection([('BICICLETA', 'BICICLETA'),('CAMINANDO', 'CAMINANDO'),('CARRO', 'CARRO'),('MOTO','MOTO'),('PATINETA','PATINETA'),('TRANSPORTE COMPARTIDO', 'TRANSPORTE COMPARTIDO'),('TRANSPORTE PRIVADO(TAXI, UBER, BEAT)','TRANSPORTE PRIVADO(TAXI, UBER, BEAT)')],'Medio de Transporte Secundario	',tracking=True)
    hour_to_arrive = fields.Selection([('MENOS DE 30 MINUTOS', 'MENOS DE 30 MINUTOS'),('30 MINUTOS', '30 MINUTOS'),('1 HORA', '1 HORA'),('1.5 HORAS','1.5 HORAS'),('2 HORAS','2 HORAS'),('2.5 HORAS', '2.5 HORAS'),('3 HORAS','3 HORAS'),('3.5 HORAS','3.5 HORAS'),('4 HORAS','4 HORAS'),('4.5 HORAS','4.5 HORAS')],'Horas para llegar al trabajo',tracking=True)
    civil_state = fields.Selection([('SOLTERO/A', 'SOLTERO/A'),('CASADO/A', 'CASADO/A'),('DIVORCIADO/A', 'DIVORCIADO/A'),('UNIÓN LIBRE','UNIÓN LIBRE'),('VIUDO/A','VIUDO/A')],'Estado Civil',tracking=True)
    #10 grupo
    first_last_name_parent = fields.Char('Primer Apellido del Conyugue',tracking=True)
    second_last_name_parent = fields.Char('Segundo Apellido del Conyugue',tracking=True)
    first_name_parent = fields.Char('Primer Nombre del Conyugue',tracking=True)
    second_name_parent = fields.Char('Segundo Nombre del Conyugue',tracking=True)
    gender_parent_emp = fields.Selection([('Masculino', 'MASCULINO'),('Femenino', 'FEMENINO')],'Genero Cónyuge')
    escolaridad_conyugue_emp=fields.Selection([('Primaria', 'PRIMARIA'),('Bachiller', 'BACHILLER'),('Curso o Seminario', 'CURSO O SEMINARIO'),('Técnica','TÉCNICA'),('Tecnológica','TECNOLÓGICA'),('Universitaria', 'UNIVERSITARIA'),('Especialización', 'ESPECIALIZACIÓN'),('Maestría','MAESTRÍA'),('Doctorado','DOCTORADO')],string="Escolaridad del Conyugue",tracking=True)
    born_place_parent_emp = fields.Many2one('res.city','Lugar de Nacimiento Cónyuge')
    country_born_parent_emp = fields.Many2one('res.country','País de Nacimiento Cónyuge')
    date_birth_parent_emp = fields.Date('Fecha de Nacimiento Cónyuge')
    #escolaridad del solicitante/empleado
    escolaridad_solicitante_emp=fields.Selection([('Primaria', 'PRIMARIA'),('Bachiller', 'BACHILLER'),('Curso o Seminario', 'CURSO O SEMINARIO'),('Técnica','TÉCNICA'),('Tecnológica','TECNOLÓGICA'),('Universitaria', 'UNIVERSITARIA'),('Especialización', 'ESPECIALIZACIÓN'),('Maestría','MAESTRÍA'),('Doctorado','DOCTORADO')],'Escolaridad del Solicitante',tracking=True)
    estudia_actualmente_solicitante_emp=fields.Selection([('Si', 'SI'),('No', 'NO')],'Estudia Actualmente',tracking=True)
    #11 grupo
    # childrens = fields.Many2many('hijo', tracking=True)
    hijos_line_emp = fields.One2many('hijo', 'employee_id', 'Hijos')
    mascotas_line_emp = fields.One2many('mascotas', 'employee_id', 'Mascotas')
    #12 grupo experiencia laboral--
    experience_business = fields.Many2many('hr.resume.line')
    resume_line_ids = fields.One2many('hr.resume.line', 'employee_id', string="Resumé lines")
    employee_skill_ids = fields.One2many('hr.employee.skill', 'employee_id', string="Skills")
    #escolaridad
    escolaridad_emp=fields.Many2many('escolaridad',tracking=True)
    #13 grupo idioma
    lenguage_emp = fields.Many2many('lenguage',string="Idioma",tracking=True)
    #informacion especifica
    miedos_emp=fields.Many2many('fobias')
    nombre_hobby_emp=fields.Many2many('hob',string="Hobbies")
    tiene_enfermedad_emp=fields.Char(string="Tiene alguna enfermedad Importante")
    toma_medicamneto_emp=fields.Char(string="Toma algun Medicamento")
    alergia_emp=fields.Many2many('alergia', string="Tiene alguna alergía?")
    #campos: entidades del sistema de seguridad
    eps_emp=fields.Many2one('res.partner','EPS',tracking=True)
    afp_emp=fields.Many2one('res.partner','AFP',tracking=True)
    afc_emp=fields.Many2one('res.partner','AFC',tracking=True)
    arl_emp=fields.Many2one('res.partner','ARL',tracking=True)
    nivel_riesgo=fields.Selection([('1 RIESGO I', '1 RIESGO I'),('2 RIESGO II', '2 RIESGO II'),('3 RIESGO III','3 RIESGO III'),('4 RIESGO IV','4 RIESGO IV'),('5 RIESGO V','5 RIESGO V')],tracking=True)
    caja_compensacion_emp=fields.Many2one('res.partner','Caja de Compensación')
    clase_beneficio=fields.Many2one('beneficio',string="Clase Beneficio",tracking=True)
    ccnomina_emp=fields.Many2one('ccnomina',string="ccnómina",tracking=True)
    clave_receptor_emp=fields.Many2one('clave',string="Clave Receptor",tracking=True)
    importe_clase_beneficio_emp=fields.Integer(string="Importe Clase Beneficio",tracking=True)
    plan_exequial=fields.Selection([('Coopserfun', 'Coopserfun'),('Coorserpark', 'Coorserpark'),('La Ascención','La Ascención'),('Los Olivos','Los Olivos'),('Recordar S.A.','Recordar S.A.')])
    importe_plan_excequial_emp=fields.Integer(string="Importe Plan Exequial")
    tipo_cotizante_emp=fields.Many2one('tipo.cotizante',string="Tipo de Cotizante",tracking=True)
    subtipo_cotizante_emp=fields.Many2one('subtipo.cotizante',string="Subtipo de Cotizante",tracking=True)
    motivo_perdida_emp=fields.Selection([('1-VACANTE', '1-VACANTE'),('2-Aumento de la Planta', '2-AUMENTO DE LA PLANTA'),('3-Creación del Cargo', '3-CREACIÓN DEL CARGO'), ('4-Reemplazo', '4-REEMPLAZO')],default='1-VACANTE',string="Motivo de Pérdida",tracking=True)
    clase_salario_emp=fields.Many2one('clase.salario',string="Clase de Salario",tracking=True)
    posicion_emp=fields.Char(string="Posición")
    area_nivel_cargo_emp=fields.Selection([('1-GRADO I', '1-GRADO I'),('2-GRADO II', '2-GRADO II'),('3-GRADO III', '3-GRADO III'), ('4-GRADO IV', '4-GRADO IV'),('ZZ-PENSIONADO','ZZ-PENSIONADO')],string="Area Nivel Cargo",tracking=True)
    grupo_sueldos_emp=fields.Selection([('13', '13'),('14', '14')],string="Grupo de Sueldos",tracking=True)
    grado_ocupacion_emp=fields.Selection([('13', '13'),('14', '14')],string="Grado de Ocupación",tracking=True)
    hora_trabajo_periodo_emp=fields.Selection([('120', '120'),('240', '240')],string="Horas de Trabajo Periodo",tracking=True)
    procedimiento_emp=fields.Integer(default=1, string="Procedimiento",tracking=True)
    division_emp=fields.Many2one('division', string="División",tracking=True)
    grupo_seleccion_emp=fields.Selection([('1 ACTIVOS', '1 ACTIVOS'),('2 PENSIONADOS', '2 PENSIONADOS'),('3 JUBILADO ANTICIPADO','3 JUBILADO ANTICIPADO'),('4 APRENDICES','4 APRENDICES'),('5 RETIRADOS','5 RETIRADOS'),('7 TEMPORALES','7 TEMPORALES'),('9 EXTERNOS','9 EXTERNOS')], string="Grupo de Selección",tracking=True)
    area_personal_emp=fields.Many2one('area.personal', string="Area de Personal",tracking=True)
    relacion_laboral_emp=fields.Selection([('01 LEY 50', '01 LEY 50'),('02 RÉG.ANTERIOR', '02 RÉG.ANTERIOR'),('03 INTEGRAL','03 INTEGRAL'),('04 APRENDIZAJE','04 APRENDIZAJE'),('05 PENSIONADO','05 PENSIONADO'),('06 EXTERNO/TEMPOR','06 EXTERNO/TEMPOR')],string="Relación Laboral ",tracking=True)
    evaluacion_tiempo_pht_emp=fields.Selection([('1- EVALUACIÓN DE TIEMPOS, REAL', '1- EVALUACIÓN DE TIEMPOS, REAL'),('2- EVALUACIÓN DE TIEMPOS, CDP', '2- EVALUACIÓN DE TIEMPOS, CDP'),('7- EVALUACIÓN DE TIEMPO SIN INTEGRACIÓN CÁLCULO DE NÓMINA','7- EVALUACION DE TIEMPO SIN INTEGRACIÓN CÁLCULO DE NÓMINA'),('8- SERVICIOS EXTERNOS','8- SERVICIOS EXTERNOS'),('9- EVALUACIÓN DE TIEMPOS TEÓRICOS','9- EVALUACIÓN DE TIEMPOS TEÓRICOS'),('0- SIN EVALUACIÓN DE TIEMPOS','0- SIN EVALUACIÓN DE TIEMPOS')],string="Evaluación de Tiempos PHT",tracking=True)
    turno_trabajo_emp=fields.Selection([('NORM', 'NORM'),('NORMLS', 'NORMLS')], string="Turno de Trabajo",tracking=True)
    evaluacion_de_tiempos=fields.Many2one('evaluacion', string="Evaluación")
    #foto14 grupo documentos_certificados
    fotocopia_cedula = fields.Binary(string="Fotocopia de la Cédula",tracking=True)
    fotocopia_cedula_filename = fields.Char("Adjunto Fotocopia de la Cédula")
    cer_estudio_emp = fields.Binary(string="Certificado de Estudio",tracking=True)
    cer_estudio_emp_filename = fields.Char("Adjunto Certificado de Estudio")
    certi_laborales_emp= fields.Binary(string="Certificaciones Laborales",tracking=True)
    certi_laborales_emp_filename = fields.Char("Adjunto Certificaciones Laborales")
    hv_emp = fields.Binary(string="Hoja de Vida",tracking=True)
    hv_emp_filename = fields.Char("Adjunto Hoja de Vida")
    #15 grupo documentos_personales
    aceptacion_condiciones_emp = fields.Binary(string="Aceptación de Condiciones",tracking=True)
    aceptacion_condiciones_emp_filename = fields.Char("Adjunto Aceptación de Condiciones")
    libreta_militar_emp = fields.Binary(string="Libreta Militar",tracking=True)
    libreta_militar_emp_filename = fields.Char("Adjunto Libreta Militar")
    refrecnias_personales_emp = fields.Binary(string="Referencias Personales",tracking=True)
    refrecnias_personales_emp_filename = fields.Char("Adjunto Referencias Personales")
    verificacion_referencias_emp = fields.Binary(string="Verificación de Referencias",tracking=True)
    verificacion_referencias_emp_filename = fields.Char("Adjunto Verificación de Referencias")
    certificado_cuenta_bancaria_emp = fields.Binary(string="Certificado de Cuenta Bancaría",tracking=True)
    certificado_cuenta_bancaria_emp_filename = fields.Char("Adjunto Certificado de Cuenta Bancaría")
    antecedentes_disciplinarios_emp = fields.Binary(string="Antecedentes Disciplinarios",tracking=True)
    antecedentes_disciplinarios_emp_filename = fields.Char("Adjunto Antecedentes Disciplinarios")
    validacion_antecedentes_emp = fields.Binary(string="Validación de Antecedentes",tracking=True)
    validacion_antecedentes_emp_filename = fields.Char("Adjunto Validación de Antecedentes")
    #informacion de datos personales
    telefono_del_empleado=fields.Char('Télefono')
    celular_del_empleado=fields.Char('Celular')
    correo_privado_del_empleado=fields.Char('Correo Privado')
    #16 grupo
    entrevista_jefe_inmediato_emp = fields.Binary(string="Entrevista Jefe Inmediato",tracking=True)
    entrevista_jefe_inmediato_emp_filename = fields.Char("Adjunto Entrevista Jefe Inmediato")
    fotografias_emp = fields.Binary(string="Fotografías",tracking=True)
    fotografias_emp_filename = fields.Char("Adjunto Fotografías")
    validacion_sarlaft_emp = fields.Binary(string="Validación Sarlaft",tracking=True)
    validacion_sarlaft_emp_filename = fields.Char("Adjunto Validación Sarlaft")
    TGS_Solidarios=fields.Binary(string="TGS Solidarios",tracking=True)
    TGS_Solidarios_filename = fields.Char("Adjunto TGS Solidarios")
    estudio_seguridad_emp = fields.Binary(string="Estudio de Seguridad",tracking=True)
    estudio_seguridad_emp_filename = fields.Char("Adjunto Estudio de Seguridad")
    examendes_medicos_emp = fields.Binary(string="Examenes Medicos",tracking=True)
    examendes_medicos_emp_filename = fields.Char("Adjunto Examenes Medicos")
    poliza_emp = fields.Binary(string="Poliza",tracking=True)
    poliza_emp_filename = fields.Char("Adjunto de Poliza")
    autorizacion_uso_correo_emp = fields.Binary(string="Autorización del Uso de Correo",tracking=True)
    autorizacion_uso_correo_emp_filename = fields.Char("Adjunto Autorización del Uso de Correo")
    licencia_conducir_emp = fields.Binary(string="Licencia de Conducir",tracking=True)
    licencia_conducir_emp_filename = fields.Char("Adjunto Licencia de Conducir")
    carta_propiedad_vehiculo_emp = fields.Binary(string="Carta de Propiedad del Vehiculo",tracking=True)
    carta_propiedad_vehiculo_emp_filename = fields.Char("Adjunto Carta de Propiedad del Vehiculo")
    cer_runt_emp = fields.Binary(string="Certificado RUNT",tracking=True)
    cer_runt_emp_filename = fields.Char("Adjunto Certificado RUNT")
    seguro_obligatorio_vigente = fields.Binary(string="Seguro Obligatorio Vigente",tracking=True)
    seguro_obligatorio_vigente_filename = fields.Char("Adjunto Seguro Obligatorio Vigente")
    revision_tecnico_mecanica_emp = fields.Binary(string="Revisión Técnico Mecanica",tracking=True)
    revision_tecnico_mecanica_emp_filename = fields.Char("Adjunto Revisión Técnico Mecanica")
    centro_induccion_emp = fields.Binary(string="Centro de Inducción",tracking=True)
    centro_induccion_emp_filename = fields.Char("Adjunto Centro de Inducción")
    certificacion_sena_emp = fields.Binary(string="Certificación Sena",tracking=True)
    documentos_generales = fields.Binary(string="Documentos Generales")
    documentos_generales_filename = fields.Char("Adjunto Documentos Generales")
    rut  = fields.Binary('RUT', tracking=True)
    file_name = fields.Char("Adjunto Certificación Sena")
    #aprobaciones
    aprobador_ninel2 = fields.Boolean('Aprobador Nivel 2')
    aprobador_ninel3 = fields.Boolean('Aprobador Nivel 3')
    #fecha de retiro
    fecha_retiro = fields.Date(string="Fecha de Retiro", tracking=True)
    check = fields.Boolean(string="Retiro")
    check_tag_ids = fields.Boolean(compute='_compute_check_tag_ids', invisible=True)

    @api.onchange('requisition_id')
    def action_req(self):
      for record in self:
        if record.requisition_id:
            record.area_requi = record.requisition_id.area
            record.sede_requi = record.requisition_id.sede
            record.ciudad_requi = record.requisition_id.res_city
            record.unidad_organizativa_requi = record.requisition_id.un_organizativa
            record.centro_de_costo_requisicion = record.requisition_id.centro_de_costo
            record.parent_id = record.requisition_id.jefe_inmediato
            record.job_id = record.requisition_id.cargo_solicitado
            record.pacto_convencion = record.requisition_id.pacto_con
            record.manejo_incapacidades_req = record.requisition_id.manejo_incapacidades
            record.manejo_vacaciones_req = record.requisition_id.manejo_vacaciones
            record.nivel_riesgo = record.requisition_id.nivel_riesgo_arl

    # funcion para colocar nombres en mayusculas
    @api.onchange('name', 'first_name', 'second_name', 'third_name', 'fourth_name')
    def _compute_maj_employee(self):
        self.name = self.name.upper() if self.name else False
        self.first_name = self.first_name.upper() if self.first_name else False
        self.second_name = self.second_name.upper() if self.second_name else False
        self.third_name = self.third_name.upper() if self.third_name else False
        self.fourth_name = self.fourth_name.upper() if self.fourth_name else False

    @api.depends('category_ids')
    def _compute_check_tag_ids(self):
        for record in self:
            record.check_tag_ids = True if record.category_ids and record.category_ids[0].name == 'APRENDIZ' else False    

    # concatenar nombre completo del empleado

    @api.onchange('tratamiento_emp', 'name', 'first_name', 'second_name', 'third_name', 'fourth_name')
    def _onchange_nombre_completo(self):
        self.name = "%s %s %s %s  %s" % (
            self.tratamiento_emp if self.tratamiento_emp else "",
            self.first_name if self.first_name else "",
            self.second_name if self.second_name else "",
            self.third_name if self.third_name else "",
            self.fourth_name if self.fourth_name else "")

    # validar fecha de nacimiento
    @api.constrains('birthday', 'confirmation_date_of_birth')
    def _check_somethi(self):
        for record in self:
            if record.birthday != record.confirmation_date_of_birth:
                raise ValidationError(
                    "Verificar la confirmación de su fecha de nacimiento! : %s" % record.confirmation_date_of_birth)

    @api.onchange('main_road_name','road_generator','land','complement')
    def _compute_address_thomas(self):        
        self.main_road_name = self.main_road_name.upper() if self.main_road_name else False
        self.road_generator = self.road_generator.upper() if self.road_generator else False
        self.land = self.land.upper() if self.land else False
        self.complement = self.complement.upper() if self.complement else False

    @api.onchange('main_road_name_parent','road_generator_parent','land_parent','complement_parent')
    def _compute_address_thomas_parent(self):        
        self.main_road_name_parent = self.main_road_name_parent.upper() if self.main_road_name_parent else False
        self.road_generator_parent = self.road_generator_parent.upper() if self.road_generator_parent else False
        self.land_parent = self.land_parent.upper() if self.land_parent else False
        self.complement_parent = self.complement_parent.upper() if self.complement_parent else False    

    # concatenación Dirección tipo DIAN
    @api.onchange('main_road', 'main_road_name', 'road_generator', 'land', 'complement')
    def _onchange_direccion_dian(self):
        self.complete_direction = "%s %s %s %s %s " % (
            self.main_road.identificador if self.main_road else "",
            self.main_road_name if self.main_road_name else "",
            self.road_generator if self.road_generator else "",
            self.land if self.land else "",
            self.complement if self.complement else "")

    # concatenación Dirección tipo DIAN persona en caso de emergencia
    @api.onchange('main_road_parent', 'main_road_name_parent', 'road_generator_parent', 'land_parent',
                  'complement_parent')
    def _onchange_direccion_dian_parent(self):
        self.complete_direction_parent = "%s %s %s %s %s " % (
            self.main_road_parent.identificador if self.main_road_parent else "",
            self.main_road_name_parent if self.main_road_name_parent else "",
            self.road_generator_parent if self.road_generator_parent else "",
            self.land_parent if self.land_parent else "",
            self.complement_parent if self.complement_parent else "")

    @api.model
    def create(self, vals):
        res = super(Todoo, self).create(vals)
        if 'fotocopia_cedula' in vals and vals['fotocopia_cedula_filename']:
            dic = {
                'name': vals['fotocopia_cedula_filename'],
                'datas': vals['fotocopia_cedula'],
                'res_model': 'hr.employee',
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        # if 'cer_estudio_emp' in vals and vals['cer_estudio_emp_filename2']:
        #     dic = {
        #         'name': vals['cer_estudio_emp_filename2'],
        #         'datas': vals['cer_estudio_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'certi_laborales_emp' in vals and vals['certi_laborales_emp_filename2']:
        #     dic = {
        #         'name': vals['certi_laborales_emp_filename2'],
        #         'datas': vals['certi_laborales_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'hv_emp' in vals and vals['hv_emp_filename2']:
        #     dic = {
        #         'name': vals['hv_emp_filename2'],
        #         'datas': vals['hv_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'aceptacion_condiciones_emp' in vals and vals['aceptacion_condiciones_emp_filename2']:
        #     dic = {
        #         'name': vals['aceptacion_condiciones_emp_filename2'],
        #         'datas': vals['aceptacion_condiciones_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'libreta_militar_emp' in vals and vals['libreta_militar_emp_filename2']:
        #     dic = {
        #         'name': vals['libreta_militar_emp_filename2'],
        #         'datas': vals['libreta_militar_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'refrecnias_personales_emp' in vals and vals['refrecnias_personales_emp_filename2']:
        #     dic = {
        #         'name':  vals['refrecnias_personales_emp_filename2'],
        #         'datas': vals['refrecnias_personales_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'verificacion_referencias_emp' in vals and vals['verificacion_referencias_emp_filename2']:
        #     dic = {
        #         'name': vals['verificacion_referencias_emp_filename2'],
        #         'datas': vals['verificacion_referencias_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'certificado_cuenta_bancaria_emp' in vals and vals['certificado_cuenta_bancaria_emp_filename2']:
        #     dic = {
        #         'name': vals['certificado_cuenta_bancaria_emp_filename2'],
        #         'datas': vals['certificado_cuenta_bancaria_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'antecedentes_disciplinarios_emp' in vals and vals['antecedentes_disciplinarios_emp_filename2']:
        #     dic = {
        #         'name': vals['antecedentes_disciplinarios_emp_filename2'],
        #         'datas': vals['antecedentes_disciplinarios_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'validacion_antecedentes_emp' in vals and vals['validacion_antecedentes_emp_filename2']:
        #     dic = {
        #         'name': vals['validacion_antecedentes_emp_filename2'],
        #         'datas': vals['validacion_antecedentes_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'entrevista_jefe_inmediato_emp' in vals and vals['entrevista_jefe_inmediato_emp_filename2']:
        #     dic = {
        #         'name': vals['entrevista_jefe_inmediato_emp_filename2'],
        #         'datas': vals['entrevista_jefe_inmediato_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'fotografias_emp' in vals and vals['fotografias_emp_filename2']:
        #     dic = {
        #         'name': vals['fotografias_emp_filename2'],
        #         'datas': vals['fotografias_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'validacion_sarlaft_emp' in vals and vals['validacion_sarlaft_emp_filename2']:
        #     dic = {
        #         'name': vals['validacion_sarlaft_emp_filename2'],
        #         'datas': vals['validacion_sarlaft_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)



        # if 'estudio_seguridad_emp' in vals and vals['estudio_seguridad_emp_filename2']:
        #     dic = {
        #         'name': vals['estudio_seguridad_emp_filename2'],
        #         'datas': vals['estudio_seguridad_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'examendes_medicos_emp'  in vals and vals['examendes_medicos_emp_filename2']:
        #     dic = {
        #         'name': vals['examendes_medicos_emp_filename2'],
        #         'datas': vals['examendes_medicos_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'poliza_emp' in vals and vals['poliza_emp_filename2']:
        #     dic = {
        #         'name': vals['poliza_emp_filename2'],
        #         'datas': vals['poliza_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'autorizacion_uso_correo_emp' in vals and vals['autorizacion_uso_correo_emp_filename2']:
        #     dic = {
        #         'name': vals['autorizacion_uso_correo_emp_filename2'],
        #         'datas': vals['autorizacion_uso_correo_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'licencia_conducir_emp' in vals and vals['licencia_conducir_emp_filename2']:
        #     dic = {
        #         'name': vals['licencia_conducir_emp_filename2'],
        #         'datas': vals['licencia_conducir_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        # if 'carta_propiedad_vehiculo_emp' in vals and vals['carta_propiedad_vehiculo_emp_filename2']:
        #     dic = {
        #         'name': vals['carta_propiedad_vehiculo_emp_filename2'],
        #         'datas': vals['carta_propiedad_vehiculo_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)


        # if 'cer_runt_emp' in vals and vals['cer_runt_emp_filename2']:
        #     dic = {
        #         'name': vals['cer_runt_emp_filename2'],
        #         'datas': vals['cer_runt_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)



        # if 'revision_tecnico_mecanica_emp' in vals and vals['revision_tecnico_mecanica_emp_filename2']:
        #     dic = {
        #         'name': vals['revision_tecnico_mecanica_emp_filename2'],
        #         'datas': vals['revision_tecnico_mecanica_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        if 'certificacion_sena_emp' in vals and vals['file_name']:
            dic = {
                'name': vals['file_name'],
                'datas': vals['certificacion_sena_emp'],
                'res_model': 'hr.employee',
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'documentos_generales' in vals and vals['documentos_generales_filename']:
            dic = {
                'name': vals['documentos_generales_filename'],
                'datas': vals['documentos_generales'],
                'res_model': 'hr.employee',
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        # if 'centro_induccion_emp' in vals and vals['centro_induccion_emp_filename2']:
        #     dic = {
        #         'name': vals['centro_induccion_emp_filename2'],
        #         'datas': vals['centro_induccion_emp'],
        #         'res_model': 'hr.employee',
        #         'res_id': res.id
        #     }
        #     self.env['ir.attachment'].create(dic)

        if 'seguro_obligatorio_vigente' in vals and vals['seguro_obligatorio_vigente_filename']:
            dic = {
                'name': vals['seguro_obligatorio_vigente_filename'],
                'datas': vals['seguro_obligatorio_vigente'],
                'res_model': 'hr.employee',
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        if 'TGS_Solidarios' in vals and vals['TGS_Solidarios_filename']:
            dic = {
                'name': vals['TGS_Solidarios_filename'],
                'datas': vals['TGS_Solidarios'],
                'res_model': 'hr.employee',
                'res_id': res.id
            }
            self.env['ir.attachment'].create(dic)

        return res

    def write(self, vals):
        res = super(Todoo, self).write(vals)
        for record in self:
            if 'fotocopia_cedula' in vals and vals['fotocopia_cedula_filename']:
                dic = {
                    'name': vals['fotocopia_cedula_filename'],
                    'datas': vals['fotocopia_cedula'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'cer_estudio_emp' in vals and vals['cer_estudio_emp_filename']:
                dic = {
                    'name': vals['cer_estudio_emp_filename'],
                    'datas': vals['cer_estudio_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'certi_laborales_emp' in vals and vals['certi_laborales_emp_filename']:
                dic = {
                    'name': vals['certi_laborales_emp_filename'],
                    'datas': vals['certi_laborales_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'hv_emp' in vals and vals['hv_emp_filename']:
                dic = {
                    'name': vals['hv_emp_filename'],
                    'datas': vals['hv_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'aceptacion_condiciones_emp' in vals and vals['aceptacion_condiciones_emp_filename']:
                dic = {
                    'name': vals['aceptacion_condiciones_emp_filename'],
                    'datas': vals['aceptacion_condiciones_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'libreta_militar_emp' in vals and vals['libreta_militar_emp_filename']:
                dic = {
                    'name': vals['libreta_militar_emp_filename'],
                    'datas': vals['libreta_militar_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'refrecnias_personales_emp' in vals and vals['refrecnias_personales_emp_filename']:
                dic = {
                    'name': vals['refrecnias_personales_emp_filename'],
                    'datas': vals['refrecnias_personales_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'verificacion_referencias_emp' in vals and vals['verificacion_referencias_emp_filename']:
                dic = {
                    'name': vals['verificacion_referencias_emp_filename'],
                    'datas': vals['verificacion_referencias_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'certificado_cuenta_bancaria_emp' in vals and vals['certificado_cuenta_bancaria_emp_filename']:
                dic = {
                    'name': vals['certificado_cuenta_bancaria_emp_filename'],
                    'datas': vals['certificado_cuenta_bancaria_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'antecedentes_disciplinarios_emp' in vals and vals['antecedentes_disciplinarios_emp_filename']:
                dic = {
                    'name': vals['antecedentes_disciplinarios_emp_filename'],
                    'datas': vals['antecedentes_disciplinarios_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'validacion_antecedentes_emp' in vals and vals['validacion_antecedentes_emp_filename']:
                dic = {
                    'name': vals['validacion_antecedentes_emp_filename'],
                    'datas': vals['validacion_antecedentes_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'entrevista_jefe_inmediato_emp' in vals and vals['entrevista_jefe_inmediato_emp_filename']:
                dic = {
                    'name': vals['entrevista_jefe_inmediato_emp_filename'],
                    'datas': vals['entrevista_jefe_inmediato_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'fotografias_emp' in vals and vals['fotografias_emp_filename']:
                dic = {
                    'name': vals['fotografias_emp_filename'],
                    'datas': vals['fotografias_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'validacion_sarlaft_emp' in vals and vals['validacion_sarlaft_emp_filename']:
                dic = {
                    'name': vals['validacion_sarlaft_emp_filename'],
                    'datas': vals['validacion_sarlaft_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)



            if 'estudio_seguridad_emp' in vals and vals['estudio_seguridad_emp_filename']:
                dic = {
                    'name': vals['estudio_seguridad_emp_filename'],
                    'datas': vals['estudio_seguridad_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'examendes_medicos_emp' in vals and vals['examendes_medicos_emp_filename']:
                dic = {
                    'name': vals['examendes_medicos_emp_filename'],
                    'datas': vals['examendes_medicos_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'poliza_emp' in vals and vals['poliza_emp_filename']:
                dic = {
                    'name': vals['poliza_emp_filename'],
                    'datas': vals['poliza_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'autorizacion_uso_correo_emp' in vals and vals['autorizacion_uso_correo_emp_filename']:
                dic = {
                    'name': vals['autorizacion_uso_correo_emp_filename'],
                    'datas': vals['autorizacion_uso_correo_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'licencia_conducir_emp' in vals and vals['licencia_conducir_emp_filename']:
                dic = {
                    'name': vals['licencia_conducir_emp_filename'],
                    'datas': vals['licencia_conducir_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'carta_propiedad_vehiculo_emp' in vals and vals['carta_propiedad_vehiculo_emp_filename']:
                dic = {
                    'name': vals['carta_propiedad_vehiculo_emp_filename'],
                    'datas': vals['carta_propiedad_vehiculo_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'cer_runt_emp' in vals and vals['cer_runt_emp_filename']:
                dic = {
                    'name': vals['cer_runt_emp_filename'],
                    'datas': vals['cer_runt_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)



            if 'revision_tecnico_mecanica_emp' in vals and vals['revision_tecnico_mecanica_emp_filename']:
                dic = {
                    'name': vals['revision_tecnico_mecanica_emp_filename'],
                    'datas': vals['revision_tecnico_mecanica_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'certificacion_sena_emp' in vals and vals['file_name']:
                dic = {

                    'name': vals['file_name'],
                    'datas': vals['certificacion_sena_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'documentos_generales' in vals and vals['documentos_generales_filename']:
                dic = {

                    'name': vals['documentos_generales_filename'],
                    'datas': vals['documentos_generales'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'centro_induccion_emp' in vals and vals['centro_induccion_emp_filename']:
                dic = {

                    'name': vals['centro_induccion_emp_filename'],
                    'datas': vals['centro_induccion_emp'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)


            if 'seguro_obligatorio_vigente' in vals and vals['seguro_obligatorio_vigente_filename']:
                dic = {

                    'name': vals['seguro_obligatorio_vigente_filename'],
                    'datas': vals['seguro_obligatorio_vigente'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)

            if 'TGS_Solidarios' in vals and vals['TGS_Solidarios_filename']:
                dic = {

                    'name': vals['TGS_Solidarios_filename'],
                    'datas': vals['TGS_Solidarios'],
                    'res_model': 'hr.employee',
                    'res_id': record.id
                }
                self.env['ir.attachment'].create(dic)




        return res
