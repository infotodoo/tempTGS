# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api,_ 

class Todoo(models.Model):
   _inherit = 'hr.contract'

   #campos relacionados del empleado//
   employee=fields.Many2one('hr.employee',string="Empleado",tracking=True)
   identificacion=fields.Char(related="employee_id.identification_id")   
   city_exp_empleado=fields.Char(related="employee_id.identification_id") 
   telefono_empleado=fields.Char(related="employee_id.phone")
   correo_empleado=fields.Char(related="employee_id.private_email")
   work_email=fields.Char()
   work_phone=fields.Char()
   direccion_empleado_con=fields.Char(related="employee_id.complete_direction")
   employee_id=fields.Many2one('hr.employee', required="True")
   job_id=fields.Many2one('hr.job', string="Puesto de Trabajo", required="True")
   #campos relacionados de la requisición//
   requisicion=fields.Many2one(related="employee_id.requisition_id",tracking=True)
   tiempo_contrato_inc = fields.Integer(tracking=True)
   rango_contrato = fields.Selection([('DÍAS', 'DÍAS'),('MESES', 'MESES'),('AÑOS', 'AÑOS')],tracking=True)
   no_cont = fields.Char(tracking=True)
   tip_contrac = fields.Selection([('FIJO', 'FIJO'),('MEDIO TIEMPO','MEDIO TIEMPO'),('SERVICIOS', 'SERVICIOS'),('INDEFINIDO', 'INDEFINIDO'),('OBRA LABOR', 'OBRA LABOR'),('APRENDIZAJE', 'APRENDIZAJE'),('DIARIO','DIARIO')])
   tip_turno = fields.Selection([('FIJO', 'FIJO'),('ROTATIVO', 'ROTATIVO')],tracking=True)
   area_req_contrato=fields.Char(related="requisicion.area",tracking=True)
   manejo_vacaciones_contrato=fields.Selection([('L-V', 'L-V'),('L-S', 'L-S')],tracking=True)
   manejo_incapacidades_contrato=fields.Selection([('PAGAR AL 66.66%', 'PAGAR AL 66.66%'),('PAGAR AL 100%', 'PAGAR AL 100%')],tracking=True)
   nivel_riesgo_arl_contrato=fields.Selection([('1 RIESGO I', '1 RIESGO I'),('2 RIESGO II', '2 RIESGO II'),('3 RIESGO III','3 RIESGO III'),('4 RIESGO IV','4 RIESGO IV'),('5 RIESGO V','5 RIESGO V')],tracking=True)
   tipo_de_salario_contrato=fields.Selection([('SUELDO BÁSICO', 'SUELDO BÁSICO'),('SALARIO INTEGRAL', 'SALARIO INTEGRAL'),('APOYO SOSTENIMIENTO', 'APOYO SOSTENIMIENTO')],tracking=True)
   pacto_convencion_contrato=fields.Selection([('PACTO COLECTIVO', 'PACTO COLECTIVO'),('CONVENCIÓN COLECTIVA DE TRABAJO', 'CONVENCIÓN COLECTIVA DE TRABAJO'),('NO APLICA','NO APLICA')],tracking=True)
   aux_alimentacion = fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
   valor_auxilio_alimentacion = fields.Float(string="Valor Auxilio de Alimentación",tracking=True, default=0)
   auxilio_de_alimentacion_a_partir_de = fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
   aux_alimentacion_pro=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
   valor_aux_alimentacion_pro=fields.Float(tracking=True, default=0) 
   aux_alimentacion_pro_partir=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)    
   aux_rodamiento=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
   Valor_Auxili_de_Rodamiento=fields.Float(string="Valor Auxilio de Rodamiento",tracking=True, default=0)
   Auxilio_de_Rodamiento_a_partir_de=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
   aux_rodamiento_pro=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
   valor_aux_rodamiento_pro=fields.Float(tracking=True, default=0)
   aux_rodamiento_pro_partir=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
   aux_celular=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
   Valor_Auxilio_de_Celular=fields.Float(string="Valor Auxilio de Celular",tracking=True, default=0)
   Auxilio_de_Celular_a_partir_de=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)
   aux_movilizacion=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
   valor_aux_movilizacion=fields.Float(tracking=True,  default=0)
   aux_movilizacion_a_partir=fields.Selection([('FECHA DE INGRESO', 'FECHA DE INGRESO'),('1 MES', '1 MES'),('2 MESES','2 MESES'),('3 MESES','3 MESES'),('4 MESES','4 MESES')],tracking=True)    
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
   cliente=fields.Char(tracking=True)
   nivel_riesgo_arl=fields.Selection([('1 RIESGO I', '1 RIESGO I'),('2 RIESGO II', '2 RIESGO II'),('3 RIESGO III','3 RIESGO III'),('4 RIESGO IV','4 RIESGO IV'),('5 RIESGO V','5 RIESGO V')],tracking=True)
   nivel_riesgo=fields.Selection([('0.522%', '0.522%'),('1.044%', '1.044%'),('2.436%', '2.436%'),('4.350%', '4.350%'),('6.960%','6.960%')],tracking=True)
   #campos grupo:representante//
   nombre_representante=fields.Many2one('hr.employee',tracking=True)
   cedula_representante=fields.Char(related="nombre_representante.identification_id")
   cargo_representante=fields.Many2one(related="nombre_representante.job_id",tracking=True)
   lugar_expedicion_con=fields.Many2one(related="nombre_representante.lugar_expedicion_id_emp")
   lugar_expedicion_contratado = fields.Many2one(related="employee_id.lugar_expedicion_id_emp")
   #campos grupo:terminos de contrato
   ciudad=fields.Many2one('ciudades',tracking=True)
   res_city=fields.Many2one('res.city',string="Ciudad",tracking=True)
   jefe_inmediato_con=fields.Many2one('hr.employee',string="Jefe Inmediato")
   cargo_jefe_inmediato_con=fields.Many2one(related="jefe_inmediato_con.job_id")
   fecha_inicio=fields.Date(tracking=True)
   fecha_final=fields.Date(tracking=True)
   No_dias_prueba=fields.Integer(tracking=True)
   fin_periodo_prueba=fields.Integer(tracking=True)
   planificacion_trabajo=fields.Many2one('resource.calendar',tracking=True)
   responsable_rrhh=fields.Char(tracking=True)
   #grupo
   via_pago=fields.Char(default='TRANSFERENCIA')   
   tipo_salario=fields.Selection(related="requisicion.tipo_de_salario")
   solicitante_contrato = fields.Many2one(related="requisicion.solicitante", string="Solicitante")
   #campo fecha firma
   fecha_firma_contrato=fields.Date()
   #campos grupo: aprendiz Sena
   tipo_aprendiz=fields.Selection([('ETAPA LECTIVA', 'ETAPA LECTIVA'),('ETAPA PRODUCTIVA', 'ETAPA PRODUCTIVA'),('PRACTICANTE', 'PRACTICANTE UNIVERSITARIO')],tracking=True)
   fecha_fin_etapa_lectiva=fields.Date(tracking=True)
   Fecha_Inicio_Etapa_Productiva=fields.Date(tracking=True)
   fecha_fin_etapa_productiva=fields.Date(tracking=True)   
   #horario
   resource_calendar_id=fields.Many2one('resource.calendar',tracking=True)
   #imagen
   firma_ed=fields.Binary()
   #cuenta bancaria
   no_cuenta_bancaria=fields.Many2one(related="employee_id.bank_account_id",tracking=True)
   #version del documento
   version_documento=fields.Char(tracking=True, default="-V")
   #dirrecion del empleado
   Via_principal = fields.Many2one('direccion', string="Vía Principal", related="employee_id.main_road")
   nombre_via_principal = fields.Char(string="Nombre Vía Principal", related="employee_id.main_road_name")
   via_generadora = fields.Char(string="Vía Generadora", related="employee_id.road_generator")
   predio = fields.Char(string="Predio", related="employee_id.land")
   complemento = fields.Char(string="Complemento", related="employee_id.complement")
   #imagen para firma
   firma = fields.Binary(string="Firma")
   clase_beneficio = fields.Integer(string="Importe Clase Beneficio", related="employee_id.importe_clase_beneficio_emp")
  
        

   #Función para llevar información de requisiciones a contratos - 
   @api.onchange('requisicion')
   def _onchange_requisicion(self):
      if self.requisicion:
         self.tip_contrac =  self.requisicion.tipo_contrato
         self.tiempo_contrato_inc =  self.requisicion.tiempo_de_contrato_inicial
         self.rango_contrato =  self.requisicion.rango
         self.no_cont =  self.requisicion.no_contrato_comercial
         self.tip_turno =  self.requisicion.turn
         self.resource_calendar_id =  self.requisicion.horari
         self.manejo_vacaciones_contrato =  self.requisicion.manejo_vacaciones
         self.manejo_incapacidades_contrato = self.requisicion.manejo_incapacidades
         self.nivel_riesgo_arl = self.requisicion.nivel_riesgo_arl
         self.tipo_de_salario_contrato = self.requisicion.tipo_de_salario
         self.pacto_convencion_contrato = self.requisicion.pacto_con
         self.aux_alimentacion = self.requisicion.aux_alimentacion
         self.valor_auxilio_alimentacion = self.requisicion.valor_auxilio_alimentacion
         self.auxilio_de_alimentacion_a_partir_de = self.requisicion.auxilio_de_alimentacion_a_partir_de
         self.aux_alimentacion_pro = self.requisicion.aux_alimentacion_pro
         self.valor_aux_alimentacion_pro = self.requisicion.valor_aux_alimentacion_pro
         self.aux_alimentacion_pro_partir = self.requisicion.aux_alimentacion_pro_partir
         self.aux_rodamiento = self.requisicion.aux_rodamiento
         self.Auxilio_de_Rodamiento_a_partir_de = self.requisicion.Auxilio_de_Rodamiento_a_partir_de
         self.aux_rodamiento_pro = self.requisicion.aux_rodamiento_pro
         self.aux_rodamiento_pro_partir = self.requisicion.aux_rodamiento_pro_partir
         self.aux_celular = self.requisicion.aux_celular
         self.Valor_Auxilio_de_Celular = self.requisicion.Valor_Auxilio_de_Celular
         self.Auxilio_de_Celular_a_partir_de = self.requisicion.Auxilio_de_Celular_a_partir_de
         self.aux_movilizacion = self.requisicion.aux_movilizacion
         self.valor_aux_movilizacion = self.requisicion.valor_aux_movilizacion
         self.aux_movilizacion_a_partir = self.requisicion.aux_movilizacion_a_partir
         self.medicina_prepagada = self.requisicion.medicina_prepagada
         self.Valor_Medicina_Prepagada = self.requisicion.Valor_Medicina_Prepagada
         self.Medicina_Prepagada_a_partir_de = self.requisicion.Medicina_Prepagada_a_partir_de
         self.bonos = self.requisicion.bonos
         self.Valor_Bonos = self.requisicion.Valor_Bonos
         self.Bonos_a_partir_de = self.requisicion.Bonos_a_partir_de
         self.comisiones = self.requisicion.comisiones
         self.Valor_Comisiones = self.requisicion.Valor_Comisiones
         self.Comisiones_a_partir_de = self.requisicion.Comisiones_a_partir_de
         self.otro = self.requisicion.otro
         self.cual_Otro_Beneficio = self.requisicion.cual_Otro_Beneficio
         self.Valor_Otro_Beneficio = self.requisicion.Valor_Otro_Beneficio
         self.Otro_Beneficio_a_partir_de = self.requisicion.Otro_Beneficio_a_partir_de
         self.wage = self.requisicion.wage
         self.cliente = self.requisicion.cliente1
         self.jefe_inmediato_con = self.requisicion.jefe_inmediato
         self.res_city = self.requisicion.res_city
         