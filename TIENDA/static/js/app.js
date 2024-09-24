let listaProductos = [];

function formatearMoneda({ currency, value }) {
    const formateador = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        minimumFractionDigits: 2,
        currency
    });
    return formateador.format(value);
}

function previsualizarFoto(evento) {
    const $inputFoto = document.querySelector('#fileFoto');
    const $imagenPrevisualizacion = document.querySelector("#imagenProducto");
    const archivos = evento.files;
    const archivoSeleccionado = archivos[0];
    let nombreArchivo = archivoSeleccionado.name;
    let extensionArchivo = nombreArchivo.split('.').pop().toLowerCase();

    if (extensionArchivo !== "jpg") {
        $inputFoto.value = "";
        alert("La imagen debe ser en formato JPG");
    } else {
        const objectURL = URL.createObjectURL(archivoSeleccionado);
        $imagenPrevisualizacion.src = objectURL;
    }
}

function eliminarProducto(id) {
    console.log(id);
    Swal.fire({
        title: "¿Está seguro de eliminar el producto?",
        showDenyButton: true,
        confirmButtonText: "Sí",
        denyButtonText: "No"
    }).then((resultado) => {
        if (resultado.isConfirmed) {
            location.href = "/eliminar/" + id;
            Swal.fire("Eliminado!", "", "success");
        }
    });
}

function obtenerListaProductos() {
    const url = "/api/listarProductos";
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            listaProductos = resultado;
            console.log(resultado);
            mostrarTablaProductos();
        })
        .catch(error => {
            console.error(error);
        });
}

function mostrarTablaProductos() {
    let datosHTML = "";
    listaProductos.forEach(producto => {
        datosHTML += "<tr>";
        datosHTML += "<td>" + producto['codigo'] + "</td>";
        datosHTML += "<td>" + producto['nombre'] + "</td>";
        const valorPrecio = parseInt(producto['precio']);
        const precioFormateado = formatearMoneda({
            currency: "COP",
            value: valorPrecio
        });
        datosHTML += "<td>" + precioFormateado + "</td>";
        datosHTML += "<td>" + producto['categoria'] + "</td>";
        datosHTML += "<td class='text-center'>" +
            "<img src='../static/imagenes/" + producto['codigo'] + ".jpg' width='50' height='50'></td>";
        datosHTML += '<td class="text-center" style="font-size:4vh">' +
            '<a href="/consultar/' + producto['_id'] + '"><i class="fa fa-edit text-warning" title="Editar"></i></a>' +
            '<i class="fa fa-trash text-danger" onclick="eliminarProducto(' + producto['_id'] + ')" title="Eliminar"></i></td>';
        datosHTML += '</tr>';
    });
    console.log(datosHTML);
    datosProductos.innerHTML = datosHTML;
}


