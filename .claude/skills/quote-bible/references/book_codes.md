# Bible Book Codes Reference

This reference provides standard USFM 3.0 book codes and common abbreviations for all 66 books of the Protestant Bible.

## Old Testament

### Pentateuch (Torah)
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Genesis | GEN | Gen, Ge, Gn |
| Exodus | EXO | Exod, Ex, Exo |
| Leviticus | LEV | Lev, Le, Lv |
| Numbers | NUM | Num, Nu, Nm, Nb |
| Deuteronomy | DEU | Deut, De, Dt |

### Historical Books
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Joshua | JOS | Josh, Jos, Jsh |
| Judges | JDG | Judg, Jdg, Jg, Jdgs |
| Ruth | RUT | Ruth, Rth, Ru |
| 1 Samuel | 1SA | 1 Sam, 1 Sa, 1 S |
| 2 Samuel | 2SA | 2 Sam, 2 Sa, 2 S |
| 1 Kings | 1KI | 1 Kgs, 1 Ki, 1 K |
| 2 Kings | 2KI | 2 Kgs, 2 Ki, 2 K |
| 1 Chronicles | 1CH | 1 Chr, 1 Ch, 1 Chron |
| 2 Chronicles | 2CH | 2 Chr, 2 Ch, 2 Chron |
| Ezra | EZR | Ezra, Ezr |
| Nehemiah | NEH | Neh, Ne |
| Esther | EST | Esth, Es |

### Wisdom Literature
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Job | JOB | Job, Jb |
| Psalms | PSA | Ps, Psalm, Psa, Psm, Pss |
| Proverbs | PRO | Prov, Pr, Prv |
| Ecclesiastes | ECC | Eccl, Ec, Ecc, Qoh |
| Song of Solomon | SNG | Song, So, SOS, Cant |

### Major Prophets
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Isaiah | ISA | Isa, Is |
| Jeremiah | JER | Jer, Je, Jr |
| Lamentations | LAM | Lam, La |
| Ezekiel | EZK | Ezek, Eze, Ezk |
| Daniel | DAN | Dan, Da, Dn |

### Minor Prophets
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Hosea | HOS | Hos, Ho |
| Joel | JOL | Joel, Joe, Jl |
| Amos | AMO | Amos, Am |
| Obadiah | OBA | Obad, Ob |
| Jonah | JON | Jonah, Jon, Jnh |
| Micah | MIC | Mic, Mc |
| Nahum | NAM | Nah, Na |
| Habakkuk | HAB | Hab, Hb |
| Zephaniah | ZEP | Zeph, Zep, Zp |
| Haggai | HAG | Hag, Hg |
| Zechariah | ZEC | Zech, Zec, Zc |
| Malachi | MAL | Mal, Ml |

## New Testament

### Gospels
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Matthew | MAT | Matt, Mt |
| Mark | MRK | Mark, Mk, Mr |
| Luke | LUK | Luke, Lk, Lu |
| John | JHN | John, Jn, Jhn |

### History
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Acts | ACT | Acts, Ac |

### Pauline Epistles
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Romans | ROM | Rom, Ro, Rm |
| 1 Corinthians | 1CO | 1 Cor, 1 Co |
| 2 Corinthians | 2CO | 2 Cor, 2 Co |
| Galatians | GAL | Gal, Ga |
| Ephesians | EPH | Eph, Ephes |
| Philippians | PHP | Phil, Php, Pp |
| Colossians | COL | Col, Co |
| 1 Thessalonians | 1TH | 1 Thess, 1 Th |
| 2 Thessalonians | 2TH | 2 Thess, 2 Th |
| 1 Timothy | 1TI | 1 Tim, 1 Ti |
| 2 Timothy | 2TI | 2 Tim, 2 Ti |
| Titus | TIT | Titus, Tit |
| Philemon | PHM | Philem, Phm, Pm |

### General Epistles
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Hebrews | HEB | Heb |
| James | JAS | James, Jas, Jm |
| 1 Peter | 1PE | 1 Pet, 1 Pe, 1 P |
| 2 Peter | 2PE | 2 Pet, 2 Pe, 2 P |
| 1 John | 1JN | 1 John, 1 Jn, 1 J |
| 2 John | 2JN | 2 John, 2 Jn, 2 J |
| 3 John | 3JN | 3 John, 3 Jn, 3 J |
| Jude | JUD | Jude, Jd |

### Prophecy
| Book | USFM Code | Common Abbr. |
|------|-----------|--------------|
| Revelation | REV | Rev, Re, The Revelation |

## Usage Notes

- **USFM Code**: The standardized 3-letter code used in the project's directory structure (`./bible/{USFM}/...`)
- **Common Abbreviations**: Various abbreviations users might use when requesting verses
- The fetch script should be flexible enough to handle various abbreviation formats
- When parsing user input, consider normalizing abbreviations to USFM codes for consistency

## Reference Format

When displaying verses, follow the project's citation format:
- `{lang}` → `{lang}-{version}` → `{lang}-{version}-{year}`

Examples:
- `eng` (minimal, language only)
- `eng-NIV` (language and version)
- `eng-NIV-2011` (full specification with year)
