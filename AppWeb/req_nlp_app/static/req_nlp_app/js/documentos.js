let documentoActualId = null;

document.addEventListener('DOMContentLoaded', () => {
    cargarListaDocumentos();
});


function crearNuevoDocumento() {
    
    fetch(URL_NUEVO_DOCUMENTO, {
        method: "POST",
         headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            nombre: "Documento nuevo desde JS"
        })
    })
    .then(response => response.json())
    .then(data => {
        const ul = document.getElementById('lista-documentos');
        const li = document.createElement('li');
        li.textContent = data.nombre;
        li.setAttribute('ondblclick', `cargarContenidoDocumento(${data.id})`);
        li.setAttribute('oncontextmenu', 'editarNombre(event, this)');
        li.classList.add('documento-item');
        // Agregar icono de eliminar
        const iconoEliminar = document.createElement('i');
        iconoEliminar.classList.add('bi', 'bi-trash');
        iconoEliminar.setAttribute('onclick', `eliminarDocumento(event, ${data.id})`);
        iconoEliminar.setAttribute('title', 'Eliminar documento');
        iconoEliminar.style.cursor = 'pointer';
        iconoEliminar.style.color = 'red';
        iconoEliminar.style.marginRight = '8px';
        li.appendChild(iconoEliminar);
  

        li.setAttribute('data-id', data.id);
        li.setAttribute('oncontextmenu', 'editarNombre(event, this)');
        ul.appendChild(li);
    });
}


function cargarContenidoDocumento(docId) {
    console.log("Cargando documento ID:", docId);
    fetch(`/obtener_contenido_documento/${docId}/`)
        .then(response => {
            console.log("Respuesta fetch status:", response.status);
            if (!response.ok) throw new Error('Error al obtener contenido');
            return response.json();
        })
        .then(data => {
            const textarea = document.querySelector('textarea');
            textarea.value = data.texto || '';
            setCurrentDocId(docId);
        })
        .catch(error => {
            console.error("Error en fetch:", error);
            alert(error);
        });
}

function getCurrentDocId() {
    return documentoActualId;
}
function setCurrentDocId(id) {
    documentoActualId = id;
}

function obtenerTexto() {
    return document.querySelector('textarea').value;
}


function guardarDocumento(docId, nuevoTexto) {
    if (!docId) {
        alert('No hay documento seleccionado');
        return;
    }
    fetch(`/guardar_documento/${docId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ texto: nuevoTexto })
    })
    .then(response => {
        if (response.ok) {
            alert('Documento guardado con éxito');
        } else {
            alert('Error al guardar el documento');
        }
    })
    .catch(() => alert('Error en la conexión al guardar'));
}


function cargarListaDocumentos() {
    console.log("Entré a cargarListaDocumentos");
    fetch('/api/documentos/')
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);
            const ul = document.getElementById('lista-documentos');
            ul.innerHTML = ''; 

            data.forEach(doc => {
                const li = document.createElement('li');
                li.setAttribute('data-id', doc.id);

                // Icono eliminar
                const iconoEliminar = document.createElement('i');
                iconoEliminar.classList.add('bi', 'bi-trash');
                iconoEliminar.style.cursor = 'pointer';
                iconoEliminar.style.color = 'red';
                iconoEliminar.style.marginRight = '8px';
                iconoEliminar.title = 'Eliminar documento';
                iconoEliminar.onclick = (e) => eliminarDocumento(e, doc.id);

                // Nombre documento
                const spanNombre = document.createElement('span');
                spanNombre.classList.add('nombre-doc');
                spanNombre.style.cursor = 'pointer';
                spanNombre.textContent = doc.nombre;
                spanNombre.setAttribute('data-id', doc.id);
                spanNombre.oncontextmenu = (e) => editarNombre(e, spanNombre);
                spanNombre.ondblclick = () => cargarContenidoDocumento(doc.id);

                li.appendChild(iconoEliminar);
                li.appendChild(spanNombre);

                ul.appendChild(li);
            });
        })
        .catch(err => console.error("Error al cargar documentos:", err));
}


function editarNombre(event, element) {
    console.log("Editar nombre...");
    event.preventDefault(); 
    const li = element.closest('li');
    const docId = li.getAttribute('data-id');

    const nombreActual = element.textContent.trim();
    const nuevoNombre = prompt("Editar nombre del documento:", nombreActual);
    if (nuevoNombre && nuevoNombre !== nombreActual) {
        li.setAttribute('data-id', docId);
        fetch(`/renombrar_documento/${docId}/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            credentials: 'include',
            body: JSON.stringify({
                id: docId,
                nombre: nuevoNombre
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta renombrar documento:", data);
            if (data.success) {
                cargarListaDocumentos();
            } else {
                alert("Error al renombrar el documento.");
            }
    })  
    .catch(error => {
        console.error("Error en renombrar documento:", error);
    });

    }
}

function eliminarDocumento(event, docId) {
    event.stopPropagation(); 

    if (!confirm("¿Estás segura/o de que querés eliminar este documento?")) return;

    fetch(`/eliminar_documento/${docId}/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error al eliminar el documento.");
        }
        // Eliminar el <li> del DOM
        const li = document.querySelector(`li[data-id="${docId}"]`);
        if (li) li.remove();
        if (getCurrentDocId() === docId) {
                document.querySelector('textarea').value = '';
                setCurrentDocId(null);
            }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("No se pudo eliminar el documento.");
    });
}




