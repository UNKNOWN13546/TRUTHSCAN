// Ease-out cubic calculation
function easeOutCubic(t) {
  return 1 - Math.pow(1 - t, 3);
}

// Counting animation for metrics
function animateCounter(el, target, decimals, duration) {
  const start = performance.now();
  
  function frame(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easeOutCubic(progress);
    const current = eased * target;
    
    el.textContent = current.toFixed(decimals);
    
    if (progress < 1) {
      requestAnimationFrame(frame);
    } else {
      el.textContent = target.toFixed(decimals);
    }
  }
  
  requestAnimationFrame(frame);
}

// Intersection Observer for the Stats section
function initStatsCounter() {
  const statsSection = document.querySelector('.stats');
  if (!statsSection) return;

  const statItems = [
    { id: 'stat-latency', target: 85, decimals: 0 },
    { id: 'stat-accuracy', target: 99.8, decimals: 1 },
    { id: 'stat-pillars', target: 6, decimals: 0 },
    { id: 'stat-scans', target: 1.4, decimals: 1 }
  ];

  let animated = false;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animated) {
        animated = true;
        
        statItems.forEach((item, i) => {
          const el = document.getElementById(item.id);
          if (!el) return;
          
          const startDelay = 480 + (i * 90);
          const duration = 1500 + (i * 80);
          
          setTimeout(() => {
            animateCounter(el, item.target, item.decimals, duration);
          }, startDelay);
        });
        
        observer.disconnect();
      }
    });
  }, { threshold: 0.25 });

  observer.observe(statsSection);
}

// Mobile Sheet Navigation
function initMobileMenu() {
  const burgerBtn = document.getElementById('burger-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileOverlay = document.getElementById('mobile-overlay');

  if (!burgerBtn || !mobileMenu || !mobileOverlay) return;

  function toggleMenu(show) {
    const isOpen = show !== undefined ? show : !mobileMenu.classList.contains('open');
    burgerBtn.classList.toggle('active', isOpen);
    burgerBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    mobileMenu.classList.toggle('open', isOpen);
    mobileOverlay.classList.toggle('open', isOpen);
    document.body.classList.toggle('menu-open', isOpen);
  }

  burgerBtn.addEventListener('click', () => toggleMenu());
  mobileOverlay.addEventListener('click', () => toggleMenu(false));

  document.querySelectorAll('.mobile-link').forEach(link => {
    link.addEventListener('click', () => toggleMenu(false));
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
      toggleMenu(false);
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 720 && mobileMenu.classList.contains('open')) {
      toggleMenu(false);
    }
  });
}

// Truthscan Modal Interaction
function initTruthscanModal() {
  const modal = document.getElementById('truthscan-modal');
  const closeBtn = document.getElementById('modal-close');
  const openButtons = document.querySelectorAll('[data-open-truthscan]');

  if (!modal) return;

  function setModal(open) {
    modal.classList.toggle('open', open);
    if (open) {
      document.body.style.overflow = 'hidden';
      if (window.lucide) lucide.createIcons();
    } else {
      document.body.style.overflow = '';
    }
  }

  openButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      setModal(true);
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => setModal(false));
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      setModal(false);
    }
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) {
      setModal(false);
    }
  });
}

// Reveal the landing page once its resources are ready.
function initPageLoader() {
  const loader = document.getElementById('ts-loader');
  if (!loader) return;

  const startedAt = performance.now();
  let dismissed = false;

  function dismissLoader() {
    if (dismissed) return;
    dismissed = true;
    loader.classList.add('ts-done');
  }

  function afterLoad() {
    const minimumVisibleMs = 2000;
    const remaining = Math.max(0, minimumVisibleMs - (performance.now() - startedAt));
    window.setTimeout(dismissLoader, remaining);
  }

  if (document.readyState === 'complete') {
    afterLoad();
  } else {
    window.addEventListener('load', afterLoad, { once: true });
  }

  window.setTimeout(dismissLoader, 3500);
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
  initPageLoader();
  initStatsCounter();
  initMobileMenu();
  initTruthscanModal();
  if (window.lucide) {
    lucide.createIcons();
  }
});
