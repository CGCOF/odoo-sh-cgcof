//------------------------------------
// - - - - Click Iniciar Sessión - - - 
//------------------------------------
$(document).on("click","#btn-acceso",function(){
    if($(".WS_acceso_portalfarma [name='usuarioAcceso']").val() === ""){
        $(".WS_acceso_portalfarma [name='usuarioAcceso']").focus();
        alert("Debe introducir su DNI/CIF");
    } else{
        if($(".WS_acceso_portalfarma [name='passwordAcceso']").val() === ""){
            $(".WS_acceso_portalfarma [name='passwordAcceso']").focus();
            alert("Debe introducir su contraseña");
        } else {
            if($(".WS_acceso_portalfarma [name='checkPrivacidadAcceso']").prop("checked") === false){
                alert("Debe aceptar nuestra Política de Privacidad");
            } else{
                
                var usuario = $(".WS_acceso_portalfarma [name='usuarioAcceso']").val();
                var pass = $(".WS_acceso_portalfarma [name='passwordAcceso']").val();

                var d = new Date();
                var dia  = d.getDate();
                if(String(dia).length===1){
                    var dia = "0"+dia;
                }
                var mes  = (d.getMonth()+1);
                if(String(mes).length===1){
                    var mes = "0"+mes;
                }
                var year = d.getFullYear();
                var fecha = dia+"-"+mes+"-"+year;

                var horas = d.getHours();
                var minutos = d.getMinutes();
                var segundos = d.getSeconds();
                if(horas.length === 1){
                    var horas = "0" + horas;
                }
                if(minutos.length === 1){
                    var minutos = "0" + minutos;
                }
                if(segundos.length === 1){
                    var segundos = "0" + segundos;
                }
                var hora = horas + ':' + minutos + ':' + segundos;

                $.ajax({
                    type: "get",
                    async: true,
                    url: "https://www.congeladosentucasa.com:8182/webCasafrio/cargar_inicio?cliente=",
                    success: function(respuesta){
                        if(usuario !== "ok"){
                            location.replace("https://danielguerracarrascosa-doce-user-comprobar-2814509.dev.odoo.com/acceso_desde_portalfarma_ok?usd="+usuario+"&userPass="+pass);
                        } else {
                            $(".WS_acceso_portalfarma").prepend("<p class='text-danger'>Usuario o clave invalida.</p>");
                        } 
                    }
                });
                
            }
        }
    }
    
});

$(document).on("click","#btn-siguiente",function(){
    
    var userDNI = $("#userDNI").val();
    var pass = $("#pass").val();
    
    location.replace("https://idppre.farmaceuticos.com/oauth2/authorize?response_type=code&client_id=AIo_EhBwSrpZNCPzkYmogFJsahMa&redirect_uri=https://pre.farmaceuticos.com/callbacksso.php&scope=openid%20cgcof&nonce=1234567%22");
});
