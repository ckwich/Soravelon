"""
Accounts for Soravelon.
"""

from evennia.accounts.accounts import DefaultAccount


class SoravelonAccount(DefaultAccount):
    """
    Account typeclass. Cross-character preferences.
    """

    def at_account_creation(self):
        super().at_account_creation()
        self.db.color_enabled = True
        self.db.brief_mode = False
        self.db.compact_combat = False
        self.db.echo_self = True
        self.db.hints_enabled = True
        self.db.inv_sort = "type"
        self.db.combine_stacks = True
        self.db.prompt_format = "default"


class Account(SoravelonAccount):
    """Compatibility alias for Evennia test resources and scaffold defaults."""
    pass
