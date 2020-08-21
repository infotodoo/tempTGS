# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, exceptions
import xmlrpc.client
import inspect

import logging

_logger = logging.getLogger(__name__)


def deal_many_2_one(self, vals):
    model_id = self.env["ir.model"].sudo().search([("model", "=", self._name)])
    many2one_fields = (
        self.env["ir.model.fields"]
        .sudo()
        .search([("model_id", "=", model_id.id), ("ttype", "=", "many2one")])
        .mapped("name")
    )
    for field in many2one_fields:
        if vals.get(field):
            field_obj = (
                self.env["ir.model.fields"]
                .sudo()
                .search([("model_id", "=", model_id.id), ("name", "=", field)])
            )
            if field_obj:
                replicant = (
                    self.env[field_obj.relation].sudo().browse(int(vals.get(field)))
                )

                if replicant:
                    relation_model_obj = (
                        self.env["ir.model"]
                        .sudo()
                        .search([("model", "=", field_obj.relation)])
                    )
                    is_replicated_prsent = (
                        self.env["ir.model.fields"]
                        .sudo()
                        .search(
                            [
                                ("model_id", "=", relation_model_obj.id),
                                ("name", "=", "replicated_id"),
                            ]
                        )
                    )
                    if is_replicated_prsent:
                        vals[field] = int(replicant.replicated_id)
                        _logger.error(
                            "\n\n{} SYNC FIELD: {} > {}".format(
                                self._name, field, vals[field]
                            )
                        )
                    else:
                        vals.pop(field)
                        _logger.error("\n\nPOP FIELD {}".format(field))
                else:
                    vals.pop(field)
    if vals.get("message_follower_ids"):
        vals.pop("message_follower_ids")
    return vals


def deal_local_regular_fields(self, vals):
    model_id = self.env["ir.model"].sudo().search([("model", "=", self._name)])
    regular_fields = (
        self.env["ir.model.fields"]
        .sudo()
        .search([("model_id", "=", model_id.id)])
        .mapped("name")
    )
    new_vals = dict()
    for field in regular_fields:
        if vals.get(field):
            new_vals.update({field: vals.get(field)})
    return new_vals


def connect_database(self, vals, operation):
    """ Connect To Database"""
    model = self.env["ir.config_parameter"]
    url = model.sudo().get_param("database_sync.url")
    db = model.sudo().get_param("database_sync.db")
    username = model.sudo().get_param("database_sync.username")
    password = model.sudo().get_param("database_sync.password")
    if url and db and username and password:
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        common.version()
        uid = common.authenticate(db, username, password, {})
        target = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))
        replicated_id = ""
        # AT LAST COMPARE EACH OPERATION CREATE AND WRITE AND REDUCE SAME CODES
        if operation == "write":
            # HR EMPLOYEE
            if self._name == "hr.employee":
                if self.company_id and not vals.get("company_id"):
                    vals.update({"company_id": self.company_id.id})
                vals = deal_many_2_one(self, vals)
                # Filter keys for write on hr.employee (sync only this fields)
                keys = [
                    "first_name",
                    "second_name",
                    "third_name",
                    "aplicante",
                    "name",
                    "job_title",
                    "job_id",
                    "fourth_name",
                    "aprobador_ninel2",
                    "aprobador_ninel3",
                    "replicated_id",
                    "company_id",
                ]
                new_vals = {
                    required_key: vals[required_key]
                    for required_key in keys
                    if vals.get(required_key)
                }
                _logger.error(
                    "SYNC WRITE EMPLOYEE: {}\n\nWRITE EMPLOYEE: {}".format(
                        new_vals, vals
                    )
                )
                vals = new_vals
            if self._name == "hr.resume.line":
                vals = deal_many_2_one(self, vals)
                if vals.get("employee_id"):
                    vals.pop("employee_id")
            # HR JOB
            if self._name == "hr.job":
                print(vals, "write")
                if vals.get("cargo1"):
                    cargo1_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo1"))).replicated_id
                    )
                    if cargo1_rec:
                        vals.update({"cargo1": int(cargo1_rec)})
                if vals.get("cargo2"):
                    cargo2_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo2"))).replicated_id
                    )
                    if cargo2_rec:
                        vals.update({"cargo2": int(cargo2_rec)})
                if vals.get("cargo3"):
                    cargo3_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo3"))).replicated_id
                    )
                    if cargo3_rec:
                        vals.update({"cargo3": int(cargo3_rec)})
                if vals.get("cargo4"):
                    cargo4_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo4"))).replicated_id
                    )
                    if cargo4_rec:
                        vals.update({"cargo4": int(cargo4_rec)})
                if vals.get("cargo4"):
                    cargo4_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo4"))).replicated_id
                    )
                    if cargo4_rec:
                        vals.update({"cargo4": int(cargo4_rec)})
                if vals.get("jefe_inmediato_apl"):
                    jefe_inmediato_apl_rec = (
                        self.env["hr.job"]
                        .browse(int(vals.get("jefe_inmediato_apl")))
                        .replicated_id
                    )
                    if jefe_inmediato_apl_rec:
                        vals.update({"jefe_inmediato_apl": int(jefe_inmediato_apl_rec)})
                if vals.get("department_id"):
                    department_id_rec = (
                        self.env["hr.job"]
                        .browse(int(vals.get("department_id")))
                        .replicated_id
                    )
                    if department_id_rec:
                        vals.update({"department_id": int(department_id_rec)})
                if vals.get("activos_line"):
                    vals.pop("activos_line")
                if vals.get("formacion_esp"):
                    vals.pop("formacion_esp")
                if vals.get("formacion_line"):
                    vals.pop("formacion_line")
            # REQUISICIONES
            if self._name == "requisiciones":
                vals = deal_many_2_one(self, vals)
            # HR APPLICANT
            if self._name == "hr.applicant":
                vals = deal_many_2_one(self, vals)
            if self._name == "hr.recruitment.stage":
                vals = deal_many_2_one(self, vals)
            if self._name == "formacion":
                vals = deal_many_2_one(self, vals)
            if self._name == "hijo":
                vals = deal_many_2_one(self, vals)
            if self._name == "lenguage":
                vals = deal_many_2_one(self, vals)
            if self._name == "mascotas":
                vals = deal_many_2_one(self, vals)
            # SURVEY.SURVEY
            if self._name == "survey.survey":
                vals = deal_many_2_one(self, vals)
            if self._name == "survey.question":
                vals = deal_many_2_one(self, vals)
                if vals.get("survey_id"):
                    vals.pop("survey_id")
            if self._name == "survey.user_input":
                vals = deal_many_2_one(self, vals)
            if self._name == "survey.user_input_line":
                vals = deal_many_2_one(self, vals)
            if self._name == "res.partner":
                vals = deal_many_2_one(self, vals)
                vals = deal_local_regular_fields(self, vals)
                # Filter keys for write on res.partner (sync only this fields)
                keys = ["name", "phone", "mobile", "email"]
                new_vals = {
                    required_key: vals[required_key]
                    for required_key in keys
                    if vals.get(required_key)
                }
                vals = new_vals
            # MAIL ACTIVITY TYPE ~ NEW MODULE INSTALL in Main DATABASE
            if vals.get("mail.activity.type"):
                vals = deal_many_2_one(self, vals)
            # OTHER MODELS
            if self._name == "centro":
                print(vals, "centro writw")
            if self._name == "unidades":
                print(vals, "unidades write")
            if self._name == "hr.department":
                print(vals, "Department Write")
            if self._name == "direccion":
                print(vals, "direccion write")
            if self._name == "formacion.cargos":
                vals.pop("job_id")
            if self._name == "activos":
                vals.pop("job_id")
            if vals.get("res_city"):
                city = self.env["res.city"].browse(int(vals.get("res_city")))
                vals.update({"res_city": int(city.replicated_id)})
            try:
                record_id = int(self.replicated_id)
                vals.update({"replicated_id": self.id})
                target.execute_kw(
                    db, uid, password, self._name, operation, [[record_id], vals]
                )
            except:
                _logger.error(
                    "Write operation in {} was not synchronized".format(self._name)
                )

        if operation == "create":
            # RES USERS
            if self._name == "res.users":
                _logger.error(f"\nSEND ONE CREATE RES USERS: {vals}\n")
                vals = deal_many_2_one(self, vals)
                # Filter keys for create hr.employee (sync only this fields)
                # keys = ['first_name', 'second_name', 'third_name', 'aplicante','name', 'job_title', 'job_id',
                #         'fourth_name','aprobador_ninel2', 'aprobador_ninel3', 'replicated_id', 'company_id']
                # new_vals = {required_key: vals[required_key] for required_key in keys if vals.get(required_key)}
                # _logger.error("SYNC CREATE EMPLOYEE: {}\n\nCREATE EMPLOYEE: {}".format(new_vals,vals))
                # vals = new_vals
                _logger.error(f"\nSEND TWO CREATE RES USERS: {vals}\n")
                vals = deal_local_regular_fields(self, vals)
                _logger.error(f"\nSEND THREE CREATE RES USERS: {vals}\n")
            # RES PARTNER
            if self._name == "res.partner":
                vals = deal_many_2_one(self, vals)
                vals = deal_local_regular_fields(self, vals)
                _logger.error(f"\nSEND ONE CREATE RES PARTNER: {vals}\n")
            # HR EMPLOYEE
            if self._name == "hr.employee":
                vals = deal_many_2_one(self, vals)
                # Filter keys for create hr.employee (sync only this fields)
                keys = [
                    "first_name",
                    "second_name",
                    "third_name",
                    "aplicante",
                    "name",
                    "job_title",
                    "job_id",
                    "fourth_name",
                    "aprobador_ninel2",
                    "aprobador_ninel3",
                    "replicated_id",
                    "company_id",
                ]
                new_vals = {
                    required_key: vals[required_key]
                    for required_key in keys
                    if vals.get(required_key)
                }
                _logger.error(
                    "SYNC CREATE EMPLOYEE: {}\n\nCREATE EMPLOYEE: {}".format(
                        new_vals, vals
                    )
                )
                vals = new_vals
            if self._name == "hr.resume.line":
                vals = deal_many_2_one(self, vals)
                if vals.get("employee_id"):
                    vals.pop("employee_id")
            # HR JOB
            if self._name == "hr.job":
                print(vals, "hr.job")
                if vals.get("cargo1"):
                    cargo1_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo1"))).replicated_id
                    )
                    if cargo1_rec:
                        vals.update({"cargo1": int(cargo1_rec)})
                if vals.get("cargo2"):
                    cargo2_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo2"))).replicated_id
                    )
                    if cargo2_rec:
                        vals.update({"cargo2": int(cargo2_rec)})
                if vals.get("cargo3"):
                    cargo3_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo3"))).replicated_id
                    )
                    if cargo3_rec:
                        vals.update({"cargo3": int(cargo3_rec)})
                if vals.get("cargo4"):
                    cargo4_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo4"))).replicated_id
                    )
                    if cargo4_rec:
                        vals.update({"cargo4": int(cargo4_rec)})
                if vals.get("cargo4"):
                    cargo4_rec = (
                        self.env["hr.job"].browse(int(vals.get("cargo4"))).replicated_id
                    )
                    if cargo4_rec:
                        vals.update({"cargo4": int(cargo4_rec)})
                if vals.get("jefe_inmediato_apl"):
                    jefe_inmediato_apl_rec = (
                        self.env["hr.job"]
                        .browse(int(vals.get("jefe_inmediato_apl")))
                        .replicated_id
                    )
                    if jefe_inmediato_apl_rec:
                        vals.update({"jefe_inmediato_apl": int(jefe_inmediato_apl_rec)})
                if vals.get("department_id"):
                    department_id_rec = (
                        self.env["hr.department"]
                        .browse(int(vals.get("department_id")))
                        .replicated_id
                    )
                    if department_id_rec:
                        vals.update({"department_id": int(department_id_rec)})
                if vals.get("activos_line"):
                    vals.pop("activos_line")
                if vals.get("formacion_esp"):
                    vals.pop("formacion_esp")
                if vals.get("formacion_line"):
                    vals.pop("formacion_line")
            if self._name == "formacion.cargos":
                vals.pop("job_id")
            if self._name == "activos":
                vals.pop("job_id")
            # REQUISICIONES
            if self._name == "requisiciones":
                vals = deal_many_2_one(self, vals)
            # HR APPLICANT
            if self._name == "hr.applicant":
                vals = deal_many_2_one(self, vals)
            if self._name == "formacion":
                vals = deal_many_2_one(self, vals)
                # vals.pop('applicant_id')
                # if vals.get('titulo_obtenido'):
                #     titulo_obtenido_rec = self.env['titulo'].browse(int(vals.get('titulo_obtenido'))).replicated_id
                #     if titulo_obtenido_rec:
                #         vals.update({'titulo_obtenido': int(titulo_obtenido_rec)})
            if self._name == "hijo":
                vals = deal_many_2_one(self, vals)
            if self._name == "lenguage":
                vals = deal_many_2_one(self, vals)
            if self._name == "mascotas":
                vals = deal_many_2_one(self, vals)
            # SURVEY.SURVEY
            if self._name == "survey.survey":
                vals = deal_many_2_one(self, vals)
            if self._name == "survey.question":
                vals = deal_many_2_one(self, vals)
            if self._name == "survey.user_input":
                vals = deal_many_2_one(self, vals)
            if self._name == "survey.user_input_line":
                vals = deal_many_2_one(self, vals)
            # MAIL ACTIVITY TYPE ~ NEW MODULE INSTALL in Main DATABASE
            if vals.get("mail.activity.type"):
                vals = deal_many_2_one(self, vals)
            # OTHER MODELS
            if self._name == "res.city":
                print(vals, "res city")
            if self._name == "direccion":
                print(vals, "direccion")
            if self._name == "fobias":
                print(vals, "fobias")
            if self._name == "hob":
                print(vals, "hob")
            if self._name == "alergia":
                print(vals, "alergia")
            if self._name == "cargo.desen":
                print(vals, "cargo desen")
            if self._name == "titulo":
                print(vals, "titulo")
            if self._name == "centro":
                print(vals, "centro")
            if self._name == "unidades":
                print(vals, "unidades")
            if self._name == "hr.department":
                print(vals, "Department")
            if self._name == "direccion":
                print(vals, "direccion")
            if self._name == "hr.department":
                print(vals, "department")

            replicated_id = target.execute_kw(
                db, uid, password, self._name, operation, [vals]
            )
            return replicated_id


def create_excute_o2m(self, model_name, operation, vals):
    model = self.env["ir.config_parameter"]
    url = model.sudo().get_param("database_sync.url")
    db = model.sudo().get_param("database_sync.db")
    username = model.sudo().get_param("database_sync.username")
    password = model.sudo().get_param("database_sync.password")
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
    common.version()
    uid = common.authenticate(db, username, password, {})
    target = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))
    try:
        target.execute_kw(db, uid, password, model_name, operation, [vals])
    except ValueError as e:
        _logger.error("%s" % e)
    return


def delete_excute_o2m(self, model_name, vals):
    model = self.env["ir.config_parameter"]
    url = model.sudo().get_param("database_sync.url")
    db = model.sudo().get_param("database_sync.db")
    username = model.sudo().get_param("database_sync.username")
    password = model.sudo().get_param("database_sync.password")
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
    common.version()
    uid = common.authenticate(db, username, password, {})
    target = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))
    try:
        records = target.execute_kw(db, uid, password, model_name, "search_read", vals)
    except ValueError as e:
        _logger.error("%s" % e)
    if records:
        for record in records:
            try:
                record = target.execute_kw(
                    db, uid, password, model_name, "unlink", [[record.get("id")]]
                )
            except ValueError as e:
                _logger.error("%s" % e)
    return


def delete_record(self, operation):
    model = self.env["ir.config_parameter"]
    url = model.sudo().get_param("database_sync.url")
    db = model.sudo().get_param("database_sync.db")
    username = model.sudo().get_param("database_sync.username")
    password = model.sudo().get_param("database_sync.password")
    if url and db and username and password:
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        common.version()
        uid = common.authenticate(db, username, password, {})
        target = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))
        record_id = int(self.replicated_id)
        record = target.execute_kw(
            db, uid, password, self._name, "search_read", [[["id", "=", record_id]]]
        )
        if record:
            result = target.execute_kw(
                db,
                uid,
                password,
                self._name,
                "write",
                [[record_id], {"replicated_id": False}],
            )
            target.execute_kw(db, uid, password, self._name, operation, [[record_id]])
            return


class JobSync(models.Model):
    _inherit = "hr.job"

    replicated_id = fields.Char(store=True)
    favorite_user_ids = fields.Many2many(
        "res.users", "job_favorite_user_rel", "job_id", "user_id"
    )

    @api.model
    def create(self, vals_list):
        if vals_list.get("favorite_user_ids"):
            vals_list.pop("favorite_user_ids")
        res = super(JobSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            try:
                replicated_id = connect_database(self, vals_list, operation)
                _logger.error(
                    "\nCREATE JOB\nFRAME: {} \nOPERATION: {} \nVALS_LIST: {}\n".format(
                        frame, operation, vals_list
                    )
                )
            except ValueError as e:
                _logger.error("%s" % e)
                _logger.error(
                    "\nCREATE JOB\nFRAME: {} \nOPERATION: {} \nVALS_LIST: {}\n".format(
                        frame, operation, vals_list
                    )
                )
            if replicated_id:
                res.replicated_id = replicated_id
            if res.activos_line:
                for activos in res.activos_line:
                    vals_activos = {
                        "job_id": res.replicated_id if res.replicated_id else False,
                        "categoria": activos.categoria if activos.categoria else False,
                        "activo_cargo": activos.activo_cargo
                        if activos.activo_cargo
                        else False,
                        "employee_id": activos.employee_id
                        if activos.employee_id
                        else False,
                        "cargo_job_id": activos.cargo_job_id
                        if activos.cargo_job_id
                        else False,
                    }
                    create_excute_o2m(self, "activos", "create", vals_activos)
            if res.formacion_esp:
                for formacion_cargo in res.formacion_esp:
                    vals_formacion_cargo = {
                        "job_id": res.replicated_id if res.replicated_id else False,
                        "formacion_especifica": formacion_cargo.formacion_especifica
                        if formacion_cargo.formacion_especifica
                        else False,
                        "certificado_academico": formacion_cargo.certificado_academico
                        if formacion_cargo.certificado_academico
                        else False,
                        "prueba_tecnica": formacion_cargo.prueba_tecnica
                        if formacion_cargo.prueba_tecnica
                        else False,
                        "certificado_laboral_funciones": formacion_cargo.certificado_laboral_funciones
                        if formacion_cargo.certificado_laboral_funciones
                        else False,
                    }
                    # for key in formacion_cargo.keys():
                    #     _logger.error("CREATE FORMACION.CARGO \n{}: {}".format(
                    #         key, formacion_cargo.get(key) if formacion_cargo.get(key) else False)
                    #         )
                    #     #Many2One fields
                    #     if key == 'job_id':
                    #         vals_formacion_cargo.update(
                    #             'job_id', res.replicated_id if res.replicated_id else False)
                    #     #other_fields
                    #     else:
                    #         vals_formacion_cargo.update(
                    #             key, formacion_cargo.get(key) if formacion_cargo.get(key) else False)
                    create_excute_o2m(
                        self, "formacion.cargos", "create", vals_formacion_cargo
                    )
        return res

    def write(self, vals):
        res = super(JobSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            try:
                connect_database(self, vals, operation)
                _logger.error(
                    "\nWRITE JOB\nFRAME: {} \nOPERATION: {} \nVALS_LIST: {}\n".format(
                        frame, operation, vals
                    )
                )
            except ValueError as e:
                _logger.error("%s" % e)
                _logger.error(
                    "\nWRITE JOB\nFRAME: {} \nOPERATION: {} \nVALS_LIST: {}\n".format(
                        frame, operation, vals
                    )
                )
            # Delete activos
            if self.replicated_id and self.activos_line:
                record_id = int(self.replicated_id)
                delete_excute_o2m(self, "activos", [[["job_id", "=", record_id]]])
                for activos in self.activos_line:
                    vals_activos = {
                        "job_id": self.replicated_id if self.replicated_id else False,
                        "categoria": activos.categoria if activos.categoria else False,
                        "activo_cargo": activos.activo_cargo
                        if activos.activo_cargo
                        else False,
                        "employee_id": activos.employee_id
                        if activos.employee_id
                        else False,
                        "cargo_job_id": activos.cargo_job_id
                        if activos.cargo_job_id
                        else False,
                    }
                    create_excute_o2m(self, "activos", "create", vals_activos)
            if self.replicated_id and self.formacion_esp:
                record_id = int(self.replicated_id)
                delete_excute_o2m(
                    self, "formacion.cargos", [[["job_id", "=", record_id]]]
                )
                for formacion_cargo in self.formacion_esp:
                    vals_formacion_cargo = {
                        "job_id": self.replicated_id if self.replicated_id else False,
                        "formacion_especifica": formacion_cargo.formacion_especifica
                        if formacion_cargo.formacion_especifica
                        else False,
                        "certificado_academico": formacion_cargo.certificado_academico
                        if formacion_cargo.certificado_academico
                        else False,
                        "prueba_tecnica": formacion_cargo.prueba_tecnica
                        if formacion_cargo.prueba_tecnica
                        else False,
                        "certificado_laboral_funciones": formacion_cargo.certificado_laboral_funciones
                        if formacion_cargo.certificado_laboral_funciones
                        else False,
                    }
                    # for key in formacion_cargo.read():
                    #     _logger.error("CREATE FORMACION.CARGO \n{}: {}".format(
                    #         key, formacion_cargo.get(key) if formacion_cargo.get(key) else False)
                    #         )
                    #     #Many2One fields
                    #     if key == 'job_id':
                    #         vals_formacion_cargo.update(
                    #             'job_id', res.replicated_id if res.replicated_id else False)
                    #     #other_fields
                    #     else:
                    #         vals_formacion_cargo.update(
                    #             key, formacion_cargo.get(key) if formacion_cargo.get(key) else False)
                    create_excute_o2m(
                        self, "formacion.cargos", "create", vals_formacion_cargo
                    )
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(JobSync, self).unlink()

    def copy(self):
        raise exceptions.ValidationError(
            "It is not possible duplicate this the record, please create a new one."
        )


class ApplicantSync(models.Model):
    _inherit = "hr.applicant"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        _logger.error("\n\n[1] CREATE APPLICANT: \nVALS:  {}".format(vals_list))
        res = super(ApplicantSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list.pop("created_user", None)
            _logger.error("\n\n[2]CREATE APPLICANT: \nVALS:  {}".format(vals_list))
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(ApplicantSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(ApplicantSync, self).unlink()


class RecruitmentStageSync(models.Model):
    _inherit = "hr.recruitment.stage"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        _logger.error("\n\n[1] CREATE STAGE \nVALS:  {}".format(vals_list))
        res = super(RecruitmentStageSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(RecruitmentStageSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(RecruitmentStageSync, self).unlink()


class ApplicantCategorySync(models.Model):
    _inherit = "hr.applicant.category"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(ApplicantCategorySync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(ApplicantCategorySync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(ApplicantCategorySync, self).unlink()


class RecruitmentDegreeSync(models.Model):
    _inherit = "hr.recruitment.degree"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(RecruitmentDegreeSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(RecruitmentDegreeSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(RecruitmentDegreeSync, self).unlink()


class RecruitmentSourceSync(models.Model):
    _inherit = "hr.recruitment.source"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(RecruitmentSourceSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            utm_source = (
                self.env["utm.source"].browse(vals_list.get("source_id")).replicated_id
            )
            vals_list["source_id"] = utm_source
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(RecruitmentSourceSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(RecruitmentSourceSync, self).unlink()


class UtmSourceSync(models.Model):
    _inherit = "utm.source"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(UtmSourceSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id

            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(UtmSourceSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(UtmSourceSync, self).unlink()


class DepartmentSync(models.Model):
    _inherit = "hr.department"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(DepartmentSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(DepartmentSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(DepartmentSync, self).unlink()


class ActivityTypeSync(models.Model):
    _inherit = "mail.activity.type"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        vals_list = deal_local_regular_fields(self, vals_list)
        res = super(ActivityTypeSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        vals = deal_local_regular_fields(self, vals)
        res = super(ActivityTypeSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(ActivityTypeSync, self).unlink()


class CitySync(models.Model):
    _inherit = "res.city"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        print(vals_list, "lop")
        res = super(CitySync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(CitySync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(CitySync, self).unlink()


class RequisicionesSync(models.Model):
    _inherit = "requisiciones"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(RequisicionesSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(RequisicionesSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(RequisicionesSync, self).unlink()

    def copy(self):
        raise exceptions.ValidationError(
            "It is not possible duplicate this the record, please create a new one."
        )


class UnidadesSync(models.Model):
    _inherit = "unidades"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(UnidadesSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(UnidadesSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(UnidadesSync, self).unlink()


class CentroSync(models.Model):
    _inherit = "centro"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(CentroSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(CentroSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(CentroSync, self).unlink()


class CalendarSync(models.Model):
    _inherit = "resource.calendar"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(CalendarSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(CalendarSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(CalendarSync, self).unlink()


class DireccionSync(models.Model):
    _inherit = "direccion"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(DireccionSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(DireccionSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(DireccionSync, self).unlink()


class EpsSync(models.Model):
    _inherit = "eps"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(EpsSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(EpsSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(EpsSync, self).unlink()


class AfpSync(models.Model):
    _inherit = "afp"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(AfpSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(AfpSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(AfpSync, self).unlink()


class AfcSync(models.Model):
    _inherit = "afc"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(AfcSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(AfcSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(AfcSync, self).unlink()


class HijoSync(models.Model):
    _inherit = "hijo"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(HijoSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(HijoSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(HijoSync, self).unlink()


class MascotasSync(models.Model):
    _inherit = "mascotas"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(MascotasSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(MascotasSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(MascotasSync, self).unlink()


class FobiasSync(models.Model):
    _inherit = "fobias"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(FobiasSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(FobiasSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(FobiasSync, self).unlink()


class HobSync(models.Model):
    _inherit = "hob"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(HobSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(HobSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(HobSync, self).unlink()


class AlergiaSync(models.Model):
    _inherit = "alergia"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(AlergiaSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(AlergiaSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(AlergiaSync, self).unlink()


class ResumeLineSync(models.Model):
    _inherit = "hr.resume.line"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(ResumeLineSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(ResumeLineSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(ResumeLineSync, self).unlink()


# class SurveyUserInputSync(models.Model):
#     _inherit = 'survey.user_input'

#     replicated_id = fields.Char(store=True)


# class SurveyUserInputLineSync(models.Model):
#     _inherit = 'survey.user_input_line'

#     replicated_id = fields.Char(store=True)


# class SurveyQuestionSync(models.Model):
#     _inherit = 'survey.question'

#     replicated_id = fields.Char(store=True)


class SurveySync(models.Model):
    _inherit = "survey.survey"

    replicated_id = fields.Char(store=True)


class PartnerSync(models.Model):
    _inherit = "res.partner"

    replicated_id = fields.Char(store=True)

    # @api.model
    # def create(self, vals_list):
    #     vals_list = deal_local_regular_fields(self, vals_list)
    #     res = super(PartnerSync, self).create(vals_list)
    #     if 'replicated_id' not in vals_list or vals_list.get('replicated_id') is False:
    #         model = self.env['ir.config_parameter']
    #         db = model.sudo().get_param('database_sync.db')
    #         main_db = model.sudo().get_param('database_sync.main_db')
    #         if db != main_db:
    #             frame = inspect.currentframe()
    #             operation = inspect.getframeinfo(frame).function
    #             vals_list['replicated_id'] = res.id
    #             replicated_id = connect_database(self, vals_list, operation)
    #             if replicated_id:
    #                 res.replicated_id = replicated_id
    #     return res

    # def write(self, vals):
    #     vals = deal_local_regular_fields(self, vals)
    #     res = super(PartnerSync, self).write(vals)
    #     if 'replicated_id' not in vals:
    #         frame = inspect.currentframe()
    #         operation = inspect.getframeinfo(frame).function
    #         connect_database(self, vals, operation)
    #     return res


class TituloSync(models.Model):
    _inherit = "titulo"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        print(vals_list, "titulo vals")
        res = super(TituloSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(TituloSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(TituloSync, self).unlink()


class EmployeeSync(models.Model):
    _inherit = "hr.employee"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(EmployeeSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(EmployeeSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(EmployeeSync, self).unlink()


class FormacionSync(models.Model):
    _inherit = "formacion"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(FormacionSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(FormacionSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(FormacionSync, self).unlink()


class LenguageSync(models.Model):
    _inherit = "lenguage"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        res = super(LenguageSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            vals_list["replicated_id"] = res.id
            replicated_id = connect_database(self, vals_list, operation)
            if replicated_id:
                res.replicated_id = replicated_id
        return res

    def write(self, vals):
        res = super(LenguageSync, self).write(vals)
        if "replicated_id" not in vals:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            connect_database(self, vals, operation)
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(LenguageSync, self).unlink()


class RequisicionStageSync(models.Model):
    _inherit = "requisicion.stage"

    replicated_id = fields.Char(store=True)


class CountrySync(models.Model):
    _inherit = "res.country"

    replicated_id = fields.Char(store=True)


class CountryStateSync(models.Model):
    _inherit = "res.country.state"

    replicated_id = fields.Char(store=True)


class CompanySync(models.Model):
    _inherit = "res.company"

    replicated_id = fields.Char(store=True)


class LangSync(models.Model):
    _inherit = "res.lang"

    replicated_id = fields.Char(store=True)


class ResUsersSync(models.Model):
    _inherit = "res.users"

    replicated_id = fields.Char(store=True)

    @api.model
    def create(self, vals_list):
        vals_list = deal_local_regular_fields(self, vals_list)
        res = super(ResUsersSync, self).create(vals_list)
        if "replicated_id" not in vals_list or vals_list.get("replicated_id") is False:
            # keys = ['login','company_id','partner_id']
            model = self.env["ir.config_parameter"]
            db = model.sudo().get_param("database_sync.db")
            main_db = model.sudo().get_param("database_sync.main_db")
            _logger.error(f"\nCREATE RES USERS: {vals_list}\n")
            if db != main_db:
                frame = inspect.currentframe()
                operation = inspect.getframeinfo(frame).function
                vals_list["replicated_id"] = res.id
                vals_list.update(
                    {"groups_id": [(6, 0, [self.env.ref("base.group_portal").id])]}
                )
                replicated_id = connect_database(self, vals_list, operation)
                if replicated_id:
                    res.replicated_id = replicated_id
        return res

    def unlink(self):
        if self and self.replicated_id:
            frame = inspect.currentframe()
            operation = inspect.getframeinfo(frame).function
            delete_record(self, operation)
        return super(ResUsersSync, self).unlink()


# class ResourceSync(models.Model):
#     _inherit = 'resource.resource'
#
#     replicated_id = fields.Char(store=True)


# class FormacionCargoSync(models.Model):
#     _inherit = 'formacion.cargos'

#     replicated_id = fields.Char(store=True)


# class ActivosSync(models.Model):
#     _inherit = 'activos'

#     replicated_id = fields.Char(store=True)
