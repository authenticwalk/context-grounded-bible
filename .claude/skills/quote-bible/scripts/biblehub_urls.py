"""BibleHub URL constants and HTTP configuration.

This module centralizes all BibleHub-related URLs and HTTP settings
for consistent usage across the Bible verse fetching system.
"""

# Base URL for BibleHub
BIBLEHUB_BASE_URL = "https://biblehub.com"

# URL template for multi-translation verse pages
# Format: https://biblehub.com/multi/{book}/{chapter}-{verse}.htm
# Example: https://biblehub.com/multi/matthew/5-3.htm
BIBLEHUB_MULTI_URL_TEMPLATE = "https://biblehub.com/multi/{book}/{chapter}-{verse}.htm"

# HTTP request timeout in seconds
REQUEST_TIMEOUT = 30

# User agent string for HTTP requests
USER_AGENT = "Mozilla/5.0 (Bible Study Tool)"
