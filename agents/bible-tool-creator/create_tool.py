#!/usr/bin/env python3
"""
Bible Study Tool Creator Agent - Phase 1 MVP

Creates a new Bible study tool with:
- Directory structure
- Template files (README, LEARNINGS, schema)
- YAML generation for 3 test verses
- State management and logging
- Validation gates

Usage:
    python create_tool.py --name "my-tool" --purpose "Tool purpose" \\
        --experiment "initial-experiment"
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Tuple, Dict

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from state_manager import StateManager
from execution_logger import ExecutionLogger
from validator import Validator


class BibleToolCreator:
    """Main agent for creating Bible study tools."""

    # Test verses for Phase 1 MVP
    TEST_VERSES = [
        ("John 1:1", "JHN", 1, 1),
        ("Matthew 5:3", "MAT", 5, 3),
        ("Job 38:36", "JOB", 38, 36)
    ]

    def __init__(self, tool_name: str, purpose: str, experiment: str):
        """
        Initialize tool creator.

        Args:
            tool_name: Name of the tool (kebab-case)
            purpose: Purpose/description of the tool
            experiment: Experiment name
        """
        self.tool_name = tool_name
        self.purpose = purpose
        self.experiment = experiment

        # Paths
        self.base_path = Path.cwd() / "bible-study-tools" / tool_name
        self.rev_path = self.base_path / f"learnings-{experiment}" / "rev1"

        # Infrastructure
        self.state_mgr = StateManager(self.base_path)
        self.logger = ExecutionLogger(self.base_path)
        self.validator = Validator()

    def run(self) -> bool:
        """
        Execute the full tool creation workflow.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create base directory first
            self.base_path.mkdir(parents=True, exist_ok=True)

            # Phase 1: Initialize
            self.logger.log_action(f"Starting tool creation: {self.tool_name}")
            if not self.phase_initialize():
                return False

            # Phase 2: Generate
            if not self.phase_generate():
                return False

            # Phase 3: Pause for Human Review
            self.phase_pause_for_review()

            return True

        except Exception as e:
            self.logger.log_error(str(e), "Main workflow")
            self.state_mgr.add_error(str(e), "Main workflow")
            return False

    def phase_initialize(self) -> bool:
        """
        Phase 1: Initialize tool structure.

        Creates:
        - Directory structure
        - state.yaml
        - execution-log.md
        - README.md template
        - LEARNINGS.md template
        - rev1/README.md with schema

        Returns:
            True if successful
        """
        self.logger.log_phase("initialize", "Started")

        try:
            # Step 1: Create directories
            self.logger.log_action("Creating directory structure")
            self.base_path.mkdir(parents=True, exist_ok=True)
            self.rev_path.mkdir(parents=True, exist_ok=True)

            # Validate directory
            passed, error = self.validator.validate_directory(self.base_path)
            self.logger.log_validation("Base directory", passed, error)
            if not passed:
                self.state_mgr.add_error(error, "Directory creation")
                return False

            # Step 2: Initialize state
            self.logger.log_action("Initializing state.yaml")
            self.state_mgr.initialize(self.tool_name, self.experiment)

            # Step 3: Initialize log
            self.logger.initialize(self.tool_name, self.experiment)
            self.logger.start_revision(1)

            # Step 4: Generate templates
            self.logger.log_action("Generating template files")
            self._generate_readme_template()
            self._generate_learnings_template()
            self._generate_schema_template()

            # Step 5: Validate templates
            for template in ["README.md", "LEARNINGS.md"]:
                template_path = self.base_path / template
                passed, error = self.validator.validate_markdown(template_path)
                self.logger.log_validation(f"Template: {template}", passed, error)
                if not passed:
                    self.state_mgr.add_warning(f"Template validation failed: {error}")

            # Step 6: Add verses to state
            self.logger.log_action("Registering test verses")
            for ref, book, chapter, verse in self.TEST_VERSES:
                yaml_file = f"rev1/{book}-{chapter}-{verse}.yaml"
                self.state_mgr.add_verse(ref, book, chapter, verse, yaml_file)

            # Step 7: Complete phase
            self.state_mgr.update_phase("initialize", "complete")
            self.logger.log_phase("initialize", "Complete")

            return True

        except Exception as e:
            self.logger.log_error(str(e), "Initialize phase")
            self.state_mgr.add_error(str(e), "Initialize phase")
            self.state_mgr.update_phase("initialize", "failed")
            return False

    def phase_generate(self) -> bool:
        """
        Phase 2: Generate YAML for test verses.

        Processes 3 verses sequentially, generating YAML output
        following SCHEMA.md standards.

        Returns:
            True if successful
        """
        self.logger.log_phase("generate", "Started")
        self.state_mgr.update_phase("generate", "in_progress")

        try:
            state = self.state_mgr.load()
            verses_to_process = [v for v in state['verses'] if v['status'] == 'pending']

            for verse_info in verses_to_process:
                ref = verse_info['reference']
                yaml_file = self.base_path / verse_info['yaml_file']

                # Process verse
                success = self._process_verse(ref, yaml_file)

                if not success:
                    self.logger.log_warning(f"Failed to process {ref}, continuing...")
                    # Continue with other verses even if one fails

            # Check if any verses completed
            state = self.state_mgr.load()
            completed = sum(1 for v in state['verses'] if v['status'] == 'complete')

            if completed == 0:
                self.logger.log_error("No verses successfully processed")
                self.state_mgr.update_phase("generate", "failed")
                return False

            # Phase complete
            self.state_mgr.update_phase("generate", "complete")
            self.logger.log_phase("generate", "Complete")
            self.logger.log_summary(
                f"Generated {completed}/{len(self.TEST_VERSES)} verses successfully"
            )

            return True

        except Exception as e:
            self.logger.log_error(str(e), "Generate phase")
            self.state_mgr.add_error(str(e), "Generate phase")
            self.state_mgr.update_phase("generate", "failed")
            return False

    def phase_pause_for_review(self) -> None:
        """
        Phase 3: Pause for human review.

        Presents summary and waits for human decision.
        """
        self.logger.log_phase("review", "Awaiting human input")
        self.state_mgr.update_phase("review", "pending")

        state = self.state_mgr.load()
        status = self.state_mgr.get_status()

        print("\n" + "=" * 60)
        print("PHASE 1 MVP COMPLETE - HUMAN REVIEW REQUIRED")
        print("=" * 60)
        print(f"\nTool: {self.tool_name}")
        print(f"Experiment: {self.experiment}")
        print(f"Status: {status['status']}")
        print(f"\nVerses processed: {status['verses']['completed']}/{status['verses']['total']}")
        print(f"Errors: {status['errors']}")
        print(f"Warnings: {status['warnings']}")
        print(f"\nOutput location: {self.base_path}")
        print(f"\nFiles to review:")
        for verse in state['verses']:
            if verse['status'] == 'complete':
                print(f"  - {verse['yaml_file']}")

        print("\n" + "-" * 60)
        print("HUMAN REVIEW TASKS:")
        print("1. Review the 3 generated YAML files")
        print("2. Evaluate:")
        print("   - Are insights useful and accurate?")
        print("   - Does the schema work well?")
        print("   - Any hallucinations detected?")
        print("3. Decide:")
        print("   - CONTINUE: Generate 7 more verses")
        print("   - ITERATE: Refine schema, regenerate")
        print("   - ABANDON: Tool concept not viable")
        print("-" * 60)

        self.logger.log_action("Paused for human review")

    def _process_verse(self, reference: str, yaml_file: Path) -> bool:
        """
        Process a single verse.

        Args:
            reference: Verse reference (e.g., "John 1:1")
            yaml_file: Path to output YAML file

        Returns:
            True if successful
        """
        start_time = time.time()

        self.logger.log_verse_start(reference)
        self.state_mgr.start_verse(reference)

        try:
            # NOTE: In Phase 1 MVP, we create a placeholder YAML
            # In full implementation, this would:
            # 1. Load schema from rev1/README.md
            # 2. Do web searches for factual data
            # 3. Generate comprehensive YAML using LLM
            # 4. Include proper citations

            # For now, create valid minimal YAML as proof of concept
            yaml_content = self._generate_placeholder_yaml(reference)

            # Ensure parent directory exists
            yaml_file.parent.mkdir(parents=True, exist_ok=True)

            # Write YAML
            yaml_file.write_text(yaml_content)

            # Validate
            validation_results = self.validator.run_all_verse_validations(yaml_file)

            all_passed = True
            for check_name, passed, error in validation_results:
                self.logger.log_validation(f"{reference} - {check_name}", passed, error)
                if not passed:
                    all_passed = False

            if not all_passed:
                self.state_mgr.fail_verse(reference, "Validation failed")
                return False

            # Count lines and citations
            lines = len(yaml_content.split('\n'))
            citations = yaml_content.count('{')

            duration = time.time() - start_time

            self.state_mgr.complete_verse(reference)
            self.logger.log_verse_complete(
                reference,
                yaml_file.name,
                lines,
                citations,
                duration
            )

            return True

        except Exception as e:
            error_msg = str(e)
            self.logger.log_verse_error(reference, error_msg)
            self.state_mgr.fail_verse(reference, error_msg)
            return False

    def _generate_placeholder_yaml(self, reference: str) -> str:
        """
        Generate placeholder YAML for testing.

        In full implementation, this would be replaced with
        actual LLM-powered generation.

        Args:
            reference: Verse reference

        Returns:
            YAML content string
        """
        # Parse reference
        parts = reference.replace(":", " ").split()
        book_name = parts[0]

        # Convert to standard format
        book_map = {"John": "JHN", "Matthew": "MAT", "Job": "JOB"}
        book_code = book_map.get(book_name, "UNK")
        chapter = int(parts[1])
        verse = int(parts[2])

        verse_ref = f"{book_code}.{chapter:03d}.{verse:03d}"

        return f"""verse: {verse_ref}

# Placeholder YAML for Phase 1 MVP Testing
# This demonstrates valid structure following SCHEMA.md

source:
  language: GRC
  text: "[Greek text would be here] {{{{grc-NA28-1993}}}}"

# Note: In full implementation, this would include:
# - Actual source language text from web search
# - Word-level analysis
# - Translation patterns
# - Theological insights
# - Cross-references
# - All with proper citations

analysis:
  note: |
    This is a placeholder generated by Phase 1 MVP to demonstrate
    the tool creation workflow. Full implementation would include
    comprehensive analysis using LLM and web search. {{{{llm-cs45}}}}

metadata:
  generated_by: "bible-tool-creator-agent"
  phase: "mvp"
  tool: "{self.tool_name}"
  experiment: "{self.experiment}"
  timestamp: "2025-10-28"
  citations:
    - "{{{{grc-NA28-1993}}}}"
    - "{{{{llm-cs45}}}}"
"""

    def _generate_readme_template(self) -> None:
        """Generate README.md template."""
        content = f"""# {self._title_case(self.tool_name)}

## Why This Tool Exists

{self.purpose}

This tool exists to provide insights that help translators, pastors, and students
understand biblical text more deeply and accurately.

## How It Works

This tool analyzes each verse by:
1. [Process step 1]
2. [Process step 2]
3. [Process step 3]

The output follows the semi-structured format defined in SCHEMA.md.

## Examples of Insights

### Example 1: [Verse Reference]

[5-line description of an incredible insight, what it was, and why it's important]

### Example 2: [Verse Reference]

[5-line description of an incredible insight]

### Example 3: [Verse Reference]

[5-line description of an incredible insight]

### Example 4: [Verse Reference]

[5-line description]

### Example 5: [Verse Reference]

[5-line description]

### Example 6: [Verse Reference]

[5-line description]

### Example 7: [Verse Reference]

[5-line description]

## Schema Reference

This tool generates YAML files following the structure defined in SCHEMA.md.

See `learnings-{self.experiment}/rev1/README.md` for the specific schema used.

## Output Location

```
./bible/{self.tool_name}/[book]/[chapter]/[verse]/
```

## How to Use

[Instructions for using this tool's outputs]

---

Generated by Bible Tool Creator Agent (Phase 1 MVP)
"""
        (self.base_path / "README.md").write_text(content)

    def _generate_learnings_template(self) -> None:
        """Generate LEARNINGS.md template."""
        content = f"""# Learnings: {self._title_case(self.tool_name)}

## Experiment: {self.experiment}

### Thesis/Goal

[What we're trying to learn or accomplish with this experiment]

### What Worked Well

- [Technique, website, or approach that was effective]
- [Another successful element]

### What Worked Poorly

- [What didn't work or caused problems]
- [Challenges encountered]

### Key Insights

[Synthesized learnings from all revisions]

### Helpful Resources

- [Websites that provided good data]
- [Tools or techniques that helped]

### Schema Evolution

#### Revision 1
- Initial schema in `learnings-{self.experiment}/rev1/README.md`
- [What fields were included and why]

### Prompt Engineering Lessons

- [What prompting strategies worked well]
- [What to avoid]

### Stellar Insights

Best examples added to README.md:
1. [Verse] - [Why this insight was exceptional]

---

Generated by Bible Tool Creator Agent
"""
        (self.base_path / "LEARNINGS.md").write_text(content)

    def _generate_schema_template(self) -> None:
        """Generate rev1/README.md with schema."""
        content = f"""# Schema: {self._title_case(self.tool_name)} - Revision 1

## Tool Purpose

{self.purpose}

## YAML Schema

This tool generates YAML files with the following structure:

```yaml
verse: BOOK.CCC.VVV  # Required, zero-padded

source:
  language: [GRC|HEB]  # Original language code
  text: "[Text]" {{source-id}}  # With citation

# Add tool-specific fields here following SCHEMA.md standards
# Examples:
# - words: Word-level analysis
# - clusters: Semantic groupings
# - translations: Translation patterns
# - theological: Theological insights
# - cross_refs: Related verses

# All content must include inline citations {{source-id}}
```

## Field Descriptions

### Required Fields

- `verse`: Verse reference in format BOOK.CCC.VVV (per STANDARDIZATION.md)

### Optional Fields

[Describe the specific fields this tool generates]

## Citation Format

Per SCHEMA.md, all content uses inline citation:
- `{{grc-NA28-1993}}` - Greek Nestle-Aland 28th edition
- `{{heb-BHS-1997}}` - Hebrew Biblia Hebraica Stuttgartensia
- `{{llm-cs45}}` - LLM analysis (Claude Sonnet 4.5)
- `{{eng-NIV-2011}}` - English NIV 2011
- `{{manual}}` - Human curation

## Output Example

```yaml
verse: JHN.001.001

source:
  language: GRC
  text: "Ἐν ἀρχῇ ἦν ὁ λόγος" {{grc-NA28-1993}}

analysis:
  insight: "Key insight here" {{llm-cs45}}
```

---

**Revision:** 1
**Experiment:** {self.experiment}
**Created:** 2025-10-28
"""
        (self.rev_path / "README.md").write_text(content)

    def _title_case(self, kebab_str: str) -> str:
        """Convert kebab-case to Title Case."""
        return " ".join(word.capitalize() for word in kebab_str.split("-"))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bible Study Tool Creator Agent - Phase 1 MVP"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Tool name in kebab-case (e.g., word-frequency-analysis)"
    )
    parser.add_argument(
        "--purpose",
        required=True,
        help="Purpose/description of the tool"
    )
    parser.add_argument(
        "--experiment",
        default="initial-experiment",
        help="Experiment name (default: initial-experiment)"
    )

    args = parser.parse_args()

    # Create and run agent
    creator = BibleToolCreator(args.name, args.purpose, args.experiment)
    success = creator.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
