#!/usr/bin/env python3

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"
INFRA_DIR = APP_DIR / "infrastructure" / "persistence" / "postgres"


def abort(message: str) -> None:
    print(f"Error: {message}")
    sys.exit(1)


def ensure_app_dir() -> None:
    if not APP_DIR.exists():
        abort("app/ directory not found. Run this script from the backend root.")


def create_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=False)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_file(path: Path, content: str = "") -> None:
    path.write_text(content)


def scaffold_domain(domain_name: str) -> None:
    if not domain_name.isidentifier():
        abort("Domain name must be a valid Python identifier")

    domain = domain_name.lower()
    domain_root = APP_DIR / "domains" / domain

    if domain_root.exists():
        abort(f"Domain '{domain}' already exists")

    # Domain root
    create_dir(domain_root)
    create_file(domain_root / "__init__.py")

    # Services
    services_dir = domain_root / "services"
    create_dir(services_dir)
    create_file(services_dir / "__init__.py")

    # Models
    models_dir = domain_root / "models"
    create_dir(models_dir)
    create_file(models_dir / "__init__.py")

    # Entities
    entities_dir = models_dir / "entities"
    create_dir(entities_dir)
    create_file(entities_dir / "__init__.py")

    # DTOs
    dto_dir = models_dir / "dto"
    create_dir(dto_dir)
    create_file(dto_dir / "__init__.py")

    # Exceptions
    exceptions_dir = domain_root / "exceptions"
    create_dir(exceptions_dir)
    create_file(exceptions_dir / "__init__.py")

    # Repository interface (domain)
    create_file(
        domain_root / "repository.py",
        "# Repository interface for domain persistence\n",
    )

    # Infrastructure repository (Postgres)
    ensure_dir(INFRA_DIR)
    create_file(
        INFRA_DIR / f"{domain}_repository.py",
        f"# Postgres implementation for {domain} repository\n",
    )

    print(f"Domain '{domain}' scaffolded successfully")


def main() -> None:
    ensure_app_dir()

    if len(sys.argv) != 2:
        abort("Usage: scaffold.py <domain_name>")

    scaffold_domain(sys.argv[1])


if __name__ == "__main__":
    main()
