const CONTACT_EMAIL = 'hey@gambhir.dev';

// Mobile menu
const toggle = document.querySelector('.nav__toggle');
const links = document.getElementById('nav-links');
toggle.addEventListener('click', () => {
  const open = links.classList.toggle('is-open');
  toggle.setAttribute('aria-expanded', String(open));
});
links.addEventListener('click', (e) => {
  if (e.target.closest('a')) {
    links.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }
});

// Proposal tabs (arrow keys move between tabs)
const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(tab) {
  tabs.forEach((t) => {
    const selected = t === tab;
    t.setAttribute('aria-selected', String(selected));
    t.tabIndex = selected ? 0 : -1;
    document.getElementById(t.getAttribute('aria-controls')).hidden = !selected;
  });
  tab.focus();
}
tabs.forEach((tab, i) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') selectTab(tabs[(i + 1) % tabs.length]);
    if (e.key === 'ArrowLeft') selectTab(tabs[(i - 1 + tabs.length) % tabs.length]);
  });
});

// Contact: no backend, so the form opens the visitor's email app
const emailLink = document.getElementById('contact-email');
emailLink.href = `mailto:${CONTACT_EMAIL}`;
emailLink.textContent = CONTACT_EMAIL;

document.getElementById('contact-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const data = new FormData(e.target);
  const subject = `Lynq NTN-Pulse enquiry from ${data.get('name')}`;
  const body = [
    data.get('message'),
    '',
    `${data.get('name')}${data.get('org') ? `, ${data.get('org')}` : ''}`,
    data.get('email'),
  ].join('\n');
  window.location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
});

document.getElementById('year').textContent = new Date().getFullYear();
