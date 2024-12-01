document.addEventListener('DOMContentLoaded', () => {
    const formFiltrar = document.getElementById('form-filtrar');
    const formModificar = document.getElementById('form-modificar');
    const datosFiltrados = document.getElementById('datos-filtrados');

    formFiltrar.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('filtrar-email').value;

        try {
            const response = await fetch('http://31.220.101.168:9091/api/filtrar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }

            const data = await response.json();

            if (data.nombre) {
                datosFiltrados.innerHTML = `
                    <div><strong>Nombre:</strong> <span>${data.nombre}</span></div>
                    <div><strong>Email:</strong> <span>${data.email}</span></div>
                    <div><strong>Rol:</strong> <span>${data.rol}</span></div>
                    <div><strong>Contraseña:</strong> <span>${data.password}</span></div>
                `;
                document.getElementById('modificar-email').value = data.email;
            } else {
                datosFiltrados.innerHTML = `<div><strong>${data.message}</strong></div>`;
            }
        } catch (error) {
            alert(`Error al filtrar usuario: ${error.message}`);
        }
    });

    formModificar.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('modificar-email').value;
        const nombre = document.getElementById('modificar-nombre').value;
        const rol = document.getElementById('modificar-rol').value;
        const password = document.getElementById('modificar-password').value;

        try {
            const response = await fetch('http://31.220.101.168:9091/api/modificar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, nombre, rol, password })
            });

            const data = await response.json();
            alert(data.message);
        } catch (error) {
            alert(`Error al modificar usuario: ${error.message}`);
        }
    });
});
