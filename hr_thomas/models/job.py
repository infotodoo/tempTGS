# -*- coding: utf-8 -*-
# BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HrJob(models.Model):
    # _inherit = ['hr.job', 'mail.activity.mixin']
    _inherit = 'hr.job'
   
    @api.constrains('modificacion', 'eliminacion')
    def _check_boolean(self):
        for record in self:
            if record.modificacion and record.eliminacion:
                raise ValidationError("No puede modificar y eliminar a la vez, seleccione solo uno")
        
    @api.constrains('state', 'active')
    def _check_archive(self):
        for record in self:
            if not record.active and record.state != 'archive':
                raise ValidationError("No puede archivar si el estado es diferente a 'Eliminar'")

    state = fields.Selection(selection_add=[('create', 'Nuevo'), ('write', 'Modificacion'), ('unlink', 'Eliminacion'), ('archive', 'Archivado')],
                             default='create')
    active = fields.Boolean('Active', default=True, copy=False, tracking=True)
    # campos hr.job
    formacion_line = fields.One2many('formacion','job_id', 'Formación', track_visibility="onchange")
    activos_line = fields.One2many('activos','job_id','Activos', track_visibility="onchange")
    company_id=fields.Many2one('res.company', required="True", tracking=True)
    tht = fields.Char('Cargo en THT',tracking=True)
    unidad_organizativa = fields.Many2one('unidades',string="Unidad Organizativa",tracking=True)
    jefe_inmediato = fields.Many2one('hr.employee',tracking=True)
    jefe_inmediato_apl = fields.Many2one('hr.job',tracking=True, string="Jefe Inmediato")
    procesos_servicios_per = fields.Char(string="Procesos o servicios a los que pertenece",tracking=True)
    centro_de_costo=fields.Many2one('centro',tracking=True)
    nombre_centro_costo=fields.Char(related="centro_de_costo.centro_costo",tracking=True)
    tiene_personal_cargo = fields.Selection([('SI', 'SI'), ('NO', 'NO')], tracking=True, string="Tiene Personal a Cargo")
    cargo1 = fields.Many2one('hr.job', tracking=True)
    tipo_relacion1 = fields.Selection([('DIRECTA', 'DIRECTA'), ('INDIRECTA', 'INDIRECTA')],tracking=True)
    cargo2 = fields.Many2one('hr.job', tracking=True)
    tipo_relacion2 = fields.Selection([('DIRECTA', 'DIRECTA'), ('INDIRECTA', 'INDIRECTA')],tracking=True)
    cargo3 = fields.Many2one('hr.job', tracking=True)
    tipo_relacion3 = fields.Selection([('DIRECTA', 'DIRECTA'), ('INDIRECTA', 'INDIRECTA')],tracking=True)
    cargo4 = fields.Many2one('hr.job', tracking=True)
    tipo_relacion4 = fields.Selection([('DIRECTA', 'DIRECTA'), ('INDIRECTA', 'INDIRECTA')],tracking=True)

    # Campos: Educación:
    nivel_primario_educativo_minimo = fields.Selection([('BACHILLER', 'BACHILLER'), ('TECNICO', 'TÉCNICO'),('TECNOLOGICO','TECNOLÓGICO'),('PROFESIONAL','PROFESIONAL'),('N/A','N/A')],tracking=True)
    nombre_programa_carrera = fields.Char('Nombre del Programa o Carrera',tracking=True)
    nivel_secundario_educativo = fields.Selection([('ESPECIALISTA', 'ESPECIALISTA'), ('MAGISTER', 'MAGISTER'),('N/A','N/A')],tracking=True)
    nombre_programa = fields.Char(tracking=True)
    requiere_tarjeta_profesional = fields.Selection([('SI', 'SI'), ('NO', 'NO')],tracking=True) 
    # campo many2may formacion
    formacion_esp = fields.One2many('formacion.cargos','job_id',tracking=True)    
    #general
    general=fields.Selection([('SIN EXPERIENCIA', 'SIN EXPERIENCIA'), ('6 MESES', '6 MESES'),('1 AÑO','1 AÑO'),('2 AÑOS','2 AÑOS'),('3 AÑOS','3 AÑOS'),('4 AÑOS','4 AÑOS'),('5 AÑOS','5 AÑOS')],tracking=True)
    especifica_cargos_similares=fields.Selection([('SIN EXPERIENCIA', 'SIN EXPERIENCIA'), ('6 MESES', '6 MESES'),('1 AÑO','1 AÑO'),('2 AÑOS','2 AÑOS'),('3 AÑOS','3 AÑOS'),('4 AÑOS','4 AÑOS'),('5 AÑOS','5 AÑOS')],tracking=True)

    # objetivo del cargo
    objetivo_cargo = fields.Text(tracking=True)
    # escala salarial
    aplica = fields.Selection([('SI', 'SI'), ('NO', 'NO')],tracking=True)
    minimo = fields.Float(tracking=True)
    maximo = fields.Float(tracking=True)
    # funciones
    que_hace = fields.Text(tracking=True)
    como_lo_hace = fields.Text(tracking=True)

    # DEBERES
    deberes = fields.Text(tracking=True)
    # responsabilidades
    responsabilidades = fields.Text(tracking=True)
    # nivel de autoridad
    nivel_autoridad = fields.Text(tracking=True)
    # campos tipo check
    modificacion = fields.Boolean(tracking=True)
    eliminacion = fields.Boolean(tracking=True)
    # Activos a Cargo
    activos_del_cargo = fields.Many2many('activos',tracking=True)
    # campo multi-encuesta
    surveys_id = fields.Many2many('survey.survey', 'job_survey_rel', 'job_id', 'survey_id', 'Entrevistas',tracking=True)
    #qweb
    reportes_line = fields.One2many('ir.actions.report','job_id', 'Acción de Informes', tracking=True)
    description_job = fields.Text(string="Observaciones", tracking=True)
    reportes = fields.Many2many('ir.actions.report','name', tracking=True)
    name = fields.Char(string="Nombre del Cargo",tracking=True)
  


    def write(self, vals):
        if 'modificacion' in vals and vals['modificacion']:
            vals['state'] = 'write'
        if 'eliminacion' in vals and vals['eliminacion']:
            vals['state'] = 'unlink'
        if 'active' in vals and not vals['active'] and self[0].state == 'unlink':
            vals['state'] = 'archive'
        if 'active' in vals and vals['active'] and self[0].state == 'archive':
            vals['state'] = 'unlink'
        res = super(HrJob, self).write(vals)
        return res

    def button_create(self):
        self.write({'state': 'create', 'eliminacion': False})

    def button_open(self):
        self.write({'state': 'open', 'modificacion': False})

    def button_unactive(self):
        self.write({'active': False})

    def button_active(self):
        self.write({'active': True})

  