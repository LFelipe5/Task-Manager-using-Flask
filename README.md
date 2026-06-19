# Task Manager (Flask) - Estudo de Caso DevSecOps

**Estudo de caso da trilha DevSecOps do Hackers do Bem.**

Uma aplicação web simples de gerenciamento de tarefas (To-Do List) com autenticação, construída em Flask, que serve como base para demonstrar práticas completas de **DevSecOps**: integração contínua, entrega contínua e **segurança automatizada** em todo o ciclo de vida (Shift-Left Security).

---

## 🎯 O que foi implementado (DevSecOps)

Este projeto não é apenas uma aplicação Flask — ele demonstra uma pipeline moderna de DevSecOps:

### ✅ Práticas DevSecOps Aplicadas

- **CI/CD completo** com GitHub Actions (branches `main`, `stage` e `dev`)
- **Linting** automático (flake8)
- **Testes automatizados** com cobertura de **100%**
- **SAST** (Static Application Security Testing) → **Bandit**
- **SCA** (Software Composition Analysis) → **pip-audit**
- **DAST** (Dynamic Application Security Testing) → **OWASP ZAP** (baseline scan)
- **Containerização** com Docker + docker-compose
- **Observabilidade** com **Prometheus** + **Grafana** (métricas da aplicação e infraestrutura)
- **Ambientes de Staging** simulados no pipeline
- **Segurança desde o desenvolvimento** (Shift-Left)

---

## 🚀 Funcionalidades da Aplicação

- Cadastro e login de usuários (senhas hasheadas com Bcrypt)
- Proteção de rotas (Flask-Login)
- CRUD completo de tarefas
- Configurações de conta (alterar usuário e senha)
- Páginas de erro customizadas (404, 403, 500)
- Design responsivo com Bootstrap

---

## 🛠️ Tecnologias

| Camada              | Tecnologias |
|---------------------|-------------|
| **Backend**         | Flask 3.0.3, Werkzeug |
| **Banco de Dados**  | SQLAlchemy + SQLite |
| **Autenticação**    | Flask-Login + Flask-Bcrypt |
| **Formulários**     | Flask-WTF |
| **Frontend**        | Jinja2 + Bootstrap 5 |
| **Testes**          | pytest + pytest-cov |
| **Segurança**       | Bandit, pip-audit, OWASP ZAP |
| **Container**       | Docker + docker-compose |
| **Observabilidade** | Prometheus + Grafana |
| **CI/CD**           | GitHub Actions |

---

## 📋 Pré-requisitos

- Docker e Docker Compose (recomendado)
- Ou Python 3.10+ (para execução local sem containers)

---

## 🐳 Como executar com Docker (Recomendado)

```bash
git clone https://github.com/LFelipe5/Task-Manager-DevSecOps-StudyCase.git
cd Task-Manager-DevSecOps-StudyCase

# Subir aplicação + Prometheus + Grafana
docker-compose up --build