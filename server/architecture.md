# Domain-Oriented Modular Architecture

## Example of Architecture

```text
app/
├─ core/
│  ├─ settings.py
│  ├─ startup.py
│  ├─ logging.py
│  ├─ security.py
│  └─ lifecycle.py
│
├─ domains/
│  ├─ identity/
│  │  ├─ models.py
│  │  ├─ repository.py
│  │  ├─ service.py
│  │  └─ README.md
│  │
│  ├─ projects/
│  │  ├─ models.py
│  │  ├─ repository.py
│  │  ├─ service.py
│  │  └─ README.md
│
├─ api/
│  ├─ http/
│  │  └─ v1/
│  │     ├─ identity.py
│  │     ├─ projects.py
│  │     └─ router.py
│  │
│  ├─ ws/
│  │  ├─ system.py
│  │  ├─ projects.py
│  │  └─ router.py
│  │
│  └─ deps.py
│
├─ ai/
│  ├─ orchestration/
│  │  ├─ planner.py
│  │  └─ context_builder.py
│  │
│  ├─ analyzers/
│  │  ├─ architecture.py
│  │  ├─ evolution.py
│  │  └─ risk.py
│  │
│  ├─ providers/
│  │  ├─ openai/
│  │  │  └─ client.py
│  │  ├─ local_llm/
│  │  │  └─ client.py
│  │  └─ registry.py
│  │
│  └─ README.md
│
├─ infrastructure/
│  ├─ persistence/
│  │  └─ postgres/
│  │     ├─ identity_repository.py
│  │     └─ projects_repository.py
│  │
│  ├─ external_services/
│  │  ├─ github/
│  │  │  └─ client.py
│  │  ├─ gitlab/
│  │  │  └─ client.py
│  │  └─ slack/
│  │     └─ notifier.py
│  │
│  └─ messaging/
│     ├─ pubsub.py
│     └─ events.py
│
├─ shared/
│  ├─ exceptions.py
│  ├─ types.py
│  ├─ utils.py
│  └─ constants.py
│
├─ migrations/
│  └─ versions/
│
├─ main.py
└─ __init__.py
```
