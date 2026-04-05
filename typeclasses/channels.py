"""
Channel typeclasses for Soravelon.

OOCChannel: Server-wide out-of-character chat. All accounts auto-subscribe.
DomainChannel: Per-domain chat. Membership checked at send time based on
    character's primary domain (highest score in db.domain_scores).
"""

from evennia.comms.comms import DefaultChannel


class Channel(DefaultChannel):
    """Base Soravelon channel."""

    pass


class OOCChannel(Channel):
    """Server-wide out-of-character chat channel."""

    def channel_prefix(self, msg=None, emit=False):
        return "|w[OOC]|n "


class DomainChannel(Channel):
    """
    Domain-specific channel. Only characters sharing the same primary domain
    can send messages. Membership checked at send time, not subscription time.
    """

    def channel_prefix(self, msg=None, emit=False):
        return f"|c[{self.key}]|n "

    def at_pre_msg(self, message, **kwargs):
        """Check sender's primary domain matches channel domain."""
        sender = message.senders[0] if message.senders else None
        if not sender:
            return super().at_pre_msg(message, **kwargs)

        # Get character (sender may be account)
        character = sender
        if hasattr(sender, "puppet"):
            character = sender.puppet
        if not character:
            return super().at_pre_msg(message, **kwargs)

        # Check primary domain
        domain_scores = character.db.domain_scores or {}
        if not domain_scores:
            message.senders[0].msg("|rYou have no domain affiliation.|n")
            return False

        primary_domain = max(domain_scores, key=domain_scores.get)
        channel_domain = self.db.domain_name or self.key.lower()

        if primary_domain != channel_domain:
            message.senders[0].msg(
                f"|rYour primary domain is {primary_domain}, "
                f"not {channel_domain}.|n"
            )
            return False

        return super().at_pre_msg(message, **kwargs)
