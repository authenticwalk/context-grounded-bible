"""
Generate comprehensive markdown report on Bible quote accuracy across models and languages.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from database import BibleQuoteDatabase


def format_percentage(value: float, total: float) -> str:
    """Format a value as a percentage of total."""
    if total == 0:
        return "0.0%"
    return f"{(value / total * 100):.1f}%"


def generate_executive_summary(db: BibleQuoteDatabase) -> str:
    """Generate executive summary section."""
    cursor = db.conn.cursor()

    # Get overall stats
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

    # Get best and worst models
    cursor.execute("""
        SELECT m.model_name, AVG(ar.similarity_score) as avg_sim
        FROM analysis_results ar
        JOIN ai_models m ON ar.model_id = m.id
        GROUP BY ar.model_id
        ORDER BY avg_sim DESC
        LIMIT 1
    """)
    best_model = dict(cursor.fetchone())

    cursor.execute("""
        SELECT m.model_name, AVG(ar.similarity_score) as avg_sim
        FROM analysis_results ar
        JOIN ai_models m ON ar.model_id = m.id
        GROUP BY ar.model_id
        ORDER BY avg_sim ASC
        LIMIT 1
    """)
    worst_model = dict(cursor.fetchone())

    # Get language coverage
    cursor.execute("SELECT COUNT(DISTINCT language) FROM bible_versions")
    num_languages = cursor.fetchone()[0]

    summary = f"""## Executive Summary

This report presents a comprehensive analysis of AI models' ability to accurately quote Bible verses across multiple languages and translations.

### Key Findings

- **Total Tests Conducted**: {overall['total']:,}
- **Overall Accuracy**: {overall['avg_similarity']:.1%} average similarity score
- **Exact Matches**: {overall['exact_matches']:,} ({format_percentage(overall['exact_matches'], overall['total'])})
- **Languages Tested**: {num_languages}
- **Best Performing Model**: {best_model['model_name']} ({best_model['avg_sim']:.1%})
- **Lowest Performing Model**: {worst_model['model_name']} ({worst_model['avg_sim']:.1%})

### Metrics Overview

- **Average Word Error Rate (WER)**: {overall['avg_wer']:.3f}
- **Average Character Error Rate (CER)**: {overall['avg_cer']:.3f}
- **Average Similarity Score**: {overall['avg_similarity']:.3f}

"""
    return summary


def generate_model_comparison(db: BibleQuoteDatabase) -> str:
    """Generate model comparison section."""
    cursor = db.conn.cursor()

    cursor.execute("""
        SELECT
            m.model_name,
            m.provider,
            m.tier,
            COUNT(*) as total_tests,
            SUM(CASE WHEN ar.exact_match = 1 THEN 1 ELSE 0 END) as exact_matches,
            AVG(ar.similarity_score) as avg_similarity,
            AVG(ar.word_error_rate) as avg_wer,
            AVG(ar.character_error_rate) as avg_cer,
            AVG(CASE WHEN mq.response_time_ms IS NOT NULL THEN mq.response_time_ms ELSE 0 END) as avg_response_time
        FROM analysis_results ar
        JOIN ai_models m ON ar.model_id = m.id
        JOIN model_quotes mq ON ar.model_quote_id = mq.id
        GROUP BY ar.model_id
        ORDER BY avg_similarity DESC
    """)

    models = [dict(row) for row in cursor.fetchall()]

    section = """## Model Performance Comparison

### Overall Model Rankings

The following table shows all tested models ranked by average similarity score:

| Rank | Model | Provider | Tier | Tests | Exact Matches | Avg Similarity | WER | CER | Avg Response Time (ms) |
|------|-------|----------|------|-------|---------------|----------------|-----|-----|------------------------|
"""

    for i, model in enumerate(models, 1):
        section += f"| {i} | {model['model_name']} | {model['provider']} | {model['tier']} | {model['total_tests']:,} | {format_percentage(model['exact_matches'], model['total_tests'])} | {model['avg_similarity']:.3f} | {model['avg_wer']:.3f} | {model['avg_cer']:.3f} | {model['avg_response_time']:.0f} |\n"

    # Add insights
    section += "\n### Key Insights\n\n"

    # Best performer
    best = models[0]
    section += f"- **Top Performer**: {best['model_name']} from {best['provider']} achieved the highest average similarity score of {best['avg_similarity']:.1%}\n"

    # Tier comparison
    cursor.execute("""
        SELECT
            m.tier,
            AVG(ar.similarity_score) as avg_similarity,
            COUNT(*) as count
        FROM analysis_results ar
        JOIN ai_models m ON ar.model_id = m.id
        GROUP BY m.tier
    """)
    tier_stats = {row['tier']: row for row in cursor.fetchall()}

    if 'high' in tier_stats and 'low' in tier_stats:
        high_tier = tier_stats['high']
        low_tier = tier_stats['low']
        diff = high_tier['avg_similarity'] - low_tier['avg_similarity']
        section += f"- **Tier Analysis**: High-tier models averaged {high_tier['avg_similarity']:.1%} similarity vs {low_tier['avg_similarity']:.1%} for low-tier models (difference: {diff:.1%})\n"

    # Provider comparison
    cursor.execute("""
        SELECT
            m.provider,
            AVG(ar.similarity_score) as avg_similarity,
            COUNT(DISTINCT m.id) as num_models
        FROM analysis_results ar
        JOIN ai_models m ON ar.model_id = m.id
        GROUP BY m.provider
        ORDER BY avg_similarity DESC
    """)
    provider_stats = [dict(row) for row in cursor.fetchall()]

    section += f"- **Best Provider**: {provider_stats[0]['provider']} models averaged {provider_stats[0]['avg_similarity']:.1%} similarity\n"

    section += "\n"
    return section


def generate_language_analysis(db: BibleQuoteDatabase) -> str:
    """Generate language analysis section."""
    cursor = db.conn.cursor()

    cursor.execute("""
        SELECT
            bv.language,
            bv.language_family,
            bv.script,
            COUNT(DISTINCT bv.id) as num_versions,
            COUNT(*) as total_tests,
            SUM(CASE WHEN ar.exact_match = 1 THEN 1 ELSE 0 END) as exact_matches,
            AVG(ar.similarity_score) as avg_similarity,
            AVG(ar.word_error_rate) as avg_wer
        FROM analysis_results ar
        JOIN bible_versions bv ON ar.version_id = bv.id
        GROUP BY bv.language
        ORDER BY avg_similarity DESC
    """)

    languages = [dict(row) for row in cursor.fetchall()]

    section = """## Language Coverage Analysis

### Performance by Language

The following table shows model performance across different languages:

| Rank | Language | Script | Family | Versions | Tests | Exact Matches | Avg Similarity | WER |
|------|----------|--------|--------|----------|-------|---------------|----------------|-----|
"""

    for i, lang in enumerate(languages, 1):
        section += f"| {i} | {lang['language']} | {lang['script']} | {lang['language_family']} | {lang['num_versions']} | {lang['total_tests']:,} | {format_percentage(lang['exact_matches'], lang['total_tests'])} | {lang['avg_similarity']:.3f} | {lang['avg_wer']:.3f} |\n"

    section += "\n### Language Insights\n\n"

    # Best and worst languages
    best_lang = languages[0]
    worst_lang = languages[-1]

    section += f"- **Best Performance**: {best_lang['language']} ({best_lang['script']} script) - {best_lang['avg_similarity']:.1%} average similarity\n"
    section += f"- **Most Challenging**: {worst_lang['language']} ({worst_lang['script']} script) - {worst_lang['avg_similarity']:.1%} average similarity\n"

    # Script analysis
    cursor.execute("""
        SELECT
            bv.script,
            AVG(ar.similarity_score) as avg_similarity,
            COUNT(*) as total_tests
        FROM analysis_results ar
        JOIN bible_versions bv ON ar.version_id = bv.id
        GROUP BY bv.script
        HAVING total_tests > 100
        ORDER BY avg_similarity DESC
    """)
    script_stats = [dict(row) for row in cursor.fetchall()]

    if len(script_stats) > 1:
        section += f"- **Script Performance**: {script_stats[0]['script']} script showed highest accuracy ({script_stats[0]['avg_similarity']:.1%})\n"

    section += "\n"
    return section


def generate_verse_difficulty_analysis(db: BibleQuoteDatabase) -> str:
    """Generate verse difficulty analysis section."""
    cursor = db.conn.cursor()

    cursor.execute("""
        SELECT
            v.difficulty_score,
            v.category,
            COUNT(DISTINCT v.id) as num_verses,
            COUNT(*) as total_tests,
            SUM(CASE WHEN ar.exact_match = 1 THEN 1 ELSE 0 END) as exact_matches,
            AVG(ar.similarity_score) as avg_similarity
        FROM analysis_results ar
        JOIN verses v ON ar.verse_id = v.id
        GROUP BY v.difficulty_score
        ORDER BY v.difficulty_score
    """)

    difficulties = [dict(row) for row in cursor.fetchall()]

    section = """## Verse Difficulty Analysis

### Performance by Verse Obscurity

This analysis examines whether models perform differently on well-known versus obscure verses:

| Difficulty | Category | Verses | Tests | Exact Matches | Avg Similarity |
|------------|----------|--------|-------|---------------|----------------|
"""

    for diff in difficulties:
        section += f"| {diff['difficulty_score']} | {diff['category']} | {diff['num_verses']} | {diff['total_tests']:,} | {format_percentage(diff['exact_matches'], diff['total_tests'])} | {diff['avg_similarity']:.3f} |\n"

    section += "\n### Difficulty Insights\n\n"

    # Check if there's a correlation between difficulty and accuracy
    if len(difficulties) >= 2:
        easiest = difficulties[0]
        hardest = difficulties[-1]
        diff_delta = easiest['avg_similarity'] - hardest['avg_similarity']

        section += f"- **Easiest Verses** (Difficulty {easiest['difficulty_score']}): {easiest['avg_similarity']:.1%} average similarity\n"
        section += f"- **Hardest Verses** (Difficulty {hardest['difficulty_score']}): {hardest['avg_similarity']:.1%} average similarity\n"
        section += f"- **Difficulty Impact**: {abs(diff_delta):.1%} {'decrease' if diff_delta > 0 else 'increase'} in accuracy from easiest to hardest verses\n"

    section += "\n"
    return section


def generate_detailed_examples(db: BibleQuoteDatabase) -> str:
    """Generate detailed examples section with best and worst cases."""
    cursor = db.conn.cursor()

    section = """## Detailed Examples

### Best Performances

Examples of perfect or near-perfect quotes:

"""

    # Get best examples
    cursor.execute("""
        SELECT
            v.reference,
            bv.code as version,
            m.model_name,
            bq.quote_text as baseline,
            mq.quote_text as model_quote,
            ar.similarity_score
        FROM analysis_results ar
        JOIN verses v ON ar.verse_id = v.id
        JOIN bible_versions bv ON ar.version_id = bv.id
        JOIN ai_models m ON ar.model_id = m.id
        JOIN baseline_quotes bq ON ar.baseline_quote_id = bq.id
        JOIN model_quotes mq ON ar.model_quote_id = mq.id
        WHERE ar.similarity_score >= 0.99
        ORDER BY ar.similarity_score DESC
        LIMIT 5
    """)

    best_examples = [dict(row) for row in cursor.fetchall()]

    for ex in best_examples:
        section += f"\n**{ex['reference']} ({ex['version']})** - {ex['model_name']} - {ex['similarity_score']:.1%} similarity\n\n"
        if ex['baseline']:
            section += f"- **Baseline**: {ex['baseline'][:200]}{'...' if len(ex['baseline']) > 200 else ''}\n"
        if ex['model_quote']:
            section += f"- **Model**: {ex['model_quote'][:200]}{'...' if len(ex['model_quote']) > 200 else ''}\n"

    section += "\n### Challenging Cases\n\nExamples where models struggled:\n\n"

    # Get worst examples
    cursor.execute("""
        SELECT
            v.reference,
            bv.code as version,
            bv.language,
            m.model_name,
            bq.quote_text as baseline,
            mq.quote_text as model_quote,
            ar.similarity_score,
            ar.notes
        FROM analysis_results ar
        JOIN verses v ON ar.verse_id = v.id
        JOIN bible_versions bv ON ar.version_id = bv.id
        JOIN ai_models m ON ar.model_id = m.id
        LEFT JOIN baseline_quotes bq ON ar.baseline_quote_id = bq.id
        JOIN model_quotes mq ON ar.model_quote_id = mq.id
        WHERE ar.similarity_score < 0.5 AND mq.quote_text IS NOT NULL
        ORDER BY ar.similarity_score ASC
        LIMIT 5
    """)

    worst_examples = [dict(row) for row in cursor.fetchall()]

    for ex in worst_examples:
        section += f"\n**{ex['reference']} ({ex['version']})** - {ex['model_name']} - {ex['similarity_score']:.1%} similarity\n\n"
        section += f"- **Language**: {ex['language']}\n"
        if ex['baseline']:
            section += f"- **Expected**: {ex['baseline'][:200]}{'...' if len(ex['baseline']) > 200 else ''}\n"
        if ex['model_quote']:
            section += f"- **Model Output**: {ex['model_quote'][:200]}{'...' if len(ex['model_quote']) > 200 else ''}\n"
        if ex['notes']:
            section += f"- **Notes**: {ex['notes']}\n"

    section += "\n"
    return section


def generate_methodology(db: BibleQuoteDatabase) -> str:
    """Generate methodology section."""
    stats = db.get_statistics()

    section = f"""## Methodology

### Test Design

This experiment was designed to evaluate AI models' ability to accurately quote Bible verses across multiple languages and translations.

#### Test Parameters

- **Verses Tested**: {stats['total_verses']} verses ranging from well-known (e.g., John 3:16) to obscure passages
- **Bible Versions**: {stats['total_versions']} versions across {stats['total_versions']} different translations and languages
- **AI Models**: {stats['total_models']} models from major providers (Google, OpenAI, Anthropic, Meta, Qwen, DeepSeek)
- **Total Test Cases**: {stats['total_model_quotes']:,} (verses × versions × models)

#### Verse Selection

Verses were categorized by familiarity:
1. **Famous** (Difficulty 1-2): Well-known verses like John 3:16, Genesis 1:1
2. **Well-Known** (Difficulty 2-3): Commonly quoted verses
3. **Moderate** (Difficulty 4-5): Less frequently quoted passages
4. **Less Common** (Difficulty 6-7): Obscure verses from minor prophets
5. **Very Obscure** (Difficulty 8-10): Rarely quoted passages

#### Language Selection

Languages were chosen to represent:
- Common English translations (NIV, KJV, ESV, etc.)
- Source languages (Greek, Hebrew, Latin)
- Gateway languages (Spanish, French, German, Chinese, Arabic, etc.)
- Regional languages with varying levels of Bible translation maturity

### Evaluation Metrics

Each model's output was compared against baseline quotes using multiple metrics:

1. **Exact Match**: Binary indicator of perfect match after normalization
2. **Similarity Score**: SequenceMatcher ratio (0.0 to 1.0)
3. **Word Error Rate (WER)**: Ratio of word-level edits needed
4. **Character Error Rate (CER)**: Ratio of character-level edits needed
5. **Levenshtein Distance**: Number of single-character edits required

### Test Execution

- Models were queried via requesty.ai API
- Temperature set to 0.1 for consistency
- Each model received identical prompts
- Response times were recorded
- All results stored in SQLite database for analysis

"""
    return section


def generate_recommendations(db: BibleQuoteDatabase) -> str:
    """Generate recommendations section."""
    section = """## Recommendations

Based on the results of this experiment:

### For Scripture Quotation Tasks

1. **Model Selection**: Choose high-tier models from top-performing providers for critical applications
2. **Language Considerations**: Expect reduced accuracy for non-English and non-Latin script languages
3. **Verification**: Always verify quotes against authoritative sources, especially for:
   - Non-English languages
   - Obscure verses
   - Critical applications

### For Future Research

1. **Expand Language Coverage**: Test additional rare languages and dialects
2. **Context Analysis**: Evaluate models' understanding of verse context
3. **Version Consistency**: Test ability to quote from specific requested versions
4. **Multi-verse Passages**: Test longer passages and chapters
5. **Paraphrase Detection**: Evaluate models' ability to identify paraphrased vs. direct quotes

### For Model Developers

1. **Training Data**: Ensure diverse Bible translations in training data
2. **Multi-script Support**: Improve non-Latin script accuracy
3. **Attribution**: Include verse reference verification in training
4. **Consistency**: Reduce variation in quote accuracy across difficulty levels

"""
    return section


def generate_full_report(db: BibleQuoteDatabase, output_path: Path):
    """Generate complete markdown report."""
    print("Generating comprehensive report...")

    report = f"""# Bible Quote Accuracy Analysis Across AI Models

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""

    # Generate each section
    sections = [
        ("Executive Summary", generate_executive_summary),
        ("Model Comparison", generate_model_comparison),
        ("Language Analysis", generate_language_analysis),
        ("Verse Difficulty", generate_verse_difficulty_analysis),
        ("Examples", generate_detailed_examples),
        ("Methodology", generate_methodology),
        ("Recommendations", generate_recommendations),
    ]

    for section_name, generator_func in sections:
        print(f"  Generating: {section_name}...")
        report += generator_func(db)

    # Add appendix
    report += """---

## Appendix

### About This Report

This report was generated automatically from experimental data testing AI models' ability to quote Bible verses accurately across multiple languages and translations.

### Data Availability

The complete dataset including all quotes, metrics, and analysis is available in the SQLite database accompanying this report.

### Contact & Feedback

For questions, corrections, or additional analysis requests, please refer to the project repository.

"""

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✓ Report generated: {output_path}")
    print(f"  Size: {len(report):,} characters")


def main():
    """Main function to generate report."""
    print("=" * 60)
    print("Bible Quote Accuracy Test - Report Generation")
    print("=" * 60)

    # Initialize database
    db_path = Path(__file__).parent / "bible_quote_accuracy.db"
    print(f"\nDatabase: {db_path}")

    if not db_path.exists():
        print("\n❌ Error: Database not found!")
        print("Please run the analysis script first.")
        sys.exit(1)

    output_path = Path(__file__).parent / "BIBLE_QUOTE_ACCURACY_REPORT.md"

    with BibleQuoteDatabase(str(db_path)) as db:
        # Check if we have analysis results
        stats = db.get_statistics()
        if stats['total_analyses'] == 0:
            print("\n❌ Error: No analysis results found!")
            print("Please run analyze_results.py first.")
            sys.exit(1)

        print(f"\nGenerating report from {stats['total_analyses']:,} analysis results...")

        # Generate report
        generate_full_report(db, output_path)

    print("\n✓ Report generation completed!")
    print(f"\nView the report: {output_path}")


if __name__ == "__main__":
    main()
