"""
SQLite database schema and management for Bible quote accuracy testing.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class BibleQuoteDatabase:
    def __init__(self, db_path: str = "bible_quote_accuracy.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Create all necessary tables for the experiment."""
        cursor = self.conn.cursor()

        # Verses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                difficulty_score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Bible versions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bible_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                language TEXT NOT NULL,
                script TEXT NOT NULL,
                language_family TEXT NOT NULL,
                rarity_score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # AI Models table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id TEXT UNIQUE NOT NULL,
                provider TEXT NOT NULL,
                model_name TEXT NOT NULL,
                tier TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Baseline quotes (from quote-bible skill)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS baseline_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                verse_id INTEGER NOT NULL,
                version_id INTEGER NOT NULL,
                quote_text TEXT,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (verse_id) REFERENCES verses (id),
                FOREIGN KEY (version_id) REFERENCES bible_versions (id),
                UNIQUE(verse_id, version_id)
            )
        """)

        # Model quotes (from requesty.ai API)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id INTEGER NOT NULL,
                verse_id INTEGER NOT NULL,
                version_id INTEGER NOT NULL,
                quote_text TEXT,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                response_time_ms REAL,
                retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (model_id) REFERENCES ai_models (id),
                FOREIGN KEY (verse_id) REFERENCES verses (id),
                FOREIGN KEY (version_id) REFERENCES bible_versions (id),
                UNIQUE(model_id, verse_id, version_id)
            )
        """)

        # Analysis results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id INTEGER NOT NULL,
                verse_id INTEGER NOT NULL,
                version_id INTEGER NOT NULL,
                baseline_quote_id INTEGER,
                model_quote_id INTEGER NOT NULL,
                exact_match BOOLEAN,
                similarity_score REAL,
                word_error_rate REAL,
                character_error_rate REAL,
                levenshtein_distance INTEGER,
                notes TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (model_id) REFERENCES ai_models (id),
                FOREIGN KEY (verse_id) REFERENCES verses (id),
                FOREIGN KEY (version_id) REFERENCES bible_versions (id),
                FOREIGN KEY (baseline_quote_id) REFERENCES baseline_quotes (id),
                FOREIGN KEY (model_quote_id) REFERENCES model_quotes (id),
                UNIQUE(model_id, verse_id, version_id)
            )
        """)

        self.conn.commit()

    def insert_verse(self, reference: str, category: str, difficulty: int) -> int:
        """Insert a verse and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO verses (reference, category, difficulty_score) VALUES (?, ?, ?)",
            (reference, category, difficulty)
        )
        self.conn.commit()
        cursor.execute("SELECT id FROM verses WHERE reference = ?", (reference,))
        return cursor.fetchone()[0]

    def insert_bible_version(self, code: str, name: str, language: str,
                            script: str, family: str, rarity: int) -> int:
        """Insert a Bible version and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO bible_versions
               (code, name, language, script, language_family, rarity_score)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (code, name, language, script, family, rarity)
        )
        self.conn.commit()
        cursor.execute("SELECT id FROM bible_versions WHERE code = ?", (code,))
        return cursor.fetchone()[0]

    def insert_ai_model(self, model_id: str, provider: str,
                       model_name: str, tier: str) -> int:
        """Insert an AI model and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO ai_models
               (model_id, provider, model_name, tier)
               VALUES (?, ?, ?, ?)""",
            (model_id, provider, model_name, tier)
        )
        self.conn.commit()
        cursor.execute("SELECT id FROM ai_models WHERE model_id = ?", (model_id,))
        return cursor.fetchone()[0]

    def insert_baseline_quote(self, verse_id: int, version_id: int,
                             quote_text: Optional[str], success: bool,
                             error_message: Optional[str] = None) -> int:
        """Insert a baseline quote from the quote-bible skill."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO baseline_quotes
               (verse_id, version_id, quote_text, success, error_message)
               VALUES (?, ?, ?, ?, ?)""",
            (verse_id, version_id, quote_text, success, error_message)
        )
        self.conn.commit()
        return cursor.lastrowid

    def insert_model_quote(self, model_id: int, verse_id: int, version_id: int,
                          quote_text: Optional[str], success: bool,
                          response_time_ms: Optional[float] = None,
                          error_message: Optional[str] = None) -> int:
        """Insert a quote from an AI model."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO model_quotes
               (model_id, verse_id, version_id, quote_text, success,
                response_time_ms, error_message)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (model_id, verse_id, version_id, quote_text, success,
             response_time_ms, error_message)
        )
        self.conn.commit()
        return cursor.lastrowid

    def insert_analysis_result(self, model_id: int, verse_id: int, version_id: int,
                              baseline_quote_id: Optional[int], model_quote_id: int,
                              exact_match: bool, similarity_score: float,
                              word_error_rate: float, character_error_rate: float,
                              levenshtein_distance: int, notes: Optional[str] = None) -> int:
        """Insert analysis results comparing baseline and model quotes."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO analysis_results
               (model_id, verse_id, version_id, baseline_quote_id, model_quote_id,
                exact_match, similarity_score, word_error_rate, character_error_rate,
                levenshtein_distance, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (model_id, verse_id, version_id, baseline_quote_id, model_quote_id,
             exact_match, similarity_score, word_error_rate, character_error_rate,
             levenshtein_distance, notes)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_verses(self) -> List[Dict[str, Any]]:
        """Get all verses."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM verses ORDER BY difficulty_score, reference")
        return [dict(row) for row in cursor.fetchall()]

    def get_bible_versions(self) -> List[Dict[str, Any]]:
        """Get all Bible versions."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bible_versions ORDER BY rarity_score, code")
        return [dict(row) for row in cursor.fetchall()]

    def get_ai_models(self) -> List[Dict[str, Any]]:
        """Get all AI models."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM ai_models ORDER BY provider, tier")
        return [dict(row) for row in cursor.fetchall()]

    def get_baseline_quote(self, verse_id: int, version_id: int) -> Optional[Dict[str, Any]]:
        """Get baseline quote for a specific verse and version."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM baseline_quotes WHERE verse_id = ? AND version_id = ?",
            (verse_id, version_id)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_model_quote(self, model_id: int, verse_id: int,
                       version_id: int) -> Optional[Dict[str, Any]]:
        """Get model quote for a specific model, verse, and version."""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM model_quotes
               WHERE model_id = ? AND verse_id = ? AND version_id = ?""",
            (model_id, verse_id, version_id)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_analysis_results(self, model_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get analysis results, optionally filtered by model."""
        cursor = self.conn.cursor()
        if model_id:
            cursor.execute(
                "SELECT * FROM analysis_results WHERE model_id = ?",
                (model_id,)
            )
        else:
            cursor.execute("SELECT * FROM analysis_results")
        return [dict(row) for row in cursor.fetchall()]

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics from the database."""
        cursor = self.conn.cursor()

        stats = {}

        # Count records
        cursor.execute("SELECT COUNT(*) as count FROM verses")
        stats['total_verses'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM bible_versions")
        stats['total_versions'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM ai_models")
        stats['total_models'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM baseline_quotes")
        stats['total_baseline_quotes'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM model_quotes")
        stats['total_model_quotes'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM analysis_results")
        stats['total_analyses'] = cursor.fetchone()['count']

        return stats

    def close(self):
        """Close database connection."""
        self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
