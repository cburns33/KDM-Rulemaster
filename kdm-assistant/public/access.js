const form = document.querySelector('#access-form');
const code = document.querySelector('#code');
const error = document.querySelector('#error');
const requested = new URLSearchParams(location.search).get('next');
const next = requested && requested.startsWith('/') && !requested.startsWith('//') ? requested : '/';

form.addEventListener('submit', async event => {
  event.preventDefault();
  error.hidden = true;
  const response = await fetch('/api/access', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: code.value }),
  });
  if (response.ok) {
    location.replace(next);
    return;
  }
  const body = await response.json().catch(() => ({}));
  error.textContent = body.error || 'Unable to enter the archive.';
  error.hidden = false;
  code.select();
});
