#!/usr/bin/env python3
"""Validate Home Assistant blueprint YAML files."""

from __future__ import annotations

import argparse
import glob
from importlib.metadata import version as package_version
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from homeassistant.exceptions import HomeAssistantError
from homeassistant.util.yaml import YamlTypeError, extract_inputs
from homeassistant.util.yaml.loader import load_yaml_dict

DEFAULT_PATTERNS = (
    "pws_weather_upload.yaml",
    "blueprints/**/*.yaml",
    "blueprints/**/*.yml",
)
GLOB_CHARS = set("*?[")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def _has_glob(pattern: str) -> bool:
    return any(char in pattern for char in GLOB_CHARS)


def expand_patterns(patterns: list[str]) -> list[Path]:
    """Expand a mix of explicit file paths and glob patterns."""
    matched: dict[Path, None] = {}

    for pattern in patterns or list(DEFAULT_PATTERNS):
        if _has_glob(pattern):
            for match in sorted(glob.glob(pattern, recursive=True)):
                path = Path(match)
                if path.is_file():
                    matched[path] = None
            continue

        path = Path(pattern)
        if path.is_file():
            matched[path] = None

    return list(matched)


def _require_mapping(value: object, label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a mapping")
    return value


def _require_string(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    return value


def _optional_string(value: object, label: str) -> None:
    if value is not None and not isinstance(value, str):
        raise ValueError(f"{label} must be a string")


def _parse_version(version: str) -> tuple[int, int, int]:
    if not VERSION_RE.match(version):
        raise ValueError(
            "blueprint.homeassistant.min_version must be formatted as "
            "{major}.{minor}.{patch}"
        )
    return tuple(int(part) for part in version.split("."))


def _validate_url(value: str, label: str) -> None:
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"{label} must be a valid URL")


def _validate_input_definition(value: object, label: str) -> None:
    if value is None:
        return

    mapping = _require_mapping(value, label)
    for key in ("name", "description"):
        _optional_string(mapping.get(key), f"{label}.{key}")

    selector = mapping.get("selector")
    if selector is not None and not isinstance(selector, dict):
        raise ValueError(f"{label}.selector must be a mapping")


def _validate_input_section(value: object, label: str) -> dict[str, object]:
    mapping = _require_mapping(value, label)
    for key in ("name", "icon", "description"):
        _optional_string(mapping.get(key), f"{label}.{key}")

    collapsed = mapping.get("collapsed")
    if collapsed is not None and not isinstance(collapsed, bool):
        raise ValueError(f"{label}.collapsed must be a boolean")

    inputs = _require_mapping(mapping.get("input"), f"{label}.input")
    for key, input_value in inputs.items():
        _validate_input_definition(input_value, f"{label}.input.{key}")
    return inputs


def _flatten_blueprint_inputs(inputs: dict[str, object]) -> set[str]:
    flat_inputs: set[str] = set()

    for key, value in inputs.items():
        if isinstance(value, dict) and "input" in value:
            section_inputs = _validate_input_section(value, f"blueprint.input.{key}")
            duplicates = flat_inputs.intersection(section_inputs)
            if duplicates:
                dupes = ", ".join(sorted(duplicates))
                raise ValueError(f"Duplicate use of input key(s): {dupes}")
            flat_inputs.update(section_inputs)
            continue

        _validate_input_definition(value, f"blueprint.input.{key}")
        if key in flat_inputs:
            raise ValueError(f"Duplicate use of input key: {key}")
        flat_inputs.add(key)

    return flat_inputs


def validate_blueprint(path: Path) -> tuple[str, str]:
    """Load and validate a Home Assistant blueprint file."""
    data = _require_mapping(load_yaml_dict(path), "file")
    blueprint = _require_mapping(data.get("blueprint"), "blueprint")
    name = _require_string(blueprint.get("name"), "blueprint.name")
    domain = _require_string(blueprint.get("domain"), "blueprint.domain")
    _optional_string(blueprint.get("description"), "blueprint.description")
    _optional_string(blueprint.get("author"), "blueprint.author")

    source_url = blueprint.get("source_url")
    if source_url is not None:
        _validate_url(
            _require_string(source_url, "blueprint.source_url"),
            "blueprint.source_url",
        )

    ha_metadata = blueprint.get("homeassistant")
    if ha_metadata is not None:
        metadata = _require_mapping(ha_metadata, "blueprint.homeassistant")
        min_version_value = metadata.get("min_version")
        if min_version_value is not None:
            min_version = _parse_version(
                _require_string(min_version_value, "blueprint.homeassistant.min_version")
            )
            current_version = _parse_version(package_version("homeassistant"))
            if current_version < min_version:
                raise HomeAssistantError(
                    f"Requires at least Home Assistant {min_version_value}"
                )

    inputs = blueprint.get("input", {})
    input_mapping = _require_mapping(inputs, "blueprint.input")
    defined_inputs = _flatten_blueprint_inputs(input_mapping)
    referenced_inputs = set(extract_inputs(data))
    missing_inputs = referenced_inputs - defined_inputs
    if missing_inputs:
        missing = ", ".join(sorted(missing_inputs))
        raise ValueError(f"Missing input definition for {missing}")

    return name, domain


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Home Assistant blueprint YAML files."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Blueprint files or glob patterns to validate.",
    )
    args = parser.parse_args()

    files = expand_patterns(args.files)
    if not files:
        print("No blueprint files found to validate.")
        return 0

    failures = 0
    for path in files:
        try:
            name, domain = validate_blueprint(path)
        except (HomeAssistantError, YamlTypeError, FileNotFoundError, ValueError) as err:
            failures += 1
            print(f"FAIL {path}: {err}", file=sys.stderr)
            continue

        print(f"OK   {path}: {name} ({domain})")

    if failures:
        print(f"{failures} blueprint file(s) failed validation.", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} blueprint file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
