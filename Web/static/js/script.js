async function obtenerEstadoServicios() {
    try {
        const respuesta = await fetch('http://31.220.101.168:6061/estado');
        const datos = await respuesta.json();

        if (datos) {
            console.log("Datos de la API recibidos:", datos);

            actualizarEstado('Web', datos['Servidor Web']);
            actualizarEstado('VPS', datos['VPS']);
            actualizarEstado('Bot', datos['Bot Discord']);
            actualizarEstado('CNC', datos['CNC']);
        } else {
            console.error('No se han recibido datos válidos de la API.');
        }
    } catch (error) {
        console.error('Error al obtener el estado de los servicios:', error);
    }
}

function actualizarEstado(servicio, estado) {
    const servicioElement = Array.from(document.querySelectorAll('.tarjeta h2')).find(h2 => h2.textContent === servicio);
    
    if (servicioElement) {
        const estadoElement = servicioElement.nextElementSibling; 

        if (estadoElement) {
            estadoElement.className = 'estado'; 

            switch (estado) {
                case 'Operando':
                    estadoElement.classList.add('operando');
                    estadoElement.textContent = 'Operando';
                    break;
                case 'Intermitente':
                    estadoElement.classList.add('intermitente');
                    estadoElement.textContent = 'Intermitente';
                    break;
                case 'Inalcanzable':
                    estadoElement.classList.add('inalcanzable');
                    estadoElement.textContent = 'Inalcanzable';
                    break;
                default:
                    estadoElement.classList.add('inalcanzable');
                    estadoElement.textContent = 'Desconocido';
                    break;
            }
        }
    }
}

window.onload = function() {
    obtenerEstadoServicios(); 
    setInterval(obtenerEstadoServicios, 1000); 
};
