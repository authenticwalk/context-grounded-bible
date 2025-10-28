#!/usr/bin/env python3
"""
Master script to run the complete Bible quote accuracy analysis pipeline.

This script orchestrates all steps:
1. Database initialization
2. Baseline collection (optional)
3. Model testing
4. Analysis
5. Report generation
"""

import sys
import os
from pathlib import Path
import subprocess
from datetime import datetime


def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70 + "\n")


def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print_header(description)
    print(f"Running: {script_name}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            cwd=Path(__file__).parent
        )
        print(f"\n✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} failed with error code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠ Pipeline interrupted by user")
        return False


def check_prerequisites():
    """Check if prerequisites are met."""
    print_header("Checking Prerequisites")

    # Check Python version
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher required")
        return False
    print("✓ Python version OK")

    # Check API key
    api_key = os.environ.get('REQUESTY_API_KEY')
    if api_key:
        print(f"✓ REQUESTY_API_KEY is set (length: {len(api_key)})")
    else:
        print("⚠ REQUESTY_API_KEY not set")
        print("  You can still run baseline collection, but model testing will fail")
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return False

    # Check if scripts exist
    scripts = [
        'collect_baseline.py',
        'test_models.py',
        'analyze_results.py',
        'generate_report.py'
    ]

    for script in scripts:
        script_path = Path(__file__).parent / script
        if script_path.exists():
            print(f"✓ {script} found")
        else:
            print(f"✗ {script} not found")
            return False

    print("\n✓ All prerequisites met")
    return True


def main():
    """Main pipeline execution."""
    print("=" * 70)
    print(" BIBLE QUOTE ACCURACY ANALYSIS - FULL PIPELINE")
    print("=" * 70)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check prerequisites
    if not check_prerequisites():
        print("\n✗ Prerequisites not met. Exiting.")
        sys.exit(1)

    # Ask user what to run
    print_header("Pipeline Configuration")
    print("This pipeline consists of 4 steps:")
    print("  1. Baseline Collection (populates database structure)")
    print("  2. Model Testing (queries AI models via requesty.ai)")
    print("  3. Analysis (compares results and calculates metrics)")
    print("  4. Report Generation (creates markdown report)")
    print("\n⚠  WARNING: Model testing will make many API calls and incur costs!")
    print("   Full test: 100 verses × 30 versions × 12 models = 36,000 calls")
    print("   Limited test: 5 verses × 3 versions × 12 models = 180 calls")

    print("\nOptions:")
    print("  [1] Run full pipeline (all 4 steps)")
    print("  [2] Run baseline collection only")
    print("  [3] Run model testing only (requires baseline)")
    print("  [4] Run analysis only (requires model data)")
    print("  [5] Run report generation only (requires analysis)")
    print("  [6] Run steps 3-4 (analysis + report)")
    print("  [0] Exit")

    choice = input("\nSelect option [0-6]: ").strip()

    steps = {
        '1': ['collect_baseline.py', 'test_models.py', 'analyze_results.py', 'generate_report.py'],
        '2': ['collect_baseline.py'],
        '3': ['test_models.py'],
        '4': ['analyze_results.py'],
        '5': ['generate_report.py'],
        '6': ['analyze_results.py', 'generate_report.py'],
    }

    if choice == '0':
        print("\nExiting.")
        sys.exit(0)

    if choice not in steps:
        print(f"\n✗ Invalid option: {choice}")
        sys.exit(1)

    selected_steps = steps[choice]

    # Confirm for model testing
    if 'test_models.py' in selected_steps:
        print("\n⚠  You selected model testing which will make API calls.")
        confirm = input("Continue? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("\nCancelled.")
            sys.exit(0)

    # Run selected steps
    start_time = datetime.now()
    success_count = 0

    step_descriptions = {
        'collect_baseline.py': 'Baseline Collection',
        'test_models.py': 'Model Testing',
        'analyze_results.py': 'Results Analysis',
        'generate_report.py': 'Report Generation',
    }

    for i, script in enumerate(selected_steps, 1):
        description = step_descriptions.get(script, script)
        print(f"\n[Step {i}/{len(selected_steps)}]")

        if run_script(script, description):
            success_count += 1
        else:
            print(f"\n⚠  Step failed: {description}")
            response = input("Continue with remaining steps? (y/n): ").strip().lower()
            if response != 'y':
                break

    # Summary
    end_time = datetime.now()
    duration = end_time - start_time

    print_header("Pipeline Summary")
    print(f"Started:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}")
    print(f"Steps completed: {success_count}/{len(selected_steps)}")

    if success_count == len(selected_steps):
        print("\n✓ Pipeline completed successfully!")

        # Show output files
        db_path = Path(__file__).parent / "bible_quote_accuracy.db"
        report_path = Path(__file__).parent / "BIBLE_QUOTE_ACCURACY_REPORT.md"

        if db_path.exists():
            size_mb = db_path.stat().st_size / (1024 * 1024)
            print(f"\nDatabase: {db_path}")
            print(f"  Size: {size_mb:.2f} MB")

        if report_path.exists():
            with open(report_path) as f:
                lines = len(f.readlines())
            print(f"\nReport: {report_path}")
            print(f"  Lines: {lines:,}")
    else:
        print("\n⚠ Pipeline completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Pipeline interrupted by user")
        sys.exit(1)
