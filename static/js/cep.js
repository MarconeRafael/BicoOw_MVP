// static/js/cep.js
document.addEventListener('DOMContentLoaded', () => {
  const cepInput = document.getElementById('cep');
  if (!cepInput) return;

  let timeout;
  cepInput.addEventListener('input', () => {
    // Remove tudo que não é dígito e limita a 8 caracteres
    const raw = cepInput.value.replace(/\D/g, '').slice(0, 8);
    // Formata 00000-000 automaticamente
    cepInput.value = raw.length > 5
      ? `${raw.slice(0,5)}-${raw.slice(5)}`
      : raw;

    // Se tiver 8 dígitos, dispara busca com debounce
    clearTimeout(timeout);
    if (raw.length === 8) {
      timeout = setTimeout(() => {
        fetch(`/users/ajax/consulta-cep/?cep=${raw}`)
          .then(res => res.json())
          .then(data => {
            if (!data.error) {
              document.getElementById('endereco')?.value = data.endereco || '';
              document.getElementById('cidade')?.value   = data.cidade   || '';
              document.getElementById('estado')?.value  = data.estado   || '';
            } else {
              ['endereco','cidade','estado'].forEach(id => {
                document.getElementById(id)?.value = '';
              });
            }
          })
          .catch(() => {
            ['endereco','cidade','estado'].forEach(id => {
              document.getElementById(id)?.value = '';
            });
          });
      }, 300);
    }
  });
});
