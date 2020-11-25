var documentos_generados = 0

//var contador_contratos = document.getElementById("numero_de_contratos").innerHTML; 
 

document.cookie = "username=12"


document.getElementById("submit").addEventListener("click",set_cookie)


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function set_cookie()
{
    var set_documento_generado = parseInt(getCookie("documentos_generados"))
    set_documento_generado += 1
    document.cookie = `documentos_generados = ${set_documento_generado}`
    return console.log(set_documento_generado)
}

