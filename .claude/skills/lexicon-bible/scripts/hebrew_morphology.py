"""Hebrew morphology parser for morphhb data.

This module parses Hebrew morphology codes from the OpenScriptures morphhb
repository (https://github.com/openscriptures/morphhb).

Morphology Code Format: H + POS + features

Examples:
- HVqp3ms = Hebrew Verb, Qal, Perfect, 3rd person masculine singular
- HR/Ncfsa = Hebrew Preposition / Noun construct feminine singular absolute
- HNcmpa = Hebrew Noun common masculine plural absolute

Code Structure:
- H = Hebrew (prefix)
- POS = Part of speech (V=verb, N=noun, A=adjective, etc.)
- Features vary by POS (stem, tense, person, gender, number, state, etc.)
"""

from typing import Dict, Optional, List

# Part of Speech codes (Hebrew)
HEBREW_POS_CODES = {
    'V': 'verb',
    'N': 'noun',
    'A': 'adjective',
    'R': 'preposition',
    'C': 'conjunction',
    'T': 'particle',
    'D': 'adverb',
    'P': 'pronoun',
    'S': 'suffix',
}

# Verb Stem codes (Binyanim)
VERB_STEM_CODES = {
    'q': 'qal',
    'N': 'niphal',
    'p': 'piel',
    'P': 'pual',
    'h': 'hiphil',
    'H': 'hophal',
    't': 'hithpael',
    'o': 'polel',
    'O': 'polal',
    'r': 'hithpolel',
    'm': 'poel',
    'M': 'poal',
    'k': 'palel',
    'K': 'pulal',
    'Q': 'qal passive',
    'l': 'pilpel',
    'L': 'polpal',
    'f': 'hithpalpel',
    'D': 'nithpael',
    'j': 'pealal',
    'i': 'pilel',
    'u': 'hothpaal',
    'c': 'tiphil',
    'v': 'hishtaphel',
    'w': 'nithpalel',
    'y': 'nithpoel',
    'z': 'hithpoel',
}

# Verb Tense/Aspect codes
VERB_TENSE_CODES = {
    'p': 'perfect',
    'q': 'sequential perfect',
    'i': 'imperfect',
    'w': 'sequential imperfect',
    'h': 'cohortative',
    'j': 'jussive',
    'v': 'imperative',
    'r': 'participle active',
    's': 'participle passive',
    'a': 'infinitive absolute',
    'c': 'infinitive construct',
}

# Person codes
PERSON_CODES = {
    '1': 'first',
    '2': 'second',
    '3': 'third',
}

# Gender codes
GENDER_CODES = {
    'm': 'masculine',
    'f': 'feminine',
    'c': 'common',
}

# Number codes
NUMBER_CODES = {
    's': 'singular',
    'd': 'dual',
    'p': 'plural',
}

# Noun State codes
NOUN_STATE_CODES = {
    'a': 'absolute',
    'c': 'construct',
    'd': 'determined',
}


def parse_hebrew_morphology(code: str) -> Dict:
    """Parse a Hebrew morphology code from morphhb.

    Args:
        code: Morphology code string (e.g., "HVqp3ms", "HR/Ncfsa")

    Returns:
        Dictionary with parsed morphological components

    Examples:
        >>> parse_hebrew_morphology("HVqp3ms")
        {'language': 'hebrew', 'pos': 'verb', 'stem': 'qal', 'tense': 'perfect',
         'person': 'third', 'gender': 'masculine', 'number': 'singular'}

        >>> parse_hebrew_morphology("HR/Ncfsa")
        {'language': 'hebrew', 'components': [
            {'pos': 'preposition'},
            {'pos': 'noun', 'type': 'common', 'gender': 'feminine',
             'number': 'singular', 'state': 'absolute'}
        ]}
    """
    if not code or not code.startswith('H'):
        return {}

    # Remove leading 'H'
    code = code[1:]

    # Check for compound morphology (prefix + word)
    if '/' in code:
        parts = code.split('/')
        return {
            'language': 'hebrew',
            'components': [parse_hebrew_component(part) for part in parts]
        }

    # Single component
    result = parse_hebrew_component(code)
    result['language'] = 'hebrew'
    return result


def parse_hebrew_component(code: str) -> Dict:
    """Parse a single Hebrew morphology component.

    Args:
        code: Component code (e.g., "Vqp3ms", "Ncfsa", "R")

    Returns:
        Dictionary with parsed component
    """
    if not code:
        return {}

    result = {}
    pos_code = code[0]

    # Get part of speech
    if pos_code in HEBREW_POS_CODES:
        result['pos'] = HEBREW_POS_CODES[pos_code]
    else:
        # Unknown POS
        return {'raw_code': code}

    # Parse based on POS
    if pos_code == 'V':
        # Verb: V + stem + tense + person + gender + number
        parse_verb(code[1:], result)
    elif pos_code == 'N':
        # Noun: N + type + gender + number + state
        parse_noun(code[1:], result)
    elif pos_code == 'A':
        # Adjective: A + gender + number + state
        parse_adjective(code[1:], result)
    elif pos_code == 'P':
        # Pronoun: P + type + person + gender + number
        parse_pronoun(code[1:], result)
    elif pos_code == 'S':
        # Suffix: S + type + person + gender + number
        parse_suffix(code[1:], result)
    # Prepositions, conjunctions, particles, adverbs typically have no additional features

    return result


def parse_verb(features: str, result: Dict) -> None:
    """Parse verb features: stem + tense + person + gender + number

    Example: "qp3ms" = qal perfect 3rd person masculine singular
    """
    if len(features) < 1:
        return

    # Position 0: Stem
    if features[0] in VERB_STEM_CODES:
        result['stem'] = VERB_STEM_CODES[features[0]]

    if len(features) < 2:
        return

    # Position 1: Tense/Aspect
    if features[1] in VERB_TENSE_CODES:
        result['tense'] = VERB_TENSE_CODES[features[1]]

    if len(features) < 3:
        return

    # Position 2: Person
    if features[2] in PERSON_CODES:
        result['person'] = PERSON_CODES[features[2]]

    if len(features) < 4:
        return

    # Position 3: Gender
    if features[3] in GENDER_CODES:
        result['gender'] = GENDER_CODES[features[3]]

    if len(features) < 5:
        return

    # Position 4: Number
    if features[4] in NUMBER_CODES:
        result['number'] = NUMBER_CODES[features[4]]


def parse_noun(features: str, result: Dict) -> None:
    """Parse noun features: type + gender + number + state

    Example: "cfsa" = common feminine singular absolute
    """
    if len(features) < 1:
        return

    # Position 0: Type (common, proper, gentilic)
    noun_types = {'c': 'common', 'p': 'proper', 'g': 'gentilic'}
    if features[0] in noun_types:
        result['type'] = noun_types[features[0]]

    if len(features) < 2:
        return

    # Position 1: Gender
    if features[1] in GENDER_CODES:
        result['gender'] = GENDER_CODES[features[1]]

    if len(features) < 3:
        return

    # Position 2: Number
    if features[2] in NUMBER_CODES:
        result['number'] = NUMBER_CODES[features[2]]

    if len(features) < 4:
        return

    # Position 3: State
    if features[3] in NOUN_STATE_CODES:
        result['state'] = NOUN_STATE_CODES[features[3]]


def parse_adjective(features: str, result: Dict) -> None:
    """Parse adjective features: gender + number + state

    Example: "msa" = masculine singular absolute
    """
    if len(features) < 1:
        return

    # Position 0: Gender
    if features[0] in GENDER_CODES:
        result['gender'] = GENDER_CODES[features[0]]

    if len(features) < 2:
        return

    # Position 1: Number
    if features[1] in NUMBER_CODES:
        result['number'] = NUMBER_CODES[features[1]]

    if len(features) < 3:
        return

    # Position 2: State
    if features[2] in NOUN_STATE_CODES:
        result['state'] = NOUN_STATE_CODES[features[2]]


def parse_pronoun(features: str, result: Dict) -> None:
    """Parse pronoun features: type + person + gender + number

    Types: d=demonstrative, f=indefinite, i=interrogative, p=personal, r=relative
    """
    if len(features) < 1:
        return

    # Position 0: Type
    pronoun_types = {
        'd': 'demonstrative',
        'f': 'indefinite',
        'i': 'interrogative',
        'p': 'personal',
        'r': 'relative',
    }
    if features[0] in pronoun_types:
        result['type'] = pronoun_types[features[0]]

    if len(features) < 2:
        return

    # Position 1: Person
    if features[1] in PERSON_CODES:
        result['person'] = PERSON_CODES[features[1]]

    if len(features) < 3:
        return

    # Position 2: Gender
    if features[2] in GENDER_CODES:
        result['gender'] = GENDER_CODES[features[2]]

    if len(features) < 4:
        return

    # Position 3: Number
    if features[3] in NUMBER_CODES:
        result['number'] = NUMBER_CODES[features[3]]


def parse_suffix(features: str, result: Dict) -> None:
    """Parse suffix features: type + person + gender + number

    Types: d=directional he, h=paragogic he, n=paragogic nun, p=pronominal
    """
    if len(features) < 1:
        return

    # Position 0: Type
    suffix_types = {
        'd': 'directional he',
        'h': 'paragogic he',
        'n': 'paragogic nun',
        'p': 'pronominal',
    }
    if features[0] in suffix_types:
        result['type'] = suffix_types[features[0]]

    if len(features) < 2:
        return

    # Position 1: Person
    if features[1] in PERSON_CODES:
        result['person'] = PERSON_CODES[features[1]]

    if len(features) < 3:
        return

    # Position 2: Gender
    if features[2] in GENDER_CODES:
        result['gender'] = GENDER_CODES[features[2]]

    if len(features) < 4:
        return

    # Position 3: Number
    if features[3] in NUMBER_CODES:
        result['number'] = NUMBER_CODES[features[3]]


def parse_strongs_number(lemma: str) -> Dict:
    """Parse augmented Strong's number from morphhb.

    morphhb includes prefixes for prepositions, articles, and conjunctions.

    Args:
        lemma: Strong's lemma (e.g., "b/7225", "1254 a", "430")

    Returns:
        Dictionary with parsed Strong's components

    Examples:
        >>> parse_strongs_number("b/7225")
        {'components': [
            {'prefix': 'b', 'meaning': 'in, with, by'},
            {'strongs': 'H7225'}
        ]}

        >>> parse_strongs_number("1254 a")
        {'strongs': 'H1254a'}
    """
    if not lemma:
        return {}

    # Common prefixes
    prefixes = {
        'a': {'meaning': 'not, without (negation)'},
        'b': {'meaning': 'in, with, by (preposition)'},
        'c': {'meaning': 'and (conjunction)'},
        'd': {'meaning': 'the (definite article)'},
        'e': {'meaning': 'to (preposition)'},
        'h': {'meaning': 'the (interrogative)'},
        'k': {'meaning': 'like, as (preposition)'},
        'l': {'meaning': 'to, for (preposition)'},
        'm': {'meaning': 'from (preposition)'},
        's': {'meaning': 'which, that (relative)'},
    }

    # Check for compound (prefix/number)
    if '/' in lemma:
        parts = lemma.split('/')
        components = []
        for part in parts:
            if part in prefixes:
                components.append({
                    'prefix': part,
                    'meaning': prefixes[part]['meaning']
                })
            else:
                # Parse as Strong's number
                clean_num = part.replace(' ', '')
                components.append({'strongs': f'H{clean_num}'})
        return {'components': components}

    # Single Strong's number (may have suffix like "1254 a")
    clean_num = lemma.replace(' ', '')
    return {'strongs': f'H{clean_num}'}


def format_morphology_display(morphology: Dict) -> str:
    """Format morphology dictionary for readable display.

    Args:
        morphology: Parsed morphology dictionary

    Returns:
        Human-readable string

    Example:
        >>> format_morphology_display({'pos': 'verb', 'stem': 'qal',
        ...                            'tense': 'perfect', 'person': 'third',
        ...                            'gender': 'masculine', 'number': 'singular'})
        'Verb: Qal Perfect, 3rd person masculine singular'
    """
    if not morphology:
        return ''

    # Handle compound morphology
    if 'components' in morphology:
        parts = [format_component_display(comp) for comp in morphology['components']]
        return ' + '.join(parts)

    return format_component_display(morphology)


def format_component_display(component: Dict) -> str:
    """Format a single morphology component for display."""
    if not component:
        return ''

    pos = component.get('pos', '').capitalize()

    if component.get('pos') == 'verb':
        # Verb: Stem Tense, Person Gender Number
        parts = [pos + ':']
        if 'stem' in component:
            parts.append(component['stem'].capitalize())
        if 'tense' in component:
            parts.append(component['tense'].capitalize())

        details = []
        if 'person' in component:
            details.append(f"{component['person']}-person")
        if 'gender' in component:
            details.append(component['gender'])
        if 'number' in component:
            details.append(component['number'])

        if details:
            parts.append(', ' + ' '.join(details))

        return ' '.join(parts)

    elif component.get('pos') == 'noun':
        # Noun: Type Gender Number State
        parts = [pos + ':']
        if 'type' in component:
            parts.append(component['type'].capitalize())
        if 'gender' in component:
            parts.append(component['gender'])
        if 'number' in component:
            parts.append(component['number'])
        if 'state' in component:
            parts.append(f"({component['state']})")

        return ' '.join(parts)

    elif component.get('pos') == 'adjective':
        # Adjective: Gender Number State
        parts = [pos + ':']
        if 'gender' in component:
            parts.append(component['gender'])
        if 'number' in component:
            parts.append(component['number'])
        if 'state' in component:
            parts.append(f"({component['state']})")

        return ' '.join(parts)

    elif component.get('pos') in ['pronoun', 'suffix']:
        # Pronoun/Suffix: Type Person Gender Number
        parts = [pos + ':']
        if 'type' in component:
            parts.append(component['type'].capitalize())
        if 'person' in component:
            parts.append(f"{component['person']}-person")
        if 'gender' in component:
            parts.append(component['gender'])
        if 'number' in component:
            parts.append(component['number'])

        return ' '.join(parts)

    else:
        # Simple POS (preposition, conjunction, etc.)
        return pos


if __name__ == '__main__':
    # Test examples
    test_cases = [
        "HVqp3ms",      # Verb: qal perfect 3ms
        "HR/Ncfsa",     # Preposition + Noun
        "HNcmpa",       # Noun: common masculine plural absolute
        "HTd/Ncmpa",    # Particle + Article + Noun
    ]

    print("Hebrew Morphology Parser Test\n")
    for code in test_cases:
        result = parse_hebrew_morphology(code)
        display = format_morphology_display(result)
        print(f"Code: {code}")
        print(f"Parsed: {result}")
        print(f"Display: {display}")
        print()
