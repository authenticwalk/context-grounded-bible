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
# Use language code only, or add version if it can be extracted
LANGUAGE_PATTERNS = {
    'Afrikaans': 'afr-PWL',
    'Albanian': 'alb-ZF',
    'Arabic': 'ara-SVD',
    'Bavarian': 'bar',  # Single translation
    'Bulgarian': 'bul-BG',
    'Croatian': 'hrv',  # Single translation
    'Czech': 'ces-BKR',
    'Danish': 'dan',  # Single translation (removed redundancy)
    'Dutch': 'nld-SV',
    'Esperanto': 'epo',  # Single translation
    'Finnish': 'fin-FB',
    'Hungarian': 'hun-KAR',
    'Indonesian': 'ind-TL',
    'Korean': 'kor',  # Single translation (removed redundancy)
    'Lithuanian': 'lit',  # Single translation (removed redundancy)
    'Maori': 'mri',  # Single translation
    'Norwegian': 'nor',  # Single translation (removed redundancy)
    'Romanian': 'ron-COR',
    'Swedish': 'swe',  # Single translation (removed redundancy)
    'Tagalog': 'tgl-ADB',
    'Thai': 'tha-KJV',
    'Turkish': 'tur',  # Single translation (removed redundancy)
    'Vietnamese': 'vie',  # Single translation (removed redundancy)
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

# BibleHub-specific naming variations (alternate names for same versions)
BIBLEHUB_VARIATIONS = {
    # Portuguese
    'Bíblia King James Atualizada': 'por-KJA',
    
    # Spanish
    'Spanish: La Biblia de las Américas': 'spa-LBLA',
    'Spanish: La Nueva Biblia de los Hispanos': 'spa-NBLH',
    'Spanish: Reina Valera Gómez': 'spa-RVG',
    'Spanish: Reina Valera 1909': 'spa-RV-1909',
    'Spanish: Sagradas Escrituras': 'spa-SE-1569',
    
    # French (alternate names)
    'French Louis Segond': 'fra-LSG',
    'French Martin': 'fra-MAR',
    
    # German (alternate names)
    'German Textbibel': 'deu-TEXT',
    
    # Italian (alternate names)
    'Italian Giovanni Diodati Bible (1649)': 'ita-DIO',
    'Italian Riveduta Bible (1927)': 'ita-RIV',
    
    # Latin (alternate names)
    'Latin Vulgate': 'lat-VUL',
    
    # Russian (alternate names)
    'Russian Synodal Translation': 'rus-SYN',
    
    # Greek Manuscripts (New Testament)
    'Byzantine Majority Text': 'grc-BYZ',
    'Greek Orthodox Church': 'grc-ORTHO',
    'Scrivener Textus Receptus 1894': 'grc-TR-1894',
    'Stephanus Textus Receptus 1550': 'grc-TR-1550',
    'Tischendorf 8th Edition': 'grc-TISCH',
    'Westcott and Hort 1881': 'grc-WH',
    'Nestlé GNT 1904': 'grc-NESTLE-1904',
    'RP Byzantine Majority Text 2005': 'grc-RP-2005',
    'Greek NT: Tischendorf 8th Ed.': 'grc-TISCH',
    'Westcott and Hort / [NA27 variants]': 'grc-WH',
    
    # Other languages
    'Armenian Western: NT': 'hye-WEST-NT',
    'Basque: (Navarro-Labourdin) NT': 'eus-NT',
    'Kabyle NT': 'kab-NT',
    'Latvian New Testament': 'lav-NT',
    'Shuar New Testament': 'jiv-NT',
    'Swahili NT': 'swa-NT',
    'Tawallammat Tamajaq NT': 'ttq-NT',
    'Ukrainian NT': 'ukr-NT',
    'Uma New Testament': 'ppk-NT',
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




