"""Morphological parsing code definitions.

This module provides mappings for standard grammatical abbreviations
used in biblical Greek and Hebrew parsing information.
"""

# Part of Speech codes
POS_CODES = {
    'N': 'noun',
    'V': 'verb',
    'A': 'adjective',
    'D': 'determiner',
    'P': 'pronoun',
    'R': 'preposition',
    'C': 'conjunction',
    'I': 'interjection',
    'T': 'particle',
    'X': 'indeclinable',
}

# Case codes (Greek)
CASE_CODES = {
    'N': 'nominative',
    'G': 'genitive',
    'D': 'dative',
    'A': 'accusative',
    'V': 'vocative',
}

# Gender codes
GENDER_CODES = {
    'M': 'masculine',
    'F': 'feminine',
    'N': 'neuter',
}

# Number codes
NUMBER_CODES = {
    'S': 'singular',
    'P': 'plural',
}

# Tense codes (Greek verbs)
TENSE_CODES = {
    'P': 'present',
    'I': 'imperfect',
    'F': 'future',
    'A': 'aorist',
    'X': 'perfect',
    'Y': 'pluperfect',
}

# Voice codes (Greek verbs)
VOICE_CODES = {
    'A': 'active',
    'M': 'middle',
    'P': 'passive',
}

# Mood codes (Greek verbs)
MOOD_CODES = {
    'I': 'indicative',
    'S': 'subjunctive',
    'O': 'optative',
    'M': 'imperative',
    'N': 'infinitive',
    'P': 'participle',
}

# Person codes (verbs)
PERSON_CODES = {
    '1': 'first',
    '2': 'second',
    '3': 'third',
}

# Hebrew stem codes (binyanim)
HEBREW_STEM_CODES = {
    'q': 'qal',
    'N': 'niphal',
    'p': 'piel',
    'P': 'pual',
    'h': 'hiphil',
    'H': 'hophal',
    't': 'hithpael',
}


def parse_morphology_code(code: str) -> dict:
    """
    Parse a morphology code into its components.

    Common patterns:
    - N-NFS = Noun, Nominative, Feminine, Singular
    - V-AIA-3S = Verb, Aorist, Indicative, Active, 3rd person, Singular
    - A-NSM = Adjective, Nominative, Singular, Masculine

    Args:
        code: Morphology code string (e.g., "N-NFS", "V-AIA-3S")

    Returns:
        Dictionary with parsed components

    Example:
        >>> parse_morphology_code("N-NFS")
        {'pos': 'noun', 'case': 'nominative', 'gender': 'feminine', 'number': 'singular'}

        >>> parse_morphology_code("V-AIA-3S")
        {'pos': 'verb', 'tense': 'aorist', 'voice': 'active', 'mood': 'indicative',
         'person': 'third', 'number': 'singular'}
    """
    if not code or code == '-':
        return {}

    result = {}
    parts = code.split('-')

    if not parts:
        return result

    # First part is always POS
    pos_code = parts[0][0] if parts[0] else None
    if pos_code in POS_CODES:
        result['pos'] = POS_CODES[pos_code]

    # For nouns, adjectives, pronouns, determiners: Case-Gender-Number
    if pos_code in ['N', 'A', 'P', 'D'] and len(parts) > 1:
        features = parts[1] if len(parts[1]) >= 3 else parts[1] + '---'

        # Case (position 0)
        if len(features) > 0 and features[0] in CASE_CODES:
            result['case'] = CASE_CODES[features[0]]

        # Gender (position 1)
        if len(features) > 1 and features[1] in GENDER_CODES:
            result['gender'] = GENDER_CODES[features[1]]

        # Number (position 2)
        if len(features) > 2 and features[2] in NUMBER_CODES:
            result['number'] = NUMBER_CODES[features[2]]

    # For verbs: Tense-Voice-Mood-Person-Number
    elif pos_code == 'V':
        if len(parts) > 1:
            verb_features = parts[1]

            # Tense (position 0)
            if len(verb_features) > 0 and verb_features[0] in TENSE_CODES:
                result['tense'] = TENSE_CODES[verb_features[0]]

            # Voice (position 1)
            if len(verb_features) > 1 and verb_features[1] in VOICE_CODES:
                result['voice'] = VOICE_CODES[verb_features[1]]

            # Mood (position 2)
            if len(verb_features) > 2 and verb_features[2] in MOOD_CODES:
                result['mood'] = MOOD_CODES[verb_features[2]]

        # Person and Number often in second hyphen group
        if len(parts) > 2:
            person_num = parts[2]

            # Person (position 0)
            if len(person_num) > 0 and person_num[0] in PERSON_CODES:
                result['person'] = PERSON_CODES[person_num[0]]

            # Number (position 1)
            if len(person_num) > 1 and person_num[1] in NUMBER_CODES:
                result['number'] = NUMBER_CODES[person_num[1]]

    return result


def format_parsing_display(parsing: dict) -> str:
    """
    Format parsing information for readable display.

    Args:
        parsing: Dictionary of parsing components

    Returns:
        Human-readable string

    Example:
        >>> format_parsing_display({'pos': 'noun', 'case': 'nominative',
        ...                         'gender': 'feminine', 'number': 'singular'})
        'Noun, Nominative Feminine Singular'
    """
    if not parsing:
        return ''

    parts = []

    # POS comes first, capitalized
    if 'pos' in parsing:
        parts.append(parsing['pos'].capitalize())

    # For verbs, show tense-voice-mood
    if parsing.get('pos') == 'verb':
        verb_parts = []
        if 'tense' in parsing:
            verb_parts.append(parsing['tense'].capitalize())
        if 'voice' in parsing:
            verb_parts.append(parsing['voice'].capitalize())
        if 'mood' in parsing:
            verb_parts.append(parsing['mood'].capitalize())
        if verb_parts:
            parts.append(' '.join(verb_parts))

        # Person and number
        person_num = []
        if 'person' in parsing:
            person_num.append(f"{parsing['person']}-person")
        if 'number' in parsing:
            person_num.append(parsing['number'])
        if person_num:
            parts.append(' '.join(person_num))

    # For nominals, show case-gender-number
    else:
        case_gen_num = []
        if 'case' in parsing:
            case_gen_num.append(parsing['case'].capitalize())
        if 'gender' in parsing:
            case_gen_num.append(parsing['gender'].capitalize())
        if 'number' in parsing:
            case_gen_num.append(parsing['number'].capitalize())
        if case_gen_num:
            parts.append(' '.join(case_gen_num))

    return ', '.join(parts)
