'use strict';

/**
 * Убирает все пробелы в данной строке.
 * @param {string} value - Строка, из которой нужно убрать пробелы
 * @returns {string} Строка без пробелов.
 */
export function removeSpaces(value) {
    return value.replace(/\s/g, '');
}

/**
 * Запрещает пользователю вводить пробелы в поле ввода.
 * Если пользователь введет пробел, функция удалит его и
 * переместит позицию курсора на один символ влево.
 * @param {Event} event - Объект события входного события.
 */
export function preventSpaces(event) {
    const cursorPosition = this.selectionStart;
    
    const newValue = removeSpaces(this.value);
    
    if (this.value !== newValue) {
        this.value = newValue;
        
        this.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
    }
}

/**
 * Устанавливает обработку событий ввода и вставления текста
 * для заданных полей ввода, запрещая пользователю вводить пробелы.
 * @param {Array<HTMLInputElement>} fields - Массив полей ввода, для которых
 * нужно настроить обработку событий.
 */
export function setupSpacePrevention(fields) {
    fields.forEach(field => {
        if (!field) return;
        
        field.addEventListener('input', preventSpaces);
        field.addEventListener('paste', function() {
            setTimeout(() => {
                const newValue = removeSpaces(this.value);
                if (this.value !== newValue) {
                    this.value = newValue;
                }
            }, 0);
        });
    });
}

/**
 * Показывает сообщение об ошибке в заданном элементе.
 * Если элемент не задан, то функция не делает ничего.
 * @param {string} message - Сообщение об ошибке, которое нужно показать.
 * @param {HTMLElement} errorMessageElement - Элемент, в котором нужно показать сообщение об ошибке.
*/
export function showError(message, errorMessageElement) {
    if (errorMessageElement) {
        errorMessageElement.textContent = message;
        errorMessageElement.style.display = 'block';
    }
}

/**
 * Скрывает сообщение об ошибке в заданном элементе.
 * Если элемент не задан, то функция не делает ничего.
 * @param {HTMLElement} errorMessageElement - Элемент, в котором нужно скрыть сообщение об ошибке.
 */
export function hideError(errorMessageElement) {
    if (errorMessageElement) {
        errorMessageElement.style.display = 'none';
    }
}

/**
 * Очищает все ошибки в полях, заданных в массиве fields.
 * Ошибки обозначаются классом errorClass.
 * Если errorClass не задан, то функция использует класс 'input-error' по умолчанию.
 * @param {Array<HTMLElement>} fields - Массив полей, в которых нужно скрыть ошибки.
 * @param {string} [errorClass='input-error'] - Класс, которым обозначаются ошибки.
 */
export function clearErrorHighlights(fields, errorClass = 'input-error') {
    fields.forEach(input => {
        if (input) input.classList.remove(errorClass);
    });
}