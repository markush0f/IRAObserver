# ARCHITECTURE.md

## IRAObserver – Backend Architecture

Este documento define **las reglas de arquitectura** del backend de IRAObserver. El objetivo es garantizar **consistencia, mantenibilidad y evolución segura** del sistema.

---

## 1. Architectural Style

IRAObserver sigue un enfoque de:

* **Monolito modular**
* **DDD pragmático (Domain-Driven Design)**
* **Clean Architecture simplificada**
* **Server-centric**

No se usan microservicios ni CQRS en v1.

---

## 2. High-Level Overview

```text
HTTP API
   ↓
Application Layer
   ↓
Domain Layer (core logic)
   ↓
Infrastructure Layer
   ↓
PostgreSQL / Filesystem / External Services
```

La **lógica del negocio vive en el dominio**. El resto del sistema orbita alrededor de él.

---

## 3. Bounded Contexts

Cada *bounded context* representa un **lenguaje y responsabilidad de negocio distinta**.

### Core Domain

* **observation**

  * Snapshots
  * Timeline
  * Change detection
  * Evolución histórica del proyecto

### Supporting Domains

* **identity**

  * Usuarios
  * Invitaciones
  * Sesiones
  * Permisos

* **projects**

  * Proyectos
  * Fuentes (GitHub, local)
  * Configuración

* **insights**

  * Observaciones automáticas
  * Heurísticas
  * IA futura

### Generic / Supporting

* **integrations**

  * Adaptadores a servicios externos
  * GitHub
  * Filesystem
  * IA providers

⚠️ Los bounded contexts **NO se definen por entidades**, sino por significado de negocio.

---

## 4. Directory Structure

```text
app/
├─ domain/          # Business logic (DDD)
├─ application/     # Coordination and orchestration
├─ infrastructure/  # DB, external services, adapters
├─ api/             # HTTP layer (FastAPI)
└─ main.py
```

Cada bounded context aparece reflejado **en domain, application y api**.

---

## 5. Dependency Rules (STRICT)

Estas reglas **NO se pueden romper**.

### Forbidden dependencies

```text
domain ❌ must NOT import application
domain ❌ must NOT import infrastructure
domain ❌ must NOT import api

application ❌ must NOT import api
application ❌ must NOT import infrastructure

api ❌ must NOT contain business logic
```

### Allowed dependencies

```text
api → application
application → domain
infrastructure → domain (via interfaces/contracts)
```

---

## 6. Domain Rules

* El dominio contiene:

  * Entidades
  * Value Objects
  * Reglas
  * Servicios de dominio
* El dominio:

  * ❌ No conoce HTTP
  * ❌ No conoce SQLAlchemy
  * ❌ No conoce GitHub ni IA
* Las entidades:

  * Tienen comportamiento
  * No son anémicas
* Los Value Objects:

  * Son inmutables
  * Se comparan por valor
  * Encapsulan reglas

---

## 7. Application Layer Rules

La capa `application`:

* Coordina dominios
* Maneja flujos
* Orquesta transacciones
* NO contiene reglas de negocio complejas

Regla clave:

> La application **no decide**, solo **orquesta**.

---

## 8. Infrastructure Rules

La infraestructura contiene:

* Persistencia (PostgreSQL)
* ORM
* Hashing
* Integraciones externas
* Schedulers

Regla clave:

> Todo lo que toca el mundo real vive aquí.

---

## 9. Communication Between Contexts

* ❌ No se comparten entidades entre contextos
* ❌ No se importan modelos de otro dominio
* ✅ Solo se usan:

  * IDs
  * DTOs simples
  * Interfaces

Ejemplo correcto:

* `projects` usa `user_id`
* `projects` NO usa `identity.User`

---

## 10. Sync vs Async (Conceptual)

* Sync:

  * Login
  * Accept invite
  * Project creation
* Async:

  * Project analysis
  * Snapshot generation
  * Insights computation

La asincronía se introduce **cuando el dominio lo exige**, no antes.

---

## 11. Scaffolding Rules

El scaffolding:

* Genera **bounded contexts**
* No genera lógica
* No genera modelos de DB
* Refuerza la arquitectura
* Es idempotente

Unidad mínima: **bounded context**, no entidad.

---

## 12. Guiding Principle

> Si mañana eliminamos FastAPI o PostgreSQL,
> el dominio debe seguir teniendo sentido.

Si algo rompe este principio, **está mal ubicado**.

---

## 13. What This Architecture Avoids

* Microservices prematuros
* CRUD anémico
* God services
* Lógica en controllers
* Acoplamiento a proveedores externos
* Over-engineering

---

## 14. Final Note

Esta arquitectura está pensada para:

* Evolucionar sin reescrituras
* Soportar múltiples integraciones
* Incorporar IA más adelante
* Ser entendible por otros desarrolladores
* Ser defendible en entrevistas técnicas

---

### Estado: **Architecture Closed ✅**
