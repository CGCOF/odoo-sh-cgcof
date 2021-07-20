$(document).on("click","#cancela-edit",function(){
    $("#cont-edit").hide();
    $("#cont-inicio").show();
});
$(document).on("click","#cancela-new",function(){
    $("#cont-new").hide();
    $("#cont-inicio").show();
});
$(document).on("click","#btn-new",function(){
    $("#cont-inicio").hide();
    $("#cont-new").show();
    var cargo = $("#cont-new input[name='cargo']").val("");
    var nombre = $("#cont-new input[name='nombre']").val("");
    var apellidos = $("#cont-new input[name='apellidos']").val("");
    var dni = $("#cont-new input[name='dni']").val("");
    var fecha_inicio = $("#cont-new input[name='fecha_inicio']").val("");
    var fecha_final = $("#cont-new input[name='fecha_final']").val("");
    var orden = $("#cont-new input[name='orden']").val("");
});
$(document).on("click",".delete",function(){
    $(this).addClass("delete2");
    $(this).css("border","1px solid red");
});
$(document).on("click",".delete2",function(){
    $(this).parent().parent().remove();
});
$(document).on("click",".edit",function(){
    $(".select").removeClass("select");
    $(this).parent().parent().addClass("select");
    $("#cont-inicio").hide();
    $("#cont-edit").show();
    $("#cont-edit input[name='cargo']").val($("tr.select>.cargo").val());
    $("#cont-edit input[name='nombre']").val($("tr.select>.nombre").val());
    $("#cont-edit input[name='apellidos']").val($("tr.select>.apellidos").val());
    $("#cont-edit input[name='dni']").val($("tr.select>.dni").val());
    $("#cont-edit input[name='fecha_inicio']").val($("tr.select>.cafecha_iniciorgo").val());
    $("#cont-edit input[name='fecha_final']").val($("tr.select>.fecha_final").val());
    $("#cont-edit input[name='erp']").val($("tr.select>.erp").val());
    $("#cont-edit input[name='orden']").val($("tr.select>.orden").val());
});
$(document).on("click","#guarda-new",function(){
    var cargo = $("#cont-new input[name='cargo']").val();
    var nombre = $("#cont-new input[name='nombre']").val();
    var apellidos = $("#cont-new input[name='apellidos']").val();
    var dni = $("#cont-new input[name='dni']").val();
    var fecha_inicio = $("#cont-new input[name='fecha_inicio']").val();
    var fecha_final = $("#cont-new input[name='fecha_final']").val();
    var erp = $("#cont-new input[name='erp']").val();
    var orden = $("#cont-new input[name='orden']").val();
});
$(document).on("click","#guarda-edit",function(){
    var cargo = $("#cont-edit input[name='cargo']").val();
    var nombre = $("#cont-edit input[name='nombre']").val();
    var apellidos = $("#cont-edit input[name='apellidos']").val();
    var dni = $("#cont-edit input[name='dni']").val();
    var fecha_inicio = $("#cont-edit input[name='fecha_inicio']").val();
    var fecha_final = $("#cont-edit input[name='fecha_final']").val();
    var erp = $("#cont-edit input[name='erp']").val();
    var orden = $("#cont-edit input[name='orden']").val();
});