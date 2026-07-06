"""Builder/admin inspection command for the Social Web kernel."""

from commands.command import Command


class CmdSocialMemory(Command):
    """
    Inspect social knowledge known by one node about another node.

    Usage:
      socialmemory <viewer_node_key> <subject_node_key>

    Example:
      socialmemory npc:npc_warden_outpost_commander player:42
    """

    key = "socialmemory"
    aliases = ["socialweb"]
    locks = "cmd:perm(Builders)"
    help_category = "Admin"

    def func(self):
        args = (self.args or "").strip().split()
        if len(args) != 2:
            self.caller.msg(
                "Usage: socialmemory <viewer_node_key> <subject_node_key>"
            )
            return

        viewer_node_key, subject_node_key = args

        from world.social_engine import query_social_context

        context = query_social_context(
            viewer_node_key=viewer_node_key,
            subject_node_key=subject_node_key,
            purpose="admin",
        )

        facts = context.get("facts", [])
        claims = context.get("claims", [])
        lines = [
            "|wSocial Context|n",
            f"viewer: {viewer_node_key}",
            f"subject: {subject_node_key}",
            f"facts: {len(facts)}",
            f"claims: {len(claims)}",
        ]
        for claim in claims:
            lines.append(
                "- {claim_key} [{status}]: {summary}".format(
                    claim_key=claim.get("claim_key", ""),
                    status=claim.get("status", ""),
                    summary=claim.get("summary", ""),
                )
            )
            for trace in claim.get("trace", []):
                edge_type = trace.get("edge_type") or "direct"
                lines.append(f"  via {edge_type}: {trace.get('summary', '')}")

        self.caller.msg("\n".join(lines))
