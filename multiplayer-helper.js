window.addEventListener('DOMContentLoaded', () => {
    // التأكد إننا جوه لعبة جماعية
    const container = document.createElement('div');
    container.innerHTML = `
        <div style="text-align: center; margin: 15px; padding: 10px; background: #1e293b; border-radius: 8px; border: 1px solid #38bdf8; max-width: 400px; margin-left: auto; margin-right: auto;">
            <p style="color: #38bdf8; font-size: 13px; margin-bottom: 8px;">للعب أسرع وبدون متصفح:</p>
            <button onclick="openInApp()" style="background: #38bdf8; color: #0f172a; border: none; padding: 8px 15px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px;">
                🚀 افتح الغرفة داخل تطبيق فلامينجو
            </button>
        </div>
    `;
    document.body.insertBefore(container, document.body.firstChild);
});

function openInApp() {
    let currentFullUrl = window.location.href;
    let deepLink = "flamengogames://open?url=" + encodeURIComponent(currentFullUrl);
    window.location.href = deepLink;
}
