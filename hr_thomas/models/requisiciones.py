# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS

from odoo import fields,models,api,_
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta


cajacom = [
    ('7000016 CAJA DE COMPENSACION FAMILIAR', '7000016 CAJA DE COMPENSACION FAMILIAR'),
    ('7000017 CAJA DE COMPENSACION FAMILIAR DEL', '7000017 CAJA DE COMPENSACION FAMILIAR DEL'),
    ('7000018 CAJA DE COMPENSACION FAMILIAR DE', '7000018 CAJA DE COMPENSACION FAMILIAR DE'),
    ('7000019 CAJA DE COMPENSACION FAMILIAR DE', '7000019 CAJA DE COMPENSACION FAMILIAR DE'),
    ('7000020 CAJA DE COMPENSACION FAMILIAR DEL', '7000020 CAJA DE COMPENSACION FAMILIAR DEL'),
    ('7000021 CAJA COMPENSACION FAMILIAR CAFAM', '7000021 CAJA COMPENSACION FAMILIAR CAFAM'),
    ('7000022 CCF CAJASAN', '7000022 CCF CAJASAN'),
    ('7000023 CCF CARTAGENA', '7000023 CCF CARTAGENA'),
    ('7000024 CCF COLSUBSIDIO', '7000024 CCF COLSUBSIDIO'),
    ('7000025 CCF COMFAMILIAR GUAJIRA', '7000025 CCF COMFAMILIAR GUAJIRA'),
    ('7000026 CCF COMFAMILIAR RISARALDA', '7000026 CCF COMFAMILIAR RISARALDA'),
    ('7000027 CCF COMFANDI', '7000027 CCF COMFANDI'),
    ('7000028 CCF COMFENALCO ANTIOQUIA', '7000028 CCF COMFENALCO ANTIOQUIA'),
    ('7000029 CCF COMFENALCO CARTAGENA', '7000029 CCF COMFENALCO CARTAGENA'),
    ('7000030 CCF COMFENALCO SANTANDER', '7000030 CCF COMFENALCO SANTANDER'),
    ('7000032 CCF CONFANORTE', '7000032 CCF CONFANORTE'),
    ('7000033 CCF CORDOBA', '7000033 CCF CORDOBA'),
    ('7000034 CCF DE ANTIOQUIA COMFAMA', '7000034 CCF DE ANTIOQUIA COMFAMA'),
    ('7000035 CCF DE BARRANCABERMEJA', '7000035 CCF DE BARRANCABERMEJA'),
    ('7000036 CCF DE BARRANQUILLA', '7000036 CCF DE BARRANQUILLA'),
    ('7000037 CCF DE BOYACA CONFABOY', '7000037 CCF DE BOYACA CONFABOY'),
    ('7000038 CAJA DE COMPENSACION FAMILIAR DE CA', '7000038 CAJA DE COMPENSACION FAMILIAR DE CA'),
    ('7000039 CCF DE CASANARE', '7000039 CCF DE CASANARE'),
    ('7000040 CCF DE HONDA', '7000040 CCF DE HONDA'),
    ('7000041 CCF DE NARIÑO', '7000041 CCF DE NARIÑO'),
    ('7000042 CCF DE SUCRE', '7000042 CCF DE SUCRE'),
    ('7000043 CCF DEL ATLANTICO', '7000043 CCF DEL ATLANTICO'),
    ('7000044 CCF DEL CAQUETA', '7000044 CCF DEL CAQUETA'),
    ('7000045 CCF DEL CAUCA', '7000045 CCF DEL CAUCA'),
    ('7000046 CCF DEL CESAR COMFACESAR', '7000046 CCF DEL CESAR COMFACESAR'),
    ('7000047 CAJA DE COMPENSACION FAMILIAR DEL', '7000047 CAJA DE COMPENSACION FAMILIAR DEL'),
    ('7000048 CCF DEL MAGDALENA', '7000048 CCF DEL MAGDALENA'),
    ('7000049 CAJA DE COMPENSACION FAMILIAR', '7000049 CAJA DE COMPENSACION FAMILIAR'),
    ('7000050 CCF FENALCO DEL TOLIMA', '7000050 CCF FENALCO DEL TOLIMA'),
    ('7000051 CCF HUILA', '7000051 CCF HUILA'),
    ('7000052 CCF REGIONAL DEL META', '7000052 CCF REGIONAL DEL META'),
    ('7000054 COMPENSAR EPS', '7000054 COMPENSAR EPS'),
    ('7000124 CAJA DE COMPENSACION FAMILIAR DE SA', '7000124 CAJA DE COMPENSACION FAMILIAR DE SA'),
    ('7000130 CAJA DE COMPENSACION FAMILIAR DEL PUTUMAYO', '7000130 CAJA DE COMPENSACION FAMILIAR DEL PUTUMAYO'),
    ('7000143 CAJA DE COMPENSACION FAMILIAR CAJACOPI ATLANTICO', '7000143 CAJA DE COMPENSACION FAMILIAR CAJACOPI ATLANTICO')
]

motivo_solicitud = [
    ('RENUNCIA TITULAR', 'RENUNCIA TITULAR'),
    ('CANCELACIÓN DE CONTRATO', 'CANCELACIÓN DE CONTRATO'),
    ('VENCIMIENTO DE CONTRATO', 'VENCIMIENTO DE CONTRATO'),
    ('EVALUACIÓN DE ASCENSO', 'EVALUACIÓN DE ASCENSO'),
    ('AMPLIACIÓN DE PLANTA', 'AMPLIACIÓN DE PLANTA'),
    ('TRANSLADO', 'TRANSLADO'),
    ('SUSTITUCIÓN PATRONAL', 'SUSTITUCIÓN PATRONAL'),
    ('VACACIONES', 'VACACIONES'),
    ('FUNCIONARIO PROMOVIDO', 'FUNCIONARIO PROMOVIDO'),
    ('INCAPACIDAD / LICENCIA', 'INCAPACIDAD / LICENCIA'),
    ('CREACIÓN DE CARGO', 'CREACIÓN DE CARGO'),
    ('PENSIÓN', 'PENSIÓN')

]


class Todoo(models.Model):
    _name = 'requisiciones'
    # _rec_name = 'requisiciones'
    _rec_name = 'name'
    _inherit = 'mail.thread'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.depends('stage_id')
    def _compute_state(self):
        for record in self:
            record.state = record.stage_id.name

    def _default_stage(self):
        return self.env['requisicion.stage'].search([('id', '>', 0)], order='sequence', limit=1)

    def _compute_no_of_hired_employee(self):
        for record in self:
            record.no_of_hired_employee = len(self.env['hr.employee'].search([('requisition_id','=',record.id)]))

    # status = fields.Selection([('Borrador', 'Borrador'),('Aprobada', 'Aprobada'),('Abierta', 'Abierta'), ('Cerrada', 'Cerrada'),('Garantía','Garantía'),('Rechazada','Rechazada')], default="Borrador", readonly=True)
    state = fields.Char('Estado', compute='_compute_state')
    stage_id = fields.Many2one('requisicion.stage', 'Estado', default= _default_stage,  tracking=True, required=True, group_expand='_expand_stages')

    name = fields.Char('Requisición', tracking=True)
    solicitante=fields.Many2one('hr.employee',tracking=True)
    cargo_soli = fields.Char(string='Cargo del Solicitante', related='solicitante.job_id.display_name',tracking=True)

    company_id = fields.Many2one('res.company', 'Compañía', required=True, readonly=True, tracking=True)

    emp=fields.Many2one('res.company', 'Prueba', required=True,  default=lambda self: self.env.company)
    prioridad=fields.Selection([('Normal', 'Normal'),('Low', 'Low'),('High', 'High'),('Very High', 'Very High')], tracking=True)
    date_aper = fields.Datetime(string='Fecha de Apertura', required=True, readonly=True, index=True,  default=fields.Datetime.now,   help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    jefe_inmediato=fields.Many2one('hr.employee', string="Jefe Inmediato", tracking=True)
    cargo_solicitado=fields.Many2one('hr.job', string="Cargo Solicitado", tracking=True)
    catidad_vacantes=fields.Integer(string="Cantidad de Vacantes",tracking=True)
    Generos=fields.Selection([('MASCULINO', 'MASCULINO'),('FEMENINO', 'FEMENINO'),('INDIFERENTE', 'INDIFERENTE')],tracking=True)

    ciudades=fields.Many2one('ciudades',string="Prueba",tracking=True)
    res_city=fields.Many2one('res.city','Ciudad', tracking=True)
    departamento=fields.Many2one('res.country.state', tracking=True)
    sede=fields.Char(string="Sede",tracking=True)
    area=fields.Char(string="Área",tracking=True)
    un_organizativa=fields.Many2one('unidades','Unidad Organizativa',tracking=True)
    centro_costo_facturable=fields.Selection([('SI', 'SI'),('NO', 'NO'),('NO APLICA','NO APLICA')],tracking=True)
    centro_de_costo=fields.Many2one('centro',tracking=True)
    nombre_centro_costo=fields.Char(related="centro_de_costo.centro_costo",tracking=True)

    personal_a_cargo=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
    masivo=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True, compute='set_masivo_def', default='NO')
    requiere_entrevista=fields.Selection([('SI', 'SI'),('NO', 'NO')],string="Requiere Entrevista",tracking=True)
    requiere_prueba=fields.Selection([('SI', 'SI'),('NO', 'NO')],string="Requiere Prueba Técnica",tracking=True)
    requiere_studio_seguridad=fields.Selection([('SI', 'SI'),('NO', 'NO')],string="Requiere Estudio de Seguridad",tracking=True)

    tipo_pag=fields.Selection([('MENSUAL', 'MENSUAL'),('QUINCENAL', 'QUINCENAL')],string="Tipo de Pago",tracking=True)
    turn=fields.Selection([('FIJO', 'FIJO'),('ROTATIVO', 'ROTATIVO')],'Turno',tracking=True)
    horari=fields.Many2one('resource.calendar','Horario',tracking=True)
    nivel_riesgo=fields.Selection([('0.522%', '0.522%'),('1.044%', '1.044%'),('2.436%', '2.436%'),('4.350%', '4.350%'),('6.960%','6.960%')],string="Porcentaje Nivel de Riesgo",tracking=True, compute='set_nivel_riesgo_arl')

    nivel_riesgo_arl=fields.Selection([('1 RIESGO I', '1 RIESGO I'),('2 RIESGO II', '2 RIESGO II'),('3 RIESGO III','3 RIESGO III'),('4 RIESGO IV','4 RIESGO IV'),('5 RIESGO V','5 RIESGO V')],tracking=True)

    manejo_vacaciones=fields.Selection([('L-V', 'L-V'),('L-S', 'L-S')],string="Manejo de Vacaciones",tracking=True)
    manejo_incapacidades=fields.Selection([('PAGAR AL 66.66%', 'PAGAR AL 66.66%'),('PAGAR AL 100%', 'PAGAR AL 100%')],string="Manejo de Incapacidades",tracking=True)

    wage = fields.Monetary('Salario', required=True, currency_id='company.currency_id', tracking=True, help="Employee's monthly gross wage.")
    currency_id = fields.Many2one(string="Moneda", related='company_id.currency_id', readonly=True)

    tipo_contrato=fields.Selection([('FIJO', 'FIJO'),('MEDIO TIEMPO','MEDIO TIEMPO'),('SERVICIOS', 'SERVICIOS'),('INDEFINIDO', 'INDEFINIDO'),('OBRA LABOR', 'OBRA LABOR'),('APRENDIZAJE', 'APRENDIZAJE'),('DIARIO','DIARIO')])
    tiempo_de_contrato_inicial=fields.Integer(string="Tiempo de Contrato Inicial",tracking=True)
    cliente1=fields.Char(string="Cliente",tracking=True)
    no_contrato_comercial=fields.Char(string="No. Contrato Comercial",tracking=True)
    tiempo_contrato=fields.Integer(string="Tiempo Real del Contrato",tracking=True)
    rango=fields.Selection([('DÍAS', 'DÍAS'),('MESES', 'MESES'),('AÑOS', 'AÑOS')],string="Rango",tracking=True)

    mo_solicitud=fields.Selection(motivo_solicitud,'Motivo de Solicitud',tracking=True)

    per_quien_reemplaza=fields.Many2one('hr.employee',string="Persona a quien reemplaza",tracking=True)
    cargo_pre=fields.Selection([('Si', 'SI'),('No', 'NO')],'Cargo Presupuestado',tracking=True)

    #informacion del salario y contrato//
    tipo_de_salario=fields.Selection([('SUELDO BÁSICO', 'SUELDO BÁSICO'),('SALARIO INTEGRAL', 'SALARIO INTEGRAL'),('APOYO SOSTENIMIENTO', 'APOYO SOSTENIMIENTO')],tracking=True)
    pacto_con=fields.Selection([('PACTO COLECTIVO', 'PACTO COLECTIVO'),('CONVENCIÓN COLECTIVA DE TRABAJO', 'CONVENCIÓN COLECTIVA DE TRABAJO'),('NO APLICA','NO APLICA')],'Pacto/Convención',tracking=True)

    docuemnto_ref=fields.Binary(string="Documento Referido",tracking=True)


    #auxilios
    aux_alimentacion = fields.Selection([('SI', 'SI'),('NO', 'NO')],'Auxilio de Alimentación Fijo',tracking=True)
    valor_auxilio_alimentacion = fields.Float(string="Valor Auxilio de Alimentación",tracking=True, default=0)
    auxilio_de_alimentacion_a_partir_de = fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],string="Auxilio de Alimentación Fijo a partir de",tracking=True)
    aux_alimentacion_pro=fields.Selection([('SI', 'SI'),('NO', 'NO')],'Auxilio de Alimentación Proporcional',tracking=True)
    valor_aux_alimentacion_pro=fields.Float(tracking=True,string="Valor Auxilio de Alimentación Proporcional", default=0)
    aux_alimentacion_pro_partir=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],string="Auxilio de Alimentación Proporcional a partir de",tracking=True)
    aux_rodamiento=fields.Selection([('SI', 'SI'),('NO', 'NO')],string="Auxilio de Rodamiento",tracking=True)
    Valor_Auxili_de_Rodamiento=fields.Float(string="Valor Auxilio de Rodamiento",tracking=True, default=0)
    Auxilio_de_Rodamiento_a_partir_de=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
    aux_rodamiento_pro=fields.Selection([('SI', 'SI'),('NO', 'NO')],string="Auxilio de Rodamiento Proporcional",tracking=True)
    valor_aux_rodamiento_pro=fields.Float(string="Valor Auxilio de Rodamiento",tracking=True, default=0)
    aux_rodamiento_pro_partir=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],string="Auxilio de Rodamiento Proporcional a partir de",tracking=True)
    aux_celular=fields.Selection([('SI', 'SI'),('NO', 'NO')],string="Auxilio de Celular",tracking=True)
    Valor_Auxilio_de_Celular=fields.Float(string="Valor Auxilio de Celular",tracking=True, default=0)
    Auxilio_de_Celular_a_partir_de=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
    aux_movilizacion=fields.Selection([('SI', 'SI'),('NO', 'NO')],string="Auxilio de Movilización",tracking=True)
    valor_aux_movilizacion=fields.Float(string="Valor Auxilio de Movilización",tracking=True,  default=0)
    aux_movilizacion_a_partir=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],string="Auxilio de Movilización a partir de",tracking=True)

    #campos Beneficios
    medicina_prepagada=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)
    Valor_Medicina_Prepagada=fields.Float(string="Valor Medicina Prepagada", tracking=True)
    Medicina_Prepagada_a_partir_de=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
    bonos=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)
    Valor_Bonos=fields.Float(string="Valor Bonos",tracking=True, default=0)
    Bonos_a_partir_de=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
    comisiones=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
    Valor_Comisiones=fields.Float(string="Valor Comisiones", default=0)
    Comisiones_a_partir_de=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
    otro=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
    cual_Otro_Beneficio=fields.Char(tracking=True)
    Valor_Otro_Beneficio=fields.Float(tracking=True, default=0)
    Otro_Beneficio_a_partir_de=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
    tipo_cargo=fields.Selection([('NIVEL OPERATIVO', 'NIVEL OPERATIVO'),('MANDOS MEDIOS Y NIVEL ADMON', 'MANDOS MEDIOS Y NIVEL ADMINISTRATIVO'),('ALTA GERENCIA Y MANDOS ESP', 'ALTA GERENCIA Y MANDOS ESPECIALES')],tracking=True)
    psicologo=fields.Many2one('hr.employee',tracking=True)
    correo_psicologo=fields.Char(tracking=True)
    reclutador=fields.Many2one('hr.employee',tracking=True)
    observaciones=fields.Char(string="Observaciones",tracking=True)
    psicologo_req = fields.Many2one('res.users', string="Psicologo",tracking=True)
    reclutador_req = fields.Many2one('res.users', string="Reclutador",tracking=True)

    applicant_count = fields.Integer('Number of sheets', compute='_compute_applicant_data')
    applicant_ids = fields.One2many('hr.applicant','requisicion')
    #aprobaciones//
    aprobador_nivel1= fields.Many2one('hr.employee',tracking=True)
    aprobador_nivel2 = fields.Many2one('hr.employee',tracking=True)
    aprobador_nivel3 = fields.Many2one('hr.employee',tracking=True)
    #campos ANS
    tiempo_1ra_aprobacion = fields.Float('Tiempo 1ra Aprobación',tracking=True)
    tiempo_2da_aprobacion = fields.Float('Tiempo 2da Aprobación',tracking=True)
    tiempo_3ra_aprobacion = fields.Float('Tiempo 3ra Aprobación',tracking=True)
    tiempo_aprobada_cliente = fields.Float('Tiempo Aprobada por el Cliente',tracking=True)
    tiempo_aprobada = fields.Float('Tiempo en Etapa Aprobada',tracking=True)
    tiempo_abierta = fields.Float('Tiempo en Etapa Abierta',tracking=True)
    tiempo_cerrada = fields.Float('Tiempo en Etapa Cerrada',tracking=True)
    tiempo_garantia = fields.Float('Tiempo en Etapa de Garantía',tracking=True)
    tiempo_total=fields.Float('Tiempo Total del Proceso', tracking=True)
    #Campos que toman la fecha y hora justa cuando se cambia la etapa
    tiempo_inicial=fields.Datetime('Fecha y hora de inicio',tracking=True, default= fields.Datetime().now())
    fecha_hora_1ra_aprobacion = fields.Datetime('Fecha y hora 1ra Aprobación', tracking=True, default= fields.Datetime().now())
    fecha_hora_2da_aprobacion = fields.Datetime('Fecha y hora 2da Aprobación', tracking=True)
    fecha_hora_3ra_aprobacion = fields.Datetime('Fecha y hora 3ra Aprobación', tracking=True)
    fecha_hora_aprobada_cliente = fields.Datetime('Fecha y hora Etapa Aprobada por el Cliente', tracking=True)
    fecha_hora_aprobacion = fields.Datetime('Fecha y hora Etapa de Aprobación', tracking=True)
    fecha_hora_abierta = fields.Datetime('Fecha y hora Etapa Abierta', tracking=True)
    fecha_hora_cerrada = fields.Datetime('Fecha y hora Etapa Cerrada', tracking=True)
    fecha_hora_garantia = fields.Datetime('Fecha y hora Etapa de Garantía', tracking=True)
    fecha_hora_finalizada = fields.Datetime('Fecha y hora Etapa de Garantía', tracking=True)
    #nombre y ID de la etapa
    estado_de_solicitud=fields.Char(related="stage_id.name")
    id_estado_de_solicitud=fields.Integer(related="stage_id.sequence")
    # no_of_hired_employee
    no_of_hired_employee = fields.Integer('Hired Employees', compute='_compute_no_of_hired_employee')

    def _compute_applicant_data(self):
        for record in self:
            count = len(record.applicant_ids)
            record.applicant_count = count



    def action_view_applicant(self):
        action = self.env.ref('hr_recruitment.crm_case_categ0_act_job').read()[0]
        action['context'] = {
            'default_requisicion': self.id,
        }
        action['domain'] = [('requisicion', '=', self.id)]
        return action

    def _expand_stages(self, stage_id, domain, order):
        stage_id = self.env['requisicion.stage'].search([])
        return stage_id


    #validar salario integral
    @api.constrains('wage')
    def _check_salario_req(self):
        for record in self:
            if record.tipo_de_salario ==  'SALARIO INTEGRAL':
                if record.wage < 11000000:
                    raise ValidationError("El Salario Integral debe ser mayor a 11.411.439 : %s" % record.wage)
            elif record.tipo_de_salario ==  'SUELDO BÁSICO':
                if record.wage <  877803:
                    raise ValidationError("El Salario Básico debe ser mayor a 877.803 : %s" % record.wage)

    @api.constrains('catidad_vacantes')
    def _check_can_vacantes(self):
        for record in self:
            if record.catidad_vacantes <= 0:
                raise ValidationError("La Cantidad de Vacantes no puede ser 0  : %s" % record.catidad_vacantes)

    @api.depends('catidad_vacantes')
    def set_masivo_def(self):
        for record in self:
            if record.catidad_vacantes:
                if record.catidad_vacantes > 10:
                    record.masivo = 'SI'
                else:
                    record.masivo = 'NO'
            else:
                record.masivo = 'NO'
    #riesgo
    @api.depends('nivel_riesgo_arl')
    def set_nivel_riesgo_arl(self):
        if self.nivel_riesgo_arl:
            if self.nivel_riesgo_arl == '1 RIESGO I':
                self.nivel_riesgo = '0.522%'
            elif self.nivel_riesgo_arl == '2 RIESGO II':
                 self.nivel_riesgo = '1.044%'
            elif self.nivel_riesgo_arl == '3 RIESGO III':
                 self.nivel_riesgo = '2.436%'
            elif self.nivel_riesgo_arl == '4 RIESGO IV':
                 self.nivel_riesgo = '4.350%'
            else:
                self.nivel_riesgo = '6.960%'


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('requisiciones') or _('Nuevo')
        vals.update()
        result = super(Todoo, self).create(vals)
        return result

    #funciones de los botones para cambiar de estados.
    def button_primera_aprobacion(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'SEGUNDA APROBACION')], limit=1)
        self.write({'stage_id': rs.id})

    def button_rechazar_primera_aprobacion(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'RECHAZADA POR EL CLIENTE')], limit=1)
        self.write({'stage_id': rs.id})

    def button_segunda_aprobacion(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'TERCERA APROBACION')], limit=1)
        self.write({'stage_id': rs.id})

    def button_rechazar_segunda_aprobacion(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'RECHAZADA POR EL CLIENTE')], limit=1)
        self.write({'stage_id': rs.id})

    def button_tercera_aprobacion(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'APROBADA POR EL CLIENTE')], limit=1)
        self.write({'stage_id': rs.id})

    def button_rechazar_tercera_aprobacion(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'RECHAZADA POR EL CLIENTE')], limit=1)
        self.write({'stage_id': rs.id})

    def button_done(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'APROBADA')], limit=1)
        self.write({'stage_id': rs.id})

    def button_abierta(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'ABIERTA')], limit=1)
        self.write({'stage_id': rs.id})
        for record in self:
            if not record.tiempo_aprobada:
                calc = fields.Datetime.now() - record.fecha_hora_aprobacion
                calc = calc.seconds/3600
                record.tiempo_aprobada = calc
            if not record.fecha_hora_abierta:
                record.fecha_hora_abierta = fields.Datetime.now()

    def button_cerrada(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'CERRADA')], limit=1)
        self.write({'stage_id': rs.id})
        for record in self:
            calc = fields.Datetime.now() - record.fecha_hora_abierta
            calc = calc.seconds/3600
            record.tiempo_abierta = calc
            if not record.fecha_hora_cerrada:
                record.fecha_hora_cerrada = fields.Datetime.now()

    def button_garantia(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'GARANTIA')], limit=1)
        self.write({'stage_id': rs.id})
        for record in self:
            calc = fields.Datetime.now() - record.fecha_hora_cerrada
            calc = calc.seconds/3600
            record.tiempo_cerrada = calc
            if not record.fecha_hora_garantia:
                record.fecha_hora_garantia = fields.Datetime.now()

    def button_devolver_garantia(self):
        self.button_abierta()

    def button_finalizada(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'FINALIZADA')], limit=1)
        self.write({'stage_id': rs.id})

    def button_rechazar(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'RECHAZADA')], limit=1)
        self.write({'stage_id': rs.id})

    def button_rechazar_final(self):
        rs = self.env['requisicion.stage'].search([('name', '=', 'RECHAZADA')], limit=1)
        self.write({'stage_id': rs.id})

    #funcion para boton inteligente
    def solicitudes(self):
        return {
           'name': _('solicitudes'),
           'domain': [('solicitante', '=', self.id)],
           'view_type': 'form',
           'res_model': 'hr.applicant',
           'view_id': False,
           'view_mode': 'tree,form',
           'type': 'ir.action.act.window',
        }

    def write(self, vals):
        if 'stage_id' in vals:
            id_stage = self.env['requisicion.stage'].browse(vals['stage_id'])
            if id_stage.sequence == 2:
                #vals['tiempo_pri_entrevista']= fields.Datetime().now()
                vals.update(fecha_hora_1ra_aprobacion=fields.Datetime().now())
            if id_stage.sequence == 3:
                #vals['tiempo_pri_entrevista']= fields.Datetime().now()
                vals.update(fecha_hora_2da_aprobacion=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_1ra_aprobacion
                calc = calc.seconds/3600
                vals.update(tiempo_1ra_aprobacion=calc)

            if id_stage.sequence == 5:
                #vals['tiempo_pri_entrevista']= fields.Datetime().now()
                vals.update(fecha_hora_3ra_aprobacion=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_2da_aprobacion
                calc = calc.seconds/3600
                vals.update(tiempo_2da_aprobacion=calc)

            if id_stage.sequence == 6:
                #vals['tiempo_pri_entrevista']= fields.Datetime().now()
                vals.update(fecha_hora_aprobada_cliente=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_3ra_aprobacion
                calc = calc.seconds/3600
                vals.update(tiempo_3ra_aprobacion=calc)

            if id_stage.sequence == 7:
                #vals['tiempo_pri_entrevista']= fields.Datetime().now()
                vals.update(fecha_hora_aprobacion=fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_aprobada_cliente
                calc = calc.seconds/3600
                vals.update(tiempo_aprobada_cliente=calc)

            # if id_stage.sequence == 7:
            #     #vals['tiempo_pri_entrevista']= fields.Datetime().now()
            #     vals.update(fecha_hora_abierta=fields.Datetime().now())
            #     calc = fields.Datetime.now() - self.fecha_hora_aprobacion
            #     vals.update(tiempo_aprobada=calc)

            # if id_stage.sequence == 8:
            #     #vals['tiempo_pri_entrevista']= fields.Datetime().now()
            #     vals.update(fecha_hora_cerrada=fields.Datetime().now())
            #     calc = fields.Datetime.now() - self.fecha_hora_abierta
            #     vals.update(tiempo_abierta=calc)

            # if id_stage.sequence == 9:
            #     #vals['tiempo_pri_entrevista']= fields.Datetime().now()
            #     vals.update(fecha_hora_garantia=fields.Datetime().now())
            #     calc = fields.Datetime.now() - self.fecha_hora_cerrada
            #     vals.update(tiempo_cerrada=calc)

            if id_stage.sequence == 8:
                #vals['tiempo_pri_entrevista']= fields.Datetime().now()
                vals.update(fecha_hora_finalizada =fields.Datetime().now())
                calc = fields.Datetime.now() - self.fecha_hora_garantia
                calc2 = fields.Datetime.now() - self.date_aper
                calc = calc.seconds/3600
                vals.update(tiempo_garantia=calc)
                calc2 = calc2.seconds/3600
                vals.update(tiempo_total=calc2)
        return super(Todoo, self).write(vals)
