"""
Bank commands for Soravelon.

CmdBank — subcommand dispatcher for deposit/withdraw/balance.
CmdDeposit / CmdWithdraw — flat aliases for quick access.
"""

from commands.command import Command
from world.banking import deposit, withdraw, get_balance


class CmdBank(Command):
    """
    Manage your banked Scales.

    Usage:
      bank balance         - show carried and banked Scales
      bank deposit <amount> - deposit Scales into the bank
      bank withdraw <amount> - withdraw Scales from the bank

    With no arguments, shows your current balance.
    """

    key = "bank"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        char = self.caller
        args = self.args.strip().split()

        if not args or args[0].lower() == "balance":
            carried = char.db.carried_scales or 0
            banked = get_balance(char)
            char.msg(
                f"|wCarried:|n {carried} Scales  |  "
                f"|wBanked:|n {banked} Scales"
            )
            return

        subcmd = args[0].lower()

        if subcmd in ("deposit", "withdraw"):
            if len(args) < 2:
                char.msg(f"Usage: bank {subcmd} <amount>")
                return
            try:
                amount = int(args[1])
            except ValueError:
                char.msg("Amount must be a number.")
                return

            if subcmd == "deposit":
                success, msg = deposit(char, amount)
            else:
                success, msg = withdraw(char, amount)
            char.msg(msg)
            return

        char.msg(
            "Usage: bank deposit <amount> | bank withdraw <amount> | bank balance"
        )


class CmdDeposit(Command):
    """
    Deposit Scales into the bank.

    Usage:
      deposit <amount>
    """

    key = "deposit"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        char = self.caller
        raw = self.args.strip()
        if not raw:
            char.msg("Usage: deposit <amount>")
            return
        try:
            amount = int(raw)
        except ValueError:
            char.msg("Amount must be a number.")
            return
        success, msg = deposit(char, amount)
        char.msg(msg)


class CmdWithdraw(Command):
    """
    Withdraw Scales from the bank.

    Usage:
      withdraw <amount>
    """

    key = "withdraw"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        char = self.caller
        raw = self.args.strip()
        if not raw:
            char.msg("Usage: withdraw <amount>")
            return
        try:
            amount = int(raw)
        except ValueError:
            char.msg("Amount must be a number.")
            return
        success, msg = withdraw(char, amount)
        char.msg(msg)
