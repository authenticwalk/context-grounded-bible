# XML Nesting Analysis: Macula Data Structures

## Current Implementation: Flattened

We currently extract words as a flat list with all attributes at the same level:

```yaml
words:
  - position: 1
    unicode: "Ἐν"
    lemma: "ἐν"
    class: "prep"
    role: "p"
    # ... all fields flat
```

## XML Hierarchical Structure

Macula uses nested `<wg>` (word group) elements to represent syntactic structure:

```xml
<wg class="cl" rule="P-VC-S">              <!-- Clause -->
  <wg class="pp" rule="PrepNp" role="p">   <!-- Prepositional Phrase -->
    <w class="prep">Ἐν</w>                 <!-- Preposition -->
    <w class="noun">ἀρχῇ</w>               <!-- Noun -->
  </wg>
  <w role="vc" class="verb">ἦν</w>         <!-- Verb -->
  <wg class="np" articular="true" rule="DetNP" role="s">  <!-- Noun Phrase -->
    <w class="det">ὁ</w>                   <!-- Determiner -->
    <w class="noun">Λόγος</w>              <!-- Noun -->
  </wg>
</wg>
```

## Use Case Analysis

### Use Case 1: Translation - Identifying Phrases

**Scenario:** Translator needs to understand which words form cohesive units for translation

**Example:** Matthew 5:3 - "οἱ πτωχοὶ τῷ πνεύματι"

**Flattened (current):**
```yaml
- position: 2
  unicode: "οἱ"
  class: "det"
- position: 3
  unicode: "πτωχοὶ"
  class: "adj"
- position: 4
  unicode: "τῷ"
  class: "det"
- position: 5
  unicode: "πνεύματι"
  class: "noun"
```

**Problem:** Can't easily tell that:
- "οἱ πτωχοὶ" (the poor) is one noun phrase
- "τῷ πνεύματι" (in spirit) is a prepositional phrase modifying "poor"

**Nested structure would show:**
```yaml
- phrase_type: "np"  # Noun phrase
  rule: "DetNP"
  role: "subject"
  words:
    - position: 2
      unicode: "οἱ"
    - position: 3
      unicode: "πτωχοὶ"
  modifiers:
    - phrase_type: "pp"  # Prepositional phrase
      rule: "PrepNp"
      words:
        - position: 4
          unicode: "τῷ"
        - position: 5
          unicode: "πνεύματι"
```

**Value:** ⭐⭐⭐⭐ HIGH - Critical for understanding phrase boundaries

### Use Case 2: Syntactic Analysis - Clause Structure

**Scenario:** Understanding complex sentence structure with multiple clauses

**Example:** John 1:1 has 3 coordinated clauses:
1. "Ἐν ἀρχῇ ἦν ὁ Λόγος" (In beginning was the Word)
2. "καὶ ὁ Λόγος ἦν πρὸς τὸν Θεόν" (and the Word was with God)
3. "καὶ Θεὸς ἦν ὁ Λόγος" (and God was the Word)

**Current:** All 17 words in one flat list

**Nested would show:**
```yaml
clauses:
  - clause_type: "cl"
    rule: "P-VC-S"
    words: [1, 2, 3, 4, 5]  # Positions
  - clause_type: "cl"
    rule: "S-VC-P"
    connector: "καί"
    words: [6, 7, 8, 9, 10, 11, 12]
  - clause_type: "cl"
    rule: "P-VC-S"  # Note: fronted predicate
    connector: "καί"
    words: [13, 14, 15, 16, 17]
```

**Value:** ⭐⭐⭐⭐ HIGH - Shows clause boundaries and coordination

### Use Case 3: Discourse Analysis - Referent Tracking

**Scenario:** Following participants across clauses (who does what to whom)

**Example:** Matthew 8:2 - A leper approaches Jesus

**Flattened:** Individual words have `referent` attributes but no grouping:
```yaml
- unicode: "αὐτόν"  # "him"
  referent: "n40008002007"  # Points to "Jesus" earlier
```

**Nested:** Could group all references to same participant:
```yaml
participants:
  - id: "n40008002007"
    references: [5, 8, 12]  # All words referring to Jesus
    role: "patient"  # Receives the action
```

**Value:** ⭐⭐⭐ MEDIUM - Helpful but can be reconstructed from flat data

### Use Case 4: Word Order Analysis - Discontinuous Constituents

**Scenario:** Greek allows word order like "A B C" where A and C belong together but B interrupts

**Example:** Rare in simple sentences, more common in poetry/complex prose

**Flattened:** `discontinuous` attribute marks it but doesn't show the relationship

**Nested:** Could explicitly group discontinuous elements:
```yaml
- phrase_type: "np"
  discontinuous: true
  words: [2, 7]  # Non-adjacent positions
  interrupted_by: [3, 4, 5, 6]
```

**Value:** ⭐⭐ LOW - The `discontinuous` attribute is sufficient

## Pros and Cons

### Flattened Structure (Current)

**Pros:**
- ✅ Simple, easy to process linearly
- ✅ Direct word-by-word lookup
- ✅ Smaller file size (no duplicate structure)
- ✅ All word data immediately accessible
- ✅ Easy to search/filter individual words
- ✅ Works well for word-level tools (concordances, lexicons)

**Cons:**
- ❌ Phrase boundaries not explicit
- ❌ Clause structure requires reconstruction
- ❌ Syntactic relationships harder to visualize
- ❌ Parent-child relationships not obvious
- ❌ Requires AI to infer phrase groupings

### Nested Structure

**Pros:**
- ✅ Explicit phrase/clause boundaries
- ✅ Natural representation of syntax trees
- ✅ Easier to extract phrases as units
- ✅ Shows hierarchical relationships
- ✅ Better for syntactic parsers
- ✅ Clearer for translation workflow
- ✅ Matches linguistic theory

**Cons:**
- ❌ More complex YAML structure
- ❌ Harder to do simple word-level queries
- ❌ Larger file size (nested structure overhead)
- ❌ Need to traverse tree for word access
- ❌ More complex code to build/parse
- ❌ Duplicate information (words appear in both tree and list)

## Hybrid Approach (Recommended)

Keep both: flat word list + phrase structure

```yaml
# Easy access to individual words
words:
  - position: 1
    unicode: "Ἐν"
    lemma: "ἐν"
    morphology:
      class: "prep"
    # ... all word data

# Syntactic structure references positions
syntax:
  clauses:
    - rule: "P-VC-S"
      phrases:
        - type: "pp"
          rule: "PrepNp"
          role: "p"
          words: [1, 2]  # References position
        - type: "v"
          words: [3]
        - type: "np"
          rule: "DetNP"
          role: "s"
          articular: true
          words: [4, 5]
```

**Benefits:**
- ✅ Best of both worlds
- ✅ Simple word access + structure
- ✅ No duplicate data
- ✅ Optional - can ignore syntax if not needed
- ✅ Explicit phrase boundaries
- ✅ Maintains word order in flat list

## Recommendation

**SHORT TERM:** Keep flattened (current approach)
- Sufficient for 90% of use cases
- Simpler to implement and maintain
- Word-level data is what translators primarily need

**LONG TERM:** Add optional syntax section
- Include phrase/clause structure as separate section
- Reference word positions (not duplicate data)
- Make it optional - users can ignore if not needed
- Implement when we have concrete use cases requiring it

## Critical Finding

The most valuable missing piece is **phrase boundary markers**. Even without full nesting, we could add:

```yaml
- position: 2
  unicode: "οἱ"
  phrase_id: "np_1"  # Belongs to noun phrase 1
  phrase_role: "determiner"

- position: 3
  unicode: "πτωχοὶ"
  phrase_id: "np_1"  # Same phrase
  phrase_role: "head"

phrases:
  - id: "np_1"
    type: "np"
    rule: "DetNP"
    words: [2, 3]
    role: "subject"
```

This is a lightweight way to capture the most important nesting information without full tree structure.
