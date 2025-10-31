"""
TBTA Review Integration

Utilities for integrating review metadata into TBTA annotations.
"""

from typing import Dict, Any, Optional, List
import yaml
from pathlib import Path

from .confidence_scorer import calculate_confidence
from .review_metadata import create_review_metadata, create_review_summary


def annotate_field_with_review(
    field_name: str,
    field_value: Any,
    context: Optional[Dict[str, Any]] = None,
    review_threshold: float = 0.95
) -> Dict[str, Any]:
    """
    Annotate a single field with review metadata.

    Args:
        field_name: Name of the TBTA field
        field_value: Value of the field
        context: Optional context dictionary
        review_threshold: Confidence threshold for review

    Returns:
        Dictionary with field value and review metadata
    """
    # Calculate confidence
    confidence = calculate_confidence(field_name, field_value, context)

    # Create review metadata
    metadata = create_review_metadata(
        field_name=field_name,
        field_value=field_value,
        confidence=confidence,
        context=context,
        review_threshold=review_threshold
    )

    # Return field with metadata
    result = {field_name: field_value}
    result.update(metadata)

    return result


def annotate_structure_with_review(
    structure: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
    review_threshold: float = 0.95,
    skip_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Recursively annotate a TBTA structure with review metadata.

    Args:
        structure: TBTA structure (clause, phrase, word)
        context: Optional context dictionary
        review_threshold: Confidence threshold for review
        skip_fields: Fields to skip (e.g., structural fields like 'children')

    Returns:
        Annotated structure with review metadata
    """
    skip_fields = skip_fields or ["children", "clauses", "verse", "source", "version"]
    context = context or {}

    result = {}

    for key, value in structure.items():
        # Skip structural fields
        if key in skip_fields:
            if key == "children" and isinstance(value, list):
                # Recursively process children
                result[key] = [
                    annotate_structure_with_review(child, context, review_threshold, skip_fields)
                    if isinstance(child, dict)
                    else child
                    for child in value
                ]
            elif key == "clauses" and isinstance(value, list):
                # Recursively process clauses
                result[key] = [
                    annotate_structure_with_review(clause, context, review_threshold, skip_fields)
                    if isinstance(clause, dict)
                    else clause
                    for clause in value
                ]
            else:
                result[key] = value
        elif isinstance(value, (dict, list)):
            # Nested structure, don't annotate
            result[key] = value
        else:
            # Leaf field, annotate with review metadata
            confidence = calculate_confidence(key, value, context)
            metadata = create_review_metadata(
                field_name=key,
                field_value=value,
                confidence=confidence,
                context=context,
                review_threshold=review_threshold
            )

            # Add field value
            result[key] = value

            # Add review metadata
            for meta_key, meta_value in metadata.items():
                if meta_key != "confidence" or meta_value is not None:
                    result[f"_{meta_key}"] = meta_value  # Prefix with _ to distinguish

    return result


def load_tbta_file(filepath: Path) -> Dict[str, Any]:
    """Load a TBTA YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_annotated_tbta(annotations: Dict[str, Any], output_path: Path):
    """Save annotated TBTA to YAML file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(annotations, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def generate_review_report(annotations: Dict[str, Any]) -> str:
    """
    Generate a human-readable review report.

    Args:
        annotations: TBTA annotations with review metadata

    Returns:
        Formatted report string
    """
    summary = create_review_summary(annotations)

    report = []
    report.append("=" * 70)
    report.append("TBTA REVIEW REPORT")
    report.append("=" * 70)
    report.append(f"Verse: {annotations.get('verse', 'N/A')}")
    report.append("")
    report.append(f"Total Fields Annotated: {summary['total_fields']}")
    report.append(f"High Confidence (≥95%): {summary['high_confidence']} ({summary['high_confidence']/summary['total_fields']*100:.1f}%)" if summary['total_fields'] > 0 else "")
    report.append(f"Needs Review (<95%):    {summary['needs_review']} ({summary['needs_review']/summary['total_fields']*100:.1f}%)" if summary['total_fields'] > 0 else "")
    report.append("")
    report.append("Review Status:")
    report.append(f"  - Pending:   {summary['pending_reviews']}")
    report.append(f"  - Approved:  {summary['approved_reviews']}")
    report.append(f"  - Corrected: {summary['corrected_reviews']}")
    report.append(f"  - Rejected:  {summary['rejected_reviews']}")
    report.append("")

    if summary['review_breakdown']:
        report.append("Review Reasons:")
        for reason, count in sorted(summary['review_breakdown'].items(), key=lambda x: x[1], reverse=True):
            report.append(f"  - {reason}: {count}")
        report.append("")

    report.append("-" * 70)

    # Find and list items needing review
    def find_review_items(node, path=""):
        """Recursively find items needing review."""
        items = []

        if isinstance(node, dict):
            if node.get("_needs_review"):
                items.append({
                    "path": path,
                    "field": path.split(".")[-1] if "." in path else path,
                    "value": node.get(path.split(".")[-1]),
                    "confidence": node.get("_confidence"),
                    "reason": node.get("_review_reason"),
                    "notes": node.get("_review_notes")
                })

            for key, value in node.items():
                if not key.startswith("_"):
                    new_path = f"{path}.{key}" if path else key
                    items.extend(find_review_items(value, new_path))

        elif isinstance(node, list):
            for i, item in enumerate(node):
                new_path = f"{path}[{i}]"
                items.extend(find_review_items(item, new_path))

        return items

    review_items = find_review_items(annotations)

    if review_items:
        report.append(f"Items Needing Review ({len(review_items)}):")
        report.append("")

        for i, item in enumerate(review_items, 1):
            report.append(f"{i}. {item['field']} = {item['value']}")
            report.append(f"   Confidence: {item['confidence']}")
            report.append(f"   Reason: {item['reason']}")
            if item['notes']:
                # Wrap long notes
                notes_lines = item['notes'].split(". ")
                for line in notes_lines:
                    report.append(f"   Note: {line.strip()}")
            report.append("")

    report.append("=" * 70)

    return "\n".join(report)


def extract_review_items(annotations: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract all items needing review as a flat list.

    Args:
        annotations: TBTA annotations with review metadata

    Returns:
        List of review items
    """
    items = []

    def extract_from_node(node, path=""):
        """Recursively extract review items."""
        if isinstance(node, dict):
            current_item = {}
            needs_review = False

            for key, value in node.items():
                if key.startswith("_"):
                    # Review metadata
                    if key == "_needs_review" and value:
                        needs_review = True
                    current_item[key[1:]] = value  # Remove _ prefix
                elif not isinstance(value, (dict, list)):
                    # Field value
                    current_item["field_name"] = key
                    current_item["field_value"] = value

            if needs_review and "field_name" in current_item:
                current_item["path"] = path
                items.append(current_item)

            # Recurse into children
            for key, value in node.items():
                if not key.startswith("_"):
                    new_path = f"{path}.{key}" if path else key
                    extract_from_node(value, new_path)

        elif isinstance(node, list):
            for i, item in enumerate(node):
                new_path = f"{path}[{i}]"
                extract_from_node(item, new_path)

    extract_from_node(annotations)
    return items


# Example usage
if __name__ == "__main__":
    # Example: Annotate a simple TBTA structure
    example_structure = {
        "Part": "Noun",
        "Constituent": "God",
        "Number": "Trial",
        "Person": "First Inclusive",
        "NounListIndex": "1",
        "Participant Tracking": "Routine"
    }

    context = {
        "verse_ref": "GEN.001.026",
        "theological_content": True,
        "entity_count": 3
    }

    print("Example: Annotating TBTA structure with review metadata")
    print("=" * 70)
    print("\nOriginal Structure:")
    print(yaml.dump(example_structure, default_flow_style=False))

    annotated = annotate_structure_with_review(example_structure, context)

    print("\nAnnotated Structure:")
    print(yaml.dump(annotated, default_flow_style=False))

    print("\nReview Items:")
    review_items = extract_review_items({"data": annotated})
    for item in review_items:
        print(f"\n{item['field_name']} = {item['field_value']}")
        print(f"  Confidence: {item['confidence']}")
        print(f"  Reason: {item['review_reason']}")
        print(f"  Notes: {item['review_notes'][:100]}..." if len(item['review_notes']) > 100 else f"  Notes: {item['review_notes']}")
