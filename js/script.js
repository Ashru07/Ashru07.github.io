// Set footer year
document.getElementById('year').textContent = new Date().getFullYear();

// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(a=>{
  a.addEventListener('click', e=>{
    const href = a.getAttribute('href');
    if(href.startsWith('#')){
      e.preventDefault();
      const el = document.querySelector(href);
      if(el) el.scrollIntoView({behavior:'smooth',block:'start'});
    }
  });
});


// Intersection observer for animations & skill bars
const observer = new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){
      entry.target.classList.add('inview');
      // animate bars
      entry.target.querySelectorAll('.bar').forEach(bar=>{
        const percent = bar.dataset.percent || '0';
        bar.querySelector('span').style.width = percent + '%';
      });
    }
  });
},{threshold:0.15});
// Observe sections and elements but exclude the Home section to avoid animating it on load
document.querySelectorAll('.skill, .section:not(#home), .project-card, .stat').forEach(el=>observer.observe(el));

// Project modal
const modal = document.getElementById('projectModal');
const modalTitle = document.getElementById('modalTitle');
const modalDesc = document.getElementById('modalDesc');
const modalLink = document.getElementById('modalLink');
document.querySelectorAll('.view-btn').forEach(btn=>{
  btn.addEventListener('click', e=>{
    const button = e.currentTarget;
    const card = button.closest('.project-card');
    const link = button.dataset.url || card.dataset.links || '#';
    if(link && link !== '#'){
      window.location.href = link;
      return;
    }
    modalTitle.textContent = card.dataset.title;
    modalDesc.textContent = card.dataset.desc;
    modalLink.href = link;
    modal.setAttribute('aria-hidden','false');
  });
});
document.getElementById('modalClose').addEventListener('click', ()=> modal.setAttribute('aria-hidden','true'));
modal.addEventListener('click', e=>{ if(e.target===modal) modal.setAttribute('aria-hidden','true'); });

// Contact form: open mailto with filled data (no backend)
const form = document.getElementById('contactForm');
if(form){
  form.addEventListener('submit', e=>{
    e.preventDefault();
    const data = new FormData(form);
    const name = data.get('name');
    const email = data.get('email');
    const message = data.get('message');
    const subject = encodeURIComponent('Portfolio contact from ' + name);
    const body = encodeURIComponent(`Name: ${name}%0AEmail: ${email}%0A%0A${message}`);
    window.location.href = `mailto:you@example.com?subject=${subject}&body=${body}`;
  });
}

// Scrollspy: highlight nav link
const navLinks = document.querySelectorAll('.main-nav .nav-link');
const sections = Array.from(navLinks).map(l=>document.querySelector(l.getAttribute('href')));
window.addEventListener('scroll', ()=>{
  let index = sections.findIndex(s=>s && s.getBoundingClientRect().top > 120);
  if(index===-1) index = sections.length - 1;
  navLinks.forEach((link,i)=> link.classList.toggle('active', i===Math.max(0,index-1)));
});

// Theme toggle (light/dark) with persistence
const themeToggle = document.getElementById('themeToggle');
function applyTheme(theme){
  if(theme==='light'){
    document.documentElement.classList.add('light-theme');
    themeToggle.textContent = '🌞';
  } else {
    document.documentElement.classList.remove('light-theme');
    themeToggle.textContent = '🌙';
  }
}

// initialize theme: prefer saved, default to light per user request
const saved = localStorage.getItem('site-theme') || 'light';
applyTheme(saved);

themeToggle.addEventListener('click', ()=>{
  const isLight = document.documentElement.classList.contains('light-theme');
  const next = isLight? 'dark' : 'light';
  applyTheme(next);
  localStorage.setItem('site-theme', next);
});
