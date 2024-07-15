document.addEventListener('DOMContentLoaded', function() {
    const originalTextarea = document.getElementById('original-textarea');
    const translatedTextarea = document.getElementById('translated-textarea');
    const textareaInfo = document.getElementById('textarea-info');
    const defaultText = "Ingrese su texto aquí";
    const maxLength = 300; // Máximo número de caracteres permitidos

    // Función para manejar el cambio de fuente, contenido y contador de caracteres

    function handleTextareaChange() {

        // Contar caracteres
        const remainingChars = maxLength - originalTextarea.value.length;
        textareaInfo.textContent = `${originalTextarea.value.length} / ${maxLength} caracteres`;

        // Actualizar el estilo del textarea traducido y su contenido
        if (originalTextarea.value.trim() !== defaultText && originalTextarea.value.trim() !== "") {
            translatedTextarea.style.fontFamily = "'braille', 'Montserrat', sans-serif";
            translatedTextarea.style.backgroundColor = "#ABE188"; // Ajusta el color de fondo según sea necesario
            translatedTextarea.value = originalTextarea.value;
            translatedTextarea.removeAttribute('placeholder'); // Elimina el placeholder si hay contenido
        } else {
            
            translatedTextarea.style.fontFamily = "'Montserrat', sans-serif";
            translatedTextarea.style.backgroundColor = "#ABE188"; // Ajusta el color de fondo según sea necesario
            translatedTextarea.value = ""; // Borra cualquier contenido
            translatedTextarea.placeholder = "Tu texto traducido"; // Restaura el placeholder
        }

        // Limitar longitud de caracteres
        if (originalTextarea.value.length > maxLength) {
            originalTextarea.value = originalTextarea.value.substring(0, maxLength);
            textareaInfo.textContent = `${maxLength} / ${maxLength} caracteres`;
        }
    }

    // Escuchar cambios en el originalTextarea
    originalTextarea.addEventListener('input', handleTextareaChange);

    // Llamar a la función al cargar la página
    handleTextareaChange();
});
