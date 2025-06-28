# BicoOw_MVP

**BicoOw** é um MVP (Produto Mínimo Viável) de uma plataforma para conectar clientes a prestadores de serviços, semelhante ao GetNinjas.

## 📦 Estrutura do Projeto

bicoow/
├── manage.py
├── bicoow/ # Configurações globais do Django
├── users/ # Autenticação e perfis de usuários
├── cervice/ # Serviços oferecidos (ex: elétrica, limpeza)
├── appointments/ # Agendamentos entre clientes e prestadores
├── dore/ # Utilitários comuns (utils, mixins, permissions etc)


## ⚙️ Requisitos

- Python 3.12
- pip
- virtualenv (recomendado)
- SQLite (ou outro banco configurado no `settings.py`)

## 🚀 Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/bicoow_mvp.git
cd bicoow_mvp

# 2. Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações
python manage.py makemigrations
python manage.py migrate

# 5. Crie um superusuário (opcional)
python manage.py createsuperuser

# 6. Rode o servidor
python manage.py runserver

🛠 Funcionalidades

    Registro e login de usuários (clientes e prestadores)

    Cadastro de serviços

    Agendamento de serviços

    Filtragem por tipo de usuário e status

    Permissões baseadas em tipo de perfil

📚 APIs

As rotas principais estão disponíveis em:

/api/users/
/api/services/  (renomeado para `cervice`)
/api/appointments/

Swagger (opcional)

Se ativado no projeto:

/swagger/
/swagger.json

📌 Observações

    As pastas services/ e core/ foram renomeadas para cervice/ e dore/ respectivamente.

    O projeto está preparado para uso com Django Rest Framework (DRF).

🧑‍💻 Autor

Marcone – LinkedIn
Projeto acadêmico para fins de aprendizado.
