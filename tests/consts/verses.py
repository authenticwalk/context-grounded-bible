"""
100 Bible verses ranging from most commonly known to obscure passages.
Used for testing AI model accuracy in quoting scripture.
"""

# Format: (reference, category, difficulty_score)
# Difficulty: 1 (most famous) to 10 (very obscure)

VERSES = [
    # Very Famous Verses (1-10) - Difficulty 1-2
    ("John 3:16", "Famous", 1),
    ("Genesis 1:1", "Famous", 1),
    ("Psalm 23:1", "Famous", 1),
    ("John 14:6", "Famous", 1),
    ("Romans 3:23", "Famous", 1),
    ("Romans 6:23", "Famous", 1),
    ("Ephesians 2:8-9", "Famous", 1),
    ("Philippians 4:13", "Famous", 1),
    ("Jeremiah 29:11", "Famous", 1),
    ("Proverbs 3:5-6", "Famous", 1),

    # Well-Known Verses (11-30) - Difficulty 2-3
    ("Matthew 28:19-20", "Well-Known", 2),
    ("1 Corinthians 13:4-8", "Well-Known", 2),
    ("Isaiah 40:31", "Well-Known", 2),
    ("Matthew 6:33", "Well-Known", 2),
    ("Joshua 1:9", "Well-Known", 2),
    ("Psalm 46:1", "Well-Known", 2),
    ("Romans 8:28", "Well-Known", 2),
    ("2 Timothy 3:16", "Well-Known", 2),
    ("Hebrews 11:1", "Well-Known", 2),
    ("James 1:2-3", "Well-Known", 2),
    ("1 John 4:8", "Well-Known", 3),
    ("Matthew 5:14-16", "Well-Known", 3),
    ("Galatians 5:22-23", "Well-Known", 3),
    ("Psalm 119:105", "Well-Known", 3),
    ("Isaiah 53:5", "Well-Known", 3),
    ("John 1:1", "Well-Known", 3),
    ("Acts 1:8", "Well-Known", 3),
    ("1 Peter 5:7", "Well-Known", 3),
    ("Proverbs 22:6", "Well-Known", 3),
    ("Ecclesiastes 3:1", "Well-Known", 3),

    # Moderately Known Verses (31-50) - Difficulty 4-5
    ("Micah 6:8", "Moderate", 4),
    ("Habakkuk 2:14", "Moderate", 4),
    ("Malachi 3:10", "Moderate", 4),
    ("Luke 6:38", "Moderate", 4),
    ("Colossians 3:23", "Moderate", 4),
    ("1 Thessalonians 5:16-18", "Moderate", 4),
    ("Psalm 139:14", "Moderate", 4),
    ("Isaiah 41:10", "Moderate", 4),
    ("Deuteronomy 31:6", "Moderate", 4),
    ("Proverbs 16:3", "Moderate", 4),
    ("Romans 12:2", "Moderate", 5),
    ("2 Corinthians 5:17", "Moderate", 5),
    ("Hebrews 13:5", "Moderate", 5),
    ("Matthew 11:28-30", "Moderate", 5),
    ("John 15:13", "Moderate", 5),
    ("1 Corinthians 10:13", "Moderate", 5),
    ("James 4:7", "Moderate", 5),
    ("Psalm 37:4", "Moderate", 5),
    ("Isaiah 26:3", "Moderate", 5),
    ("Philippians 4:6-7", "Moderate", 5),

    # Less Common Verses (51-70) - Difficulty 6-7
    ("Zephaniah 3:17", "Less Common", 6),
    ("Nehemiah 8:10", "Less Common", 6),
    ("Lamentations 3:22-23", "Less Common", 6),
    ("Joel 2:25", "Less Common", 6),
    ("Haggai 2:9", "Less Common", 6),
    ("Zechariah 4:6", "Less Common", 6),
    ("Hosea 6:6", "Less Common", 6),
    ("Amos 5:24", "Less Common", 6),
    ("Obadiah 1:15", "Less Common", 6),
    ("Jonah 2:9", "Less Common", 6),
    ("Nahum 1:7", "Less Common", 7),
    ("1 Chronicles 16:11", "Less Common", 7),
    ("2 Chronicles 7:14", "Less Common", 7),
    ("Ezra 7:10", "Less Common", 7),
    ("Esther 4:14", "Less Common", 7),
    ("Job 19:25", "Less Common", 7),
    ("Song of Solomon 2:4", "Less Common", 7),
    ("Daniel 12:3", "Less Common", 7),
    ("Titus 2:11-12", "Less Common", 7),
    ("Philemon 1:6", "Less Common", 7),

    # Obscure Verses (71-85) - Difficulty 8
    ("Judges 6:12", "Obscure", 8),
    ("1 Samuel 16:7", "Obscure", 8),
    ("2 Samuel 22:31", "Obscure", 8),
    ("1 Kings 8:61", "Obscure", 8),
    ("2 Kings 20:5", "Obscure", 8),
    ("Leviticus 19:18", "Obscure", 8),
    ("Numbers 6:24-26", "Obscure", 8),
    ("Deuteronomy 6:5", "Obscure", 8),
    ("Ruth 1:16", "Obscure", 8),
    ("Ezekiel 36:26", "Obscure", 8),
    ("2 Peter 3:9", "Obscure", 8),
    ("Jude 1:24", "Obscure", 8),
    ("3 John 1:4", "Obscure", 8),
    ("2 John 1:6", "Obscure", 8),
    ("1 Timothy 4:12", "Obscure", 8),

    # Very Obscure Verses (86-100) - Difficulty 9-10
    ("Haggai 1:5", "Very Obscure", 9),
    ("Zephaniah 2:3", "Very Obscure", 9),
    ("Nahum 2:4", "Very Obscure", 9),
    ("Habakkuk 3:19", "Very Obscure", 9),
    ("Obadiah 1:3", "Very Obscure", 9),
    ("Philemon 1:7", "Very Obscure", 9),
    ("3 John 1:2", "Very Obscure", 9),
    ("2 John 1:4", "Very Obscure", 9),
    ("Jude 1:3", "Very Obscure", 9),
    ("Titus 3:5", "Very Obscure", 9),
    ("2 Thessalonians 3:3", "Very Obscure", 10),
    ("Colossians 4:6", "Very Obscure", 10),
    ("1 Chronicles 29:11", "Very Obscure", 10),
    ("2 Chronicles 16:9", "Very Obscure", 10),
    ("Ezra 10:4", "Very Obscure", 10),
    ("Nehemiah 9:6", "Very Obscure", 10),
    ("Leviticus 26:12", "Very Obscure", 10),
    ("Numbers 23:19", "Very Obscure", 10),
    ("Judges 5:31", "Very Obscure", 10),
    ("Song of Solomon 8:7", "Very Obscure", 10),
]

def get_verses_by_difficulty(min_diff=1, max_diff=10):
    """Get verses filtered by difficulty range."""
    return [v for v in VERSES if min_diff <= v[2] <= max_diff]

def get_verse_references():
    """Get just the verse references as a list."""
    return [v[0] for v in VERSES]

def get_verses_by_category(category):
    """Get verses filtered by category."""
    return [v for v in VERSES if v[1] == category]
