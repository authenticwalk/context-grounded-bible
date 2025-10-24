#!/usr/bin/env python3
"""
Initialize a new bible study tool with complete file structure.
This script is called by the bible-study-tool-creator skill.
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime


def replace_placeholders(content, replacements):
    """Replace all {{PLACEHOLDER}} tags with actual values."""
    for key, value in replacements.items():
        placeholder = f"{{{{{key}}}}}"
        content = content.replace(placeholder, str(value))
    return content


def load_template(template_path):
    """Load a template file."""
    with open(template_path, 'r') as f:
        return f.read()


def create_tool_structure(tool_data, base_dir="/Users/chrispriebe/projects/context-grounded-bible"):
    """Create the complete directory and file structure for a new tool."""

    tool_name_kebab = tool_data['tool_name_kebab']
    tool_dir = Path(base_dir) / "bible-study-tools" / tool_name_kebab
    skill_dir = Path(base_dir) / ".claude/skills/bible-study-tool-creator"

    # Create main tool directory
    tool_dir.mkdir(parents=True, exist_ok=True)

    # Create tests directory
    tests_dir = tool_dir / "tests"
    tests_dir.mkdir(exist_ok=True)

    # Prepare replacement dictionary
    replacements = {
        'TOOL_NAME': tool_data['tool_name'],
        'TOOL_NAME_KEBAB': tool_name_kebab,
        'DESCRIPTION': tool_data['description'],
        'TASK_NAME': tool_data['task_name'],
        'GOALS': tool_data['goals_formatted'],
        'EXAMPLES': tool_data['examples_formatted'],
        'RELATED_TOOLS': tool_data.get('related_tools', 'None'),
        'DATA_STRUCTURE': tool_data['data_structure'],
        'STATUS': 'Initial - Self-learning loop not started',
        'DATE': datetime.now().strftime('%Y-%m-%d'),
        'TEST_VERSE': tool_data.get('test_verse', 'MAT 5:3'),
        'RELATED_TOOLS_LEARNINGS': tool_data.get('related_tools_learnings', 'No related tools identified yet.'),
        'SPECIFIC_AREA': tool_data.get('specific_area', 'various aspects'),
        'CUSTOM_EXPERIMENT_1': 'Test with different literary genres (poetry vs prose)',
        'CUSTOM_EXPERIMENT_2': 'Validate against expert commentary',
        'QUESTION_1': 'What additional data sources would improve accuracy?',
        'QUESTION_2': 'How can we measure practical impact on translators?',
        'QUESTION_3': 'What edge cases need special handling?',
        'TEST_CASES_LIST': 'No test cases yet. Start with the initial test verse.',
        'TASK_DESCRIPTION': tool_data['description'],
        'OBJECTIVES': tool_data['goals_formatted'],
        'SPECIFIC_INSTRUCTIONS': tool_data.get('specific_instructions', 'Follow the guidelines above and produce high-quality output.'),
        'YAML_STRUCTURE': tool_data['yaml_structure_inline'],
        'FIELD_DEFINITIONS': tool_data.get('field_definitions', '(To be defined based on YAML structure)'),
        'CUSTOM_QUALITY_CHECK_1': 'Output addresses all stated goals',
        'CUSTOM_QUALITY_CHECK_2': 'Examples are concrete and verifiable',
        'EXAMPLE_OUTPUT': tool_data.get('example_output', '(Example to be added)'),
    }

    # Create README.md
    readme_template = load_template(skill_dir / "templates/README.template.md")
    readme_content = replace_placeholders(readme_template, replacements)
    with open(tool_dir / "README.md", 'w') as f:
        f.write(readme_content)

    # Create LEARNING.md
    learning_template = load_template(skill_dir / "templates/LEARNING.template.md")
    learning_content = replace_placeholders(learning_template, replacements)
    with open(tool_dir / "LEARNING.md", 'w') as f:
        f.write(learning_content)

    # Create tool template
    tool_template = load_template(skill_dir / "templates/tool-template.template.md")
    tool_content = replace_placeholders(tool_template, replacements)
    with open(tool_dir / f"{tool_name_kebab}-template.md", 'w') as f:
        f.write(tool_content)

    # Create tests README
    tests_readme_template = load_template(skill_dir / "templates/tests-README.template.md")
    tests_readme_content = replace_placeholders(tests_readme_template, replacements)
    with open(tests_dir / "README.md", 'w') as f:
        f.write(tests_readme_content)

    return tool_dir


def parse_user_input(input_file):
    """Parse the filled-out user input template."""
    with open(input_file, 'r') as f:
        content = f.read()

    # This is a simplified parser - in practice, you'd want more robust parsing
    # For now, we'll expect the data to be passed as a YAML file

    # TODO: Implement proper markdown parsing or switch to YAML input
    raise NotImplementedError("Parser needs to be implemented based on user input format")


def main():
    if len(sys.argv) < 2:
        print("Usage: python init-tool.py <tool-definition.yaml>")
        print("\nOr use interactively with the bible-study-tool-creator skill")
        sys.exit(1)

    input_file = sys.argv[1]

    # Load tool definition
    with open(input_file, 'r') as f:
        tool_data = yaml.safe_load(f)

    # Create tool structure
    tool_dir = create_tool_structure(tool_data)

    print(f"✅ Successfully created bible study tool at: {tool_dir}")
    print(f"\nNext steps:")
    print(f"1. Review generated files in {tool_dir}")
    print(f"2. Customize {tool_data['tool_name_kebab']}-template.md with specific instructions")
    print(f"3. Run first test: claude 'Using {tool_data['tool_name_kebab']}-template.md, process {tool_data.get('test_verse', 'MAT 5:3')}'")
    print(f"4. Analyze output and update LEARNING.md")
    print(f"5. Iterate until quality is excellent")


if __name__ == "__main__":
    main()
