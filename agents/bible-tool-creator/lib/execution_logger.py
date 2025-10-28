#!/usr/bin/env python3
"""
Execution Logger for Bible Tool Creator Agent

Provides structured logging to execution-log.md for debugging,
progress monitoring, and time tracking.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional


class ExecutionLogger:
    """Manages execution-log.md for a tool creation session."""

    def __init__(self, tool_path: Path):
        """
        Initialize execution logger.

        Args:
            tool_path: Path to tool directory
        """
        self.tool_path = Path(tool_path)
        self.log_file = self.tool_path / "execution-log.md"
        self.current_revision = 1

    def initialize(self, tool_name: str, experiment: str) -> None:
        """
        Create initial execution log.

        Args:
            tool_name: Name of the tool
            experiment: Experiment name
        """
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        content = f"""# Execution Log: {tool_name}

**Experiment:** {experiment}
**Started:** {self._timestamp()}

---

"""
        self.log_file.write_text(content)

    def start_revision(self, revision: int) -> None:
        """
        Log start of a new revision.

        Args:
            revision: Revision number
        """
        self.current_revision = revision
        self._append(f"\n## Revision {revision}\n")

    def log_phase(self, phase: str, status: str = "Started") -> None:
        """
        Log phase transition.

        Args:
            phase: Phase name (initialize, generate, review, etc.)
            status: Status (Started, Complete, Failed)
        """
        self._append(f"- [{self._timestamp()}] Phase: {phase} - {status}")

    def log_action(self, action: str, details: Optional[str] = None) -> None:
        """
        Log a specific action.

        Args:
            action: Description of action
            details: Optional additional details
        """
        message = f"- [{self._timestamp()}] {action}"
        if details:
            message += f" - {details}"
        self._append(message)

    def log_verse_start(self, reference: str) -> None:
        """
        Log start of verse processing.

        Args:
            reference: Verse reference
        """
        self._append(f"- [{self._timestamp()}] Processing verse: {reference}")

    def log_verse_complete(self, reference: str, yaml_file: str,
                          lines: int, citations: int,
                          duration_seconds: float) -> None:
        """
        Log completion of verse processing.

        Args:
            reference: Verse reference
            yaml_file: Generated YAML filename
            lines: Number of lines in YAML
            citations: Number of citations included
            duration_seconds: Time taken
        """
        self._append(
            f"- [{self._timestamp()}] Generated {yaml_file} "
            f"({lines} lines, {citations} citations, "
            f"{duration_seconds:.1f}s)"
        )

    def log_verse_error(self, reference: str, error: str) -> None:
        """
        Log verse processing error.

        Args:
            reference: Verse reference
            error: Error message
        """
        self._append(f"- [{self._timestamp()}] ERROR processing {reference}: {error}")

    def log_web_search(self, query: str, success: bool = True) -> None:
        """
        Log web search attempt.

        Args:
            query: Search query
            success: Whether search succeeded
        """
        status = "SUCCESS" if success else "FAILED"
        self._append(f"- [{self._timestamp()}] Web search ({status}): \"{query}\"")

    def log_validation(self, check: str, passed: bool, details: Optional[str] = None) -> None:
        """
        Log validation check.

        Args:
            check: What was validated
            passed: Whether validation passed
            details: Optional details
        """
        symbol = "✓" if passed else "✗"
        message = f"- [{self._timestamp()}] Validation {symbol} {check}"
        if details:
            message += f" - {details}"
        self._append(message)

    def log_error(self, error: str, context: Optional[str] = None) -> None:
        """
        Log a general error.

        Args:
            error: Error message
            context: Optional context
        """
        message = f"- [{self._timestamp()}] ERROR: {error}"
        if context:
            message += f" (Context: {context})"
        self._append(message)

    def log_warning(self, warning: str) -> None:
        """
        Log a warning.

        Args:
            warning: Warning message
        """
        self._append(f"- [{self._timestamp()}] WARNING: {warning}")

    def log_summary(self, summary: str) -> None:
        """
        Log a summary section.

        Args:
            summary: Summary text
        """
        self._append(f"\n### Summary\n{summary}\n")

    def _timestamp(self) -> str:
        """Get current timestamp in consistent format."""
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def _append(self, message: str) -> None:
        """
        Append message to log file.

        Args:
            message: Message to append
        """
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')
