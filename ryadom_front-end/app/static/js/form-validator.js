'use strict';

import { clearErrorHighlights, showError, hideError } from './form-utils.js';

/**
 * Создает объект валидатора формы.
 * @param {Object} config - Объект конфигурации.
 * @param {Array<HTMLElement>} config.fields - Массив полей формы для валидации.
 * @param {string} [config.errorClass='input-error'] - Класс CSS для добавления к недействительным полям.
 * @param {HTMLElement} [config.errorMessageElement] - Элемент для отображения сообщений об ошибках.
 * @param {function} config.validateField - Функция проверки поля формы.
 * @param {function} [config.onValidationSuccess] - Функция, вызываемая, когда все поля действительны.
 * @param {function} [config.onValidationFailure] - Функция, вызываемая при наличии недействительных полей.
 * @returns {Object} Объект валидатора формы с методами `validateForm` и `setupValidation`.
 */
export function createFormValidator(config) {
    const {
        fields,
        errorClass = 'input-error',
        errorMessageElement,
        validateField,
        onValidationSuccess,
        onValidationFailure
    } = config;

    /**
     * Проверяет все поля формы и отображает первую найденную ошибку.
     * Если ошибок нет, вызывает обратный вызов onValidationSuccess.
     * Если есть ошибки, вызывает onValidationFailure с первой найденной ошибкой.
     * @returns {boolean} True, если все поля действительны, в противном случае false.
     */
    function validateForm() {
        clearErrorHighlights(fields, errorClass);
        hideError(errorMessageElement);

        const errors = [];
        
        for (const field of fields) {
            if (!field) continue;
            
            const error = validateField(field);
            if (error) {
                errors.push(error);
            }
        }

        if (errors.length > 0) {
            const firstError = errors[0];
            firstError.field.classList.add(errorClass);
            showError(firstError.message, errorMessageElement);
            
            if (onValidationFailure) {
                onValidationFailure(firstError);
            }
            
            return false;
        }
        
        if (onValidationSuccess) {
            onValidationSuccess();
        }
        
        return true;
    }

    /**
     * Настраивает слушателей событий для проверки полей формы.
     * Добавлены слушатели для событий «input» и «blur».
     */
    function setupValidation() {
        fields.forEach(field => {
            if (!field) return;
            
            field.addEventListener('input', validateForm);
            field.addEventListener('blur', validateForm);
        });
    }

    return {
        validateForm,
        setupValidation
    };
}