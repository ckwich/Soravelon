"""
Scripts for Soravelon.
"""

from evennia.scripts.scripts import DefaultScript


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
            # Flush ALL accumulators consistently (matches safety flush and logout)
            from world.world_state import commit_session_xp
            commit_session_xp(character)
            from world.skill_engine import commit_skill_accumulators
            commit_skill_accumulators(character)
            from world.base_attributes import commit_stat_growth
            commit_stat_growth(character)
            from world.banking import decrement_debt_timer, get_active_debt
            if get_active_debt(character):
                decrement_debt_timer(character, seconds_played=600)


