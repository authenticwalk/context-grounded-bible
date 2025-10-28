"""
Analyze and compare AI model Bible quote results against baseline.

Calculates various accuracy metrics including:
- Exact match
- Similarity score (using SequenceMatcher)
- Word Error Rate (WER)
- Character Error Rate (CER)
- Levenshtein distance
"""

import sys
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from difflib import SequenceMatcher

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from database import BibleQuoteDatabase


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison.

    - Convert to lowercase
    - Remove extra whitespace
    - Remove common punctuation variations
    - Strip leading/trailing whitespace
    """
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Normalize quotes and apostrophes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Strip
    text = text.strip()

    return text


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity ratio between two texts using SequenceMatcher.

    Returns:
        Float between 0.0 and 1.0, where 1.0 is identical
    """
    if not text1 or not text2:
        return 0.0

    return SequenceMatcher(None, text1, text2).ratio()


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate Levenshtein distance between two strings.

    Returns:
        Number of single-character edits needed to transform s1 into s2
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def word_error_rate(reference: str, hypothesis: str) -> float:
    """
    Calculate Word Error Rate (WER).

    WER = (Substitutions + Deletions + Insertions) / Total Words in Reference

    Returns:
        Float representing error rate (0.0 = perfect, higher = more errors)
    """
    if not reference:
        return 1.0 if hypothesis else 0.0

    ref_words = reference.split()
    hyp_words = hypothesis.split()

    # Use dynamic programming to calculate edit distance at word level
    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]

    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j

    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(ref_words)][len(hyp_words)] / len(ref_words)


def character_error_rate(reference: str, hypothesis: str) -> float:
    """
    Calculate Character Error Rate (CER).

    CER = Levenshtein Distance / Length of Reference

    Returns:
        Float representing error rate (0.0 = perfect, higher = more errors)
    """
    if not reference:
        return 1.0 if hypothesis else 0.0

    distance = levenshtein_distance(reference, hypothesis)
    return distance / len(reference)


def analyze_quote_pair(baseline: Optional[str], model_quote: Optional[str]) -> Dict[str, Any]:
    """
    Analyze a pair of quotes (baseline vs model output).

    Args:
        baseline: The correct/reference quote
        model_quote: The model's quote

    Returns:
        Dictionary containing various metrics
    """
    # Handle missing quotes
    if not baseline or not model_quote:
        return {
            "exact_match": False,
            "similarity_score": 0.0,
            "word_error_rate": 1.0,
            "character_error_rate": 1.0,
            "levenshtein_distance": -1,
            "notes": "Missing baseline or model quote"
        }

    # Normalize for comparison
    norm_baseline = normalize_text(baseline)
    norm_model = normalize_text(model_quote)

    # Calculate metrics
    exact_match = (norm_baseline == norm_model)
    similarity = calculate_similarity(norm_baseline, norm_model)
    wer = word_error_rate(norm_baseline, norm_model)
    cer = character_error_rate(norm_baseline, norm_model)
    lev_dist = levenshtein_distance(norm_baseline, norm_model)

    # Generate notes
    notes = []
    if exact_match:
        notes.append("Perfect match")
    elif similarity >= 0.95:
        notes.append("Near perfect match")
    elif similarity >= 0.80:
        notes.append("High similarity")
    elif similarity >= 0.60:
        notes.append("Moderate similarity")
    elif similarity >= 0.40:
        notes.append("Low similarity")
    else:
        notes.append("Very low similarity")

    if wer > 0.5:
        notes.append("High word error rate")
    if cer > 0.3:
        notes.append("High character error rate")

    return {
        "exact_match": exact_match,
        "similarity_score": similarity,
        "word_error_rate": wer,
        "character_error_rate": cer,
        "levenshtein_distance": lev_dist,
        "notes": "; ".join(notes)
    }


def analyze_all_results(db: BibleQuoteDatabase):
    """
    Analyze all model quotes against baseline quotes.

    This compares every model quote with its corresponding baseline
    and stores the analysis results.
    """
    print("\n" + "=" * 60)
    print("Analyzing Results")
    print("=" * 60)

    # Get all model quotes
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT
            mq.id as model_quote_id,
            mq.model_id,
            mq.verse_id,
            mq.version_id,
            mq.quote_text as model_text,
            mq.success as model_success,
            bq.id as baseline_quote_id,
            bq.quote_text as baseline_text,
            bq.success as baseline_success,
            v.reference as verse_ref,
            bv.code as version_code,
            m.model_name
        FROM model_quotes mq
        JOIN verses v ON mq.verse_id = v.id
        JOIN bible_versions bv ON mq.version_id = bv.id
        JOIN ai_models m ON mq.model_id = m.id
        LEFT JOIN baseline_quotes bq ON mq.verse_id = bq.verse_id AND mq.version_id = bq.version_id
    """)

    model_quotes = cursor.fetchall()
    total = len(model_quotes)

    print(f"\nAnalyzing {total:,} model quotes...")

    analyzed = 0
    perfect_matches = 0
    high_quality = 0  # similarity >= 0.9
    missing_baseline = 0

    for row in model_quotes:
        row_dict = dict(row)

        # Check if baseline exists
        if not row_dict['baseline_text']:
            missing_baseline += 1
            # Still analyze, but note the missing baseline
            metrics = analyze_quote_pair(None, row_dict['model_text'])
            baseline_id = None
        else:
            metrics = analyze_quote_pair(
                row_dict['baseline_text'],
                row_dict['model_text']
            )
            baseline_id = row_dict['baseline_quote_id']

        # Store analysis
        db.insert_analysis_result(
            model_id=row_dict['model_id'],
            verse_id=row_dict['verse_id'],
            version_id=row_dict['version_id'],
            baseline_quote_id=baseline_id,
            model_quote_id=row_dict['model_quote_id'],
            exact_match=metrics['exact_match'],
            similarity_score=metrics['similarity_score'],
            word_error_rate=metrics['word_error_rate'],
            character_error_rate=metrics['character_error_rate'],
            levenshtein_distance=metrics['levenshtein_distance'],
            notes=metrics['notes']
        )

        # Track stats
        if metrics['exact_match']:
            perfect_matches += 1
        if metrics['similarity_score'] >= 0.9:
            high_quality += 1

        analyzed += 1

        # Progress indicator
        if analyzed % 100 == 0:
            print(f"  Progress: {analyzed:,}/{total:,} ({analyzed/total*100:.1f}%)")

    print(f"\n✓ Analysis complete!")
    print(f"\nResults Summary:")
    print(f"  Total analyzed: {analyzed:,}")
    print(f"  Perfect matches: {perfect_matches:,} ({perfect_matches/analyzed*100:.1f}%)")
    print(f"  High quality (≥90% similarity): {high_quality:,} ({high_quality/analyzed*100:.1f}%)")
    print(f"  Missing baseline: {missing_baseline:,}")


def generate_summary_statistics(db: BibleQuoteDatabase) -> Dict[str, Any]:
    """
    Generate summary statistics from analysis results.

    Returns:
        Dictionary with overall statistics
    """
    cursor = db.conn.cursor()

    stats = {}

    # Overall stats
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN exact_match = 1 THEN 1 ELSE 0 END) as exact_matches,
            AVG(similarity_score) as avg_similarity,
            AVG(word_error_rate) as avg_wer,
            AVG(character_error_rate) as avg_cer
        FROM analysis_results
    """)
    overall = dict(cursor.fetchone())
    stats['overall'] = overall

    # Per model stats
    cursor.execute("""
        SELECT
            m.model_name,
            m.provider,
            m.tier,
            COUNT(*) as total,
            SUM(CASE WHEN ar.exact_match = 1 THEN 1 ELSE 0 END) as exact_matches,
            AVG(ar.similarity_score) as avg_similarity,
            AVG(ar.word_error_rate) as avg_wer,
            AVG(ar.character_error_rate) as avg_cer
        FROM analysis_results ar
        JOIN ai_models m ON ar.model_id = m.id
        GROUP BY ar.model_id
        ORDER BY avg_similarity DESC
    """)
    stats['by_model'] = [dict(row) for row in cursor.fetchall()]

    # Per language stats
    cursor.execute("""
        SELECT
            bv.language,
            COUNT(*) as total,
            SUM(CASE WHEN ar.exact_match = 1 THEN 1 ELSE 0 END) as exact_matches,
            AVG(ar.similarity_score) as avg_similarity,
            AVG(ar.word_error_rate) as avg_wer
        FROM analysis_results ar
        JOIN bible_versions bv ON ar.version_id = bv.id
        GROUP BY bv.language
        ORDER BY avg_similarity DESC
    """)
    stats['by_language'] = [dict(row) for row in cursor.fetchall()]

    # Per difficulty stats
    cursor.execute("""
        SELECT
            v.difficulty_score,
            COUNT(*) as total,
            SUM(CASE WHEN ar.exact_match = 1 THEN 1 ELSE 0 END) as exact_matches,
            AVG(ar.similarity_score) as avg_similarity
        FROM analysis_results ar
        JOIN verses v ON ar.verse_id = v.id
        GROUP BY v.difficulty_score
        ORDER BY v.difficulty_score
    """)
    stats['by_difficulty'] = [dict(row) for row in cursor.fetchall()]

    return stats


def main():
    """Main function to analyze all results."""
    print("=" * 60)
    print("Bible Quote Accuracy Test - Analysis")
    print("=" * 60)

    # Initialize database
    db_path = Path(__file__).parent / "bible_quote_accuracy.db"
    print(f"\nDatabase: {db_path}")

    if not db_path.exists():
        print("\n❌ Error: Database not found!")
        print("Please run test_models.py first to collect data.")
        sys.exit(1)

    with BibleQuoteDatabase(str(db_path)) as db:
        # Check if we have data
        stats = db.get_statistics()
        if stats['total_model_quotes'] == 0:
            print("\n❌ Error: No model quotes found in database!")
            print("Please run test_models.py first to collect data.")
            sys.exit(1)

        print(f"\nFound {stats['total_model_quotes']:,} model quotes to analyze")

        # Analyze all results
        analyze_all_results(db)

        # Generate summary statistics
        print("\n" + "=" * 60)
        print("Generating Summary Statistics")
        print("=" * 60)

        summary = generate_summary_statistics(db)

        print("\nOverall Performance:")
        print(f"  Total: {summary['overall']['total']:,}")
        print(f"  Exact matches: {summary['overall']['exact_matches']:,} ({summary['overall']['exact_matches']/summary['overall']['total']*100:.1f}%)")
        print(f"  Average similarity: {summary['overall']['avg_similarity']:.3f}")
        print(f"  Average WER: {summary['overall']['avg_wer']:.3f}")
        print(f"  Average CER: {summary['overall']['avg_cer']:.3f}")

        print("\nTop 5 Models by Similarity:")
        for i, model in enumerate(summary['by_model'][:5], 1):
            print(f"  {i}. {model['model_name']:.<40} {model['avg_similarity']:.3f}")

        print("\nTop Languages by Similarity:")
        for i, lang in enumerate(summary['by_language'][:10], 1):
            print(f"  {i}. {lang['language']:.<20} {lang['avg_similarity']:.3f}")

    print("\n✓ Analysis completed")
    print("\nNext step: Run the report generation script")


if __name__ == "__main__":
    main()
