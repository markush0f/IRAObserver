#!/usr/bin/env python3

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"
DOMAINS_DIR = APP_DIR / "domains"
API_HTTP_V1_DIR = APP_DIR / "api" / "http" / "v1"


def abort(message: str) -> None:
    print(f"Error: {message}")
    sys.exit(1)


def ensure_base_structure() -> None:
    if not APP_DIR.exists():
        abort("app/ directory not found. Run this script from the project root.")

    if not DOMAINS_DIR.exists():
        abort("domains/ directory not found inside app/.")

    if not API_HTTP_V1_DIR.exists():
        abort("api/http/v1/ directory not found inside app/.")


def create_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_file(path: Path, content: str = "") -> None:
    if path.exists():
        return
    path.write_text(content)


def scaffold_domain(domain_name: str) -> None:
    if not domain_name.isidentifier():
        abort("Domain name must be a valid Python identifier.")

    domain = domain_name.lower()

    domain_dir = DOMAINS_DIR / domain
    api_file = API_HTTP_V1_DIR / f"{domain}.py"

    if domain_dir.exists():
        abort(f"Domain '{domain}' already exists.")

    # Domain structure
    create_dir(domain_dir)

    create_file(domain_dir / "models.py")
    create_file(domain_dir / "repository.py")
    create_file(domain_dir / "service.py")

    create_file(
        domain_dir / "README.md",
        f"# {domain.capitalize()} Domain\n\n"
        "## Purpose\n\n"
        "Describe the responsibility of this domain.\n\n"
        "## Responsibilities\n\n"
        "- \n\n"
        "## Notes\n\n"
        "- \n",
    )

    # API exposure
    create_file(
        api_file,
        f'"""\nHTTP API for {domain} domain.\n"""\n',
    )

    print(f"Domain '{domain}' generated successfully.")


def main() -> None:
    ensure_base_structure()

    if len(sys.argv) != 2:
        abort("Usage: scaffold.py <domain_name>")

    scaffold_domain(sys.argv[1])


if __name__ == "__main__":
    main()
