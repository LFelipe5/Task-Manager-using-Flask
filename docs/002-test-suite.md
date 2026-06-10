# [002] - Suíte de Testes Automatizados com Cobertura >= 90%

## Contexto
O projeto Flask Task Manager não possuía nenhum teste nem framework de teste. Era necessária uma suíte automatizada com quality gate obrigatório de cobertura de statements >= 90% sobre o pacote da aplicação, medida com pytest-cov.

## Escopo

### Incluído
- Instalação de pytest e pytest-cov no venv compartilhado.
- Config de teste injetável via variáveis de ambiente sem alterar comportamento de produção.
- Testes unitários (models, forms) e de integração (rotas de auth, CRUD de tarefas, account, error handlers).
- Quality gate `--cov-fail-under=90`.

### Excluído
- Refatoração para application factory completo (apenas config injetável via env).
- Alteração de lógica de negócio de rotas/models/forms.
- Testes E2E com browser.

## Solução Implementada

### Arquitetura
- `todo_project/todo_project/__init__.py` passou a ler `SECRET_KEY`, `DATABASE_URI` e `TESTING` de variáveis de ambiente, com defaults idênticos aos de produção (`os.environ.get(..., default)`). Quando `TESTING=1`, ativa `TESTING` e desabilita CSRF do Flask-WTF. Sem env vars, o comportamento de produção é byte-a-byte o mesmo.
- `conftest.py` define as env vars de teste ANTES de importar o pacote (config é aplicada no import-time), usa um arquivo SQLite temporário e recria o schema por teste (fixture de escopo `function`) para isolamento total.
- Fixtures reutilizáveis: `app`, `client`, `make_user`, `auth_client`.
- Error handlers 403/500 testados via rotas auxiliares registradas no app; o teste de 500 desativa temporariamente `TESTING`/`PROPAGATE_EXCEPTIONS` para o handler ser invocado em vez de re-raise.

### Arquivos Modificados
| Arquivo | Tipo de Mudança |
|---------|-----------------|
| `todo_project/todo_project/__init__.py` | Modificado (config via env) |
| `pytest.ini` | Criado |
| `.coveragerc` | Criado |
| `requirements-dev.txt` | Criado |
| `todo_project/tests/__init__.py` | Criado |
| `todo_project/tests/conftest.py` | Criado |
| `todo_project/tests/test_models.py` | Criado |
| `todo_project/tests/test_forms.py` | Criado |
| `todo_project/tests/test_auth_routes.py` | Criado |
| `todo_project/tests/test_task_routes.py` | Criado |
| `todo_project/tests/test_account_routes.py` | Criado |

## Testes
| Métrica | Valor |
|---------|-------|
| Cobertura do pacote da aplicação | 100% |
| Total de testes | 47 |
| Testes unitários (models + forms) | 16 |
| Testes de integração (rotas) | 31 |
| Quality gate | `--cov-fail-under=90` (atingido) |

Cobertura por módulo: `__init__.py` 100%, `forms.py` 100%, `models.py` 100%, `routes.py` 100%.

### Como rodar
```bash
venv/bin/pip install -r requirements-dev.txt
venv/bin/pytest
```

## Verificação de Qualidade
| Critério | Status |
|----------|--------|
| Todos os testes passam (47) | ✅ |
| Cobertura >= 90% (100%) | ✅ |
| Produção intacta (run.py sem env) | ✅ |
| Determinismo / isolamento | ✅ |
| Sem credenciais em código | ✅ |

---
**Verificado por:** Workflow Orchestrator
**Data:** 2026-06-10
**Status Final:** ✅ APROVADO
