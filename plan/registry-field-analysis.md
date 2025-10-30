# Tool Registry Field Analysis

## Current State

Tool registry currently has TWO fields:
- `complexity: low|medium|high` - File size and processing requirements
- `depth: light|medium|full|all` - Minimum depth level to include this tool

## Problem

Having both fields is:
1. **Redundant** - Highly correlated (large files = full depth only)
2. **Confusing** - Which field takes precedence?
3. **Maintenance burden** - Two fields to keep in sync

## Options Analysis

### Option 1: Keep Only "depth"

**Values:** `light | medium | full | all`

**Pros:**
- User-facing concept (matches query depth levels)
- Direct mapping to scripture-study behavior
- Simpler (one field vs two)

**Cons:**
- Loses technical information about file size
- Doesn't convey performance expectations
- Name "depth" is ambiguous (depth of what?)

### Option 2: Keep Only "complexity"

**Values:** `low | medium | high`

**Pros:**
- Technical metric (objective, measurable)
- Helps with performance planning
- Clear file size expectations

**Cons:**
- Not user-facing (users don't query by "complexity")
- Awkward mapping to query depth levels
- Doesn't clearly indicate when to include

### Option 3: Single Field "scope"

**Values:** `core | standard | comprehensive`

**Pros:**
- Better semantic meaning than "depth"
- Conveys BOTH detail level AND file size
- Clear user intent mapping:
  - light queries → core only
  - medium queries → core + standard
  - full queries → core + standard + comprehensive
- Professional terminology

**Cons:**
- Need to document size expectations per scope
- Existing tools need migration

**Scope Definitions:**

| Scope | Size Range | Description | Examples | Query Inclusion |
|-------|-----------|-------------|----------|-----------------|
| `core` | 1-50 KB | Essential data, always valuable | sermon-illustrations, cross-references | light, medium, full |
| `standard` | 50-500 KB | Standard research depth | word-studies, historical-context | medium, full |
| `comprehensive` | >500 KB | Exhaustive reference data | all-translations, full-lexicon | full only |

### Option 4: Single Field "inclusion_level"

**Values:** `essential | standard | comprehensive`

**Pros:**
- Extremely clear what it controls (inclusion in queries)
- Similar benefits to "scope"

**Cons:**
- Longer field name
- Less concise than "scope"

## Recommendation

**Use single field `scope` with values `core | standard | comprehensive`**

**Rationale:**
1. **Clarity** - "Scope" clearly conveys "how much data this tool provides"
2. **Dual purpose** - Implies both detail level AND file size expectations
3. **User-centric** - Maps naturally to user queries (light/medium/full depth)
4. **Professional** - Common terminology in software design
5. **Concise** - Short field name, clear values

**Mapping to queries:**
```python
if query_depth == "light":
    include_scopes = ["core"]
elif query_depth == "medium":
    include_scopes = ["core", "standard"]
elif query_depth == "full":
    include_scopes = ["core", "standard", "comprehensive"]
```

## Migration Plan

1. Update `tool-registry.yaml` to use `scope` instead of `complexity` and `depth`
2. Update `scripture_study.py` to filter by `scope`
3. Update `bible-study-tool-creator` SKILL.md to ask about scope
4. Update `tool-experimenter` SKILL.md to include registry updates
5. Test with existing tools
6. Commit changes

## Example Registry Entry (After Change)

```yaml
sermon-illustrations:
  name: Sermon Illustrations
  summary: Concrete examples from films, literature, history for preaching and teaching
  scope: core
  category: practical

translations-ebible:
  name: eBible Translations
  summary: Comprehensive translation database from eBible corpus (1000+ translations)
  scope: comprehensive
  category: linguistic
```
