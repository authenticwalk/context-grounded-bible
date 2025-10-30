# Five Sources Verification - Blue Letter Bible, STEPBible, BibleHub, Bolls API

**Date:** 2025-10-30
**Purpose:** Verify five suggested sources for Strong's enhancement and lexicon data

## Summary Table

| Source | Downloadable Data? | API? | License | Format | Recommendation |
|--------|-------------------|------|---------|--------|----------------|
| 1. Blue Letter Bible | ❌ No | ❌ No | Web only | - | ❌ WEB PLATFORM ONLY |
| 2. STEPBible | ✅ Yes | ❌ No | CC BY 4.0 | TSV | ✅ ALREADY USING |
| 3. BibleHub Text pages | ❌ No | ❌ No | Web only | - | ❌ WEB DISPLAY ONLY |
| 4. BibleHub Interlinear | ⚠️ Partial | ❌ No | Public Domain | XLSX, TSV, USFM | ⚠️ INVESTIGATE FURTHER |
| 5. Bolls Bible API | ✅ Yes | ✅ Yes | Free | JSON | ✅ GOOD FOR LOOKUPS |

## Detailed Findings

### 1. Blue Letter Bible ❌

**What they have:**
- Comprehensive online lexicons (Thayer's, TDNT, BDB, etc.)
- Strong's concordance integration
- Excellent web interface for study

**What we need:**
- Downloadable structured data (JSON, XML, CSV)
- API access
- Programmatic access to lexicons

**Status:** ❌ **Not available for programmatic use**

**Findings:**
- Blue Letter Bible is a web platform only
- No API or data downloads mentioned
- No GitHub repositories found
- TDNT (Theological Dictionary of the New Testament) and TWOT are copyrighted works not available through BLB
- Thayer's is available on their website but not as downloadable structured data

**Verdict:** Great resource for manual study, but **not usable for our project**

### 2. STEPBible ✅

**Status:** ✅ **Already thoroughly covered**

**What we have from STEPBible:**
- **TBESG** - Greek lexicon (Abbott-Smith + LSJ)
- **TBESH** - Hebrew lexicon (Abridged BDB)
- **TFLSJ** - Full LSJ for Biblical Greek
- All in TSV format
- All CC BY 4.0 license
- All keyed to Strong's numbers

**Source:** https://github.com/STEPBible/STEPBible-Data

**Verdict:** ✅ **This is our primary source - already identified**

### 3. BibleHub Text Pages ❌

**What they show:**
- Greek text analysis pages (e.g., biblehub.com/text/romans/8-1.htm)
- Multiple Greek textual traditions displayed
- Manuscript variant information
- Comparative display of different Greek texts

**What we need:**
- Downloadable manuscript variant data
- Structured data for "8 Greek traditions"
- API or bulk data access

**Status:** ❌ **Web display only, no downloadable data**

**Findings:**
- BibleHub displays manuscript variants on their website
- No downloadable structured data found
- No API for accessing variant readings
- Data appears to be for web display only

**Alternative found:**
- Princeton University has digitized Greek manuscripts downloadable as CSV/XLS
- greeknewtestament.net is transcribing/collating multiple manuscripts

**Verdict:** ❌ **Not available as downloadable data** - Manual web scraping would violate terms of service

### 4. BibleHub Interlinear / Berean Bible ⚠️

**What they have:**
- **Berean Interlinear Bible** with:
  - Greek/Hebrew original text
  - Transliteration
  - Morphology (Person, Tense, Mood, Voice, Case, Number, Gender)
  - Strong's numbers
  - Word-by-word English

**License:** ✅ **Public domain as of April 30, 2023**

**Available formats:**
- Word documents (.docx)
- Spreadsheets (.xlsx, .tsv)
- Plain text (.txt)
- PDF
- E-book (.epub, .azw3, .mobi)
- USFM (Unicode Standard Format Markup)

**Source:** https://berean.bible/downloads.htm

**What's unclear:**
- ⚠️ Do the downloadable spreadsheet formats include Strong's numbers and morphology?
- ⚠️ Is the interlinear data structured in the TSV/XLSX files?
- ⚠️ Or are these just plain text translations?

**Findings:**
- Bible text itself is clearly downloadable in multiple formats
- Page mentions "Interlinear Bible" and "Greek New Testament"
- No explicit mention of Strong's numbers in downloadable files
- Would need to actually download files to verify content

**Modules for Bible software:**
- Available for e-Sword, MySword, and other platforms
- These modules DO include Strong's and morphology
- But these are app-specific formats, not raw data

**No API available** - Licensing is available for apps/websites but requires contact

**Verdict:** ⚠️ **Potentially useful, needs investigation**
- Public domain (excellent!)
- TSV/XLSX formats available
- **TODO:** Download sample files to verify if Strong's/morphology included
- If yes, could be supplemental source
- If no, just another Bible translation

### 5. Bolls Bible API ✅

**Status:** ✅ **Working API with lexicon access**

**API Endpoint:** https://bolls.life/api/

**What it provides:**
- **Dictionaries/Lexicons:**
  - BDBT: Brown-Driver-Briggs (Hebrew) + Thayer's (Greek)
  - RUSD: Russian lexicon (Полный лексикон по Стронгу и Дворецкому)

- **Strong's number queries:**
  - Query by Strong's number (e.g., H125, G523)
  - Returns definitions as JSON

- **Word searches:**
  - Query in Greek, Hebrew, English, or Russian
  - Returns related words and definitions

- **Bible text:**
  - Multiple translations
  - Verse lookups
  - Comparisons

**Response format:** JSON arrays

**License:** Free to use

**API Features:**
- Dictionary endpoint: `https://bolls.life/static/dictionaries/<dictionary>.[json|zip]`
- Strong's lookup (added Feb 2024)
- No authentication required
- Returns JSON for easy parsing

**GitHub:**
- Open source project: https://github.com/Bohooslav/bain (also Bolls-Bible/bain)
- Client/proxy projects available

**Pros:**
- ✅ Free, no authentication
- ✅ JSON responses
- ✅ Strong's number indexed
- ✅ BDB + Thayer's lexicons
- ✅ Good for dynamic lookups

**Cons:**
- ⚠️ API-based (not bulk download)
- ⚠️ Need internet connection for queries
- ⚠️ Rate limits unknown
- ⚠️ Dictionary download endpoint exists but format unclear

**Use cases:**
- Real-time lexicon lookups
- Supplemental definitions
- Validation of our data
- Dynamic web applications

**Verdict:** ✅ **Good supplemental resource**
- Excellent for programmatic lookups
- Not ideal for bulk data processing (our use case)
- Could use to verify/supplement our STEPBible data
- Dictionary download endpoint worth exploring

## Additional Findings

### Other Free Bible APIs with Strong's:

**Complete Study Bible API** (RapidAPI)
- Strong's Numbers
- Greek & Hebrew
- Lexicons
- Location data
- Search functionality
- **BUT:** Requires RapidAPI account, may have rate limits

**Bible SuperSearch API**
- API for Bible text
- Features unclear for lexicons

**Free Use Bible API**
- JSON API for Bible translations
- Hosted on Cloudflare
- No mention of lexicons/Strong's

### Open Source Morphology Projects:

**morphhb** (Hebrew Bible)
- GitHub: openscriptures/morphhb
- Lemma and morphology in OSIS XML
- Augmented Strong's numbers
- JSON version published to npm
- CC BY 4.0 license
- ✅ Good for Hebrew morphology if needed

**morphgnt** (Greek New Testament)
- Linguistic databases
- Python API and REST API
- Strong's Greek Dictionary in XML
- MorphGNT Strong's dictionary: CC0 (public domain)
- ✅ Good for Greek morphology if needed

## Recommendations

### For Strong's Enhancement Project:

**Primary Source (Already Identified):**
- ✅ **STEPBible** - Best comprehensive source, TSV format, CC BY 4.0

**Supplemental Sources Worth Using:**

1. **Bolls Bible API** ✅
   - Use for: Real-time lookups, validation
   - Format: JSON API
   - When: Need to verify definitions or supplement missing entries
   - How: HTTP requests to API endpoints

2. **Berean Bible Interlinear** ⚠️
   - Use for: If TSV files include Strong's/morphology
   - Format: TSV, XLSX
   - When: Need interlinear word-by-word data
   - **Action needed:** Download and verify content

3. **morphhb / morphgnt** ✅
   - Use for: Morphological analysis if we expand beyond lexicons
   - Format: XML, JSON
   - When: Adding detailed grammatical parsing
   - License: CC BY 4.0, CC0

**Not Recommended:**

- ❌ **Blue Letter Bible** - Web only, no data access
- ❌ **BibleHub Text Pages** - Web display only, no downloads
- ❌ **RapidAPI services** - Require accounts, potential costs

### Action Items:

1. ✅ **STEPBible** - Continue as planned (already using)

2. ⚠️ **Berean Bible** - Download sample TSV/XLSX files to verify:
   - Do they include Strong's numbers?
   - Do they include morphology?
   - Is data structured or just plain text?
   - If yes → Add as supplemental source
   - If no → Skip

3. ✅ **Bolls API** - Consider for:
   - Validation script to check our definitions
   - Real-time lookup tool for researchers
   - Not for bulk data import (use STEPBible instead)

4. ⚠️ **morphhb/morphgnt** - Bookmark for future:
   - If we add morphological analysis
   - If we need verse-level word parsing
   - Not needed for basic Strong's enhancement

## Conclusion

**Of the five sources suggested:**

1. ❌ **Blue Letter Bible** - Not available for data access
2. ✅ **STEPBible** - Already using, excellent source
3. ❌ **BibleHub Text pages** - Not available for download
4. ⚠️ **BibleHub Interlinear** - Needs verification of TSV/XLSX content
5. ✅ **Bolls Bible API** - Good for lookups, not bulk data

**Best approach:**
- **Primary:** STEPBible (already planned)
- **Supplemental:** Bolls API for validation/lookups
- **Investigate:** Berean Bible TSV files
- **Future:** morphhb/morphgnt for morphology

**We haven't missed anything critical.** STEPBible remains the best comprehensive source for our Strong's enhancement project.
