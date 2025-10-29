"""USFM 3.0 Book Code Mappings

Maps USFM 3.0 3-letter uppercase book codes to book names and API.Bible book IDs.
Reference: https://ubsicap.github.io/usfm/identification/books.html
"""

# USFM 3.0 book codes to full book names
USFM_TO_NAME = {
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


def parse_reference(reference: str) -> tuple[str, int, int]:
    """
    Parse a USFM reference string into book, chapter, and verse.
    
    Args:
        reference: USFM reference (e.g., "MAT.5.3" or "MAT 5:3")
    
    Returns:
        Tuple of (book_code, chapter, verse)
    
    Raises:
        ValueError: If the reference format is invalid
    """
    # Normalize separators
    reference = reference.replace(":", ".").replace(" ", ".")
    
    parts = reference.split(".")
    if len(parts) != 3:
        raise ValueError(
            f"Invalid reference format: '{reference}'. "
            "Expected format: BOOK.CHAPTER.VERSE (e.g., MAT.5.3)"
        )
    
    book_code = parts[0].upper()
    if book_code not in USFM_TO_NAME:
        raise ValueError(
            f"Invalid book code: '{book_code}'. "
            f"Must be a valid USFM 3.0 code (e.g., GEN, MAT, REV)"
        )
    
    try:
        chapter = int(parts[1])
        verse = int(parts[2])
    except ValueError:
        raise ValueError(
            f"Chapter and verse must be numbers in reference: '{reference}'"
        )
    
    if chapter < 1 or verse < 1:
        raise ValueError(
            f"Chapter and verse must be positive numbers: '{reference}'"
        )
    
    return book_code, chapter, verse


def format_verse_id(book_code: str, chapter: int, verse: int) -> str:
    """
    Format a verse reference for API.Bible.
    
    Args:
        book_code: USFM book code (e.g., "MAT")
        chapter: Chapter number
        verse: Verse number
    
    Returns:
        Formatted verse ID (e.g., "MAT.5.3")
    """
    return f"{book_code}.{chapter}.{verse}"


def get_book_name(book_code: str) -> str:
    """
    Get the full book name from a USFM code.
    
    Args:
        book_code: USFM book code (e.g., "MAT")
    
    Returns:
        Full book name (e.g., "Matthew")
    
    Raises:
        ValueError: If the book code is invalid
    """
    book_code = book_code.upper()
    if book_code not in USFM_TO_NAME:
        raise ValueError(f"Invalid book code: '{book_code}'")
    return USFM_TO_NAME[book_code]


# USFM 3.0 book codes to BibleHub URL book names
# Based on BibleHub's actual directory structure at https://biblehub.com/multi/
USFM_TO_BIBLEHUB = {
    # Old Testament
    "GEN": "genesis",
    "EXO": "exodus",
    "LEV": "leviticus",
    "NUM": "numbers",
    "DEU": "deuteronomy",
    "JOS": "joshua",
    "JDG": "judges",
    "RUT": "ruth",
    "1SA": "1_samuel",
    "2SA": "2_samuel",
    "1KI": "1_kings",
    "2KI": "2_kings",
    "1CH": "1_chronicles",
    "2CH": "2_chronicles",
    "EZR": "ezra",
    "NEH": "nehemiah",
    "EST": "esther",
    "JOB": "job",
    "PSA": "psalms",
    "PRO": "proverbs",
    "ECC": "ecclesiastes",
    "SNG": "songs",
    "ISA": "isaiah",
    "JER": "jeremiah",
    "LAM": "lamentations",
    "EZK": "ezekiel",
    "DAN": "daniel",
    "HOS": "hosea",
    "JOL": "joel",
    "AMO": "amos",
    "OBA": "obadiah",
    "JON": "jonah",
    "MIC": "micah",
    "NAM": "nahum",
    "HAB": "habakkuk",
    "ZEP": "zephaniah",
    "HAG": "haggai",
    "ZEC": "zechariah",
    "MAL": "malachi",
    # New Testament
    "MAT": "matthew",
    "MRK": "mark",
    "LUK": "luke",
    "JHN": "john",
    "ACT": "acts",
    "ROM": "romans",
    "1CO": "1_corinthians",
    "2CO": "2_corinthians",
    "GAL": "galatians",
    "EPH": "ephesians",
    "PHP": "philippians",
    "COL": "colossians",
    "1TH": "1_thessalonians",
    "2TH": "2_thessalonians",
    "1TI": "1_timothy",
    "2TI": "2_timothy",
    "TIT": "titus",
    "PHM": "philemon",
    "HEB": "hebrews",
    "JAS": "james",
    "1PE": "1_peter",
    "2PE": "2_peter",
    "1JN": "1_john",
    "2JN": "2_john",
    "3JN": "3_john",
    "JUD": "jude",
    "REV": "revelation",
}


def get_biblehub_book_name(book_code: str) -> str:
    """
    Get the BibleHub URL book name from a USFM code.
    
    Args:
        book_code: USFM book code (e.g., "MAT")
    
    Returns:
        BibleHub URL book name (e.g., "matthew")
    
    Raises:
        ValueError: If the book code is invalid
    
    Example:
        >>> get_biblehub_book_name("MAT")
        'matthew'
        >>> get_biblehub_book_name("1SA")
        '1_samuel'
    """
    book_code = book_code.upper()
    if book_code not in USFM_TO_BIBLEHUB:
        raise ValueError(f"Invalid book code: '{book_code}'")
    return USFM_TO_BIBLEHUB[book_code]

