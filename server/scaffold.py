#!/usr/bin/env python3

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"


def abort(message: str) -> None:
    print(f"Error: {message}")
    sys.exit(1)


def ensure_app_dir() -> None:
    if not APP_DIR.exists():
        abort("app/ directory not found. Run this script from the backend root.")


def create_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=False)


def create_file(path: Path, content: str = "") -> None:
    path.write_text(content)


def scaffold_context(context_name: str) -> None:
    if not context_name.isidentifier():
        abort("Context name must be a valid Python identifier")

    context = context_name.lower()

    domain = APP_DIR / "domain" / context
    application = APP_DIR / "application" / context
    api = APP_DIR / "api" / "v1" / context

    if domain.exists() or application.exists() or api.exists():
        abort(f"Bounded context '{context}' already exists")

    # Domain
    create_dir(domain)
    create_dir(domain / "entities")
    create_dir(domain / "value_objects")
    create_dir(domain / "services")
    create_dir(domain / "exceptions")

    create_file(domain / "__init__.py")
    create_file(domain / "entities" / "__init__.py")
    create_file(domain / "value_objects" / "__init__.py")
    create_file(domain / "services" / "__init__.py")
    create_file(domain / "exceptions" / "__init__.py")

    create_file(domain / "repository.py", "# Domain repository interfaces\n")

    # Application
    create_dir(application)
    create_file(application / "__init__.py")
    create_file(application / "interfaces.py", "# Application ports and interfaces\n")
    create_file(
        application / "service.py",
        f"# Application service for '{context}' bounded context\n",
    )

    # API
    create_dir(api)
    create_file(api / "__init__.py")
    create_file(
        api / "routes.py", f'"""\nHTTP routes for {context} bounded context.\n"""\n'
    )
    create_file(api / "schemas.py", "# HTTP request/response schemas\n")

    print(f"Bounded context '{context}' scaffolded successfully")


def main() -> None:
    ensure_app_dir()

    if len(sys.argv) != 2:
        abort("Usage: scaffold.py <bounded_context_name>")

    scaffold_context(sys.argv[1])


if __name__ == "__main__":
    main()
