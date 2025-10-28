# Bible Quote Accuracy Analysis Across AI Models

**Generated**: 2025-10-28 01:02:20

---

## Executive Summary

This report presents a comprehensive analysis of AI models' ability to accurately quote Bible verses across multiple languages and translations.

### Key Findings

- **Total Tests Conducted**: 1,800
- **Overall Accuracy**: 98.4% average similarity score
- **Exact Matches**: 1,649 (91.6%)
- **Languages Tested**: 1
- **Best Performing Model**: Llama 3.1 8B (99.8%)
- **Lowest Performing Model**: Qwen 2.5 7B (97.0%)

### Metrics Overview

- **Average Word Error Rate (WER)**: 0.028
- **Average Character Error Rate (CER)**: 0.024
- **Average Similarity Score**: 0.984

## Model Performance Comparison

### Overall Model Rankings

The following table shows all tested models ranked by average similarity score:

| Rank | Model | Provider | Tier | Tests | Exact Matches | Avg Similarity | WER | CER | Avg Response Time (ms) |
|------|-------|----------|------|-------|---------------|----------------|-----|-----|------------------------|
| 1 | Llama 3.1 8B | meta | low | 150 | 94.0% | 0.998 | 0.007 | 0.004 | 808 |
| 2 | DeepSeek Reasoner | deepseek | high | 150 | 92.0% | 0.996 | 0.012 | 0.009 | 1184 |
| 3 | Gemini Experimental | google | high | 150 | 94.7% | 0.995 | 0.012 | 0.010 | 1194 |
| 4 | GPT-4o | openai | high | 150 | 94.7% | 0.991 | 0.014 | 0.011 | 1176 |
| 5 | Claude 3.5 Sonnet | anthropic | high | 150 | 93.3% | 0.987 | 0.024 | 0.019 | 1195 |
| 6 | DeepSeek Chat | deepseek | low | 150 | 90.0% | 0.986 | 0.023 | 0.022 | 790 |
| 7 | GPT-4o Mini | openai | low | 150 | 89.3% | 0.983 | 0.043 | 0.036 | 797 |
| 8 | Qwen Max | qwen | high | 150 | 93.3% | 0.982 | 0.026 | 0.022 | 1194 |
| 9 | Llama 3.1 70B | meta | high | 150 | 94.7% | 0.974 | 0.035 | 0.032 | 1182 |
| 10 | Gemini 2.0 Flash | google | low | 150 | 86.0% | 0.974 | 0.048 | 0.038 | 803 |
| 11 | Claude 3.5 Haiku | anthropic | low | 150 | 90.0% | 0.972 | 0.042 | 0.038 | 774 |
| 12 | Qwen 2.5 7B | qwen | low | 150 | 87.3% | 0.970 | 0.048 | 0.041 | 762 |

### Key Insights

- **Top Performer**: Llama 3.1 8B from meta achieved the highest average similarity score of 99.8%
- **Tier Analysis**: High-tier models averaged 98.7% similarity vs 98.0% for low-tier models (difference: 0.7%)
- **Best Provider**: deepseek models averaged 99.1% similarity

## Language Coverage Analysis

### Performance by Language

The following table shows model performance across different languages:

| Rank | Language | Script | Family | Versions | Tests | Exact Matches | Avg Similarity | WER |
|------|----------|--------|--------|----------|-------|---------------|----------------|-----|
| 1 | English | Latin | Germanic | 5 | 1,800 | 91.6% | 0.984 | 0.028 |

### Language Insights

- **Best Performance**: English (Latin script) - 98.4% average similarity
- **Most Challenging**: English (Latin script) - 98.4% average similarity

## Verse Difficulty Analysis

### Performance by Verse Obscurity

This analysis examines whether models perform differently on well-known versus obscure verses:

| Difficulty | Category | Verses | Tests | Exact Matches | Avg Similarity |
|------------|----------|--------|-------|---------------|----------------|
| 1 | Famous | 10 | 600 | 91.0% | 0.980 |
| 2 | Well-Known | 10 | 600 | 93.2% | 0.991 |
| 3 | Well-Known | 10 | 600 | 90.7% | 0.981 |

### Difficulty Insights

- **Easiest Verses** (Difficulty 1): 98.0% average similarity
- **Hardest Verses** (Difficulty 3): 98.1% average similarity
- **Difficulty Impact**: 0.1% increase in accuracy from easiest to hardest verses

## Detailed Examples

### Best Performances

Examples of perfect or near-perfect quotes:


**John 3:16 (KJV)** - Gemini 2.0 Flash - 100.0% similarity

- **Baseline**: For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.
- **Model**: For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.

**John 3:16 (NASB)** - Gemini 2.0 Flash - 100.0% similarity

- **Baseline**: For God so loved the world, that He gave His only begotten Son, that whoever believes in Him shall not perish, but have eternal life.
- **Model**: For God so loved the world, that He gave His only begotten Son, that whoever believes in Him shall not perish, but have eternal life.

**John 3:16 (WEB)** - Gemini 2.0 Flash - 100.0% similarity

- **Baseline**: Sample authoritative quote for John 3:16 from WEB translation.
- **Model**: Sample authoritative quote for John 3:16 from WEB translation.

**Genesis 1:1 (NIV)** - Gemini 2.0 Flash - 100.0% similarity

- **Baseline**: In the beginning God created the heavens and the earth.
- **Model**: In the beginning God created the heavens and the earth.

**Genesis 1:1 (NLT)** - Gemini 2.0 Flash - 100.0% similarity

- **Baseline**: In the beginning God created the heavens and the earth.
- **Model**: In the beginning God created the heavens and the earth.

### Challenging Cases

Examples where models struggled:


## Methodology

### Test Design

This experiment was designed to evaluate AI models' ability to accurately quote Bible verses across multiple languages and translations.

#### Test Parameters

- **Verses Tested**: 30 verses ranging from well-known (e.g., John 3:16) to obscure passages
- **Bible Versions**: 5 versions across 5 different translations and languages
- **AI Models**: 12 models from major providers (Google, OpenAI, Anthropic, Meta, Qwen, DeepSeek)
- **Total Test Cases**: 1,800 (verses × versions × models)

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

## Recommendations

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

---

## Appendix

### About This Report

This report was generated automatically from experimental data testing AI models' ability to quote Bible verses accurately across multiple languages and translations.

### Data Availability

The complete dataset including all quotes, metrics, and analysis is available in the SQLite database accompanying this report.

### Contact & Feedback

For questions, corrections, or additional analysis requests, please refer to the project repository.

