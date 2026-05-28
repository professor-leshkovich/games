// ==================== ЛОКАЛЬНОЕ ХРАНИЛИЩЕ ФАЙЛОВ ====================

// ==================== DOM ЭЛЕМЕНТЫ ====================
const filesContainer = document.getElementById('filesContainer');
const codeViewer    = document.getElementById('codeViewer');
const viewerFileName = document.getElementById('viewerFileName');
const codeContent   = document.getElementById('codeContent');
const closeViewerBtn = document.getElementById('closeViewerBtn');

// ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================
function escapeHTML(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// ==================== ОТРИСОВКА ФАЙЛОВ ====================
function renderFiles(files) {
    if (!files || files.length === 0) {
        filesContainer.innerHTML = `
            <div class="empty-message">
                <p>📁 Нет файлов. Добавьте их в массив <code>PYTHON_FILES</code> в script.js</p>
            </div>`;
        return;
    }

    filesContainer.innerHTML = files.map((file, index) => `
        <div class="file-item" data-index="${index}">
            <div class="file-info">
                <span class="file-icon">🐍</span>
                <div class="file-name">
                    ${escapeHTML(file.name)}
                    <small>${escapeHTML(file.size)} • ${escapeHTML(file.modified)}</small>
                </div>
            </div>
            <div class="file-actions">
                <button class="btn-view" data-action="view" data-index="${index}">
                    👁️ Смотреть код
                </button>
            </div>
        </div>
    `).join('');
}

// ==================== ПРОСМОТР КОДА ====================
function showCode(index) {
    const file = PYTHON_FILES[index];
    if (!file) return;

    viewerFileName.textContent = `📄 ${file.name}`;
    codeContent.textContent = file.content;
    codeViewer.classList.add('active');

    // Плавный скролл к окну просмотра
    codeViewer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideCode() {
    codeViewer.classList.remove('active');
}

// ==================== ОБРАБОТЧИКИ СОБЫТИЙ ====================
filesContainer.addEventListener('click', (e) => {
    const button = e.target.closest('button');
    if (!button) return;

    const action = button.getAttribute('data-action');
    const index  = parseInt(button.getAttribute('data-index'), 10);

    if (action === 'view' && !isNaN(index)) {
        showCode(index);
    }
});

closeViewerBtn.addEventListener('click', hideCode);

// ==================== ИНИЦИАЛИЗАЦИЯ ====================
document.addEventListener('DOMContentLoaded', () => {
    renderFiles(PYTHON_FILES);
});