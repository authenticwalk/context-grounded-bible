"""BibleHub URL constants for lexical data endpoints.

This module provides URL templates for various BibleHub lexical pages
including lexicon, interlinear, Strong's, textual variants, and grammar.
"""

# Base URL for BibleHub
BIBLEHUB_BASE_URL = "https://biblehub.com"

# URL templates for different lexical pages
# All use format: {book}/{chapter}-{verse}.htm

# Lexicon page - Strong's numbers with full parsing information
# Example: https://biblehub.com/lexicon/matthew/1-1.htm
LEXICON_URL_TEMPLATE = "https://biblehub.com/lexicon/{book}/{chapter}-{verse}.htm"

# Interlinear page - Word-by-word original text with translations
# Example: https://biblehub.com/interlinear/matthew/1-1.htm
INTERLINEAR_URL_TEMPLATE = "https://biblehub.com/interlinear/{book}/{chapter}-{verse}.htm"

# Strong's concordance page - Detailed Strong's data
# Example: https://biblehub.com/strongs/matthew/1-1.htm
STRONGS_URL_TEMPLATE = "https://biblehub.com/strongs/{book}/{chapter}-{verse}.htm"

# Text page - Manuscript variants across traditions
# Example: https://biblehub.com/text/matthew/1-1.htm
TEXT_URL_TEMPLATE = "https://biblehub.com/text/{book}/{chapter}-{verse}.htm"

# Grammar page - Grammatical analysis
# Example: https://biblehub.com/grammar/matthew/1-1.htm
GRAMMAR_URL_TEMPLATE = "https://biblehub.com/grammar/{book}/{chapter}-{verse}.htm"

# HTTP request timeout in seconds
REQUEST_TIMEOUT = 30

# User agent string for HTTP requests
USER_AGENT = "Mozilla/5.0 (Bible Study Tool - Lexicon Analysis)"
