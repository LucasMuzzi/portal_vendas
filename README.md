# Portal de Vendas - Desafio SEMEQ

Este projeto foi desenvolvido como parte do teste de aptidão para a vaga de Desenvolvedor na SEMEQ. Trata-se de um sistema de vendas completo construído com Python, Django, PostgreSQL e MongoDB, focado em uma interface rica e interativa no frontend.

## ✨ Funcionalidades

- **Autenticação Dupla:** Tela de login com perfis distintos para **Vendedores** (com usuário e senha) e **Clientes** (com acesso via e-mail).
- **Tela de Vendas Interativa:** Interface de ponto de venda (POS) single-page para registro de novas vendas.
- **Busca de Produtos Assíncrona:** Campo de busca que consulta o banco de dados em tempo real para sugerir produtos.
- **Carrinho de Compras Dinâmico:** Adição e remoção de itens da venda com atualização automática do total.
- **Integração com API Externa:** Preenchimento automático de endereço a partir do CEP, utilizando a API do ViaCEP.
- **Persistência Híbrida de Dados:**
  - **PostgreSQL:** Utilizado como banco de dados principal para dados transacionais (Produtos, Clientes, Vendas).
  - **MongoDB:** Utilizado para armazenar um "snapshot" de cada venda, servindo como um banco de dados de histórico.
- **Histórico de Vendas:** Tela para consulta de vendas passadas, com uma visão geral para vendedores e uma visão filtrada por e-mail para clientes.
- **Testes Automatizados:** Suíte de testes unitários para garantir a qualidade e a integridade da lógica de negócio no backend.
- **Design Responsivo:** Interface adaptável a diferentes tamanhos de tela, construída com Bootstrap 5.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.12, Django 4.2
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Banco de Dados Principal:** PostgreSQL
- **Banco de Dados de Histórico:** MongoDB
- **Dependências Python:** `psycopg2-binary`, `pymongo`, `Pillow`

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o ambiente de desenvolvimento local.

### Pré-requisitos

- Python 3.10+
- Git
- PostgreSQL instalado e rodando.
- MongoDB instalado e rodando (ou um cluster no MongoDB Atlas).

### 1. Clonar o Repositório

````bash
git clone [https://github.com/LucasMuzzi/portal_vendas.git](https://github.com/LucasMuzzi/portal_vendas.git)
cd portal_vendas
````

### 2. Configurar o Ambiente

Crie e ative um ambiente virtual:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
````

Instale todas as dependências do projeto:

```bash
pip install -r requirements.txt
```

### 3. Banco de Dados

**PostgreSQL:**

1.  Crie um novo banco de dados no PostgreSQL (ex: `portal_vendas_db`).
2.  Edite diretamente o `settings.py` com seus dados:

    ```python
    # portal_vendas/settings.py
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'nome_do_seu_banco',
            'USER': 'seu_usuario_postgres',
            'PASSWORD': 'sua_senha_postgres',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

**MongoDB:**

1.  Garanta que seu servidor MongoDB esteja acessível.
2.  Configure a `MONGO_URI` no arquivo `settings.py`:
    ```python
    # portal_vendas/settings.py
    MONGO_URI = "mongodb://localhost:27017/" # Ou a string de conexão do Atlas
    MONGO_DATABASE_NAME = "historico_vendas"
    ```

### 4. Preparar o Banco e Rodar a Aplicação

Aplique as migrações para criar as tabelas no PostgreSQL:

```bash
python manage.py migrate
```

Carregue os dados iniciais de produtos na tabela:

```bash
python manage.py loaddata produtos.json
```

Crie um superusuário para acessar o painel de admin e a área do vendedor:

```bash
python manage.py createsuperuser
```

Siga os prompts para criar seu usuário e senha.

Finalmente, inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

A aplicação estará disponível em `http://127.0.0.1:8000/`.

## 🧪 Testes

O projeto conta com uma suíte de testes automatizados para garantir a qualidade do backend.

### Como Executar os Testes

Para rodar todos os testes, execute o seguinte comando:

```bash
python manage.py test
```

### Cobertura dos Testes

- **Modelos:** Testa a criação e o método `__str__` do modelo `Produto`.
- **API:** Valida o endpoint de busca de produtos, verificando se a resposta é `200 OK`, em formato `JSON`, e se os resultados correspondem à busca.
- **Views:** Testa o registro completo de uma venda por um usuário logado, verificando a criação dos objetos `Cliente`, `Venda` e `VendaProduto` no banco de dados.

## 👤 Autor

**Lucas Muzzi**

- [LinkedIn](https://www.linkedin.com/in/lucas-muzzi-b804ab219/)
- [GitHub](https://github.com/LucasMuzzi)
