from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import warnings


EXPECTED_CONTENT_MARKERS = {
    "lean_baseline_service_template_module.md": 'akr:section id="quick_reference"',
    "backend-service.instructions.md": "CONSTANTS_VERSION",
    "ui-component.instructions.md": "CONSTANTS_VERSION",
    "database.instructions.md": "CONSTANTS_VERSION",
}

TTL_DAYS = {
    "templates": 7,
    "charters": 3,
}


class CacheIntegrityError(RuntimeError):
    pass


class CacheStalenessWarning(Warning):
    pass


def encode_cache_key(raw_key: str) -> str:
    return raw_key.replace("\\", "__").replace("/", "__").replace("@", "_at_")


def cache_path_for_key(cache_key: str, cache_dir: Path) -> Path:
    return cache_dir / f"{encode_cache_key(cache_key)}.md"


def get_cache_bucket(cache_key: str) -> str:
    lowered = cache_key.lower()
    if "charter" in lowered or "instructions" in lowered:
        return "charters"
    return "templates"


def get_cache_age_days(cache_path: Path, now: datetime | None = None) -> int:
    current_time = now or datetime.now(timezone.utc)
    modified = datetime.fromtimestamp(cache_path.stat().st_mtime, tz=timezone.utc)
    return max(0, (current_time - modified).days)


def read_encoded_cache(cache_key: str, cache_dir: Path) -> str:
    cache_path = cache_path_for_key(cache_key, cache_dir)
    return cache_path.read_text(encoding="utf-8")


def read_cache_with_integrity(
    cache_key: str,
    cache_dir: Path,
    *,
    expected_markers: dict[str, str] | None = None,
    ttl_days: dict[str, int] | None = None,
    now: datetime | None = None,
) -> str:
    marker_map = expected_markers or EXPECTED_CONTENT_MARKERS
    ttl_map = ttl_days or TTL_DAYS

    cache_path = cache_path_for_key(cache_key, cache_dir)
    content = cache_path.read_text(encoding="utf-8")
    age_days = get_cache_age_days(cache_path, now=now)

    marker_key = cache_key.rsplit("/", 1)[-1]
    marker = marker_map.get(marker_key)
    if marker and marker not in content:
        raise CacheIntegrityError(
            f"Corrupt cache for {cache_key} - content marker missing. Run /akr-docs update-cache before proceeding."
        )

    bucket = get_cache_bucket(cache_key)
    ttl = ttl_map[bucket]
    if age_days > ttl:
        warnings.warn(
            (
                f"Cache for {cache_key} is {age_days}d old (TTL: {ttl}d). "
                "Run /akr-docs update-cache at session end."
            ),
            CacheStalenessWarning,
            stacklevel=2,
        )

    return content