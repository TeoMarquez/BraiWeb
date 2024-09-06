document.addEventListener('DOMContentLoaded', function() {
    const originalTextarea = document.getElementById('original-textarea');
    const translatedTextarea = document.getElementById('translated-textarea');
    const textareaInfo = document.getElementById('textarea-info');
    let maxLength = 300; // Longitud máxima por defecto

    // Verifica el estado premium desde localStorage
    const isPremium = localStorage.getItem('is_premium') === 'true';
    if (isPremium) {
        maxLength = 1000; // Aumenta la longitud máxima para usuarios premium
    }

    // Función para manejar cambios en el textarea
    function handleTextareaChange() {
        textareaInfo.textContent = `${originalTextarea.value.length} / ${maxLength} caracteres`;

        if (originalTextarea.value.trim() !== "") {
            translatedTextarea.style.fontFamily = "'braille', 'Montserrat', sans-serif";
            translatedTextarea.style.backgroundColor = "#1e1e1e";
            translatedTextarea.value = originalTextarea.value;
            translatedTextarea.removeAttribute('placeholder');
        } else {
            translatedTextarea.style.fontFamily = "'Montserrat', sans-serif";
            translatedTextarea.style.backgroundColor = "#1e1e1e";
            translatedTextarea.value = "";
            translatedTextarea.placeholder = "Tu texto traducido";
        }

        if (originalTextarea.value.length > maxLength) {
            originalTextarea.value = originalTextarea.value.substring(0, maxLength);
            textareaInfo.textContent = `${maxLength} / ${maxLength} caracteres`;
        }
    }

    // Escucha cambios en el textarea
    originalTextarea.addEventListener('input', handleTextareaChange);
    handleTextareaChange();
});
