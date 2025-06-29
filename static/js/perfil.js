document.addEventListener('DOMContentLoaded', function () {
    // Máscara para CEP (00000-000)
    const cepInput = document.getElementById('cep');
    if (cepInput) {
      cepInput.addEventListener('input', function () {
          let v = this.value.replace(/\D/g, '');
          if (v.length > 5) {
              this.value = v.substr(0, 5) + '-' + v.substr(5, 3);
          } else {
              this.value = v;
          }
      });

      // Consulta CEP para preencher cidade
      cepInput.addEventListener('blur', function () {
          const cep = this.value.replace(/\D/g, '');
          if (cep.length === 8) {
              fetch(`/users/ajax/consulta-cep/?cep=${cep}`)
                  .then(response => response.json())
                  .then(data => {
                      if (!data.error) {
                          const cidadeInput = document.getElementById('cidade');
                          if (cidadeInput) cidadeInput.value = data.localidade || '';
                      } else {
                          alert('CEP não encontrado.');
                          const cidadeInput = document.getElementById('cidade');
                          if (cidadeInput) cidadeInput.value = '';
                      }
                  }).catch(() => {
                      alert('Erro ao consultar CEP.');
                      const cidadeInput = document.getElementById('cidade');
                      if (cidadeInput) cidadeInput.value = '';
                  });
          }
      });
    }

    // Máscara para telefone (99) 99999-9999
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
      phoneInput.addEventListener('input', function () {
          let v = this.value.replace(/\D/g, '');
          if (v.length > 10) {
              this.value = '(' + v.substr(0, 2) + ') ' + v.substr(2, 5) + '-' + v.substr(7, 4);
          } else if (v.length > 5) {
              this.value = '(' + v.substr(0, 2) + ') ' + v.substr(2);
          } else if (v.length > 2) {
              this.value = '(' + v.substr(0, 2) + ') ' + v.substr(2);
          } else {
              this.value = v;
          }
      });
    }
});
