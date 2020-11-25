var contador_contratos = document.getElementById("numero_de_contratos").innerHTML;





function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

contador_contratos = parseInt(getCookie("documentos_generados"))
document.getElementById("numero_de_contratos").innerHTML = contador_contratos