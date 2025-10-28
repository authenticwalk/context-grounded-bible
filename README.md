# context-grounded-bible

Improve AI (specifically large language models like chatGPT) by grounding it in truth (feeding it several books worth of context on each verse of the Bible)

## Bible Quote Accuracy Analysis

This repository includes a comprehensive test suite to evaluate AI models' ability to accurately quote Bible verses across multiple languages and translations.

### Features

- **100 test verses** ranging from famous (John 3:16) to very obscure passages
- **30 Bible versions** across different languages and scripts
- **12 AI models** from major providers (Google, OpenAI, Anthropic, Meta, Qwen, DeepSeek)
- **Comprehensive metrics**: Exact match, similarity score, WER, CER, Levenshtein distance
- **Automated pipeline**: From data collection to report generation

### Quick Start

```bash
# Navigate to tests directory
cd tests

# Install dependencies
pip install -r requirements.txt

# Set your requesty.ai API key
export REQUESTY_API_KEY='your-api-key'

# Run the full pipeline
python run_full_pipeline.py
```

See [tests/README.md](tests/README.md) for detailed documentation.

## Project Goals

1. **Ground AI in Truth**: Improve LLM accuracy by providing rich contextual information for Bible verses
2. **Measure Accuracy**: Quantify how well different AI models can quote scripture across languages
3. **Language Coverage**: Test AI performance across major world languages and rare Bible translations
4. **Identify Gaps**: Find areas where AI models struggle with Biblical text

## License

See [LICENSE](LICENSE) file for details.
