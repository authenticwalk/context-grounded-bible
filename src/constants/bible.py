"""
Bible verse reference constants and utilities.

Provides comprehensive Bible structure data aligned with STANDARDIZATION.md:
- USFM 3.0 book codes (3-letter uppercase)
- Verse reference format: {BOOK}.{chapter:03d}.{verse:03d}
- Complete chapter and verse counts for all 66 books (Protestant canon)
"""

from typing import Dict, List, Optional, Tuple

# Bible structure: book_code -> list of verse counts per chapter
# Index 0 = Chapter 1, Index 1 = Chapter 2, etc.
BIBLE_STRUCTURE = {
    # OLD TESTAMENT
    # Pentateuch (Torah)
    "GEN": [31, 25, 24, 26, 32, 22, 24, 22, 29, 32, 32, 20, 18, 24, 21, 16, 27, 33, 38, 18, 34, 24, 20, 67, 34, 35, 46, 22, 35, 43, 55, 32, 20, 31, 29, 43, 36, 30, 23, 23, 57, 38, 34, 34, 28, 34, 31, 22, 33, 26],
    "EXO": [22, 25, 22, 31, 23, 30, 25, 32, 35, 29, 10, 51, 22, 31, 27, 36, 16, 27, 25, 26, 36, 31, 33, 18, 40, 37, 21, 43, 46, 38, 18, 35, 23, 35, 35, 38, 29, 31, 43, 38],
    "LEV": [17, 16, 17, 35, 19, 30, 38, 36, 24, 20, 47, 8, 59, 57, 33, 34, 16, 30, 37, 27, 24, 33, 44, 23, 55, 46, 34],
    "NUM": [54, 34, 51, 49, 31, 27, 89, 26, 23, 36, 35, 16, 33, 45, 41, 50, 13, 32, 22, 29, 35, 41, 30, 25, 18, 65, 23, 31, 40, 16, 54, 42, 56, 29, 34, 13],
    "DEU": [46, 37, 29, 49, 33, 25, 26, 20, 29, 22, 32, 32, 18, 29, 23, 22, 20, 22, 21, 20, 23, 30, 25, 22, 19, 19, 26, 68, 29, 20, 30, 52, 29, 12],
    
    # Historical Books
    "JOS": [18, 24, 17, 24, 15, 27, 26, 35, 27, 43, 23, 24, 33, 15, 63, 10, 18, 28, 51, 9, 45, 34, 16, 33],
    "JDG": [36, 23, 31, 24, 31, 40, 25, 35, 57, 18, 40, 15, 25, 20, 20, 31, 13, 31, 30, 48, 25],
    "RUT": [22, 23, 18, 22],
    "1SA": [28, 36, 21, 22, 12, 21, 17, 22, 27, 27, 15, 25, 23, 52, 35, 23, 58, 30, 24, 42, 15, 23, 29, 22, 44, 25, 12, 25, 11, 31, 13],
    "2SA": [27, 32, 39, 12, 25, 23, 29, 18, 13, 19, 27, 31, 39, 33, 37, 23, 29, 33, 43, 26, 22, 51, 39, 25],
    "1KI": [53, 46, 28, 34, 18, 38, 51, 66, 28, 29, 43, 33, 34, 31, 34, 34, 24, 46, 21, 43, 29, 53],
    "2KI": [18, 25, 27, 44, 27, 33, 20, 29, 37, 36, 21, 21, 25, 29, 38, 20, 41, 37, 37, 21, 26, 20, 37, 20, 30],
    "1CH": [54, 55, 24, 43, 26, 81, 40, 40, 44, 14, 47, 40, 14, 17, 29, 43, 27, 17, 19, 8, 30, 19, 32, 31, 31, 32, 34, 21, 30],
    "2CH": [17, 18, 17, 22, 14, 42, 22, 18, 31, 19, 23, 16, 22, 15, 19, 14, 19, 34, 11, 37, 20, 12, 21, 27, 28, 23, 9, 27, 36, 27, 21, 33, 25, 33, 27, 23],
    "EZR": [11, 70, 13, 24, 17, 22, 28, 36, 15, 44],
    "NEH": [11, 20, 32, 23, 19, 19, 73, 18, 38, 39, 36, 47, 31],
    "EST": [22, 23, 15, 17, 14, 14, 10, 17, 32, 3],
    
    # Wisdom Literature
    "JOB": [22, 13, 26, 21, 27, 30, 21, 22, 35, 22, 20, 25, 28, 22, 35, 22, 16, 21, 29, 29, 34, 30, 17, 25, 6, 14, 23, 28, 25, 31, 40, 22, 33, 37, 16, 33, 24, 41, 30, 24, 34, 17],
    "PSA": [6, 12, 8, 8, 12, 10, 17, 9, 20, 18, 7, 8, 6, 7, 5, 11, 15, 50, 14, 9, 13, 31, 6, 10, 22, 12, 14, 9, 11, 12, 24, 11, 22, 22, 28, 12, 40, 22, 13, 17, 13, 11, 5, 26, 17, 11, 9, 14, 20, 23, 19, 9, 6, 7, 23, 13, 11, 11, 17, 12, 8, 12, 11, 10, 13, 20, 7, 35, 36, 5, 24, 20, 28, 23, 10, 12, 20, 72, 13, 19, 16, 8, 18, 12, 13, 17, 7, 18, 52, 17, 16, 15, 5, 23, 11, 13, 12, 9, 9, 5, 8, 28, 22, 35, 45, 48, 43, 13, 31, 7, 10, 10, 9, 8, 18, 19, 2, 29, 176, 7, 8, 9, 4, 8, 5, 6, 5, 6, 8, 8, 3, 18, 3, 3, 21, 26, 9, 8, 24, 13, 10, 7, 12, 15, 21, 10, 20, 14, 9, 6],
    "PRO": [33, 22, 35, 27, 23, 35, 27, 36, 18, 32, 31, 28, 25, 35, 33, 33, 28, 24, 29, 30, 31, 29, 35, 34, 28, 28, 27, 28, 27, 33, 31],
    "ECC": [18, 26, 22, 16, 20, 12, 29, 17, 18, 20, 10, 14],
    "SNG": [17, 17, 11, 16, 16, 13, 13, 14],
    
    # Major Prophets
    "ISA": [31, 22, 26, 6, 30, 13, 25, 22, 21, 34, 16, 6, 22, 32, 9, 14, 14, 7, 25, 6, 17, 25, 18, 23, 12, 21, 13, 29, 24, 33, 9, 20, 24, 17, 10, 22, 38, 22, 8, 31, 29, 25, 28, 28, 25, 13, 15, 22, 26, 11, 23, 15, 12, 17, 13, 12, 21, 14, 21, 22, 11, 12, 19, 12, 25, 24],
    "JER": [19, 37, 25, 31, 31, 30, 34, 22, 26, 25, 23, 17, 27, 22, 21, 21, 27, 23, 15, 18, 14, 30, 40, 10, 38, 24, 22, 17, 32, 24, 40, 44, 26, 22, 19, 32, 21, 28, 18, 16, 18, 22, 13, 30, 5, 28, 7, 47, 39, 46, 64, 34],
    "LAM": [22, 22, 66, 22, 22],
    "EZK": [28, 10, 27, 17, 17, 14, 27, 18, 11, 22, 25, 28, 23, 23, 8, 63, 24, 32, 14, 49, 32, 31, 49, 27, 17, 21, 36, 26, 21, 26, 18, 32, 33, 31, 15, 38, 28, 23, 29, 49, 26, 20, 27, 31, 25, 24, 23, 35],
    "DAN": [21, 49, 30, 37, 31, 28, 28, 27, 27, 21, 45, 13],
    
    # Minor Prophets
    "HOS": [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9],
    "JOL": [20, 32, 21],
    "AMO": [15, 16, 15, 13, 27, 14, 17, 14, 15],
    "OBA": [21],
    "JON": [17, 10, 10, 11],
    "MIC": [16, 13, 12, 13, 15, 16, 20],
    "NAM": [15, 13, 19],
    "HAB": [17, 20, 19],
    "ZEP": [18, 15, 20],
    "HAG": [15, 23],
    "ZEC": [21, 13, 10, 14, 11, 15, 14, 23, 17, 12, 17, 14, 9, 21],
    "MAL": [14, 17, 18, 6],
    
    # NEW TESTAMENT
    # Gospels
    "MAT": [25, 23, 17, 25, 48, 34, 29, 34, 38, 42, 30, 50, 58, 36, 39, 28, 27, 35, 30, 34, 46, 46, 39, 51, 46, 75, 66, 20],
    "MRK": [45, 28, 35, 41, 43, 56, 37, 38, 50, 52, 33, 44, 37, 72, 47, 20],
    "LUK": [80, 52, 38, 44, 39, 49, 50, 56, 62, 42, 54, 59, 35, 35, 32, 31, 37, 43, 48, 47, 38, 71, 56, 53],
    "JHN": [51, 25, 36, 54, 47, 71, 53, 59, 41, 42, 57, 50, 38, 31, 27, 33, 26, 40, 42, 31, 25],
    
    # Acts
    "ACT": [26, 47, 26, 37, 42, 15, 60, 40, 43, 48, 30, 25, 52, 28, 41, 40, 34, 28, 41, 38, 40, 30, 35, 27, 27, 32, 44, 31],
    
    # Pauline Epistles
    "ROM": [32, 29, 31, 25, 21, 23, 25, 39, 33, 21, 36, 21, 14, 23, 33, 27],
    "1CO": [31, 16, 23, 21, 13, 20, 40, 13, 27, 33, 34, 31, 13, 40, 58, 24],
    "2CO": [24, 17, 18, 18, 21, 18, 16, 24, 15, 18, 33, 21, 14],
    "GAL": [24, 21, 29, 31, 26, 18],
    "EPH": [23, 22, 21, 32, 33, 24],
    "PHP": [30, 30, 21, 23],
    "COL": [29, 23, 25, 18],
    "1TH": [10, 20, 13, 18, 28],
    "2TH": [12, 17, 18],
    "1TI": [20, 15, 16, 16, 25, 21],
    "2TI": [18, 26, 17, 22],
    "TIT": [16, 15, 15],
    "PHM": [25],
    
    # General Epistles
    "HEB": [14, 18, 19, 16, 14, 20, 28, 13, 28, 39, 40, 29, 25],
    "JAS": [27, 26, 18, 17, 20],
    "1PE": [25, 25, 22, 19, 14],
    "2PE": [21, 22, 18],
    "1JN": [10, 29, 24, 21, 21],
    "2JN": [13],
    "3JN": [14],
    "JUD": [25],
    
    # Apocalypse
    "REV": [20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20, 8, 21, 18, 24, 21, 15, 27, 21],
}


# Book names (full English names for reference)
BOOK_NAMES = {
    # Old Testament
    "GEN": "Genesis",
    "EXO": "Exodus",
    "LEV": "Leviticus",
    "NUM": "Numbers",
    "DEU": "Deuteronomy",
    "JOS": "Joshua",
    "JDG": "Judges",
    "RUT": "Ruth",
    "1SA": "1 Samuel",
    "2SA": "2 Samuel",
    "1KI": "1 Kings",
    "2KI": "2 Kings",
    "1CH": "1 Chronicles",
    "2CH": "2 Chronicles",
    "EZR": "Ezra",
    "NEH": "Nehemiah",
    "EST": "Esther",
    "JOB": "Job",
    "PSA": "Psalms",
    "PRO": "Proverbs",
    "ECC": "Ecclesiastes",
    "SNG": "Song of Solomon",
    "ISA": "Isaiah",
    "JER": "Jeremiah",
    "LAM": "Lamentations",
    "EZK": "Ezekiel",
    "DAN": "Daniel",
    "HOS": "Hosea",
    "JOL": "Joel",
    "AMO": "Amos",
    "OBA": "Obadiah",
    "JON": "Jonah",
    "MIC": "Micah",
    "NAM": "Nahum",
    "HAB": "Habakkuk",
    "ZEP": "Zephaniah",
    "HAG": "Haggai",
    "ZEC": "Zechariah",
    "MAL": "Malachi",
    # New Testament
    "MAT": "Matthew",
    "MRK": "Mark",
    "LUK": "Luke",
    "JHN": "John",
    "ACT": "Acts",
    "ROM": "Romans",
    "1CO": "1 Corinthians",
    "2CO": "2 Corinthians",
    "GAL": "Galatians",
    "EPH": "Ephesians",
    "PHP": "Philippians",
    "COL": "Colossians",
    "1TH": "1 Thessalonians",
    "2TH": "2 Thessalonians",
    "1TI": "1 Timothy",
    "2TI": "2 Timothy",
    "TIT": "Titus",
    "PHM": "Philemon",
    "HEB": "Hebrews",
    "JAS": "James",
    "1PE": "1 Peter",
    "2PE": "2 Peter",
    "1JN": "1 John",
    "2JN": "2 John",
    "3JN": "3 John",
    "JUD": "Jude",
    "REV": "Revelation",
}


def format_verse_ref(book: str, chapter: int, verse: int) -> str:
    """
    Format a verse reference according to STANDARDIZATION.md.
    
    Format: {BOOK}.{chapter:03d}.{verse:03d}
    Example: JHN.003.016
    
    Args:
        book: USFM 3.0 book code (3-letter uppercase)
        chapter: Chapter number (1-indexed)
        verse: Verse number (1-indexed)
        
    Returns:
        Formatted verse reference string
    """
    return f"{book}.{chapter:03d}.{verse:03d}"


def parse_verse_ref(ref: str) -> Tuple[str, int, int]:
    """
    Parse a verse reference string into components.
    
    Args:
        ref: Verse reference (e.g., "JHN.003.016")
        
    Returns:
        Tuple of (book_code, chapter, verse)
        
    Raises:
        ValueError: If reference format is invalid
    """
    parts = ref.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid verse reference format: {ref}")
    
    book, chapter_str, verse_str = parts
    
    if book not in BIBLE_STRUCTURE:
        raise ValueError(f"Invalid book code: {book}")
    
    try:
        chapter = int(chapter_str)
        verse = int(verse_str)
    except ValueError:
        raise ValueError(f"Invalid chapter or verse number in: {ref}")
    
    return book, chapter, verse


def validate_verse_ref(book: str, chapter: int, verse: int) -> bool:
    """
    Validate that a verse reference exists in the Bible.
    
    Args:
        book: USFM 3.0 book code
        chapter: Chapter number (1-indexed)
        verse: Verse number (1-indexed)
        
    Returns:
        True if valid, False otherwise
    """
    if book not in BIBLE_STRUCTURE:
        return False
    
    chapters = BIBLE_STRUCTURE[book]
    
    if chapter < 1 or chapter > len(chapters):
        return False
    
    verse_count = chapters[chapter - 1]
    return 1 <= verse <= verse_count


def get_all_verses(book: str = None) -> List[str]:
    """
    Generate all verse references in standardized format.
    
    Args:
        book: Optional book code to limit results to one book
        
    Returns:
        List of all verse references (e.g., ["GEN.001.001", "GEN.001.002", ...])
    """
    verses = []
    
    books = [book] if book else BIBLE_STRUCTURE.keys()
    
    for book_code in books:
        chapters = BIBLE_STRUCTURE[book_code]
        for chapter_num, verse_count in enumerate(chapters, start=1):
            for verse_num in range(1, verse_count + 1):
                verses.append(format_verse_ref(book_code, chapter_num, verse_num))
    
    return verses


def get_book_stats() -> Dict[str, int]:
    """
    Get statistics about the Bible structure.
    
    Returns:
        Dictionary with counts of books, chapters, and verses
    """
    total_chapters = 0
    total_verses = 0
    
    for chapters in BIBLE_STRUCTURE.values():
        total_chapters += len(chapters)
        total_verses += sum(chapters)
    
    return {
        "books": len(BIBLE_STRUCTURE),
        "chapters": total_chapters,
        "verses": total_verses,
    }


# Translation version keys following STANDARDIZATION.md format
# Format: {lang}-{version} or {lang}-{version}-{year}
# See source-abbreviations.yaml for complete list

# Sample translations for MAT.005.003 (Matthew 5:3) demonstrating the data structure
# Full translation database would be loaded from external file
SAMPLE_TRANSLATIONS = {
    "MAT.005.003": {
        # Primary English translations
        "eng-NIV": "Blessed are the poor in spirit, for theirs is the kingdom of heaven.",
        "eng-ESV": "Blessed are the poor in spirit, for theirs is the kingdom of heaven.",
        "eng-KJV": "Blessed are the poor in spirit: for theirs is the kingdom of heaven.",
        "eng-NASB": "Blessed are the poor in spirit, for theirs is the kingdom of heaven.",
        "eng-NLT": "God blesses those who are poor and realize their need for him, for the Kingdom of Heaven is theirs.",
        
        # Ancient languages
        "grc-NA28": "Μακάριοι οἱ πτωχοὶ τῷ πνεύματι· ὅτι αὐτῶν ἐστιν ἡ βασιλεία τῶν οὐρανῶν.",
        "heb": "אַשְׁרֵי עֲנִיֵּי רוּחַ כִּי לָהֶם מַלְכוּת הַשָּׁמָיִם׃",
        
        # Major modern languages
        "spa-RV1960": "Bienaventurados los pobres en espíritu, porque de ellos es el reino de los cielos.",
        "fra-LSG": "Heureux les pauvres en esprit, car le royaume des cieux est à eux!",
        "deu-LU1912": "Selig sind, die da geistlich arm sind; denn das Himmelreich ist ihr.",
        "por-ARC": "Bem-aventurados os pobres de espírito, porque deles é o reino dos céus;",
        "rus-RUSV": "Блаженны нищие духом, ибо их есть Царство Небесное.",
        "zho-CUV": "虛心的人有福了！因為天國是他們的。",
        "ara-SVD": "طُوبَى لِلْمَسَاكِينِ بِالرُّوحِ، لأَنَّ لَهُمْ مَلَكُوتَ السَّمَاوَاتِ.",
        
        # Additional languages (sample from eBible corpus)
        "mal": "ആത്മാവിൽ ദരിദ്രരായവർ ഭാഗ്യവാന്മാർ; സ്വർഗ്ഗരാജ്യം അവർക്കുള്ളത്.",
        "hin": "धन्य हैं वे, जो मन के दीन हैं, क्योंकि स्वर्ग का राज्य उन्हीं का है।",
        "tam": "ஆவியில் எளிமையுள்ளவர்கள் பாக்கியவான்கள்; பரலோகராஜ்யம் அவர்களுடையது.",
        "tel": "ఆత్మలో దీనత్వం గలవారు ధన్యులు, పరలోకరాజ్యం వారిదే.",
        "swh": "Heri walio maskini wa roho, maana ufalme wa mbinguni ni wao.",
    }
}


def get_translation(verse_ref: str, translation_key: str) -> Optional[str]:
    """
    Get a specific translation for a verse.
    
    Args:
        verse_ref: Verse reference (e.g., "MAT.005.003")
        translation_key: Translation key (e.g., "eng-NIV", "grc-NA28")
        
    Returns:
        Translation text or None if not found
    """
    if verse_ref in SAMPLE_TRANSLATIONS:
        return SAMPLE_TRANSLATIONS[verse_ref].get(translation_key)
    return None


def get_available_translations(verse_ref: str) -> List[str]:
    """
    Get list of available translation keys for a verse.
    
    Args:
        verse_ref: Verse reference (e.g., "MAT.005.003")
        
    Returns:
        List of translation keys available for this verse
    """
    if verse_ref in SAMPLE_TRANSLATIONS:
        return list(SAMPLE_TRANSLATIONS[verse_ref].keys())
    return []


def parse_translation_key(translation_key: str) -> Dict[str, str]:
    """
    Parse a translation key into its components.
    
    Per STANDARDIZATION.md, format is: {lang}-{version}-{year} (incremental)
    
    Args:
        translation_key: Translation key (e.g., "eng-NIV-2011", "grc-NA28", "spa")
        
    Returns:
        Dictionary with 'lang', 'version' (optional), 'year' (optional)
    """
    parts = translation_key.split("-")
    result = {"lang": parts[0]}
    
    if len(parts) > 1:
        # Check if last part is a year (4 digits)
        if len(parts) > 2 and parts[-1].isdigit() and len(parts[-1]) == 4:
            result["year"] = parts[-1]
            result["version"] = "-".join(parts[1:-1])
        else:
            result["version"] = "-".join(parts[1:])
    
    return result


def format_translation_key(lang: str, version: str = None, year: str = None) -> str:
    """
    Format a translation key from components.
    
    Per STANDARDIZATION.md, uses incremental specificity.
    
    Args:
        lang: ISO-639-3 language code (3 letters, lowercase)
        version: Translation version (optional, e.g., "NIV", "ESV")
        year: Publication year (optional, 4 digits)
        
    Returns:
        Formatted translation key
    """
    parts = [lang]
    if version:
        parts.append(version)
    if year:
        parts.append(year)
    return "-".join(parts)


def merge_translations(ebible_data: Dict[str, str], biblehub_data: Dict[str, str], 
                       prefer_ebible: bool = True) -> Dict[str, str]:
    """
    Merge translation data from eBible and BibleHub sources.
    
    Handles:
    - Duplicate detection (same lang-version)
    - Unknown language codes (unk) from BibleHub
    - Preference for eBible standard when conflicts occur
    
    Args:
        ebible_data: Translations from eBible corpus
        biblehub_data: Translations from BibleHub
        prefer_ebible: If True, eBible takes precedence in conflicts
        
    Returns:
        Merged translation dictionary
    """
    result = {}
    
    # Add eBible data first if preferred
    if prefer_ebible:
        result.update(ebible_data)
    
    # Add BibleHub data, skipping unknowns and duplicates
    for key, value in biblehub_data.items():
        # Skip unknown language codes
        if key.startswith("unk-"):
            continue
        
        # Add if not duplicate or if BibleHub is preferred
        if key not in result or not prefer_ebible:
            result[key] = value
    
    # Add eBible data last if not preferred
    if not prefer_ebible:
        result.update(ebible_data)
    
    return result


# Example usage and testing
if __name__ == "__main__":
    # Print statistics
    stats = get_book_stats()
    print(f"Bible Statistics:")
    print(f"  Books: {stats['books']}")
    print(f"  Chapters: {stats['chapters']}")
    print(f"  Verses: {stats['verses']}")
    print()
    
    # Example verse references
    examples = [
        ("JHN", 1, 1),
        ("MAT", 5, 3),
        ("JOB", 38, 36),
        ("PSA", 119, 176),  # Longest chapter
        ("REV", 22, 21),    # Last verse
    ]
    
    print("Example verse references:")
    for book, chapter, verse in examples:
        ref = format_verse_ref(book, chapter, verse)
        valid = validate_verse_ref(book, chapter, verse)
        book_name = BOOK_NAMES.get(book, "Unknown")
        print(f"  {ref} - {book_name} {chapter}:{verse} (valid: {valid})")
    print()
    
    # Show first 10 verses
    print("First 10 verses in the Bible:")
    all_verses = get_all_verses()
    for verse_ref in all_verses[:10]:
        print(f"  {verse_ref}")
    print()
    
    # Parse example
    example_ref = "JHN.003.016"
    book, chapter, verse = parse_verse_ref(example_ref)
    print(f"Parsed '{example_ref}':")
    print(f"  Book: {book} ({BOOK_NAMES[book]})")
    print(f"  Chapter: {chapter}")
    print(f"  Verse: {verse}")
    print()
    
    # Translation examples
    mat_ref = "MAT.005.003"
    print(f"Available translations for {mat_ref}:")
    translations = get_available_translations(mat_ref)
    print(f"  {len(translations)} translations available")
    
    # Show sample translations
    sample_keys = ["eng-NIV", "eng-KJV", "grc-NA28", "spa-RV1960"]
    print(f"\nSample translations:")
    for key in sample_keys:
        text = get_translation(mat_ref, key)
        if text:
            print(f"  {key}: {text[:60]}...")
    
    # Translation key parsing
    print(f"\nTranslation key parsing examples:")
    test_keys = ["eng-NIV-2011", "grc-NA28", "spa", "eng-ESV"]
    for key in test_keys:
        parsed = parse_translation_key(key)
        print(f"  {key} -> {parsed}")

