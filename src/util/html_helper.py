"""HTML processing utilities for BibleHub pages."""

import html
import quopri
import re


def decode_html_file(html_bytes: bytes) -> str:
    """
    Decode HTML content that may be quoted-printable encoded or in MHTML format.
    
    Args:
        html_bytes: Raw bytes from HTML file
        
    Returns:
        Decoded HTML string
    """
    # Try quoted-printable decoding first
    try:
        decoded = quopri.decodestring(html_bytes).decode('utf-8')
    except:
        # Fall back to plain UTF-8
        decoded = html_bytes.decode('utf-8')
    
    # If it's an MHTML file (saved web page), extract the HTML content
    if 'Content-Type: text/html' in decoded and 'MultipartBoundary' in decoded:
        # Find the HTML content section
        html_start = decoded.find('<!DOCTYPE')
        if html_start == -1:
            html_start = decoded.find('<html')
        if html_start > 0:
            decoded = decoded[html_start:]
    
    # Unescape HTML entities (&lt; becomes <, etc.)
    return html.unescape(decoded)


def clean_verse_text(text: str) -> str:
    """
    Clean verse text by removing HTML artifacts and extra whitespace.
    
    Args:
        text: Raw verse text with possible HTML artifacts
        
    Returns:
        Clean verse text
    """
    # Stop at any HTML artifact markers (including class=" which indicates we hit HTML)
    markers = ['<', '&lt;', '&gt;', '&amp;', 'class="', 'href="', '<span']
    for marker in markers:
        if marker in text:
            text = text.split(marker)[0]
    
    # Remove any remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove HTML entities that represent tags
    text = re.sub(r'&lt;[^&]+&gt;', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def extract_text_from_html_pattern(decoded_html: str, start_pos: int, lookahead: int = 600) -> str:
    """
    Extract verse text from BibleHub's syntax-highlighted HTML.
    
    The HTML has syntax highlighting applied where the actual content is
    wrapped in various span tags. This extracts the text after a <br> tag.
    
    Args:
        decoded_html: The decoded HTML string (after html.unescape)
        start_pos: Position to start looking from
        lookahead: How many characters ahead to search
        
    Returns:
        Extracted verse text, or empty string if not found
    """
    context = decoded_html[start_pos:start_pos + lookahead]
    
    # After html.unescape, look for text after <br> tag and before next <p> tag
    # Pattern: <span class="html-tag"><br /></span>VERSE_TEXT<span class="html-tag"><p>
    text_pattern = r'<span class="html-tag"><br[^>]*></span>(.*?)(?=<span class="html-tag"><p>|$)'
    text_match = re.search(text_pattern, context, re.DOTALL)
    
    if not text_match:
        return ""
    
    raw_text = text_match.group(1)
    
    # The text might be:
    # 1. Directly after </span>: ...</span>TEXT<span...
    # 2. Inside a language span: ...<span class="fr">TEXT</span>...
    
    # Try to find text in language-specific span first
    lang_span_pattern = r'<span class="html-attribute-value">(\w+)</span>"></span>([^<]+)<span class="html-tag"></span></span>'
    lang_match = re.search(lang_span_pattern, raw_text)
    if lang_match:
        return lang_match.group(2).strip()
    
    # Or try simple pattern: ></span>TEXT<span class="html-tag">
    simple_match = re.search(r'></span>([^<]+?)(?=<span class="html-tag">|$)', raw_text)
    if simple_match:
        text = simple_match.group(1).strip()
        if len(text) > 5:  # Make sure we got actual text
            return text
    
    # Otherwise clean up the raw text
    return clean_verse_text(raw_text)

