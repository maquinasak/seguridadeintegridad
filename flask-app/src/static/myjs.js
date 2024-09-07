function mostrarDatos(lugar, datos){

    let cTabla = "<table border=2><tr><td>Nombre</td><td>Apellido</td><td>Borrar</td></tr>";
    datos.forEach(element => {
        cTabla += `<tr><td>${element[1]}</td><td>${element[2]}</td><td><input type="button" value="X" onclick="eliminarUsuario('${element[0]}');"></td></tr>`;        
    });
    cTabla += "</table>";

    let destino=document.getElementById(lugar);
    destino.innerHTML=cTabla;
}

function cargarUsuarios(){

    /* obtener usuarios */
    fetch("/usuarios")
    .then(response => response.json())
    .then(data => {
        console.log(data);
        mostrarDatos("grilla",data);

    });

}


function eliminarUsuario(email){

    /* obtener usuarios */
    fetch(`/usuarios/${email}`,{
        method:"DELETE"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert("dato eliminado");
        cargarUsuarios();
    });

}



let formNuevoUsuario = document.getElementById("nuevoUsuario");
formNuevoUsuario.addEventListener("submit", event => {
    event.preventDefault();

    // Agrego un usuarios

    let data = new FormData(formNuevoUsuario);
    // Convert form data to a regular object (optional)
    const formObject = {};
    data.forEach((value, key) => {
        formObject[key] = value;
    });
    console.log(formObject);

    fetch("/usuarios", { 
        method: "POST", 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formObject)
    })
    .then(response => response.json())
    .then(data => {
            console.log(data);
    });
    
});
