// =============================================
// POCKET DOCTOR — MAIN JS
// Dark mode + scroll animations
// =============================================

(function () {
    var html = document.getElementById('pd-html');
    var toggle = document.getElementById('pd-dark-toggle');

    // Auth pages opt out of dark mode via data-no-dark attribute on body
    // Their split-screen design has fixed light/dark panels
    var isAuthPage = document.body.getAttribute('data-no-dark') === 'true';

    if (!isAuthPage && html) {
        // Apply saved dark mode preference
        function applyDark(on) {
            if (on) {
                html.classList.add('dark');
                if (toggle) toggle.textContent = 'Light';
            } else {
                html.classList.remove('dark');
                if (toggle) toggle.textContent = 'Dark';
            }
        }

        var saved = localStorage.getItem('pd_dark') === 'true';
        applyDark(saved);

        if (toggle) {
            toggle.addEventListener('click', function () {
                var now = !html.classList.contains('dark');
                applyDark(now);
                localStorage.setItem('pd_dark', now);
            });
        }
    }

    // =============================================
    // SCROLL ANIMATIONS
    // =============================================

    var animated = document.querySelectorAll('.fade-up, .fade-in');

    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    var el = entry.target;
                    var delay = parseInt(el.getAttribute('data-delay') || '0', 10);
                    setTimeout(function () { el.classList.add('in'); }, delay);
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.1 });

        animated.forEach(function (el) { observer.observe(el); });
    } else {
        // Fallback for browsers without IntersectionObserver
        animated.forEach(function (el) { el.classList.add('in'); });
    }

    // Hero elements trigger on load with stagger
    window.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.hero-animate').forEach(function (el, i) {
            setTimeout(function () { el.classList.add('in'); }, i * 110);
        });
    });

    // Mockup "analyzing" pulse animation
    window.addEventListener('DOMContentLoaded', function () {
        var analyzing = document.querySelector('.m-analyzing');
        if (!analyzing) return;
        var visible = true;
        setInterval(function () {
            visible = !visible;
            analyzing.style.opacity = visible ? '1' : '0.2';
        }, 900);
    });

    // Auto-grow textareas (used on prescription form)
    document.querySelectorAll('.rx-textarea').forEach(function (el) {
        function resize() {
            el.style.height = 'auto';
            el.style.height = el.scrollHeight + 'px';
        }
        el.addEventListener('input', resize);
        resize(); // run once on load in case there's existing content (edit mode)
    });

})();
