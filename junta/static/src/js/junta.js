$(document).on("click","#cancela-edit",function(){
    $("#cont-edit").hide();
    $("#cont-inicio").show();
    $(".delete2").removeClass("delete2");
    $(".select").removeClass("select");
});
$(document).on("click","#cancela-new",function(){
    $("#cont-new").hide();
    $("#cont-inicio").show();
    $(".delete2").removeClass("delete2");
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
});
$(document).on("click",".delete2",function(){
    $(this).parent().parent().remove();
});
$(document).on("click",".edit",function(){
    $(".select").removeClass("select");
    $(this).parent().parent().addClass("select");
    $("#cont-inicio").hide();
    $("#cont-edit").show();
    $("#cont-edit input[name='cargo']").val($("tr.select>.cargo").text());
    $("#cont-edit input[name='nombre']").val($("tr.select>.nombre").text());
    $("#cont-edit input[name='apellidos']").val($("tr.select>.apellidos").text());
    $("#cont-edit input[name='dni']").val($("tr.select>.dni").text());
    $("#cont-edit input[name='fecha_inicio']").val($("tr.select>.cafecha_iniciorgo").text());
    $("#cont-edit input[name='fecha_final']").val($("tr.select>.fecha_final").text());
    var dato_web = $("tr.select>.web").text();
    if(dato_web === "Sí"){
        $("#cont-edit input[value='Sí']").replaceWith("<input type='radio' name='web' value='Sí' checked/>");
        $("#cont-edit input[value='No']").replaceWith("<input type='radio' name='web' value='No'/>");
    } else {
        $("#cont-edit input[value='Sí']").replaceWith("<input type='radio' name='web' value='Sí'/>");
        $("#cont-edit input[value='No']").replaceWith("<input type='radio' name='web' value='No' checked/>");
    }
    $("#cont-edit input[name='orden']").val($("tr.select>.orden").text());
});
$(document).on("click","#guarda-new",function(){
    var cargo = $("#cont-new input[name='cargo']").val();
    var nombre = $("#cont-new input[name='nombre']").val();
    var apellidos = $("#cont-new input[name='apellidos']").val();
    var dni = $("#cont-new input[name='dni']").val();
    var fecha_inicio = $("#cont-new input[name='fecha_inicio']").val();
    var fecha_final = $("#cont-new input[name='fecha_final']").val();
    var web = $("#cont-new input[name='web']").val();
    var orden = $("#cont-new input[name='orden']").val();
});
$(document).on("click","#guarda-edit",function(){
    var cargo = $("#cont-edit input[name='cargo']").val();
    var nombre = $("#cont-edit input[name='nombre']").val();
    var apellidos = $("#cont-edit input[name='apellidos']").val();
    var dni = $("#cont-edit input[name='dni']").val();
    var fecha_inicio = $("#cont-edit input[name='fecha_inicio']").val();
    var fecha_final = $("#cont-edit input[name='fecha_final']").val();
    var web = $("#cont-edit input[name='web']").val();
    var orden = $("#cont-edit input[name='orden']").val();
});