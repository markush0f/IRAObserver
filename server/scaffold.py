#!/usr/bin/env python3

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
APP_DIR = BASE_DIR / "app"

DOMAIN_DIR = APP_DIR / "domain"
APPLICATION_DIR = APP_DIR / "application"

# TODO change the api version to dynamic api version.
API_DIR = APP_DIR / "api" / "v1"


def abort(message: str) -> None:
    print(f"Error: {message}")
    sys.exit(1)


def create_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=False)


def create_file(path: Path, content: str = "") -> None:
    path.write_text(content)


def scaffold_context(context_name: str) -> None:
    if not context_name.isidentifier():
        abort("Context name must be a valid Python identifier")

    context_name = context_name.lower()

    domain_path = DOMAIN_DIR / context_name
    application_path = APPLICATION_DIR / context_name
    api_path = API_DIR / context_name

    if domain_path.exists() or application_path.exists() or api_path.exists():
        abort(f"Context '{context_name}' already exists")

    # Domain
    create_dir(domain_path)
    create_dir(domain_path / "entities")
    create_dir(domain_path / "value_objects")
    create_dir(domain_path / "services")
    create_dir(domain_path / "exceptions")

    create_file(domain_path / "__init__.py")
    create_file(domain_path / "entities" / "__init__.py")
    create_file(domain_path / "value_objects" / "__init__.py")
    create_file(domain_path / "services" / "__init__.py")
    create_file(domain_path / "exceptions" / "__init__.py")

    # Application
    create_dir(application_path)
    create_file(application_path / "__init__.py")

    # API
    create_dir(api_path)
    create_file(api_path / "__init__.py")
    create_file(
        api_path / "routes.py",
        f'''"""
HTTP routes for {context_name} bounded context.
"""
''',
    )

    print(f"Bounded context '{context_name}' scaffolded successfully")


def main() -> None:
    if len(sys.argv) != 2:
        abort("Usage: scaffold.py <context_name>")

    context_name = sys.argv[1]
    scaffold_context(context_name)


if __name__ == "__main__":
    main()
