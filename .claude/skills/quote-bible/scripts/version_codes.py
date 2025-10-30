"""
BibleHub version name to standardized code mappings.

Standardized format (incremental): {lang} or {lang}-{version} or {lang}-{version}-{year}
- lang: ISO-639-3 language code (3 letters, lowercase) - REQUIRED
- version: Version abbreviation (UPPERCASE: NIV, KJV, ESV) - add when needed
- year: Publication year (4 digits) - add only when disambiguating versions

Examples:
    "New International Version" -> "eng-NIV"
    "Reina Valera 1909" -> "spa-RV-1909"
    "Afrikaans PWL" -> "afr-PWL"
"""

# English Bible versions
ENGLISH_VERSIONS = {
    'New International Version': 'eng-NIV',
    'New Living Translation': 'eng-NLT',
    'English Standard Version': 'eng-ESV',
    'Berean Study Bible': 'eng-BSB',
    'New American Standard Bible': 'eng-NASB',
    'King James Bible': 'eng-KJV',
    'Holman Christian Standard Bible': 'eng-HCSB',
    'International Standard Version': 'eng-ISV',
    'NET Bible': 'eng-NET',
    "GOD'S WORD® Translation": 'eng-GWT',
    'Jubilee Bible 2000': 'eng-JUB',
    'King James 2000 Bible': 'eng-KJ2000',
    'American King James Version': 'eng-AKJV',
    'American Standard Version': 'eng-ASV',
    'Douay-Rheims Bible': 'eng-DRB',
    'Darby Bible Translation': 'eng-DBT',
    'English Revised Version': 'eng-ERV',
    "Webster's Bible Translation": 'eng-WBT',
    'World English Bible': 'eng-WEB',
    "Young's Literal Translation": 'eng-YLT',
    'Aramaic Bible in Plain English': 'eng-ABPE',
    'Weymouth New Testament': 'eng-WNT',
    "God's Word® Translation": 'eng-GW',  # Alternate naming
}

# Language indicators for non-English versions (when no specific version detected)
# These patterns match the START of version names and assign appropriate language codes
# Ordered from most specific to least specific to avoid false matches
LANGUAGE_PATTERNS = {
    # Explicit language prefixes (BibleHub format: "Language: Version Name")
    'Spanish:': 'spa',
    'French:': 'fra',
    'German:': 'deu',
    'Italian:': 'ita',
    'Portuguese:': 'por',
    'Russian:': 'rus',
    'Chinese:': 'zho',
    'Greek:': 'grc',
    'Hebrew:': 'heb',
    'Latin:': 'lat',
    'Arabic:': 'ara',
    'Armenian:': 'hye',
    
    # Language names without colons
    'Afrikaans': 'afr',
    'Albanian': 'sqi',
    'Aramaic': 'arc',
    'Bavarian': 'bar',
    'Bulgarian': 'bul',
    'Croatian': 'hrv',
    'Czech': 'ces',
    'Danish': 'dan',
    'Dutch': 'nld',
    'Esperanto': 'epo',
    'Finnish': 'fin',
    'Hungarian': 'hun',
    'Indonesian': 'ind',
    'Korean': 'kor',
    'Lithuanian': 'lit',
    'Maori': 'mri',
    'Norwegian': 'nor',
    'Romanian': 'ron',
    'Swedish': 'swe',
    'Tagalog': 'tgl',
    'Thai': 'tha',
    'Turkish': 'tur',
    'Vietnamese': 'vie',
}

# Chinese versions
CHINESE_VERSIONS = {
    'CUVMP Traditional': 'zho-CUV-TRAD',
    'Chinese Bible: Union (Traditional)': 'zho-CUV-TRAD',
    'CUVMP Simplified': 'zho-CUV-SIMP',
    'Chinese Bible: Union (Simplified)': 'zho-CUV-SIMP',
    'CSB Simplified': 'zho-CUV-SIMP',  # Alternate naming
    'CSB Traditional': 'zho-CUV-TRAD',  # Alternate naming
}

# French versions
FRENCH_VERSIONS = {
    'French: Darby': 'fra-DAR',
    'French: Louis Segond': 'fra-LSG',
    'French: Martin': 'fra-MAR',
}

# German versions
GERMAN_VERSIONS = {
    'German: Modernized': 'deu-MOD',
    'German: Luther (1912)': 'deu-LU-1912',
    'German: Textbibel': 'deu-TEXT',
}

# Greek versions
GREEK_VERSIONS = {
    "Swete's Septuagint": 'grc-LXX',
    'Septuagint': 'grc-LXX',
}

# Hebrew versions
HEBREW_VERSIONS = {
    'Westminster Leningrad Codex': 'heb-WLC',
    'WLC (Consonants Only)': 'heb-WLC-CONS',
    'Aleppo Codex': 'heb-ALEP',
}

# Italian versions
ITALIAN_VERSIONS = {
    'Italian: Riveduta': 'ita-RIV',
    'Italian: Giovanni Diodati': 'ita-DIO',
}

# Latin versions
LATIN_VERSIONS = {
    'Latin: Vulgata': 'lat-VUL',
    'Vulgata': 'lat-VUL',
}

# Portuguese versions
PORTUGUESE_VERSIONS = {
    'King James Atualizada': 'por-KJA',
    'Portugese Bible': 'por-JFA',
    'Portuguese': 'por-JFA',
}

# Russian versions
RUSSIAN_VERSIONS = {
    'Russian: Synodal': 'rus-SYN',
    'Russian koi8r': 'rus-KOI8',
}

# Spanish versions
SPANISH_VERSIONS = {
    'La Biblia de las Américas': 'spa-LBLA',
    'La Nueva Biblia de los Hispanos': 'spa-NBLH',
    'Reina Valera Gómez': 'spa-RVG',
    'Reina Valera 1909': 'spa-RV-1909',
    'Sagradas Escrituras 1569': 'spa-SE-1569',
}

# BibleHub-specific naming variations (exact names from BibleHub HTML)
BIBLEHUB_VARIATIONS = {
    # English variations (exact BibleHub names)
    "GOD'S WORD® Translation": 'eng-GW',
    "GOD'S WORD&reg; Translation": 'eng-GW',  # HTML entity version
    'Aramaic Bible in Plain English': 'eng-ABPE',
    'Weymouth New Testament': 'eng-WNT',
    
    # Portuguese (exact BibleHub names)
    'Bíblia King James Atualizada Português': 'por-KJA',
    
    # Spanish variations (exact BibleHub names with years)
    'Spanish: La Biblia de las Américas': 'spa-LBLA',
    'Spanish: La Nueva Biblia de los Hispanos': 'spa-NBLH',
    'Spanish: Reina Valera Gómez': 'spa-RVG',
    'Spanish: Reina Valera (1909)': 'spa-RV-1909',
    'Spanish: Reina Valera 1909': 'spa-RV-1909',  # Without parentheses
    'Spanish: Sagradas Escrituras (1569)': 'spa-SE-1569',
    'Spanish: Sagradas Escrituras 1569': 'spa-SE-1569',  # Without parentheses
    
    # French variations (exact BibleHub names with years)
    'French: Louis Segond (1910)': 'fra-LSG-1910',
    'French: Martin (1744)': 'fra-MAR-1744',
    
    # German variations (exact BibleHub names with years)
    'German: Textbibel (1899)': 'deu-TEXT-1899',
    
    # Italian variations (exact BibleHub names with years)
    'Italian: Giovanni Diodati Bible (1649)': 'ita-DIO-1649',
    'Italian: Riveduta Bible (1927)': 'ita-RIV-1927',
    
    # Latin variations (exact BibleHub names)
    'Latin: Vulgata Clementina': 'lat-VUL-CLEM',
    
    # Russian variations (exact BibleHub names with years)
    'Russian: Synodal Translation (1876)': 'rus-SYN-1876',
    
    # Chinese variations (exact BibleHub names with Chinese characters)
    '現代標點和合本 (CUVMP Traditional)': 'zho-CUV-TRAD',
    '现代标点和合本 (CUVMP Simplified)': 'zho-CUV-SIMP',
    '中文標準譯本 (CSB Traditional)': 'zho-CSB-TRAD',
    '中文标准译本 (CSB Simplified)': 'zho-CSB-SIMP',
    
    # Greek Manuscripts (New Testament) - all variants
    # Standard texts
    'Byzantine Majority Text': 'grc-BYZ',
    'Byzantine/Majority Text (2000)': 'grc-BYZ-2000',
    'Byzantine/Majority Text (2000) w/o Diacritics': 'grc-BYZ-2000',
    'Byzantine/Majority Text (2000) - Transliterated': 'grc-BYZ-2000-TRANS',
    'Greek Orthodox Church': 'grc-ORTHO',
    'Greek Orthodox Church 1904': 'grc-ORTHO-1904',
    'Scrivener Textus Receptus 1894': 'grc-TR-1894',
    "Scrivener's Textus Receptus 1894": 'grc-TR-1894',
    "Scrivener's Textus Receptus 1894 w/o Diacritics": 'grc-TR-1894',
    "Scrivener's Textus Receptus (1894) - Transliterated": 'grc-TR-1894-TRANS',
    'Stephanus Textus Receptus 1550': 'grc-TR-1550',
    'Stephens Textus Receptus (1550) - Transliterated': 'grc-TR-1550-TRANS',
    'Tischendorf 8th Edition': 'grc-TISCH',
    'Tischendorf 8th Ed. w/o Diacritics': 'grc-TISCH',
    'Greek NT: Tischendorf 8th Ed. - Transliterated': 'grc-TISCH-TRANS',
    'Westcott and Hort 1881': 'grc-WH-1881',
    'Westcott and Hort 1881 w/o Diacritics': 'grc-WH-1881',
    'Westcott and Hort 1881 - Transliterated': 'grc-WH-1881-TRANS',
    'Westcott and Hort / [NA27 variants]': 'grc-WH-NA27',
    'Westcott/Hort - Transliterated': 'grc-WH-TRANS',
    'Westcott/Hort, UBS4 variants': 'grc-WH-UBS4',
    'Westcott/Hort, UBS4 variants w/o Diacritics': 'grc-WH-UBS4',
    'Westcott/Hort, UBS4 variants - Transliterated': 'grc-WH-UBS4-TRANS',
    'Nestlé GNT 1904': 'grc-NESTLE-1904',
    'Nestle Greek New Testament 1904': 'grc-NESTLE-1904',
    'Nestle Greek New Testament 1904 - Transliterated': 'grc-NESTLE-1904-TRANS',
    'RP Byzantine Majority Text 2005': 'grc-RP-2005',
    
    # Other languages - exact BibleHub names (including variations)
    'Armenian Western: NT': 'hye-WEST-NT',
    'Armenian (Western): NT': 'hye-WEST-NT',  # Alternate format
    'Basque: (Navarro-Labourdin) NT': 'eus-NT',
    'Kabyle NT': 'kab-NT',
    'Kabyle: NT': 'kab-NT',  # Alternate format
    'Latvian New Testament': 'lav-NT',
    'Shuar New Testament': 'jiv-NT',
    'Swahili NT': 'swa-NT',
    'Tawallammat Tamajaq NT': 'ttq-NT',
    'Tawallamat Tamajaq NT': 'ttq-NT',  # Spelling variant
    'Ukrainian NT': 'ukr-NT',
    'Ukrainian: NT': 'ukr-NT',  # With colon
    'Uma New Testament': 'ppk-NT',
}

# Special patterns that need custom handling (e.g., verse refs embedded in version name)
# These will be checked with startswith() in the mapping function
VERSION_NAME_PREFIXES = {
    'Euangelioa': 'eus-NT',  # Basque Gospel (may have verse ref embedded)
    'Sv. Jānis': 'lav-NT',   # Latvian (may have verse ref embedded)
}

# Combine all version mappings
ALL_VERSION_MAPPINGS = {
    **ENGLISH_VERSIONS,
    **CHINESE_VERSIONS,
    **FRENCH_VERSIONS,
    **GERMAN_VERSIONS,
    **GREEK_VERSIONS,
    **HEBREW_VERSIONS,
    **ITALIAN_VERSIONS,
    **LATIN_VERSIONS,
    **PORTUGUESE_VERSIONS,
    **RUSSIAN_VERSIONS,
    **SPANISH_VERSIONS,
    **BIBLEHUB_VARIATIONS,
}




