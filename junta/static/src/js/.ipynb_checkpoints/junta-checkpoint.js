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
    var ultimo_orden = $("table tr:last .orden").text();
    $("#cont-new input[name='orden']").val(ultimo_orden);
    $("#cont-new input[name='dni']").focus();
});
$(document).on("focusout","#cont-new input[name='dni']",function(){
    if($("#cont-new input[name='dni']").val() === ""){
        $("#cont-new input[name='dni']").focus();
    } else {
        var dni = $("#cont-new input[name='dni']").val();
        $.ajax({
            type: "post",
            contentType: "application/json"
            async: true,
            data: {
                dni: dni
            },
            url: "/busca_dni",
            success: function(respuesta){
                if (respuesta.array.length !== 0 && respuesta.array[0].dato.nombre !== ""){
                    var nombre = respuesta.array[0].dato.nombre;
                    var apellidos = respuesta.array[0].dato.apellidos;
                    var dni = respuesta.array[0].dato.dni;
                }
            }
        });
    }
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
    
    $.ajax({
        type: "post",
        async: true,
        data: {
            cargo: cargo,
            nombre: nombre,
            apellidos: apellidos,
            dni: dni,
            fecha_inicio: fecha_inicio,
            fecha_final: fecha_final,
            web: web,
            orden: orden
        },
        url: "/guarda_new",
        success: function(respuesta){
            alert(respuesta);
        }
    });
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