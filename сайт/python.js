// Этот файл подключается ПОСЛЕ eel.js в index.html

async function передатьФайл(событие) {
    const кнопка = событие.target;
    // Вызов Python-функции через eel
    await eel.передатьФайл(кнопка.dataset)();
}