"""
Scripts for Soravelon.
"""

import time

from evennia.scripts.scripts import DefaultScript
from evennia.utils import logger


class SoravelonScript(DefaultScript):
    """Base script for new Soravelon scripts going forward."""

    def at_script_creation(self):
        super().at_script_creation()
        self.db.script_version = 1


class SessionCommitScript(SoravelonScript):
    """Per-character 10-minute safety XP flush."""

    def at_script_creation(self):
        super().at_script_creation()
        self.key = "session_commit_script"
        self.interval = 600
        self.persistent = False
        self.repeats = 0
        self.tags.add("session_commit", category="script_type")

    def at_repeat(self):
        character = self.obj
        if character:
            from world.world_state import commit_session_xp
            commit_session_xp(character)
            from world.banking import decrement_debt_timer, get_active_debt
            if get_active_debt(character):
                decrement_debt_timer(character, seconds_played=600)


class WorldEventScript(SoravelonScript):
    """
    Base class for timed world event scripts.

    Tracks event type, timestamps, tick counts, and state changes.
    Subclasses override ``on_event_tick`` to implement per-tick behavior
    and call ``log_state_change`` to record progression through states.
    The script automatically completes when ``expires_at`` is reached.
    """

    def at_script_creation(self):
        super().at_script_creation()
        self.db.event_type = None
        self.db.event_data = {}
        self.db.started_at = None
        self.db.expires_at = None
        self.tags.add("world_event", category="script_type")

    def at_start(self):
        """Record start time and log the event beginning."""
        self.db.started_at = time.time()
        logger.log_info(
            f"WorldEvent '{self.db.event_type}' started on {self.key}"
        )

    def at_repeat(self):
        """Tick handler -- check expiry then delegate to on_event_tick."""
        if self.db.expires_at and time.time() > self.db.expires_at:
            self.complete_event()
        else:
            self.on_event_tick()

    def on_event_tick(self):
        """
        Called every tick while the event is active.

        Base implementation increments a tick counter.
        Subclasses should override to add domain-specific behavior.
        """
        data = self.db.event_data
        data["tick_count"] = data.get("tick_count", 0) + 1
        self.db.event_data = data

    def complete_event(self):
        """Mark the event as completed and stop the script."""
        data = self.db.event_data
        data["completed"] = True
        data["completed_at"] = time.time()
        self.db.event_data = data
        logger.log_info(
            f"WorldEvent '{self.db.event_type}' completed on {self.key}"
        )
        self.stop()

    def log_state_change(self, old_state, new_state):
        """
        Record a state transition in the event data log.

        Useful for tracking world event progression (e.g. weather
        shifting from 'gathering' to 'storm' to 'clearing').
        """
        data = self.db.event_data
        state_log = data.get("state_log") or []
        state_log.append({
            "old_state": old_state,
            "new_state": new_state,
            "timestamp": time.time(),
        })
        data["state_log"] = state_log
        self.db.event_data = data
