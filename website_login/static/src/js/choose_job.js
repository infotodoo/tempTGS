odoo.define('website_login.fetch_job', function (require){
"use strict";
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
var ajax = require('web.ajax');

        $('#job_name').on('change', function() {
        if (this.value !== 'Elige un trabajo aplicado...')
        {   $('#job_details').show();
        }
        });

        $('#job_name').on('change', function() {
        if (this.value == 'Elige un trabajo aplicado...')
        {
          $('#job_details').hide();
        }});

// Section 0 ######################################################################

         $("input[name='ide'], input[name='numero_mascota'], input[name='identificacion'] ").on('input', function(e)
         {   $(this).val($(this).val().replace(/[^0-9]/g, '')); });

         $("input[name='wage'], input[name='tiempo_estudio'], input[name='porcent_dominio'] ").on('input', function(e)
         {   $(this).val($(this).val().replace(/[^0-9\.]/g, ''));
         });

         $("input[name='porcent_dominio'] ").on('input', function(e)
         {   if (this.value < 0){this.value = 0;}
                else if (this.value > 100) {this.value = 100;}
         });

         $("#valor_auxilio_alimentacion, #valor_aux_alimentacion_pro, #Valor_Auxili_de_Rodamiento, #valor_aux_rodamiento_pro, #Valor_Auxilio_de_Celular, #Valor_Medicina_Prepagada, #Valor_Bonos, #Valor_Comisiones, #Valor_Otro_Beneficio, #valor_aux_movilizacion").on('input', function(e)
         {   $(this).val($(this).val().replace(/[^0-9\.]/g, '')); });

         $("input[name='catidad_vacantes']").on('input', function(e)
         {   $(this).val($(this).val().replace(/[^0-9]/g, ''));
             if(this.value > 10){
             document.getElementById('masivo').value = 'SI'}
             else{document.getElementById('masivo').value = 'NO'}
             if((this.value == 0) && (this.value !== '')){
             alert("seleccione un número mayor que cero");
             }});

         $("input[name='cide']").on('input', function(e)
        { $(this).val($(this).val().replace(/[^0-9]/g, '')); });

        $("input[name='tiempo_de_contrato_inicial']").on('input', function(e)
        { $(this).val($(this).val().replace(/[^0-9]/g, ''));

         });

// Section 1 ######################################################################
         $('input[name="cide"], input[name="ide"] ').on('change', function()
         {
            var ide = document.getElementById('ide').value;
            var cide = document.getElementById('cide').value;
            if((cide !=='') && (ide !== ''))
            {   if(cide !== ide)
                {   alert("Los números de identificación no coinciden");
                document.getElementById('cide').value = ''
                }
             }
         });

         $('input[name="namef"]').on('change', function()
         {  var namef = document.getElementById('namef').value;
            document.getElementById('conf').value = namef
         });

         $('input[name="conf"]').on('change', function()
         {  var namef = document.getElementById('namef').value;
            var conf = document.getElementById('conf').value;
            if((namef !== '') && (conf !== ''))
            {   if(namef !== conf)
                {   alert("las fechas de nacimiento no coinciden");
                    document.getElementById('conf').value = ''
                }
            }
         });


         $('input[name="email_from"]').on('change', function()
         {  var email_from_check = document.getElementById('email_from').value;
            var testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
            if (testEmail.test(email_from_check))
            {
            var email_from = email_from_check;
            }else
            {
            alert("ha ingresado una dirección de correo electrónico no válida, intente nuevamente")
            document.getElementById('email_from').value = '';
            }
            });

        $('input[name="emal_cc"]').on('change', function()
         {
            var emal_cc_check = document.getElementById('emal_cc').value;
            var testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
            if (testEmail.test(emal_cc_check))
            {
             var emal_cc = emal_cc_check;
            }else
            {
            alert("ha ingresado una dirección de correo electrónico no válida, intente nuevamente")
            document.getElementById('emal_cc').value = '';
            }
            var email_from = document.getElementById('email_from').value;
            if((emal_cc != '') && (email_from != ''))
            {
            if((email_from !== '') && (typeof(emal_cc) !== 'undefined'))
            {   if(emal_cc !== email_from)
                {   alert("Los correos no concuerdan");
                    document.getElementById('emal_cc').value = ''
                }
            }}
         });
// Section 2 ######################################################################
        $('select[name="job_name"]').on('change', function() {
        if (this.value !== 'Choose a applied job...')
        {
            $('#job_details').show()
        }
        else{  $('#job_details').hide() }
        });
// Section 3 ######################################################################
        $('#direccion_dian, #nombre_via_principla, #via_generadora, #Predio, #complemento').on('change', function()
        {
        var direccion_dian_value = document.getElementById('direccion_dian')
        var direccion_dian = $(direccion_dian_value).children("option:selected")[0].getAttribute('data') || '';
        var nombre_via_principla = document.getElementById('nombre_via_principla').value;
        var via_generadora = document.getElementById('via_generadora').value;
        var Predio = document.getElementById('Predio').value;
        var complemento = document.getElementById('complemento').value;
        document.getElementById('dire_completo').value = ''.concat(direccion_dian, ' ', nombre_via_principla, ' ',
         via_generadora, ' ',  Predio, ' ', complemento).toUpperCase();
        });

        $("input[name='nombre_via_principla']").on('input', function(e)
        {
          $(this).val($(this).val().replace(/[^A-Z0-9\s]/gi, ''));
        });

        $("input[name='via_generadora']").on('input', function(e)
        {
          $(this).val($(this).val().replace(/[^A-Z0-9\s]/gi, ''));
        });

        $("input[name='Predio']").on('input', function(e)
        {
          $(this).val($(this).val().replace(/[^A-Z0-9\s]/gi, ''));
        });

        $("input[name='complemento']").on('input', function(e)
        {
          $(this).val($(this).val().replace(/[^A-Z0-9\s]/gi, ''));
        });
// Section 4 ######################################################################
         $('#tipo_vivienda').on('change', function(){
         if(this.value == 'OTRO')
         {
            $('#otro, #otro1').show()
            document.getElementById("cual_tipo_vivienda").required = true;
         }else{ $('#otro, #otro1').hide()
                document.getElementById("cual_tipo_vivienda").required = false;   }
         });
// Section 5 ######################################################################
         $('#carac_vivienda').on('change', function(){
         if(this.value == 'OTRO')
         {
            $('#otro_a, #otro_b').show()
            document.getElementById("cual_carc_vivienda").required = true;
         }else{ $('#otro_a, #otro_b').hide()
                document.getElementById("cual_carc_vivienda").required = false;   }
         });

         $("input[name='partner_mobile']").on('input', function(e)
         {   $(this).val($(this).val().replace(/[^0-9]/g, ''));
             $(this).val($(this).val().replace(/^\d{11}$/, ''));
         });

         $("input[name='partner_phone']").on('input', function(e)
         {   $(this).val($(this).val().replace(/[^0-9]/g, ''));
             $(this).val($(this).val().replace(/^\d{11}$/, ''));
         });
// Section 6 ######################################################################
         $('#parentesco').on('change', function(){
         if(this.value == 'OTRO')
         {
            $('#otro_c, #otro_d').show()
            document.getElementById("Cual_Parentezco").required = true;
         }else{ $('#otro_c, #otro_d').hide()
                document.getElementById("Cual_Parentezco").required = false;   }
         });
// Section 7 ######################################################################
        $('#no_personas_nucleo_familiar').on('input', function(e)
        {   $(this).val($(this).val().replace(/[^0-9]/g, '')); });

        $('#no_personas_estado_incapacidad').on('input', function(e)
        {   $(this).val($(this).val().replace(/[^0-9]/g, '')); });
// Section 8 ######################################################################
         $('#estado_civil').on('change', function(){
         if((this.value == 'CASADO/A') || (this.value == 'UNIÓN LIBRE') )
         {  $('#estado_div').show()
            document.getElementById('primer_apellido_conyugue').required = true;
            document.getElementById('primer_nombre_conyugue').required = true;
            document.getElementById('escolaridad_conyugue').required = true;
            document.getElementById('genero_conyugue').required = true;
            document.getElementById('lugar_nacimiento_conyugue').required = true;
            document.getElementById('pais_nacimiento_conyugue').required = true;
            document.getElementById('fecha_conyugue').required = true;
         }else{ $('#estado_div').hide()
            document.getElementById('primer_apellido_conyugue').required = false;
            document.getElementById('primer_nombre_conyugue').required = false;
            document.getElementById('escolaridad_conyugue').required = false;
            document.getElementById('genero_conyugue').required = false;
            document.getElementById('lugar_nacimiento_conyugue').required = false;
            document.getElementById('pais_nacimiento_conyugue').required = false;
            document.getElementById('fecha_conyugue').required = false;
         }});
// Section 9 ######################################################################
        $('#via_principal_con, #nombre_via_principal_cont, #via_generadora_con, #predio_con, #complemento_con').on('change', function()
        {
        var via_principal_con_value = document.getElementById('via_principal_con')
        var via_principal_con = $(via_principal_con_value).children("option:selected")[0].getAttribute('data') || '';
        var nombre_via_principal_cont = document.getElementById('nombre_via_principal_cont').value;
        var via_generadora_con = document.getElementById('via_generadora_con').value;
        var predio_con = document.getElementById('predio_con').value;
        var complemento_con = document.getElementById('complemento_con').value;
        document.getElementById('direccion_contacto').value = ''.concat(via_principal_con, ' ',
            nombre_via_principal_cont, ' ', via_generadora_con, ' ',  predio_con, ' ', complemento_con).toUpperCase();
        });
        $("input[name='nombre_via_principal_cont']").on('input', function(e)
        {
          $(this).val($(this).val().replace(/[^A-Z0-9\s]/gi, ''));
        });

        $("input[name='via_generadora_con']").on('input', function(e)
        {
          $(this).val($(this).val().replace(/[^A-Z0-9\s]/gi, ''));
        });

        $("input[name='predio_con']").on('input', function(e)
        {
          $(this).val($(this).val().replace(/[^A-Z0-9\s]/gi, ''));
        });

        $("input[name='complemento_con']").on('input', function(e)
        {
          $(this).val($(this).val().replace(/[^A-Z0-9\s]/gi, ''));
        });
// Section 10 ######################################################################
         $('#tipo_contrato').on('change', function(){
         if(this.value == 'OBRA LABOR')
         {
            $('#tipo_contrato_a, #tipo_contrato_b').show()
            $('#tipo_contrato_c, #tipo_contrato_d').show()
            document.getElementById("cliente1").required = true;
            document.getElementById("no_contrato_comercial").required = true;
         }else{ $('#tipo_contrato_a, #tipo_contrato_b').hide()
                $('#tipo_contrato_c, #tipo_contrato_d').hide()
                document.getElementById("cliente1").required = false;
                document.getElementById("no_contrato_comercial").required = false;}
         if((this.value =='FIJO') || (this.value == 'MEDIO TIEMPO'))
         {
            document.getElementById("tiempo_de_contrato_inicial").required = true;
            document.getElementById("tiempo_de_contrato_inicial").value = 0;
            document.getElementById("rango").required = true;
            $('#contrato_inicial_div_a').show()
            $('#contrato_inicial_div_b').show()
            $('#rango_visible').show();
            $('#rango_div').addClass('o_website_form_required_custom');
         }else{ document.getElementById("tiempo_de_contrato_inicial").required = false;
                document.getElementById("tiempo_de_contrato_inicial").value = '';
                document.getElementById("rango").required = false;
                $('#contrato_inicial_div_a').hide()
                $('#contrato_inicial_div_b').hide()
                $('#rango_visible').hide();
                $('#rango_div').removeClass('o_website_form_required_custom');}
         });
// Section 11 ######################################################################
         $('#nivel_riesgo_arl').on('change', function(){
         if(this.value == '1 RIESGO I')
         {  document.getElementById("nivel_riesgo").value = '0.522%';
         }else if(this.value == '2 RIESGO II')
         {  document.getElementById("nivel_riesgo").value = '1.044%';
         }else if(this.value == '3 RIESGO III')
         {  document.getElementById("nivel_riesgo").value = '2.436%';
         }else if(this.value == '4 RIESGO IV')
         {  document.getElementById("nivel_riesgo").value = '4.350%';
         }else if(this.value == '5 RIESGO V')
         {  document.getElementById("nivel_riesgo").value = '6.960%'; }
         });

// Section 12 ######################################################################
        $('#wage, #tipo_de_salario').on('change', function(){
            var tipo_de_salario = document.getElementById("tipo_de_salario").value;
            var wage = document.getElementById("wage").value;
            if ((tipo_de_salario == 'SUELDO BÁSICO') && (wage !== '') && (wage < 877803))
            {
            alert("El Salario Básico debe ser mayor a 877803")
            document.getElementById("wage").value = ''
            }else if ((tipo_de_salario == 'SALARIO INTEGRAL') && (wage !== '') && (wage < 11411439))
            {
            alert("El Salario Integral debe ser mayor a 11411439")
            document.getElementById("wage").value = ''
            }
        });

// Section 13 ######################################################################
         $('#aux_alimentacion').on('change', function(){
         if(this.value == 'SI')
         {
            $('#aux_alimentacion_a, #aux_alimentacion_b').show()
            $('#aux_alimentacion_c, #aux_alimentacion_d').show()
            document.getElementById("valor_auxilio_alimentacion").required = true;
            document.getElementById("auxilio_de_alimentacion_a_partir_de").required = true;
         }else{ $('#aux_alimentacion_a, #aux_alimentacion_b').hide()
                $('#aux_alimentacion_c, #aux_alimentacion_d').hide()
                document.getElementById("valor_auxilio_alimentacion").required = false;
                document.getElementById("auxilio_de_alimentacion_a_partir_de").required = true;}
         });

         $('#lic_conducir').on('change', function(){
         if(this.value == 'SI')
         {
            $('#conducir_a, #conducir_b').show()
            document.getElementById("tipo_lic_conducir").required = true;
         }else{ $('#conducir_a, #conducir_b').hide()
                document.getElementById("tipo_lic_conducir").required = false;
         }});

// Section 14 ######################################################################
        $('#aux_alimentacion_pro').on('change', function(){
         if(this.value == 'SI')
         {
            $('#aux_alimentacion_pro_a, #aux_alimentacion_pro_b').show()
            $('#aux_alimentacion_pro_c, #aux_alimentacion_pro_d').show()
            document.getElementById("valor_aux_alimentacion_pro").required = true;
            document.getElementById("aux_alimentacion_pro_partir").required = true;
         }else{ $('#aux_alimentacion_pro_a, #aux_alimentacion_pro_b').hide()
                $('#aux_alimentacion_pro_c, #aux_alimentacion_pro_d').hide()
                document.getElementById("valor_aux_alimentacion_pro").required = false;
                document.getElementById("aux_alimentacion_pro_partir").required = false; }
         });
// Section 15 ######################################################################
         $('#aux_rodamiento').on('change', function(){
         if(this.value == 'SI')
         {
            $('#aux_rodamiento_a, #aux_rodamiento_b').show()
            $('#aux_rodamiento_c, #aux_rodamiento_d').show()
            document.getElementById("Valor_Auxili_de_Rodamiento").required = true;
            document.getElementById("Auxilio_de_Rodamiento_a_partir_de").required = true;
         }else{ $('#aux_rodamiento_a, #aux_rodamiento_b').hide()
                $('#aux_rodamiento_c, #aux_rodamiento_d').hide()
                document.getElementById("Valor_Auxili_de_Rodamiento").required = false;
                document.getElementById("Auxilio_de_Rodamiento_a_partir_de").required = false; }
         });
// Section 16 ######################################################################
        $('#aux_rodamiento_pro').on('change', function(){
         if(this.value == 'SI')
         {
            $('#aux_rodamiento_pro_a, #aux_rodamiento_pro_b').show()
            $('#aux_rodamiento_pro_c, #aux_rodamiento_pro_d').show()
            document.getElementById("valor_aux_rodamiento_pro").required = true;
            document.getElementById("aux_rodamiento_pro_partir").required = true;
         }else{ $('#aux_rodamiento_pro_a, #aux_rodamiento_pro_b').hide()
                $('#aux_rodamiento_pro_c, #aux_rodamiento_pro_d').hide()
                document.getElementById("valor_aux_rodamiento_pro").required = false;
                document.getElementById("aux_rodamiento_pro_partir").required = false; }
         });
// Section 17 ######################################################################
        $('#aux_celular').on('change', function(){
         if(this.value == 'SI')
         {
            $('#aux_celular_a, #aux_celular_b').show()
            $('#aux_celular_c, #aux_celular_d').show()
            document.getElementById("Valor_Auxilio_de_Celular").required = true;
            document.getElementById("Auxilio_de_Celular_a_partir_de").required = true;
         }else{ $('#aux_celular_a, #aux_celular_b').hide()
                $('#aux_celular_c, #aux_celular_d').hide()
                document.getElementById("Valor_Auxilio_de_Celular").required = false;
                document.getElementById("Auxilio_de_Celular_a_partir_de").required = false; }
         });
// Section 18 ######################################################################
        $('#medicina_prepagada').on('change', function(){
         if(this.value == 'SI')
         {
            $('#medicina_prepagada_a, #medicina_prepagada_b').show()
            $('#medicina_prepagada_c, #medicina_prepagada_d').show()
            document.getElementById("Valor_Medicina_Prepagada").required = true;
            document.getElementById("Medicina_Prepagada_a_partir_de").required = true;
         }else{ $('#medicina_prepagada_a, #medicina_prepagada_b').hide()
                $('#medicina_prepagada_c, #medicina_prepagada_d').hide()
                document.getElementById("Valor_Medicina_Prepagada").required = false;
                document.getElementById("Medicina_Prepagada_a_partir_de").required = false; }
         });
// Section 19 ######################################################################
        $('#comisiones').on('change', function(){
         if(this.value == 'SI')
         {
            $('#comisiones_a, #comisiones_b').show()
            $('#comisiones_c, #comisiones_d').show()
            document.getElementById("Valor_Comisiones").required = true;
            document.getElementById("Comisiones_a_partir_de").required = true;
         }else{ $('#comisiones_a, #comisiones_b').hide()
                $('#comisiones_c, #comisiones_d').hide()
                document.getElementById("Valor_Comisiones").required = false;
                document.getElementById("Comisiones_a_partir_de").required = false; }
         });
// Section 20 ######################################################################
        $('#comisiones').on('change', function(){
         if(this.value == 'SI')
         {
            $('#comisiones_a, #comisiones_b').show()
            $('#comisiones_c, #comisiones_d').show()
            document.getElementById("Valor_Comisiones").required = true;
            document.getElementById("Comisiones_a_partir_de").required = true;
         }else{ $('#comisiones_a, #comisiones_b').hide()
                $('#comisiones_c, #comisiones_d').hide()
                document.getElementById("Valor_Comisiones").required = false;
                document.getElementById("Comisiones_a_partir_de").required = false; }
         });
// Section 21 ######################################################################
        $('#otro').on('change', function(){
         if(this.value == 'SI')
         {
            $('#otro_a, #otro_b').show()
            $('#otro_c, #otro_d').show()
            $('#otro_e, #otro_f').show()
            document.getElementById("cual_Otro_Beneficio").required = true;
            document.getElementById("Valor_Otro_Beneficio").required = true;
            document.getElementById("Otro_Beneficio_a_partir_de").required = true;
         }else{ $('#otro_a, #otro_b').hide()
                $('#otro_c, #otro_d').hide()
                $('#otro_e, #otro_f').hide()
                document.getElementById("cual_Otro_Beneficio").required = false;
                document.getElementById("Valor_Otro_Beneficio").required = false;
                document.getElementById("Otro_Beneficio_a_partir_de").required = true;}
         });
// Section 22 ######################################################################
        $('#aux_movilizacion').on('change', function(){
         if(this.value == 'SI')
         {
            $('#aux_movilizacion_a, #aux_movilizacion_b').show()
            $('#aux_movilizacion_c, #aux_movilizacion_d').show()
            document.getElementById("valor_aux_movilizacion").required = true;
            document.getElementById("aux_movilizacion_a_partir").required = true;
         }else{ $('#aux_movilizacion_a, #aux_movilizacion_b').hide()
                $('#aux_movilizacion_c, #aux_movilizacion_d').hide()
                document.getElementById("valor_aux_movilizacion").required = false;
                document.getElementById("aux_movilizacion_a_partir").required = false; }
         });
// Section 23 ######################################################################
        $('#bonos').on('change', function(){
         if(this.value == 'SI')
         {
            $('#bonos_a, #bonos_b').show()
            $('#bonos_c, #bonos_d').show()
            document.getElementById("Valor_Bonos").required = true;
            document.getElementById("Bonos_a_partir_de").required = true;
         }else{ $('#bonos_a, #bonos_b').hide()
                $('#bonos_c, #bonos_d').hide()
                document.getElementById("Valor_Bonos").required = false;
                document.getElementById("Bonos_a_partir_de").required = false; }
         });
// Section 24 ######################################################################
        $('#add_hijo').on('click', function(){
        var nombre_hijo = document.getElementById("nombre_hijo").value || alert("Nombre del hijo es requerido")
        var segundo_nombre = document.getElementById("segundo_nombre").value || ''
        var primer_apellido = document.getElementById("primer_apellido").value || alert("Primer Apellido es requerido")
        var segundo_apellido = document.getElementById("segundo_apellido").value || ''
        var identificacion = document.getElementById("identificacion").value || alert("Identificación es requerido")
        var nivel_escolaridad_hijo = document.getElementById("nivel_escolaridad_hijo").value || alert("Escolaridad es requerido")
        var ocupacion_hijo = document.getElementById("ocupacion_hijo").value || alert("Ocupación es requerido")
        var fecha_nac_hijo = document.getElementById("fecha_nac_hijo").value || alert("Fecha de nacimiento del hijo es requerido")
        var genero_hijo = document.getElementById("genero_hijo").value || alert("Genero es requerido")
        var grupo_sanguineo = document.getElementById("grupo_sanguineo").value || alert("Grupo Sanguíneo es requerido")
        var nacionalidad = document.getElementById("nacionalidad").value || alert("Nacionalidad es requerido")
        var pais_nacimiento = document.getElementById("pais_nacimiento").value || alert("País de Nacimiento es requerido")
        var hijastro = document.getElementById("hijastro").value || alert("Hijastro es requerido")

        if((typeof(nombre_hijo) !== 'undefined') && (typeof(primer_apellido) !== 'undefined') && (typeof(identificacion) !== 'undefined') && (typeof(nivel_escolaridad_hijo) !== 'undefined') && (typeof(ocupacion_hijo) !== 'undefined') && (typeof(fecha_nac_hijo) !== 'undefined') && (typeof(genero_hijo) !== 'undefined') && (typeof(grupo_sanguineo) !== 'undefined') && (typeof(nacionalidad) !== 'undefined') && (typeof(pais_nacimiento) !== 'undefined') && (typeof(hijastro) !== 'undefined'))
        {
        var id = parseInt(document.getElementById("no_of_hijos").value)
            id +=1;
            document.getElementById("no_of_hijos").value = id;
        var dict = {
        'id': id,
        'nombre_hijo': nombre_hijo,
        'segundo_nombre': segundo_nombre,
        'primer_apellido': primer_apellido,
        'segundo_apellido': segundo_apellido,
        'identificacion': identificacion,
        'nivel_escolaridad_hijo': nivel_escolaridad_hijo,
        'ocupacion_hijo': ocupacion_hijo,
        'fecha_nac_hijo': fecha_nac_hijo,
        'genero_hijo': genero_hijo,
        'grupo_sanguineo': grupo_sanguineo,
        'nacionalidad': nacionalidad,
        'pais_nacimiento': pais_nacimiento,
        'hijastro': hijastro,
        }
        var hijo = document.getElementById("hijos_Line").value;
        if (hijo == ''){
        document.getElementById("hijos_Line").value = hijo.concat(JSON.stringify(dict));
        }else{
        document.getElementById("hijos_Line").value = hijo.concat(',',JSON.stringify(dict));
        }
        alert("Se agrega información de Los Hijos");

        $('#hijos_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" + dict['nombre_hijo'] + "</td><td>" +
        dict['segundo_nombre'] + "</td><td>" + dict['primer_apellido'] + "</td><td>" + dict['segundo_apellido'] +
        "</td><td style='width: 2px;'><a class='btn btn-primary btn-l hijos-remove'>remove</a></td></tr>");
        $('.hijos-remove').unbind("click").click(function(ev)
       {
          ev.preventDefault();
          var tr_element = $(ev.currentTarget).parents().eq(1)[0]
          var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
          $(tr_element).css("display", "none");
          var to_remove = document.getElementById('hijos_to_remove').value;
          if (to_remove === '')
          {     var list_ids = new Array();
                list_ids.push(id_to_remove)
                document.getElementById('hijos_to_remove').value = JSON.stringify(list_ids);
                return;
          }else
          {     var new_value = JSON.parse(to_remove)
                new_value.push(id_to_remove)
                document.getElementById('hijos_to_remove').value = JSON.stringify(new_value);
                return;
          }
          $(tr_element).css("display", "none");
      });

        document.getElementById("nombre_hijo").value = '';
        document.getElementById("segundo_nombre").value = '';
        document.getElementById("primer_apellido").value = '';
        document.getElementById("segundo_apellido").value = '';
        document.getElementById("identificacion").value = '';
        document.getElementById("nivel_escolaridad_hijo").value = '';
        document.getElementById("ocupacion_hijo").value = '';
        document.getElementById("fecha_nac_hijo").value = '';
        document.getElementById("genero_hijo").value = '';
        document.getElementById("grupo_sanguineo").value = '';
        document.getElementById("nacionalidad").value = '';
        document.getElementById("pais_nacimiento").value = '';
        document.getElementById("hijastro").value = '';
        var hijo = document.getElementById("hijos_Line").value;
        document.getElementById("nombre_hijo").required = false;
        document.getElementById("primer_apellido").required = false;
        document.getElementById("identificacion").required = false;
        document.getElementById("nivel_escolaridad_hijo").required = false;
        document.getElementById("ocupacion_hijo").required = false;
        document.getElementById("fecha_nac_hijo").required = false;
        document.getElementById("grupo_sanguineo").required = false;
        document.getElementById("genero_hijo").required = false;
        document.getElementById("nacionalidad").required = false;
        document.getElementById("pais_nacimiento").required = false;
        document.getElementById("hijastro").required = false;

        var hijo_records = '['.concat(hijo, ']');
        document.getElementById("hijos_Line").value = hijo_records;
        document.getElementById( 'add_hijos_div' ).style.display = 'none';
        $('#add_another_hijo').show()
        }
        });

        $('#cancel_hijos').on('click', function(){
        var hijo = document.getElementById("hijos_Line").value;
        document.getElementById("nombre_hijo").required = false;
        document.getElementById("primer_apellido").required = false;
        document.getElementById("identificacion").required = false;
        document.getElementById("nivel_escolaridad_hijo").required = false;
        document.getElementById("ocupacion_hijo").required = false;
        document.getElementById("fecha_nac_hijo").required = false;
        document.getElementById("grupo_sanguineo").required = false;
        document.getElementById("genero_hijo").required = false;
        document.getElementById("nacionalidad").required = false;
        document.getElementById("pais_nacimiento").required = false;
        document.getElementById("hijastro").required = false;

        var hijo_records = '['.concat(hijo, ']');
        document.getElementById("hijos_Line").value = hijo_records;
        document.getElementById( 'add_hijos_div' ).style.display = 'none';
        $('#add_another_hijo').show()
        });




// Section 25 ######################################################################
        $('#add_hijo_button').on('click', function(){
        document.getElementById( 'add_hijos_div' ).style.display = '';

        document.getElementById("nombre_hijo").required = true;
        document.getElementById("primer_apellido").required = true;
        document.getElementById("identificacion").required = true;
        document.getElementById("nivel_escolaridad_hijo").required = true;
        document.getElementById("ocupacion_hijo").required = true;
        document.getElementById("fecha_nac_hijo").required = true;
        document.getElementById("grupo_sanguineo").required = true;
        document.getElementById("genero_hijo").required = true;
        document.getElementById("nacionalidad").required = true;
        document.getElementById("pais_nacimiento").required = true;
        document.getElementById("hijastro").required = true;

        var hijo = document.getElementById("hijos_Line").value;
        var hijo_records = hijo.substring(1, hijo.length-1);
        document.getElementById("hijos_Line").value = hijo_records;
        $('#add_another_hijo').hide()
        });
// Section 26 ######################################################################

        $('#add_mascotas_line').on('click', function(){
        var tipo_mascota = document.getElementById("tipo_mascota").value || alert("Tipo de Mascota es requerido")
        var numero_mascota = document.getElementById("numero_mascota").value || alert("numero_mascota es requerido")


        if((typeof(tipo_mascota) !== 'undefined') && (typeof(numero_mascota) !== 'undefined'))
        {
        var id = parseInt(document.getElementById("no_of_mascotas").value)
            id +=1;
            document.getElementById("no_of_mascotas").value = id;

        var dict = {    'id': id,
                        'tipo_mascota': tipo_mascota,
                        'numero_mascota': numero_mascota, }
        var mascotas = document.getElementById("mascotas_lines").value;
        if (mascotas == ''){
        document.getElementById("mascotas_lines").value = mascotas.concat(JSON.stringify(dict));
        }else{
        document.getElementById("mascotas_lines").value = mascotas.concat(',',JSON.stringify(dict));
        }
        alert("Se agrega información de mascotas");

        $('#mascotas_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" +
        dict['tipo_mascota'] + "</td><td>"+ dict['numero_mascota'] +"</td><td><td><a class='btn btn-primary btn-l mascotas-remove'>remove</a></td></tr>");

           $('.mascotas-remove').unbind("click").click(function(ev)
           {
               ev.preventDefault();
              var tr_element = $(ev.currentTarget).parents().eq(1)[0]
              var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
              $(tr_element).css("display", "none");
              var to_remove = document.getElementById('mascotas_to_remove').value;
              if (to_remove === '')
              {     var list_ids = new Array();
                    list_ids.push(id_to_remove)
                    document.getElementById('mascotas_to_remove').value = JSON.stringify(list_ids);
                    return;
              }else
              {     var new_value = JSON.parse(to_remove)
                    new_value.push(id_to_remove)
                    document.getElementById('mascotas_to_remove').value = JSON.stringify(new_value);
                    return;
              }
              $(tr_element).css("display", "none");
          });

        document.getElementById("tipo_mascota").value = '';
        document.getElementById("numero_mascota").value = '';
        document.getElementById("tipo_mascota").required = false;
        document.getElementById("numero_mascota").required = false;
        var mascotas = document.getElementById("mascotas_lines").value;
        var mascotas_records = '['.concat(mascotas, ']');
        document.getElementById("mascotas_lines").value = mascotas_records;
        document.getElementById( 'add_mascotas_lines_div' ).style.display = 'none';
        $('#add_another_mascotas').show()
        }
        });

        $('#cancel_mascotas').on('click', function(){
        document.getElementById("tipo_mascota").required = false;
        document.getElementById("numero_mascota").required = false;
        var mascotas = document.getElementById("mascotas_lines").value;
        var mascotas_records = '['.concat(mascotas, ']');
        document.getElementById("mascotas_lines").value = mascotas_records;
        document.getElementById( 'add_mascotas_lines_div' ).style.display = 'none';
        $('#add_another_mascotas').show()
        });


// Section 27 ######################################################################
        $('#add_mascotas_button').on('click', function(){
        document.getElementById( 'add_mascotas_lines_div' ).style.display = '';
        document.getElementById("tipo_mascota").required = true;
        document.getElementById("numero_mascota").required = true;
        var mascotas = document.getElementById("mascotas_lines").value;
        var mascotas_records = mascotas.substring(1, mascotas.length-1);
        document.getElementById("mascotas_lines").value = mascotas_records;
        $('#add_another_mascotas').hide()
        });

// Section 28 ######################################################################
        var form = document.getElementById("edit_applied_jobs");
        $("#enviar_form").on("click", function () {
        form.submit();
        });
// Section 29 ######################################################################
        $('#add_resume_line').on('click', function(){
        var name = document.getElementById("name").value || alert("Nombre es requerido")
        var rama_empresa_laboro = document.getElementById("rama_empresa_laboro").value || alert("Rama de la Empresa en la que Laboró es requerido")
        var cargo_desempenado = document.getElementById("cargo_desempenado").value || alert("Cargo Desempeñado es requerido")
        var Tipo_de_Contrato = document.getElementById("Tipo_de_Contrato").value || alert("Tipo de Contrato es requerido")
        var pais = document.getElementById("pais").value || alert("País es requerido")
        var actualmente_laborando = document.getElementById("actualmente_laborando").value || alert("Actualmente Laborando es requerido")
        var date_start = document.getElementById("date_start").value || alert("Fecha de inicio es requerido")
        var date_end = document.getElementById("date_end").value || ''


        if((typeof(name) !== 'undefined') && (typeof(rama_empresa_laboro) !== 'undefined') && (typeof(cargo_desempenado) !== 'undefined') && (typeof(Tipo_de_Contrato) !== 'undefined') && ((typeof(pais) !== 'undefined')) && ((typeof(actualmente_laborando) !== 'undefined')) && ((typeof(date_start) !== 'undefined')))
        {
        var id = parseInt(document.getElementById("no_of_resume_line").value)
            id +=1;
            document.getElementById("no_of_resume_line").value = id;
        var dict = {    'id': id,
                        'name': name,
                        'rama_empresa_laboro': rama_empresa_laboro,
                        'cargo_desempenado': cargo_desempenado,
                        'Tipo_de_Contrato': Tipo_de_Contrato,
                        'pais': pais,
                        'actualmente_laborando': actualmente_laborando,
                        'date_start': date_start,
                        'date_end': date_end,
                        }
        var resume_line = document.getElementById("resume_line_ids").value;
        if (resume_line == ''){
        document.getElementById("resume_line_ids").value = resume_line.concat(JSON.stringify(dict));
        }else{
        document.getElementById("resume_line_ids").value = resume_line.concat(',',JSON.stringify(dict));
        }
        alert("Se agrega información sobre experiencia laboral y certificados");

        $('#resume_line_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" + dict['name'] +
        "</td><td style='width: 2px;'><a class='btn btn-primary btn-l resume_line-remove'>remove</a></td></tr>");
        $('.resume_line-remove').unbind("click").click(function(ev)
       {
          ev.preventDefault();
          var tr_element = $(ev.currentTarget).parents().eq(1)[0]
          var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
          $(tr_element).css("display", "none");
          var to_remove = document.getElementById('resume_line_to_remove').value;
          if (to_remove === '')
          {     var list_ids = new Array();
                list_ids.push(id_to_remove)
                document.getElementById('resume_line_to_remove').value = JSON.stringify(list_ids);
                return;
          }else
          {     var new_value = JSON.parse(to_remove)
                new_value.push(id_to_remove)
                document.getElementById('resume_line_to_remove').value = JSON.stringify(new_value);
                return;
          }
          $(tr_element).css("display", "none");
      });

        document.getElementById("name").value = '';
        document.getElementById("rama_empresa_laboro").value = '';
        document.getElementById("cargo_desempenado").value = '';
        document.getElementById("Tipo_de_Contrato").value = '';
        document.getElementById("pais").value = '';
        document.getElementById("actualmente_laborando").value = '';
        document.getElementById("date_start").value = '';
        document.getElementById("date_end").value = '';

        document.getElementById("name").required = false;
        document.getElementById("rama_empresa_laboro").required = false;
        document.getElementById("cargo_desempenado").required = false;
        document.getElementById("Tipo_de_Contrato").required = false;
        document.getElementById("pais").required = false;
        document.getElementById("actualmente_laborando").required = false;
        document.getElementById("date_start").required = false;


        var resume_line = document.getElementById("resume_line_ids").value;
        var resme_line_records = '['.concat(resume_line, ']');
        document.getElementById("resume_line_ids").value = resme_line_records;
        document.getElementById( 'add_resume_lines_div' ).style.display = 'none';
        $('#add_another_resume').show()
        }
        });

        $('#cancel_resume_line').on('click', function(){
        document.getElementById("name").required = false;
        document.getElementById("rama_empresa_laboro").required = false;
        document.getElementById("cargo_desempenado").required = false;
        document.getElementById("Tipo_de_Contrato").required = false;
        document.getElementById("pais").required = false;
        document.getElementById("actualmente_laborando").required = false;
        document.getElementById("date_start").required = false;
        var resume_line = document.getElementById("resume_line_ids").value;
        var resme_line_records = '['.concat(resume_line, ']');
        document.getElementById("resume_line_ids").value = resme_line_records;
        document.getElementById( 'add_resume_lines_div' ).style.display = 'none';
        $('#add_another_resume').show()
        });

// Section 30 ######################################################################

        $('#add_resume_button').on('click', function(){
        document.getElementById( 'add_resume_lines_div' ).style.display = '';
        document.getElementById("name").required = true;
        document.getElementById("rama_empresa_laboro").required = true;
        document.getElementById("cargo_desempenado").required = true;
        document.getElementById("Tipo_de_Contrato").required = true;
        document.getElementById("pais").required = true;
        document.getElementById("actualmente_laborando").required = true;
        document.getElementById("date_start").required = true;

        var resume_line = document.getElementById("resume_line_ids").value;
        var resme_line_records = resume_line.substring(1, resume_line.length-1);
        document.getElementById("resume_line_ids").value = resme_line_records;
        $('#add_another_resume').hide()
        });
// Section 31 ######################################################################
        $('#estado_formacion').on('change', function(){
         if(this.value == 'COMPLETADO')
         {
         document.getElementById("fecha_graduacion").required = true;
         $('#estado_formacion_diva').show()
         $('#estado_formacion_divb').show()
         }else{
         document.getElementById("fecha_graduacion").required = false;
         $('#estado_formacion_diva').hide()
         $('#estado_formacion_divb').hide()
         }
         });

        $('#add_formacion_line').on('click', function(){
        var formacion = document.getElementById("formacion").value || alert("Formación es requerido")
        var estudia_actualmente_for = document.getElementById("estudia_actualmente_for").value || alert("Estudia Actualmente es requerido")
        var nombre_institucion = document.getElementById("nombre_institucion").value || alert("Nombre Institución es requerido")
        var titulo_obtenido = document.getElementById("titulo_obtenido").value || alert("Título Obtenido es requerido")
        var clase_titulo = document.getElementById("clase_titulo").value || alert("Clase de Instituto es requerido")
        var estado_formacion = document.getElementById("estado_formacion").value || alert("Estado Formación es requerido")
        var pais_donde_estudio = document.getElementById("pais_donde_estudio").value || alert("País Donde Estudio es requerido")
        var tiempo_estudio = document.getElementById("tiempo_estudio").value || alert("Tiempo Estudio es requerido")
        var periocidad_estudio = document.getElementById("periocidad_estudio").value || alert("Periocidad Estudio es requerido")
        if((typeof(estado_formacion) !== 'undefined') && (estado_formacion == 'COMPLETADO'))
        {
        var fecha_graduacion = document.getElementById("fecha_graduacion").value || alert("Fecha de Graduación es requerido")
        }

        if((typeof(formacion) !== 'undefined') && (typeof(estudia_actualmente_for) !== 'undefined') && (typeof(nombre_institucion) !== 'undefined') && (typeof(titulo_obtenido) !== 'undefined') && ((typeof(clase_titulo) !== 'undefined')) && ((typeof(estado_formacion) !== 'undefined')) && ((typeof(pais_donde_estudio) !== 'undefined')) && ((typeof(tiempo_estudio) !== 'undefined')) && ((typeof(periocidad_estudio) !== 'undefined')))
        {
        var id = parseInt(document.getElementById("no_of_formacion_line").value)
            id +=1;
            document.getElementById("no_of_formacion_line").value = id;
        var dict = {    'id': id,
                        'formacion': formacion,
                        'estudia_actualmente_for': estudia_actualmente_for,
                        'nombre_institucion': nombre_institucion,
                        'titulo_obtenido': titulo_obtenido,
                        'clase_titulo': clase_titulo,
                        'estado_formacion': estado_formacion,
                        'pais_donde_estudio': pais_donde_estudio,
                        'tiempo_estudio': tiempo_estudio,
                        'periocidad_estudio': periocidad_estudio,
                        'fecha_graduacion': fecha_graduacion || ''}
        var formacion_line = document.getElementById("formacion_line").value;
        if (formacion_line == ''){
        document.getElementById("formacion_line").value = formacion_line.concat(JSON.stringify(dict));
        }else{
        document.getElementById("formacion_line").value = formacion_line.concat(',',JSON.stringify(dict));
        }
        alert("Se agrega información de capacitación académica");

        $('#formacion_line_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" + dict['nombre_institucion'] +
        "</td><td style='width: 2px;'><a class='btn btn-primary btn-l formacion_line-remove'>remove</a></td></tr>");
        $('.formacion_line-remove').unbind("click").click(function(ev)
       {
          ev.preventDefault();
          var tr_element = $(ev.currentTarget).parents().eq(1)[0]
          var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
          $(tr_element).css("display", "none");
          var to_remove = document.getElementById('formacion_line_to_remove').value;
          if (to_remove === '')
          {     var list_ids = new Array();
                list_ids.push(id_to_remove)
                document.getElementById('formacion_line_to_remove').value = JSON.stringify(list_ids);
                return;
          }else
          {     var new_value = JSON.parse(to_remove)
                new_value.push(id_to_remove)
                document.getElementById('formacion_line_to_remove').value = JSON.stringify(new_value);
                return;
          }
          $(tr_element).css("display", "none");
      });

        document.getElementById("formacion").value = '';
        document.getElementById("estudia_actualmente_for").value = '';
        document.getElementById("nombre_institucion").value = '';
        document.getElementById("titulo_obtenido").value = '';
        document.getElementById("clase_titulo").value = '';
        document.getElementById("estado_formacion").value = '';
        document.getElementById("pais_donde_estudio").value = '';
        document.getElementById("tiempo_estudio").value = '';
        document.getElementById("periocidad_estudio").value = '';
        document.getElementById("fecha_graduacion").value = '';

        document.getElementById("formacion").required = false;
        document.getElementById("estudia_actualmente_for").required = false;
        document.getElementById("nombre_institucion").required = false;
        document.getElementById("titulo_obtenido").required = false;
        document.getElementById("clase_titulo").required = false;
        document.getElementById("estado_formacion").required = false;
        document.getElementById("pais_donde_estudio").required = false;
        document.getElementById("tiempo_estudio").required = false;
        document.getElementById("periocidad_estudio").required = false;
        document.getElementById("fecha_graduacion").required = false;


        var formacion_line_given = document.getElementById("formacion_line").value;
        var formacion_records = '['.concat(formacion_line_given, ']');
        document.getElementById("formacion_line").value = formacion_records;
        document.getElementById( 'add_formacion_lines_div' ).style.display = 'none';
        $('#add_another_formacion').show()
        }
        });

        $('#cancel_formacion').on('click', function(){
        document.getElementById("formacion").required = false;
        document.getElementById("estudia_actualmente_for").required = false;
        document.getElementById("nombre_institucion").required = false;
        document.getElementById("titulo_obtenido").required = false;
        document.getElementById("clase_titulo").required = false;
        document.getElementById("estado_formacion").required = false;
        document.getElementById("pais_donde_estudio").required = false;
        document.getElementById("tiempo_estudio").required = false;
        document.getElementById("periocidad_estudio").required = false;
        document.getElementById("fecha_graduacion").required = false;


        var formacion_line_given = document.getElementById("formacion_line").value;
        var formacion_records = '['.concat(formacion_line_given, ']');
        document.getElementById("formacion_line").value = formacion_records;
        document.getElementById( 'add_formacion_lines_div' ).style.display = 'none';
        $('#add_another_formacion').show()
        });

// Section 32 ######################################################################
        $('#add_formacion_button').on('click', function(){
        document.getElementById( 'add_formacion_lines_div' ).style.display = '';

        document.getElementById("formacion").required = true;
        document.getElementById("estudia_actualmente_for").required = true;
        document.getElementById("nombre_institucion").required = true;
        document.getElementById("titulo_obtenido").required = true;
        document.getElementById("clase_titulo").required = true;
        document.getElementById("estado_formacion").required = true;
        document.getElementById("pais_donde_estudio").required = true;
        document.getElementById("tiempo_estudio").required = true;
        document.getElementById("periocidad_estudio").required = true;
        var formacion_line_current = document.getElementById("formacion_line").value;
        var formacion_records = formacion_line_current.substring(1, formacion_line_current.length-1);
        document.getElementById("formacion_line").value = formacion_records;
        $('#add_another_formacion').hide()
        });

// Section 33 ######################################################################
        $('#add_idioma_line').on('click', function(){
        var nombre = document.getElementById("nombre").value || alert("Idioma es requerido")
        var porcent_dominio = document.getElementById("porcent_dominio").value || alert("Porcentaje de Dominio es requerido")


        if((typeof(nombre) !== 'undefined') && (typeof(porcent_dominio) !== 'undefined'))
        {
        var id = parseInt(document.getElementById("no_of_idioma").value)
            id +=1;
            document.getElementById("no_of_idioma").value = id;

        var dict = {    'id': id,
                        'nombre': nombre,
                        'porcent_dominio': porcent_dominio, }
        var idioma = document.getElementById("idioma_line").value;
        if (idioma == ''){
        document.getElementById("idioma_line").value = idioma.concat(JSON.stringify(dict));
        }else{
        document.getElementById("idioma_line").value = idioma.concat(',',JSON.stringify(dict));
        }
        alert("Se agrega idioma");

        $('#idioma_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" +
        dict['nombre'] + "</td><td>"+ dict['porcent_dominio'] +"%</td><td><td><a class='btn btn-primary btn-l idioma-remove'>remove</a></td></tr>");

           $('.idioma-remove').unbind("click").click(function(ev)
           {
              ev.preventDefault();
              var tr_element = $(ev.currentTarget).parents().eq(1)[0]
              var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
              $(tr_element).css("display", "none");
              var to_remove = document.getElementById('idioma_to_remove').value;
              if (to_remove === '')
              {     var list_ids = new Array();
                    list_ids.push(id_to_remove)
                    document.getElementById('idioma_to_remove').value = JSON.stringify(list_ids);
                    return;
              }else
              {     var new_value = JSON.parse(to_remove)
                    new_value.push(id_to_remove)
                    document.getElementById('idioma_to_remove').value = JSON.stringify(new_value);
                    return;
              }
              $(tr_element).css("display", "none");
          });

        document.getElementById("nombre").value = '';
        document.getElementById("porcent_dominio").value = '';
        document.getElementById("nombre").required = false;
        document.getElementById("porcent_dominio").required = false;
        var idioma = document.getElementById("idioma_line").value;
        var idioma_records = '['.concat(idioma, ']');
        document.getElementById("idioma_line").value = idioma_records;
        document.getElementById( 'add_idioma_lines_div' ).style.display = 'none';
        $('#add_another_idioma').show()
        }
        });

        $('#cancel_idioma').on('click', function(){
        document.getElementById("nombre").required = false;
        document.getElementById("porcent_dominio").required = false;
        var idioma = document.getElementById("idioma_line").value;
        var idioma_records = '['.concat(idioma, ']');
        document.getElementById("idioma_line").value = idioma_records;
        document.getElementById( 'add_idioma_lines_div' ).style.display = 'none';
        $('#add_another_idioma').show()
        });


// Section 34 ######################################################################
        $('#add_idioma_button').on('click', function(){
        document.getElementById( 'add_idioma_lines_div' ).style.display = '';
        document.getElementById("nombre").required = true;
        document.getElementById("porcent_dominio").required = true;
        var idioma = document.getElementById("idioma_line").value;
        var idioma_records = idioma.substring(1, idioma.length-1);
        document.getElementById("idioma_line").value = idioma_records;
        $('#add_another_idioma').hide()
        });
// Section 35 ######################################################################

        $('#add_fobia').on('click', function(){
        var miedos = document.getElementById("miedos").value || ''
        if (miedos !== '')
        {
        var selected_option = document.getElementById("miedos")
        var selected_value = $(selected_option).find("option:selected").text();
        var id = parseInt(document.getElementById("no_of_fobia").value)
            id +=1;
            document.getElementById("no_of_fobia").value = id;

        var dict = {'id': id,
                    'name': miedos,}
        var miedos_data = document.getElementById("miedos_line").value;
        if (miedos_data == ''){
        document.getElementById("miedos_line").value = miedos_data.concat(JSON.stringify(dict));
        }else{
        document.getElementById("miedos_line").value = miedos_data.concat(',',JSON.stringify(dict));
        }
        alert("se agrega información de miedos");

        $('#fobia_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" +
        selected_value + "</td><td style='width: 2px;'><a class='btn btn-primary btn-l fobia-remove'>remove</a></td></tr>");
        $('.fobia-remove').unbind("click").click(function(ev)
           {
              ev.preventDefault();
              var tr_element = $(ev.currentTarget).parents().eq(1)[0]
              var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
              $(tr_element).css("display", "none");
              var to_remove = document.getElementById('fobia_to_remove').value;
              if (to_remove === '')
              {     var list_ids = new Array();
                    list_ids.push(id_to_remove)
                    document.getElementById('fobia_to_remove').value = JSON.stringify(list_ids);
                    return;
              }else
              {     var new_value = JSON.parse(to_remove)
                    new_value.push(id_to_remove)
                    document.getElementById('fobia_to_remove').value = JSON.stringify(new_value);
                    return;
              }
              $(tr_element).css("display", "none");
          });
        var miedos = document.getElementById("miedos_line").value;
        var idioma_records = '['.concat(miedos, ']');
        document.getElementById("miedos_line").value = idioma_records;
        document.getElementById("miedos").value = '';
        $('#fobia_add_again').show()
        $('#fobia_add').hide()
        $('#fobia_input').hide()
        }else{alert("no hay información para agregar")}
        });

        $('#add_another_fobia').on('click', function(){
        var miedos = document.getElementById("miedos_line").value;
        var miedos_records = miedos.substring(1, miedos.length-1);
        document.getElementById("miedos_line").value = miedos_records;

        $('#fobia_add_again').hide()
        $('#fobia_add').show()
        $('#fobia_input').show()
        });

// Section 35 ######################################################################
        $('#add_hobby').on('click', function(){
        var hobby = document.getElementById("nombre_hobby").value || ''
        if(hobby !== '')
        {
        var selected_option = document.getElementById("nombre_hobby")
        var selected_value = $(selected_option).find("option:selected").text();
        var id = parseInt(document.getElementById("no_of_hobby").value)
            id +=1;
            document.getElementById("no_of_hobby").value = id;
        var dict = {'id': id,
                    'nombre': hobby,}
        var hobby_data = document.getElementById("hobby_line").value;
        if (hobby_data == ''){
        document.getElementById("hobby_line").value = hobby_data.concat(JSON.stringify(dict));
        }else{
        document.getElementById("hobby_line").value = hobby_data.concat(',',JSON.stringify(dict));
        }
        alert("se agrega hobby");

        $('#hobby_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" +
        selected_value + "</td><td style='width: 2px;'><a class='btn btn-primary btn-l hobby-remove'>remove</a></td></tr>");
        $('.hobby-remove').unbind("click").click(function(ev)
           {
              ev.preventDefault();
              var tr_element = $(ev.currentTarget).parents().eq(1)[0]
              var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
              $(tr_element).css("display", "none");
              var to_remove = document.getElementById('hobby_to_remove').value;
              if (to_remove === '')
              {     var list_ids = new Array();
                    list_ids.push(id_to_remove)
                    document.getElementById('hobby_to_remove').value = JSON.stringify(list_ids);
                    return;
              }else
              {     var new_value = JSON.parse(to_remove)
                    new_value.push(id_to_remove)
                    document.getElementById('hobby_to_remove').value = JSON.stringify(new_value);
                    return;
              }
              $(tr_element).css("display", "none");
          });

        var hobby = document.getElementById("hobby_line").value;
        var hobby_records = '['.concat(hobby, ']');
        document.getElementById("hobby_line").value = hobby_records;
        document.getElementById("nombre_hobby").value = '';
        $('#hobby_add_again').show()
        $('#hobby_add').hide()
        $('#hobby_input').hide()
        }else{alert("no hay información para agregar")}
        });

        $('#add_another_hobby').on('click', function(){
        var hobby = document.getElementById("hobby_line").value;
        var hobby_records = hobby.substring(1, hobby.length-1);
        document.getElementById("hobby_line").value = hobby_records;
        $('#hobby_add_again').hide()
        $('#hobby_add').show()
        $('#hobby_input').show()
        });

// Section 35 ###################################################################### alergia_line
        $('#add_alergia').on('click', function(){
        var alergia = document.getElementById("alergia").value || ''
        if(alergia !== '')
        {
        var selected_option = document.getElementById("alergia")
        var selected_value = $(selected_option).find("option:selected").text();
        var id = parseInt(document.getElementById("no_of_alergia").value)
            id +=1;
            document.getElementById("no_of_alergia").value = id;
        var dict = {'id': id,
                    'Nombre': alergia,}
        var alergia_data = document.getElementById("alergia_line").value;
        if (alergia_data == ''){
        document.getElementById("alergia_line").value = alergia_data.concat(JSON.stringify(dict));
        }else{
        document.getElementById("alergia_line").value = alergia_data.concat(',',JSON.stringify(dict));
        }
        alert("se agrega información sobre alergias");

        $('#alergia_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" +
        selected_value + "</td><td style='width: 2px;'><a class='btn btn-primary btn-l alergia-remove'>remove</a></td></tr>");
        $('.alergia-remove').unbind("click").click(function(ev)
           {
              ev.preventDefault();
              var tr_element = $(ev.currentTarget).parents().eq(1)[0]
              var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
              $(tr_element).css("display", "none");
              var to_remove = document.getElementById('alergia_to_remove').value;
              if (to_remove === '')
              {     var list_ids = new Array();
                    list_ids.push(id_to_remove)
                    document.getElementById('alergia_to_remove').value = JSON.stringify(list_ids);
                    return;
              }else
              {     var new_value = JSON.parse(to_remove)
                    new_value.push(id_to_remove)
                    document.getElementById('alergia_to_remove').value = JSON.stringify(new_value);
                    return;
              }
              $(tr_element).css("display", "none");
          });




        var alergia = document.getElementById("alergia_line").value;
        var alergia_records = '['.concat(alergia, ']');
        document.getElementById("alergia_line").value = alergia_records;
        document.getElementById("alergia").value = '';
        $('#alergia_add_again').show()
        $('#alergia_add').hide()
        $('#alergia_input').hide()
        }else{alert("no hay información para agregar")}
        });

        $('#add_another_alergia').on('click', function(){
        var alergia = document.getElementById("alergia_line").value;
        var alergia_records = alergia.substring(1, alergia.length-1);
        document.getElementById("alergia_line").value = alergia_records;
        $('#alergia_add_again').hide()
        $('#alergia_add').show()
        $('#alergia_input').show()
        });

// Section 35 ######################################################################
        $('#centro_de_costo').on('change', function() {
            var id = parseInt(this.value);
            rpc.query({
            model: 'centro',
            method: 'fetch_centro_details',
            args: [this, id],

        }).then(function (data)
        {
          document.getElementById("centro_costo").value = data;
        });
        });

        $('#solicitante').on('change', function() {
            var id = parseInt(this.value);
            rpc.query({
            model: 'hr.employee',
            method: 'fetch_job_details',
            args: [this, id],

        }).then(function (data)
        {
          document.getElementById("cargo_soli").value = data;
        });
        });

// Section 35 ######################################################################

        $('#add_job_formacion').on('click', function(){
        var formacion_especifica = document.getElementById("formacion_especifica").value || ''
        var certificado_academico = document.getElementById("certificado_academico").value || ''
        var prueba_tecnica = document.getElementById("prueba_tecnica").value || ''
        var certificado_laboral_funciones = document.getElementById("certificado_laboral_funciones").value || ''

        if((formacion_especifica != '') && (certificado_academico != '') && (prueba_tecnica != '') & (certificado_laboral_funciones != ''))
        {
            var id = parseInt(document.getElementById("no_of_formacion_especifica").value)
            id +=1;
            document.getElementById("no_of_formacion_especifica").value = id;

        var dict = {
            'id': id,
            'formacion_especifica': formacion_especifica,
            'certificado_academico': certificado_academico,
            'prueba_tecnica': prueba_tecnica,
            'certificado_laboral_funciones': certificado_laboral_funciones,
        }

        var job_formacion_data = document.getElementById("formacion_esp").value;
        if (job_formacion_data == ''){
        document.getElementById("formacion_esp").value = job_formacion_data.concat(JSON.stringify(dict));
        }else{
        document.getElementById("formacion_esp").value = job_formacion_data.concat(',',JSON.stringify(dict));
        }
        alert("Se agrega información de entrenamiento");

        $('#formacion_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" +
        dict['formacion_especifica'] + "</td><td>"+ dict['certificado_academico'] +"</td><td>"+
        dict['prueba_tecnica'] +"</td><td>"+ dict['certificado_laboral_funciones']
        +"</td><td><a class='btn btn-primary btn-l formaction-remove'>remove</a></td></tr>");

           $('.formaction-remove').unbind("click").click(function(ev)
           {
               ev.preventDefault();
              var tr_element = $(ev.currentTarget).parents().eq(1)[0]
              var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
              $(tr_element).css("display", "none");
              var to_remove = document.getElementById('formacion_especifica_to_remove').value;
              console.log(to_remove, "to remove")
              if (to_remove === '')
              {     var list_ids = new Array();
                    list_ids.push(id_to_remove)
                    document.getElementById('formacion_especifica_to_remove').value = JSON.stringify(list_ids);
                    return;
              }else
              {     var new_value = JSON.parse(to_remove)
                    console.log(new_value, "new value")
                    new_value.push(id_to_remove)
                    console.log(new_value, "n2")
                    document.getElementById('formacion_especifica_to_remove').value = JSON.stringify(new_value);
                    return;
              }
              $(tr_element).css("display", "none");
          });

        var job_formacion = document.getElementById("formacion_esp").value;
        var job_formacion_records = '['.concat(job_formacion, ']');
        document.getElementById("formacion_esp").value = job_formacion_records;
        document.getElementById("formacion_especifica").value = '';
        document.getElementById("certificado_academico").value = '';
        document.getElementById("prueba_tecnica").value = '';
        document.getElementById("certificado_laboral_funciones").value = '';
        $('#job_formacion_add_again').show()
        $('#job_formacion_add').hide()
        $('#formacion_table').hide()

        }else{alert("no hay información para agregar")}
        });

        $('#add_another_job_formacion').on('click', function(){
        var job_formacion = document.getElementById("formacion_esp").value;
        var job_formacion_records = job_formacion.substring(1, job_formacion.length-1);
        document.getElementById("formacion_esp").value = job_formacion_records;

        $('#job_formacion_add_again').hide()
        $('#job_formacion_add').show()
        $('#formacion_table').show()
        });
// Section 36 ######################################################################
         $('#add_activo').on('click', function(){
        var categoria = document.getElementById("categoria").value || ''
        var activo_cargo = document.getElementById("activo_cargo").value || ''

        if((categoria != '') || (activo_cargo != ''))
        {
        var id = parseInt(document.getElementById("no_of_activos_cargo").value)
            id +=1;
            document.getElementById("no_of_activos_cargo").value = id;

        var dict = {
            'id': id,
            'categoria': categoria,
            'activo_cargo': activo_cargo,
        }

        var job_activo_data = document.getElementById("activos_line").value;
        if (job_activo_data == ''){
        document.getElementById("activos_line").value = job_activo_data.concat(JSON.stringify(dict));
        }else{
        document.getElementById("activos_line").value = job_activo_data.concat(',',JSON.stringify(dict));
        }
        alert("Se agrega información de activos de carga");

        $('#activos_append').find('tbody').append("<tr t-att-id="+ dict['id'] +"><td>" +
        dict['categoria'] + "</td><td>"+ dict['activo_cargo']
        +"</td><td><a class='btn btn-primary btn-l activos-remove'>remove</a></td></tr>");

       $('.activos-remove').unbind("click").on('click', function(ev)
       {
          ev.preventDefault();
          var tr_element = $(ev.currentTarget).parents().eq(1)[0]
          var id_to_remove = $(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id')
          $(tr_element).css("display", "none");
          var to_remove = document.getElementById('activos_cargo_to_remove').value;
          if (to_remove === '')
          {     var list_ids = new Array();
                list_ids.push(id_to_remove)
                document.getElementById('activos_cargo_to_remove').value = JSON.stringify(list_ids);
                return;
          }else
          {     var new_value = JSON.parse(to_remove)
                new_value.push(id_to_remove)
                document.getElementById('activos_cargo_to_remove').value = JSON.stringify(new_value);
                return;
          }
          $(tr_element).css("display", "none");
      });





        var job_activos = document.getElementById("activos_line").value;
        var job_activos_records = '['.concat(job_activos, ']');
        document.getElementById("activos_line").value = job_activos_records;
        document.getElementById("categoria").value = '';
        document.getElementById("activo_cargo").value = '';
        $('#activo_add_again').show()
        $('#activo_add').hide()
        $('#activos_table').hide()
        }else{alert("no hay información para agregar")}
        });

        $('#add_another_activo').on('click', function(){
        var job_activos = document.getElementById("activos_line").value;
        var job_activos_records = job_activos.substring(1, job_activos.length-1);
        document.getElementById("activos_line").value = job_activos_records;
        $('#activo_add_again').hide()
        $('#activo_add').show()
        $('#activos_table').show()
        });

// Section 36 ######################################################################
       $('#tiene_personal_cargo').on('change', function() {
        if (this.value == 'SI')
        {
            $('#corgos_table').show()
        }else{  $('#corgos_table').hide()
                }});

        $("#minimo, #maximo").on('input', function(e)
         {   $(this).val($(this).val().replace(/[^0-9\.]/g, ''));
         });

// Section 36 ######################################################################
        $('.jobline').on('click', function(ev) {

        $('.jobline').each(function(i, obj) {
        if(obj.getAttributeNode('style') != null)
        {
        obj.removeAttribute('style');
        }
        });
        ev.currentTarget.style.border = 'solid';
        var id = parseInt(ev.currentTarget.getAttribute('id'));
        rpc.query({
            model: 'hr.job',
            method: 'fetch_cargo_state',
            args: [this, id],

        }).then(function (data)
        {
          if((data == 'open') || (data == 'write'))
          {
            $('#edit_cargo_div').show()
            $('#create_cargo_div').hide()
          }else{
            $('#edit_cargo_div').hide()
            $('#create_cargo_div').show()
          }
        });
        });
// Section 36 ######################################################################
        $('#create_cargo').on('click', function(ev) {
        document.getElementById('create_cargo').style.display = ' none';
        $('#group_1').hide()
        $('#group_2').show()
        $('#cancel_cargo_div').show()
        if($('#modifications').css('display') != 'none')
        {
        $('#modifications').hide()
        }
        });
// Section 36 ######################################################################
        $('#edit_cargo').on('click', function(ev) {
        document.getElementById('modificacion').checked = false;
        document.getElementById('modificacion').checked = false;

        $('.jobline').each(function(i, obj) {
        if(obj.getAttributeNode('style') != null)
        {   var selected_id = parseInt(obj.getAttribute('id'));
            rpc.query({
            model: 'hr.job',
            method: 'fetch_cargo_details',
            args: [this, selected_id],

        }).then(function (data)
        {
          var formacion_data = data['formacion']
          if (formacion_data != '')
          {
          $('#formacion_append').show()
          formacion_data.forEach(function(i)
          {     $('#formacion_append').find('tbody').append("<tr t-att-id="+ i['id'] +"><td>" +
                i['formacion_especifica'] + "</td><td>"+ i['certificado_academico'] +"</td><td>"+
                i['prueba_tecnica'] +"</td><td>"+ i['certificado_laboral_funciones']
                +"</td><td><a class='btn btn-primary btn-l formaction-remove'>remove</a></td></tr>");
          });
          $('.formaction-remove').on('click', function(ev)
          {
              var tr_element = $(ev.currentTarget).parents().eq(1)[0]
              var id = parseInt($(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id'));
                        rpc.query({
                        model: 'formacion.cargos',
                        method: 'unlink_formacion_cargos',
                        args: [this, id],
                    })
                    .then(function (data) {
                        if(data == true)
                        {
                        $(tr_element).css("display", "none");
                        }
                    });
          });
         }

          var activos_data = data['activos']
          if (activos_data != '')
          {
          $('#activos_append').show()
          activos_data.forEach(function(i)
          {     $('#activos_append').find('tbody').append("<tr t-att-id="+ i['id'] +"><td>" +
                i['categoria'] + "</td><td>"+ i['activo_cargo']
                +"</td><td><a class='btn btn-primary btn-l activos-remove'>remove</a></td></tr>");
          });
          $('.activos-remove').on('click', function(ev) {
          var tr_element = $(ev.currentTarget).parents().eq(1)[0]
          var id = parseInt($(ev.currentTarget).parents().eq(1)[0].getAttribute('t-att-id'));
                    rpc.query({
                    model: 'activos',
                    method: 'unlink_activos',
                    args: [this, id],
                })
                .then(function (data) {
                    if(data == true)
                    {
                    $(tr_element).css("display", "none");
                    }
                });
            });
          }
        var cargos_details = data['cargos']

        document.getElementById('name').value = cargos_details['name'];
        document.getElementById('company_id').value = parseInt(cargos_details['company_id'][0]) || ''
        document.getElementById('jefe_inmediato_apl').value = parseInt(cargos_details['jefe_inmediato_apl'][0]) || ''
        document.getElementById('procesos_servicios_per').value = cargos_details['procesos_servicios_per'] || ''
        var status = document.getElementById('tiene_personal_cargo').value = cargos_details['tiene_personal_cargo'] || ''
        if (status == 'SI')
        {
            $('#corgos_table').show()
        }else{  $('#corgos_table').hide()
                }
        document.getElementById('cargo1').value = parseInt(cargos_details['cargo1'][0]) || ''
        document.getElementById('tipo_relacion1').value = cargos_details['tipo_relacion1'];
        document.getElementById('cargo2').value = parseInt(cargos_details['cargo2'][0]) || ''
        document.getElementById('tipo_relacion2').value = cargos_details['tipo_relacion2'] || ''
        document.getElementById('cargo3').value = parseInt(cargos_details['cargo3'][0]) || ''
        document.getElementById('tipo_relacion3').value = cargos_details['tipo_relacion3'] || ''
        document.getElementById('cargo4').value = parseInt(cargos_details['cargo4'][0]) || ''
        document.getElementById('tipo_relacion4').value = cargos_details['tipo_relacion4'] || ''
        document.getElementById('nivel_primario_educativo_minimo').value = cargos_details['nivel_primario_educativo_minimo'] || ''
        document.getElementById('nombre_programa_carrera').value = cargos_details['nombre_programa_carrera'] || ''
        document.getElementById('nivel_secundario_educativo').value = cargos_details['nivel_secundario_educativo'] || ''
        document.getElementById('nombre_programa').value = cargos_details['nombre_programa'] || ''
        document.getElementById('requiere_tarjeta_profesional').value = cargos_details['requiere_tarjeta_profesional'] || ''
        document.getElementById('objetivo_cargo').value = cargos_details['objetivo_cargo'] || ''
        var applica_state = document.getElementById('aplica').value = cargos_details['aplica'] || ''
        if(applica_state == 'SI')
        {    $('#aplica_table_a').show()
             $('#aplica_table_b').show()
             $('#aplica_table_c').show()
             $('#aplica_table_d').show()
        }else
            {    $('#aplica_table_a').hide()
                 $('#aplica_table_b').hide()
                 $('#aplica_table_c').hide()
                 $('#aplica_table_d').hide()
               }
        document.getElementById('minimo').value = cargos_details['minimo'] || ''
        document.getElementById('general').value = cargos_details['general'] || ''
        document.getElementById('especifica_cargos_similares').value = cargos_details['especifica_cargos_similares'] || ''
        document.getElementById('maximo').value = cargos_details['maximo'] || ''
        document.getElementById('que_hace').value = cargos_details['que_hace'] || ''
        document.getElementById('como_lo_hace').value = cargos_details['como_lo_hace'] || ''
        document.getElementById('deberes').value = cargos_details['deberes'] || ''
        document.getElementById('responsabilidades').value = cargos_details['responsabilidades'] || ''
        document.getElementById('nivel_autoridad').value = cargos_details['nivel_autoridad'] || ''
        document.getElementById('description').value = cargos_details['description'] || ''
        document.getElementById('edit_cargo_id').value = selected_id;
        });
        }
        });
        $('#group_1').hide()
        $('#group_2').show()
        $('#modifications').show()
        $('#submit_cargo').hide()
        $('#edit_cargo_div').hide()
        $('#save_cargo_div').show()
        $('#cancel_cargo_div').show()
        });
// Section 36 ######################################################################
         $('#save_cargo').on('click', function() {
         var modificacion = document.getElementById('modificacion').checked;
         var eliminacion =  document.getElementById('eliminacion').checked;
         var isValid = true;

         $('input,textarea,select').filter('[required]:visible').each(function()
         {  if ($(this).val() === '')
            {  isValid = false;
            }
         });

         if(isValid == true)
         {  if ((modificacion == false) && (eliminacion == false))
            {   alert("por favor elija modificación o eliminación");}
            else
            {   var form = document.getElementById("add_cargos");
                form.submit();
                document.getElementById('name').value = ''
                document.getElementById('company_id').value = ''
                document.getElementById('procesos_servicios_per').value = ''
                document.getElementById('tiene_personal_cargo').value = ''
                document.getElementById('cargo1').value = ''
                document.getElementById('tipo_relacion1').value = ''
                document.getElementById('cargo2').value = ''
                document.getElementById('tipo_relacion2').value = ''
                document.getElementById('cargo3').value = ''
                document.getElementById('tipo_relacion3').value = ''
                document.getElementById('cargo4').value = ''
                document.getElementById('tipo_relacion4').value = ''
                document.getElementById('nivel_primario_educativo_minimo').value = ''
                document.getElementById('nombre_programa_carrera').value = ''
                document.getElementById('nivel_secundario_educativo').value = ''
                document.getElementById('nombre_programa').value = ''
                document.getElementById('requiere_tarjeta_profesional').value = ''
                document.getElementById('objetivo_cargo').value = ''
                document.getElementById('aplica').value = ''
                document.getElementById('minimo').value = ''
                document.getElementById('maximo').value = ''
                document.getElementById('que_hace').value = ''
                document.getElementById('como_lo_hace').value = ''
                document.getElementById('deberes').value = ''
                document.getElementById('responsabilidades').value = ''
                document.getElementById('nivel_autoridad').value = ''
                document.getElementById('description').value = ''
                document.getElementById('edit_cargo_id').value = ''
                document.getElementById('modificacion').checked = false;
                document.getElementById('modificacion').checked = false;
            }
         }
         else{ alert("Por favor, rellene los campos obligatorios") }
         });
// Section 36 ######################################################################
        $('#submit_entrevista').on('click', function(){
        var self = this;
        var survey_id = parseInt(document.getElementById('entrevista').value)
        var record = parseInt(document.getElementById('record_id').value)
            return rpc.query({
            model: 'wizard.survey',
            method: 'action_start_survey_portal',
            args: [this, survey_id, record],

        }).then(function (url) {
            window.open(url, '_blank');
        });
        });
// Section 36 ######################################################################
          $('#aplica').on('change', function() {
               if(this.value == 'SI')
               {    $('#aplica_table_a').show()
                    $('#aplica_table_b').show()
                    $('#aplica_table_c').show()
                    $('#aplica_table_d').show()
               }
               else{    $('#aplica_table_a').hide()
                        $('#aplica_table_b').hide()
                        $('#aplica_table_c').hide()
                        $('#aplica_table_d').hide()
               }
          });
// Section 36 ######################################################################
        $("#modificacion").change(function() {
        var eliminacion_check = document.getElementById('eliminacion').checked;
            if(this.checked)
            {   if (eliminacion_check == true)
                {   document.getElementById('eliminacion').checked = false; }
            }
        });
         $("#eliminacion").change(function() {
        var modificacion_check = document.getElementById('modificacion').checked;
            if(this.checked)
            {   if (modificacion_check == true)
                {   document.getElementById('modificacion').checked = false; }
            }
        });
// Section 36 ######################################################################
        $('#requisicion_approve, #requisicion_reject').on('click', function(){
        var requisicion_id = parseInt(document.getElementById('requisicion_id').value)
        var user = parseInt(document.getElementById('user').value)
        var action = $(this).data("value");
            return rpc.query({
            model: 'requisiciones',
            method: 'requisicion_approval',
            args: [this, requisicion_id, user, action],

        }).then(function (url) {
            console.log(url, "url")
            window.location.href = url;
        });
        });

    $("#requisicion_approve, #requisicion_reject").hover(function(){
    $(this).animate({'opacity': 1}, 100)
    }, function(){
    $(this).animate({'opacity': 0.6}, 100)
    });

// Section 36 ######################################################################
});
