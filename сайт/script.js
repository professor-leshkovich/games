// ==================== ЗАГРУЗКА РЕАЛЬНЫХ .py ФАЙЛОВ ====================
async function loadPythonFiles() {
    try {
        console.log('🔍 Пытаюсь подключиться к серверу...');
        
        // Запрос к серверу, который вернёт список .py файлов
        const response = await fetch('/api/files');
        console.log('📡 Ответ сервера:', response.status);
        
        if (!response.ok) {
            console.error('❌ Сервер ответил с ошибкой:', response.status);
            throw new Error(`Сервер не ответил (статус ${response.status})`);
        }
        
        const files = await response.json();
        console.log('📂 Получены файлы:', files);
        
        if (!files || files.length === 0) {
            console.warn('⚠️ Сервер вернул пустой список файлов');
        }
        
        return files;
    } catch (error) {
        console.error('❌ Ошибка загрузки файлов:', error);
        return null; // Возвращаем null вместо пустого массива
    }
}

async function loadFileContent(filename) {
    try {
        console.log(`📄 Загружаю содержимое: ${filename}`);
        const response = await fetch(`/api/file?name=${encodeURIComponent(filename)}`);
        
        if (!response.ok) {
            console.error('❌ Ошибка загрузки файла:', response.status);
            throw new Error('Не удалось загрузить файл');
        }
        
        const data = await response.json();
        console.log(`✅ Файл ${filename} загружен (${data.content.length} символов)`);
        return data.content;
    } catch (error) {
        console.error('❌ Ошибка загрузки содержимого:', error);
        return '# Ошибка загрузки файла';
    }
}

// ==================== DOM ЭЛЕМЕНТЫ ====================
const filesContainer = document.getElementById('filesContainer');
const codeViewer = document.getElementById('codeViewer');
const viewerFileName = document.getElementById('viewerFileName');
const codeContent = document.getElementById('codeContent');
const closeViewerBtn = document.getElementById('closeViewerBtn');

// ==================== ГЛОБАЛЬНОЕ ХРАНИЛИЩЕ ФАЙЛОВ ====================
let currentFiles = [];

// ==================== ФУНКЦИИ ОТРИСОВКИ ====================
function renderFiles(files) {
    if (!filesContainer) {
        console.error('❌ Контейнер #filesContainer не найден на странице!');
        return;
    }

    // Показываем диагностическое сообщение
    if (files === null) {
        filesContainer.innerHTML = `
            <div class="empty-message">
                <p>❌ Не удалось подключиться к серверу</p>
                <p style="font-size: 0.8rem; margin-top: 10px;">
                    Проверьте что сервер запущен: <br>
                    <code style="background: #330000; padding: 4px 8px; border-radius: 4px;">python server.py</code>
                </p>
                <p style="font-size: 0.8rem; margin-top: 5px;">
                    И откройте: <code style="background: #330000; padding: 4px 8px; border-radius: 4px;">http://localhost:8080</code>
                </p>
            </div>`;
        return;
    }

    if (!files || files.length === 0) {
        filesContainer.innerHTML = `
            <div class="empty-message">
                <p>📁 В папке <code style="background: #330000; padding: 4px 8px; border-radius: 4px;">python_files/</code> нет .py файлов</p>
                <p style="font-size: 0.8rem; margin-top: 10px;">
                    Положите ваши .py файлы в эту папку и обновите страницу
                </p>
            </div>`;
        return;
    }

    filesContainer.innerHTML = files.map((file, index) => `
        <div class="file-item" data-index="${index}" data-filename="${escapeHTML(file.name)}">
            <div class="file-info">
                <span class="file-icon">🐍</span>
                <div class="file-name">
                    ${escapeHTML(file.name)}
                    <small>${escapeHTML(file.size)} • ${escapeHTML(file.modified)}</small>
                </div>
            </div>
            <div class="file-actions">
                <button class="btn-view" data-action="view" data-filename="${escapeHTML(file.name)}">
                    👁️ Смотреть код
                </button>
            </div>
        </div>
    `).join('');
    
    console.log(`✅ Отрисовано ${files.length} файлов`);
}

async function showCode(filename) {
    viewerFileName.textContent = `📄 ${filename}`;
    codeContent.textContent = '⏳ Загрузка...';
    codeViewer.classList.add('active');
    
    const content = await loadFileContent(filename);
    codeContent.textContent = content;
}

function hideCode() {
    codeViewer.classList.remove('active');
}

// ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================
function escapeHTML(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// ==================== ОБРАБОТЧИКИ СОБЫТИЙ ====================
filesContainer.addEventListener('click', (e) => {
    const button = e.target.closest('button');
    if (!button) return;

    const action = button.getAttribute('data-action');
    const filename = button.getAttribute('data-filename');

    if (action === 'view' && filename) {
        showCode(filename);
    }
});

closeViewerBtn.addEventListener('click', hideCode);

// ==================== ИНИЦИАЛИЗАЦИЯ ====================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Страница загружена, начинаю загрузку файлов...');
    currentFiles = await loadPythonFiles();
    renderFiles(currentFiles);
});