document.addEventListener('DOMContentLoaded', () => {
  const phoneInput = document.getElementById('phone');
  if (!phoneInput) return;

  phoneInput.addEventListener('input', () => {
    const v = phoneInput.value.replace(/\D/g, '').slice(0, 11);
    if (v.length >= 11) {
      phoneInput.value = `(${v.slice(0,2)}) ${v.slice(2,7)}-${v.slice(7)}`;
    } else if (v.length >= 7) {
      phoneInput.value = `(${v.slice(0,2)}) ${v.slice(2,6)}-${v.slice(6)}`;
    } else if (v.length >= 3) {
      phoneInput.value = `(${v.slice(0,2)}) ${v.slice(2)}`;
    } else if (v.length >= 1) {
      phoneInput.value = `(${v}`;
    } else {
      phoneInput.value = '';
    }
  });
});
