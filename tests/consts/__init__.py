"""
Constants for Bible quote accuracy testing.

Contains verse lists, Bible versions, and model configurations.
"""

from .verses import VERSES, get_verses_by_difficulty, get_verse_references, get_verses_by_category
from .languages import (
    BIBLE_VERSIONS,
    MODELS_TO_TEST,
    get_versions_by_rarity,
    get_version_codes,
    get_versions_by_language_family,
    get_versions_by_script,
    get_models_by_provider,
    get_models_by_tier,
)

__all__ = [
    'VERSES',
    'BIBLE_VERSIONS',
    'MODELS_TO_TEST',
    'get_verses_by_difficulty',
    'get_verse_references',
    'get_verses_by_category',
    'get_versions_by_rarity',
    'get_version_codes',
    'get_versions_by_language_family',
    'get_versions_by_script',
    'get_models_by_provider',
    'get_models_by_tier',
]
