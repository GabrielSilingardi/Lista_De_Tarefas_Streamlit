# Lista de Tarefas 📝

Este é um projeto de gerenciamento de tarefas desenvolvido com **Streamlit**, que permite aos usuários criar, visualizar, atualizar e excluir tarefas. O sistema inclui funcionalidades de autenticação (login e cadastro) e integração com um banco de dados SQL Server.

## Funcionalidades

### Autenticação
- **Cadastro de Usuário**: Permite que novos usuários se cadastrem com nome, e-mail e senha.
  - A senha deve conter letras maiúsculas, minúsculas, números, caracteres especiais e ter no mínimo 8 caracteres.
- **Login**: Usuários podem acessar suas tarefas utilizando e-mail e senha.
- **Validação de Credenciais**: As senhas são armazenadas de forma segura utilizando o algoritmo **Argon2**.

### Gerenciamento de Tarefas
- **Criação de Tarefas**: Usuários podem criar novas tarefas.
- **Edição de Tarefas**: É possível atualizar o nome, descrição, status, data de início e data de conclusão de cada tarefa.
- **Exclusão de Tarefas**: Tarefas podem ser excluídas individualmente.
- **Visualização de Tarefas**: As tarefas são exibidas em uma tabela com as seguintes colunas:
  - Status
  - Nome
  - Descrição
  - Data de Início
  - Data de Conclusão
  - Botão para exclusão

### Interface do Usuário
- **Interface Responsiva**: Desenvolvida com **Streamlit**, a interface é simples e intuitiva.
- **Notificações**: Mensagens de feedback são exibidas para ações como login, cadastro, criação e exclusão de tarefas.

## Tecnologias Utilizadas
- **Python**: Linguagem principal do projeto.
- **Streamlit**: Framework para criação de interfaces web.
- **PyODBC**: Biblioteca para conexão com o banco de dados SQL Server.
- **Argon2**: Para hashing seguro de senhas.
- **dotenv**: Para gerenciamento de variáveis de ambiente.
- **Pandas**: Para manipulação de dados.
- **SQL Server**: Banco de dados utilizado para armazenar informações de usuários e tarefas.

## Requisitos
- **Python 3.8+**
- **Dependências**:
  - streamlit
  - pandas
  - pyodbc
  - python-dotenv
  - argon2-cffi

## Configuração do Ambiente
1. Clone este repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```

2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure as variáveis ambiente:
- Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
    ```bash
    DB_SERVER=<seu_servidor>
    DB_NAME=<nome_do_banco>
    DB_USER=<usuario>
    DB_PASSWORD=<senha>
    ```

## Como Executar
1. Certifique-se de que o banco de dados SQL Server está configurado e acessível.
2. Execute o aplicativo:
    ```bash
    streamlit run main.py
    ```
3. Acesse o aplicativo no navegador em http://localhost:8501.

## Estrutura do Projeto
- main.py: Arquivo principal contendo toda a lógica do aplicativo.
- teste.py: Arquivo auxiliar (não detalhado no código fornecido).