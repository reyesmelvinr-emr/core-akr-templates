from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import os
import warnings

import pytest

from harness.cache_guard import CacheIntegrityError, CacheStalenessWarning, cache_path_for_key, read_cache_with_integrity


def test_read_cache_with_integrity_warns_on_stale_content(tmp_path: Path) -> None:
    cache_key = "owner/repo@main/backend-service.instructions.md"
    cache_path = cache_path_for_key(cache_key, tmp_path)
    cache_path.write_text("CONSTANTS_VERSION = '1.0.0'", encoding="utf-8")

    stale_time = datetime.now(timezone.utc) - timedelta(days=10)
    os.utime(cache_path, (stale_time.timestamp(), stale_time.timestamp()))

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        content = read_cache_with_integrity(cache_key, tmp_path)

    assert content == "CONSTANTS_VERSION = '1.0.0'"
    assert any(issubclass(item.category, CacheStalenessWarning) for item in caught)


def test_read_cache_with_integrity_blocks_corrupt_content(tmp_path: Path) -> None:
    cache_key = "owner/repo@main/backend-service.instructions.md"
    cache_path = cache_path_for_key(cache_key, tmp_path)
    cache_path.write_text("missing marker", encoding="utf-8")

    with pytest.raises(CacheIntegrityError):
        read_cache_with_integrity(cache_key, tmp_path)
