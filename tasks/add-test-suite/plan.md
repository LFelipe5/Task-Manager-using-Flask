# Plano: Suíte de Testes Automatizados — Flask Task Manager

## 🎯 SCOPE

### Arquivos Afetados (criados)
- [x] `requirements-dev.txt` — deps de teste (pytest, pytest-cov)
- [x] `pytest.ini` — config do pytest + cobertura apontando para `todo_project`
- [x] `todo_project/tests/__init__.py`
- [x] `todo_project/tests/conftest.py` — fixtures (app de teste, client, db in-memory, usuário autenticado)
- [x] `todo_project/tests/test_models.py` — User, Task
- [x] `todo_project/tests/test_forms.py` — validações de formulários
- [x] `todo_project/tests/test_auth_routes.py` — register/login/logout, credenciais inválidas, proteção (302)
- [x] `todo_project/tests/test_task_routes.py` — CRUD de tarefas + autorização
- [x] `todo_project/tests/test_account_routes.py` — account, change_password, error handlers

### Arquivos Modificados (mínimo, sem quebrar produção)
- [x] `todo_project/todo_project/__init__.py` — tornar config sobrescrevível por env vars (TESTING, DB URI, SECRET_KEY) e CSRF; manter defaults de produção idênticos.

### Fora do Escopo
- Refatorar para application factory completo (mudança grande de arquitetura — risco a `run.py`). Apenas tornar config injetável via env.
- Alterar lógica de negócio das rotas/models/forms.
- Testes E2E com browser (Selenium) — não há requisito.

### Riscos de Impacto
- R1: `app` é objeto global criado no import; testar exige reset de DB entre testes. Mitigação: fixture que recria schema por teste em SQLite :memory: e limpa session.
- R2: Mexer em `__init__.py` pode quebrar `run.py`/produção. Mitigação: usar `os.environ.get(..., default_producao)` — sem env, comportamento idêntico ao atual.
- R3: CSRF do Flask-WTF bloqueia POSTs nos testes. Mitigação: `WTF_CSRF_ENABLED=False` na config de teste.
- R4: Sandbox bloqueia TCP local (memória do projeto). Mitigação: usar `app.test_client()` (WSGI in-process), nunca curl/requests a localhost.

## 📋 REQUIREMENTS

### Requisitos Funcionais
- [x] RF01: Instalar pytest + pytest-cov no venv `./venv`.
- [x] RF02: Config de teste com DB SQLite :memory: e CSRF desabilitado, sem afetar produção.
- [x] RF03: Cobrir models (User repr, Task repr, relacionamento author, load_user).
- [x] RF04: Cobrir forms (RegistrationForm validate_username duplicado, Length, EqualTo; UpdateUserInfoForm; Task/Update forms).
- [x] RF05: Cobrir auth routes (register sucesso/duplicado, login sucesso/falha, logout, redirect quando já autenticado).
- [x] RF06: Cobrir proteção de rotas (acesso sem login → 302 para login).
- [x] RF07: Cobrir CRUD de tarefas (add, list all_tasks, update com/sem mudança, delete, get_or_404 → 404).
- [x] RF08: Cobrir account/change_password (sucesso, senha errada, username duplicado) e error handlers 404/403/500.

### Requisitos Não-Funcionais
- [x] RNF01: **Cobertura de statements >= 90%** sobre o pacote `todo_project` (medido com pytest-cov). QUALITY GATE.
- [x] RNF02: Pirâmide de testes — foco unit (models/forms) + integration (rotas via test client).
- [x] RNF03: Testes determinísticos e isolados (sem estado compartilhado).

### Critérios de Aceitação
- [x] CA01: `venv/bin/pytest --cov` roda verde (todos passam).
- [x] CA02: Relatório cobre >= 90%.
- [x] CA03: `run.py` continua funcionando sem env vars (produção intacta).

### Edge Cases
- EC01: Login com usuário inexistente → flash danger, sem login.
- EC02: Login com senha errada → flash danger.
- EC03: update_task com mesmo conteúdo → flash "No Changes Made".
- EC04: update/delete de task_id inexistente → 404.
- EC05: change_password com senha antiga errada → flash danger.
- EC06: register/login quando já autenticado → redirect all_tasks.
- EC07: username fora de Length(3,10) → form inválido.

## 🏗️ DESIGN

### Padrões Utilizados
- Fixtures pytest com escopo `function` para isolamento total (recria schema por teste).
- Config injetável via env var preservando defaults de produção (Open/Closed: estende sem modificar comportamento atual).
- Helper de autenticação (registrar+login via test client) para testes de rota protegidos.

### Estratégia de testabilidade do app (sem quebrar produção)
Em `__init__.py`:
```
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '45cf93c4d41348cd9980674ade9a7356')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///site.db')
if os.environ.get('TESTING') == '1':
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
```
- conftest seta env vars ANTES de importar `todo_project` (import-time config) e usa `sqlite:///:memory:`.
- Como `db.create_all()` roda no import com :memory:, e :memory: é por-conexão, a fixture controla create/drop via app_context.

### Fluxo de Dados (teste de rota)
client POST/GET -> WSGI app in-process -> rota -> db :memory: -> assert status/flash/db state

### Componentes Reutilizáveis
- Fixtures `app`, `client`, `db_session`, `auth_user`, `logged_in_client` no conftest.

## 📝 TASKS

### Fase 1: Setup
- [x] T1.1: [LOW] Instalar pytest, pytest-cov no venv; criar `requirements-dev.txt`.
- [x] T1.2: [LOW] Criar `pytest.ini` com `--cov=todo_project --cov-report=term-missing --cov-fail-under=90`.
- [x] T1.3: [MEDIUM] Tornar config de `__init__.py` injetável via env (TESTING/DB/SECRET/CSRF) sem alterar defaults.

### Fase 2: Testes Unit
- [x] T2.1: [LOW] `test_models.py` — User/Task repr, relacionamento, load_user.
- [x] T2.2: [MEDIUM] `test_forms.py` — validações dos forms.

### Fase 3: Testes Integration (rotas)
- [x] T3.1: [MEDIUM] `test_auth_routes.py` — register/login/logout + proteção 302.
- [x] T3.2: [MEDIUM] `test_task_routes.py` — CRUD + 404 + autorização.
- [x] T3.3: [MEDIUM] `test_account_routes.py` — account, change_password, error handlers.

### Fase 4: Cobertura
- [x] T4.1: [LOW] Rodar `venv/bin/pytest --cov`, iterar até >= 90%, reportar número real.

## Análise Dual

### 🔴 Riscos (perspectiva pessimista) e mitigações incorporadas
- **DB :memory: por-conexão**: SQLite :memory: cria um banco novo por conexão. Flask-SQLAlchemy 3.x usa pool com `scoped_session`; o `db.create_all()` no import roda numa conexão e o test client pode pegar outra → "no such table". MITIGAÇÃO: na fixture, dentro de `app.app_context()`, chamar `db.create_all()` e usar `StaticPool`/`SQLALCHEMY_ENGINE_OPTIONS` se necessário, OU usar arquivo temporário por teste. Validar empiricamente; cair para arquivo tmp se :memory: instável.
- **Config aplicada só no import-time**: env vars precisam estar setadas ANTES de `import todo_project`. MITIGAÇÃO: conftest seta `os.environ` no topo do módulo, antes de qualquer import do app.
- **`db.create_all()` roda 1x no import**: schema do import inicial pode não bater com :memory: do client. Já coberto pela fixture que recria.
- **Linha `redirect(url_for('account'))` sem return em change_password (rota 144-157)**: bug latente (return ausente) — não corrigir (fora de escopo, é lógica), mas garantir que o teste de sucesso de troca de senha ainda cobre a linha 153.
- **`--cov-fail-under=90`** pode quebrar CI se algum branch defensivo (error handlers 500/403) for difícil de disparar. MITIGAÇÃO: testar error handlers via `app.test_request_context` ou abortando manualmente; 403/500 podem precisar de `app.test_client()` + rota que aborta. Se inalcançáveis, usar `# pragma: no cover` pontual SOMENTE em handlers triviais.

### 🟢 Oportunidades (perspectiva otimista)
- Código é pequeno (~4 arquivos, <200 linhas) → 90% é altamente factível, provável chegar a ~95%+.
- Templates já existem (login, register, all_tasks, etc.) → rotas renderizam sem mock.
- `bcrypt` real funciona em teste (rápido o suficiente para a suíte).
- Reuso: um único helper `register_and_login(client)` cobre a maioria das rotas protegidas de uma vez.
- error handlers 404 já disparam naturalmente via `get_or_404` em update/delete com id inexistente (cobre handler 404 + a linha do abort).

### Ajustes ao plano
- Adicionado fallback de DB para arquivo temporário caso :memory: + pool dê "no such table".
- Permitido `# pragma: no cover` cirúrgico apenas em handlers 403/500 se comprovadamente inalcançáveis pelo test client; preferir cobri-los de verdade.
- Spike confirmou: `__init__.py` atual ignora env (hardcoded) → T1.3 é pré-requisito real.
