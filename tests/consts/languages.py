"""
30 Bible versions across different languages for testing AI model accuracy.
Includes common English versions, gateway languages, and increasingly rare Bible languages.
"""

# Format: (code, name, language, script, language_family, rarity_score)
# Rarity: 1 (most common) to 10 (very rare)

BIBLE_VERSIONS = [
    # Common English Versions (1-7) - Rarity 1-2
    ("NIV", "New International Version", "English", "Latin", "Germanic", 1),
    ("NLT", "New Living Translation", "English", "Latin", "Germanic", 1),
    ("KJV", "King James Version", "English", "Latin", "Germanic", 1),
    ("NASB", "New American Standard Bible", "English", "Latin", "Germanic", 1),
    ("WEB", "World English Bible", "English", "Latin", "Germanic", 1),
    ("ESV", "English Standard Version", "English", "Latin", "Germanic", 2),
    ("CSB", "Christian Standard Bible", "English", "Latin", "Germanic", 2),

    # Less Common English Versions (8-10) - Rarity 3
    ("NRSV", "New Revised Standard Version", "English", "Latin", "Germanic", 3),
    ("ASV", "American Standard Version", "English", "Latin", "Germanic", 3),
    ("YLT", "Young's Literal Translation", "English", "Latin", "Germanic", 3),

    # Ancient/Source Languages (11-13) - Rarity 2-3
    ("TR", "Textus Receptus (Greek NT)", "Greek", "Greek", "Hellenic", 2),
    ("BHS", "Biblia Hebraica Stuttgartensia", "Hebrew", "Hebrew", "Semitic", 2),
    ("VUL", "Latin Vulgate", "Latin", "Latin", "Italic", 3),

    # Major Gateway Languages (14-21) - Rarity 2-4
    ("GER", "Luther Bibel", "German", "Latin", "Germanic", 2),
    ("FRE", "Louis Segond", "French", "Latin", "Italic", 2),
    ("CHI", "Chinese Union Version (和合本)", "Chinese", "Han", "Sino-Tibetan", 3),
    ("IND", "Terjemahan Baru (TB)", "Indonesian", "Latin", "Austronesian", 3),
    ("ARA", "Arabic Van Dyck", "Arabic", "Arabic", "Semitic", 3),
    ("SWA", "Swahili Bible", "Swahili", "Latin", "Niger-Congo", 4),
    ("SPA", "Reina-Valera 1960", "Spanish", "Latin", "Italic", 2),
    ("POR", "Almeida Revista e Atualizada", "Portuguese", "Latin", "Italic", 3),

    # Regional Gateway Languages (22-26) - Rarity 5-6
    ("RUS", "Russian Synodal", "Russian", "Cyrillic", "Slavic", 4),
    ("HIN", "Hindi Bible", "Hindi", "Devanagari", "Indo-Aryan", 5),
    ("THA", "Thai Bible", "Thai", "Thai", "Kra-Dai", 6),
    ("VIE", "Vietnamese Bible", "Vietnamese", "Latin", "Austroasiatic", 5),
    ("KOR", "Korean Revised Version", "Korean", "Hangul", "Koreanic", 5),

    # Increasingly Rare Languages (27-30) - Rarity 7-10
    ("AMH", "Amharic Bible", "Amharic", "Ge'ez", "Semitic", 7),
    ("NEP", "Nepali Bible", "Nepali", "Devanagari", "Indo-Aryan", 8),
    ("QUE", "Quechua Bible", "Quechua", "Latin", "Quechuan", 9),
    ("NAV", "Navajo Bible", "Navajo", "Latin", "Na-Dene", 10),
]

# Model configurations for testing
# Format: (model_id, provider, model_name, tier)
# NOTE: Requesty.ai requires provider prefix in model_id (e.g., "google/gemini-2.0-flash-exp")
MODELS_TO_TEST = [
    # Google
    ("google/gemini-2.0-flash-exp", "google", "Gemini 2.0 Flash", "low"),
    ("google/gemini-exp-1206", "google", "Gemini Experimental", "high"),

    # OpenAI
    ("openai/gpt-4o-mini", "openai", "GPT-4o Mini", "low"),
    ("openai/gpt-4o", "openai", "GPT-4o", "high"),

    # Anthropic Claude
    ("anthropic/claude-3-5-haiku-20241022", "anthropic", "Claude 3.5 Haiku", "low"),
    ("anthropic/claude-3-5-sonnet-20241022", "anthropic", "Claude 3.5 Sonnet", "high"),

    # Qwen
    ("qwen/qwen-2.5-7b-instruct", "qwen", "Qwen 2.5 7B", "low"),
    ("qwen/qwen-max", "qwen", "Qwen Max", "high"),

    # DeepSeek
    ("deepseek/deepseek-chat", "deepseek", "DeepSeek Chat", "low"),
    ("deepseek/deepseek-reasoner", "deepseek", "DeepSeek Reasoner", "high"),

    # Meta Llama
    ("meta-llama/llama-3.1-8b-instruct", "meta", "Llama 3.1 8B", "low"),
    ("meta-llama/llama-3.1-70b-instruct", "meta", "Llama 3.1 70B", "high"),
]

def get_versions_by_rarity(min_rarity=1, max_rarity=10):
    """Get Bible versions filtered by rarity range."""
    return [v for v in BIBLE_VERSIONS if min_rarity <= v[5] <= max_rarity]

def get_version_codes():
    """Get just the version codes as a list."""
    return [v[0] for v in BIBLE_VERSIONS]

def get_versions_by_language_family(family):
    """Get Bible versions filtered by language family."""
    return [v for v in BIBLE_VERSIONS if v[4] == family]

def get_versions_by_script(script):
    """Get Bible versions filtered by script type."""
    return [v for v in BIBLE_VERSIONS if v[3] == script]

def get_models_by_provider(provider):
    """Get models filtered by provider."""
    return [m for m in MODELS_TO_TEST if m[1] == provider]

def get_models_by_tier(tier):
    """Get models filtered by tier (low/high)."""
    return [m for m in MODELS_TO_TEST if m[3] == tier]
