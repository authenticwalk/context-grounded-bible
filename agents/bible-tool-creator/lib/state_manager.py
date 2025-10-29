#!/usr/bin/env python3
"""
State Management for Bible Tool Creator Agent

Provides functions to manage state.yaml for tracking agent progress,
enabling resume capability, and providing single source of truth.
"""

import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class StateManager:
    """Manages state.yaml for a tool creation session."""

    def __init__(self, tool_path: Path):
        """
        Initialize state manager.

        Args:
            tool_path: Path to tool directory (e.g., ./bible-study-tools/my-tool/)
        """
        self.tool_path = Path(tool_path)
        self.state_file = self.tool_path / "state.yaml"

    def initialize(self, tool_name: str, experiment: str) -> Dict[str, Any]:
        """
        Create initial state.yaml.

        Args:
            tool_name: Name of the tool being created
            experiment: Experiment name

        Returns:
            Initial state dictionary
        """
        state = {
            'tool_name': tool_name,
            'experiment': experiment,
            'revision': 1,
            'phase': 'initialize',
            'status': 'in_progress',
            'started_at': datetime.utcnow().isoformat() + 'Z',
            'last_activity': datetime.utcnow().isoformat() + 'Z',
            'verses': [],
            'errors': [],
            'warnings': []
        }

        self._write_state(state)
        return state

    def load(self) -> Dict[str, Any]:
        """
        Load current state from state.yaml.

        Returns:
            State dictionary

        Raises:
            FileNotFoundError: If state.yaml doesn't exist
        """
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")

        with open(self.state_file, 'r') as f:
            return yaml.safe_load(f)

    def update_phase(self, phase: str, status: str = 'in_progress') -> None:
        """
        Update current phase and status.

        Args:
            phase: New phase (initialize, generate, review, refine, finalize, complete)
            status: New status (pending, in_progress, complete, failed)
        """
        state = self.load()
        state['phase'] = phase
        state['status'] = status
        state['last_activity'] = datetime.utcnow().isoformat() + 'Z'

        if status == 'complete' and 'completed_at' not in state:
            state['completed_at'] = datetime.utcnow().isoformat() + 'Z'

        self._write_state(state)

    def add_verse(self, reference: str, book: str, chapter: int, verse: int,
                  yaml_file: str) -> None:
        """
        Add a verse to be processed.

        Args:
            reference: Human-readable reference (e.g., "John 1:1")
            book: Book code (e.g., "JHN")
            chapter: Chapter number
            verse: Verse number
            yaml_file: Relative path to YAML file
        """
        state = self.load()

        verse_entry = {
            'reference': reference,
            'book': book,
            'chapter': chapter,
            'verse': verse,
            'status': 'pending',
            'yaml_file': yaml_file
        }

        state['verses'].append(verse_entry)
        state['last_activity'] = datetime.utcnow().isoformat() + 'Z'

        self._write_state(state)

    def start_verse(self, reference: str) -> None:
        """
        Mark a verse as in_progress.

        Args:
            reference: Verse reference to update
        """
        state = self.load()

        for verse in state['verses']:
            if verse['reference'] == reference:
                verse['status'] = 'in_progress'
                verse['started_at'] = datetime.utcnow().isoformat() + 'Z'
                break

        state['last_activity'] = datetime.utcnow().isoformat() + 'Z'
        self._write_state(state)

    def complete_verse(self, reference: str) -> None:
        """
        Mark a verse as complete.

        Args:
            reference: Verse reference to update
        """
        state = self.load()

        for verse in state['verses']:
            if verse['reference'] == reference:
                verse['status'] = 'complete'
                verse['completed_at'] = datetime.utcnow().isoformat() + 'Z'
                break

        state['last_activity'] = datetime.utcnow().isoformat() + 'Z'
        self._write_state(state)

    def fail_verse(self, reference: str, error: str) -> None:
        """
        Mark a verse as failed and log error.

        Args:
            reference: Verse reference to update
            error: Error message
        """
        state = self.load()

        for verse in state['verses']:
            if verse['reference'] == reference:
                verse['status'] = 'failed'
                verse['error'] = error
                verse['failed_at'] = datetime.utcnow().isoformat() + 'Z'
                break

        state['errors'].append({
            'reference': reference,
            'error': error,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })

        state['last_activity'] = datetime.utcnow().isoformat() + 'Z'
        self._write_state(state)

    def add_error(self, error: str, context: Optional[str] = None) -> None:
        """
        Log a general error.

        Args:
            error: Error message
            context: Optional context about where error occurred
        """
        state = self.load()

        error_entry = {
            'error': error,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }

        if context:
            error_entry['context'] = context

        state['errors'].append(error_entry)
        state['last_activity'] = datetime.utcnow().isoformat() + 'Z'

        self._write_state(state)

    def add_warning(self, warning: str, context: Optional[str] = None) -> None:
        """
        Log a warning.

        Args:
            warning: Warning message
            context: Optional context
        """
        state = self.load()

        warning_entry = {
            'warning': warning,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }

        if context:
            warning_entry['context'] = context

        state['warnings'].append(warning_entry)
        state['last_activity'] = datetime.utcnow().isoformat() + 'Z'

        self._write_state(state)

    def get_status(self) -> Dict[str, Any]:
        """
        Get current status summary.

        Returns:
            Dictionary with status information
        """
        state = self.load()

        total_verses = len(state['verses'])
        completed = sum(1 for v in state['verses'] if v['status'] == 'complete')
        in_progress = sum(1 for v in state['verses'] if v['status'] == 'in_progress')
        failed = sum(1 for v in state['verses'] if v['status'] == 'failed')
        pending = sum(1 for v in state['verses'] if v['status'] == 'pending')

        return {
            'phase': state['phase'],
            'status': state['status'],
            'revision': state['revision'],
            'verses': {
                'total': total_verses,
                'completed': completed,
                'in_progress': in_progress,
                'failed': failed,
                'pending': pending
            },
            'errors': len(state['errors']),
            'warnings': len(state['warnings']),
            'started_at': state.get('started_at'),
            'last_activity': state.get('last_activity')
        }

    def _write_state(self, state: Dict[str, Any]) -> None:
        """
        Write state to state.yaml atomically.

        Args:
            state: State dictionary to write
        """
        # Ensure directory exists
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file then rename (atomic operation)
        temp_file = self.state_file.with_suffix('.yaml.tmp')

        with open(temp_file, 'w') as f:
            yaml.dump(state, f, default_flow_style=False, sort_keys=False)

        temp_file.rename(self.state_file)
