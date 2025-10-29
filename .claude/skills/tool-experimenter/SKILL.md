---
name: tool-experimenter
description: Systematically experiment with and improve Bible study tools. Use this skill when the user requests to "experiment|refine|improve {tool-name}".  Don't use it if they are just wanting to run the tool.
---

# Tool Experimenter

## Overview

This skill enables systematic experimentation and improvement of Bible study tools by generating diverse experimental approaches, testing them in parallel on representative verses, and synthesizing the results into improved tool designs. The skill orchestrates the bible-researcher agent to run experiments, evaluates outcomes, and iteratively refines approaches from broad strategic differences to granular prompt optimizations.

## When to Use This Skill

Use this skill when:
- User says "experiment with {tool-name}" or "run experiments on {tool-name}" or "improve {tool-name}"
- A Bible study tool needs empirical validation and improvement
- Different approaches to a research task need to be compared
- A tool's effectiveness needs to be tested across diverse verse types

## Key Files

Filename are relative to project root

 - **@bible-study-tools/TEMPLATE.md** - The template and instructions for a tools README.md file
 - **@STANDARDIZATION.md** - Naming conventions for bible books, versions, citations, languages, etc.
 - **@REVIEW-GUIDELINES.md** - Detailed instructions on how to review a biblical yarml file for accuracy

## Core Workflow

### Phase 1: Initialization and Planning

1. **Load Tool Context**
   - Create and switch to a git branch following git-flow naming conventions
     - Example: feat/tool-sermon-illustrations
   - Read `./bible-study-tools/{tool-name}/README.md` (if exists) to understand:
     - The tool's purpose and research methodology
     - The current schema and data structure
     - Expected outputs and quality criteria
   - Read `./bible-study-tools/{tool-name}/LEARNINGS.md` (if exists) to understand:
     - Past experiment results
     - Known challenges and solutions
     - Techniques that worked well or poorly
  
  ** If the tool does not exist yet**

  If the tool does not exist make sure you know what they are trying to achieve and create a new tool for it following the template in ./bible-study-tools/TEMPLATE.md


1. **Create Experiment Infrastructure**
   - Create directory: `./bible-study-tools/{tool-name}/experiments/` (if not exists)
   - This will contain all experimental outputs and variations

2. **Design Initial Experiments**
   - Generate **3 fundamentally diverse experimental approaches** that test different strategic directions
   - Use deep thinking to identify truly different approaches, not just variations

   **Example:** If the tool is about Greek words:
   - Experiment A: Focus exclusively on Strong's concordance data
   - Experiment B: Focus on morphological analysis (word forms, tenses, cases)
   - Experiment C: Focus on semantic domains and conceptual relationships

   **Example:** If the tool is asking for sermon illustrations:
   - Find a way to identify top YouTube sermons and their transcriptions for this verse
   - Think deeply about movies and scenes that will help
   - Search the internet for sermon illustrations on this verse

   **Critical Guidelines:**
   - Each experiment should pursue a different philosophical approach
   - Experiments should test different hypotheses about what makes the tool valuable
   - Think broadly: different data sources, different organizational structures, different levels of detail
   - Document each experiment's thesis/hypothesis clearly

### Phase 2: Run Initial Broad Experiments

For each of the 3 initial experiments:

1. **Create Experiment Schema**
   - Copy the base README.md schema as a starting point
   - Modify it according to the experiment's thesis
   - Save as: `./bible-study-tools/{tool-name}/experiments/{experiment-name}/README-rev1.md`

2. **Test on Representative Verses**
   - Select 3 diverse test verses (one at a time):
     - **Verse 1:** Well-known, rich context (e.g., John 1:1)
     - **Verse 2:** Moderate complexity (e.g., Matthew 5:3)
     - **Verse 3:** Obscure or challenging (e.g., Job 38:36 or Habakkuk 3:9)

3. **Generate Data with bible-researcher Agent**
   - For each verse foreach experiment, invoke the bible-researcher agent in parallel (9 instances) with:
     - The experiment's modified README.md
     - The verse reference
   - Save outputs as: `./bible-study-tools/{tool-name}/experiments/{experiment-name}/{BOOK}-{CH:03d}-{VS:03d}-{experiment-name}-rev1.yaml`

4. **Fix Issues and Iterate Within Experiment**
   - Review the generated YAML files
   - Review the feedback the research agent returned (it will tell you what it thought was good and what it struggled with)
   - Identify problems while staying true to the experiment's thesis
   - Document learnings in: `./bible-study-tools/{tool-name}/experiments/{experiment-name}/LEARNINGS.md`
   - Commit using gitflow syntax
     - Example: chore:initial experiments\n(short description of experiments)
     - Example: fix: {website} is unparsable\n(short description of learnings))
   - If issues found:
     - Update the README to rev2
     - Re-run problematic verses
     - Continue up to rev3 if needed

   - 

**Parallelization Strategy:**
- Run all 3 initial experiments concurrently by launching 3 bible-researcher agents in parallel for each verse
- This significantly reduces total execution time
- Each agent works on its own experiment independently

### Phase 3: Evaluate and Decide on Next Steps

1. **Cross-Experiment Analysis**
   - Compare the outputs from all 3 experiments
   - Extract all relevant tests from REVIEW-GUIDELINES.md as a table with headings (test, expected, exp1, exp2, exp3) and add to LEARNINGS.md 
   - Evaluate based on:
     - **Insight Quality:** Which approach surfaced the most valuable insights?
     - **Consistency:** Which approach worked well across all verse types?
     - **AI-Grounding Value:** Which would best help AI systems ground responses?
     - **Completeness:** Which approach provided sufficient context?
     - **Practicality:** Which is sustainable to generate at scale?

2. **Decision Point**

   Determine the next course of action:

   **Option A - Clear Winner:**
   - If one experiment significantly outperforms others
   - Skip to Phase 5 (Refinement) with the winning approach

   **Option B - Complementary Approaches:**
   - If multiple experiments provide different valuable insights
   - Generate 2-3 new "blend" experiments that combine the best elements
   - Return to Phase 2 with these blend experiments

   **Option C - Fundamentally Different Tools:**
   - If experiments reveal distinct, incompatible value propositions
   - Split into multiple separate tools

   **Option D - All Experiments Weak:**
   - If none of the approaches are satisfactory
   - Generate 3 entirely new experimental approaches based on learnings
   - Return to Phase 2 with new experiments

### Phase 4: Granular Refinement Experiments

Once a promising direction is identified, progressively refine with increasingly granular experiments:

1. **Structural Refinements** (if needed)
   - Experiment with different schema organizations
   - Test different levels of detail or groupings
   - Example: Flat vs. nested structures, different field names

2. **Methodological Refinements** (if needed)
   - Experiment with different research techniques
   - Test different source priorities
   - Example: Different website search patterns

3. **Prompt Refinements** (most granular)
   - Experiment with different instruction phrasings
   - Test different examples or constraints in the README
   - Example: Different ways to request citations, different emphasis on thoroughness

**Diminishing Returns Detection:**
- Stop when improvements between revisions become minimal
- Typically after 3-5 total rounds of refinement
- Document when diminishing returns are reached

### Phase 5: Synthesis and Deployment

1. **Update Tool README.md**
   - Incorporate the winning approach or blended approach
   - Update schema with validated improvements
   - Add stellar examples discovered during experiments to the examples section
   - Ensure research methodology reflects proven effective techniques

2. **Consolidate LEARNINGS.md**
   - Synthesize learnings from all experiment LEARNINGS.md files
   - Create a comprehensive summary in `./bible-study-tools/{tool-name}/LEARNINGS.md`
   - Include:
     - **What Worked Well:** Successful techniques, helpful websites, effective schema fields
     - **What Worked Poorly:** Failed approaches, unhelpful sources, problematic structures
     - **Key Insights:** Breakthrough discoveries during experimentation
     - **Recommendations:** Guidance for future tool development or usage

3. **Preserve Experiment History**
   - Keep all experiment folders for future reference
   - This creates an audit trail of the tool's evolution

4. **Commit to Source**
   - Commit using PR friendly name and description
   - Create a PR

## File Naming Conventions

Follow these strict naming patterns:

**Experiment Schema Revisions:**
```
./bible-study-tools/{tool-name}/experiments/{experiment-name}/README-rev{N}.md
```

**Experiment Data Outputs:**
```
./bible-study-tools/{tool-name}/experiments/output/{BOOK}-{CH:03d}-{VS:03d}-{experiment-name}-rev{N}.yaml
```

**Experiment Learnings:**
```
./bible-study-tools/{tool-name}/experiments/{experiment-name}/LEARNINGS.md
```

Where:
- `{tool-name}`: The Bible study tool being experimented on
- `{experiment-name}`: A descriptive name for the experimental approach (e.g., "strongs-focused", "morphology-based")
- `{N}`: Revision number (1, 2, 3, etc.)
- `{BOOK}`: USFM 3.0 three-letter book code (MAT, JHN, GEN, etc.)
- `{CH:03d}`: Zero-padded chapter number (001, 005, 038, etc.)
- `{VS:03d}`: Zero-padded verse number (001, 016, etc.)

## Test Verse Selection Strategy

Choose test verses that represent different complexity levels:

**High-Context Verses** (well-studied, rich theological content):
- John 1:1, John 3:16, Matthew 5:3-10, Romans 3:23, Genesis 1:1

**Medium-Context Verses** (moderately studied, specific contexts):
- Colossians 3:1, 1 Samuel 15:3, Daniel 9:25, Psalm 119:105

**Low-Context Verses** (obscure, challenging, less-studied):
- Job 38:36, Habakkuk 3:9, Genesis 36:11, John 11:35 (shortest verse)

Mix these categories to ensure experiments work across the spectrum.

## Quality Standards

Each experiment should:
- Stay true to its core thesis/hypothesis
- Generate valid YAML that conforms to schema
- Include proper citations following project standards
- Provide substantial, AI-grounding content (not superficial summaries)
- Work consistently across different verse types

## Success Metrics

The experimentation process is complete when:
- A clear winning approach or blend is identified
- The approach works consistently across diverse verse types
- Diminishing returns are reached in refinement
- README.md and LEARNINGS.md are updated with validated improvements
- Future tool usage and development is informed by empirical evidence
