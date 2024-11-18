// Código JavaScript para manejar el envío con AJAX  en la creacion
$(document).ready(function () {
    $('#formCrearVendedor').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío tradicional del formulario

        // Obtener los datos del formulario
        var formData = $(this).serialize();

        // Enviar datos con AJAX
        $.ajax({
            type: 'POST',
            url: '/vendedores_crear',
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    alert(response.message); // Mensaje de éxito
                    window.location.href = '/vendedores_ver';
                }
            },
            error: function (xhr) {
                // Procesar errores específicos y mostrar mensajes en el HTML
                const errores = xhr.responseJSON ? xhr.responseJSON.errores : {};

                // Limpiar mensajes de error previos
                $('#tipoDocumentoError').text('');
                $('#numeroDocumentoError').text('');
                $('#nombreVnededorError').text('');
                $('#telefonoVendedorError').text('');
                $('#direccionVendedorError').text('');
                $('#emailVendedorError').text('');
                $('#mensajeErrorGeneral').text('');

                // Mostrar mensajes de error específicos;
                if (errores.tipoDocumento) {
                    $('#tipoDocumentoError').text(errores.tipoDocumento);
                }
                if (errores.numeroDocumento) {
                    $('#numeroDocumentoError').text(errores.numeroDocumento);
                }
                if (errores.nombreVendedor) {
                    $('#nombreVendedorError').text(errores.nombreVendedor);
                }
                if (errores.telefonoVendedor) {
                    $('#telefonoVendedorError').text(errores.telefonoVendedor);
                }
                if (errores.direccionVendedor) {
                    $('#direccionVendedorError').text(errores.direccionVendedor);
                }
                if (errores.emailVendedor) {
                    $('#emailVendedorError').text(errores.emailVendedor);
                }

                // Mostrar mensaje de error general si existen otros errores
                if (Object.keys(errores).length > 0) {
                    $('#mensajeErrorGeneral').text("Corrige los errores en el formulario antes de guardar.");
                } else if (xhr.responseJSON && xhr.responseJSON.message) {
                    $('#mensajeErrorGeneral').text(xhr.responseJSON.message);
                } else {
                    $('#mensajeErrorGeneral').text('Ocurrió un error inesperado. Inténtalo nuevamente.');
                }
            }
        });
    });
});

//Código JavaScript para validacion de datos duplicados(numero_documento,email) del vendedor 

// Asignar la validación solo a los campos específicos
$('#numeroDocumentoVendedor').on('blur', function () {
    validarVendedor('numeroDocumento');
});

$('#emailVendedor').on('blur', function () {
    validarVendedor('emailVendedor');
});

function validarVendedor(campo) {
    // Recopilar los valores de los campos
    const numeroDocumento = $('#numeroDocumentoVendedor').val().trim();
    const emailVendedor = $('#emailVendedor').val().trim();

    // Crear un objeto de datos para enviar solo los campos que deben validarse
    const datos = {};
    if (campo === 'numeroDocumento' && numeroDocumento !== '') {
        datos.numeroDocumento = numeroDocumento;
    }
    if (campo === 'emailVendedor' && emailVendedor !== '') {
        datos.emailVendedor = emailVendedor;
    }

    // Si no hay datos que validar, salir de la función
    if (Object.keys(datos).length === 0) return;

    // Enviar datos al backend para validación
    $.ajax({
        type: 'POST',
        url: '/validar_vendedor',
        contentType: 'application/json',
        data: JSON.stringify(datos),
        success: function (response) {
            // Limpiar mensajes de error para los campos que se están validando
            if (campo === 'numeroDocumento') {
                $('#numeroDocumentoError').text('');
            }
            if (campo === 'emailVendedor') {
                $('#emailVendedorError').text('');
            }
        },
        error: function (xhr) {
            const errores = xhr.responseJSON.errores || {};
            // Mostrar mensajes de error específicos solo para los campos que se están validando
            if (campo === 'numeroDocumento') {
                $('#numeroDocumentoError').text(errores.numeroDocumento || '');
            }
            if (campo === 'emailVendedor') {
                $('#emailVendedorError').text(errores.emailVendedor || '');
            }
        }
    });
}
