'use strict';

import { showError, hideError } from './form-utils.js';

/**
 * Настраивает форму для отправки данных на сервер.
 * @param {Object} config - Объект конфигурации.
 * @param {HTMLFormElement} config.form - Форма, которую нужно настроить.
 * @param {HTMLButtonElement} config.submitBtn - Кнопка отправки формы.
 * @param {Array<HTMLInputElement>} config.fields - Массив полей формы, которые нужно валидировать.
 * @param {HTMLElement} config.errorMessageElement - Элемент, в котором нужно отображать сообщение об ошибке.
 * @param {function} config.prepareData - Функция, которая должна вернуть объект с данными для отправки на сервер.
 * @param {string} config.apiUrl - URL сервера, на который нужно отправлять данные.
 * @param {function} [config.onSuccess] - Функция, вызываемая, когда отправка формы прошла успешно.
 * @param {function} [config.onError] - Функция, вызываемая, когда отправка формы закончилась ошибкой.
 * @param {string} [config.loadingText='Отправляем...'] - Текст, который будет отображаться на кнопке отправки формы во время отправки.
 * @param {string} [config.defaultText='Отправить'] - Текст, который будет отображаться на кнопке отправки формы по умолчанию.
 */
export function setupFormSubmit(config) {
    const {
        form,
        submitBtn,
        fields,
        errorMessageElement,
        prepareData,
        apiUrl,
        onSuccess,
        onError,
        loadingText = 'Отправляем...',
        defaultText = 'Отправить'
    } = config;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (config.validate && !config.validate()) return;
        
        submitBtn.disabled = true;
        submitBtn.textContent = loadingText;
        
        hideError(errorMessageElement);

        try {
            const data = prepareData();
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(data),
                credentials: 'include'
            });

            if (response.ok) {
                onSuccess();
            } else {
                const errorData = await response.json().catch(() => null);
                
                if (errorData && errorData.detail && Array.isArray(errorData.detail)) {
                    const firstError = errorData.detail[0];
                    showError(firstError.msg || 'Ошибка валидации данных', errorMessageElement);
                    
                    if (firstError.loc && firstError.loc[1]) {
                        const field = document.getElementById(firstError.loc[1]);
                        if (field) {
                            field.classList.add('input-error');
                            field.focus();
                        }
                    }
                } else {
                    showError(errorData?.message || 'Ошибка. Попробуйте позже.', errorMessageElement);
                }
                
                if (onError) onError(errorData);
            }
        } catch (error) {
            showError('Ошибка соединения с сервером. Проверьте интернет-соединение.', errorMessageElement);
            console.error('Form submission error:', error);
            if (onError) onError(error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = defaultText;
        }
    });
}