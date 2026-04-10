"""
Command Preprocessor — prefix matching and alias expansion.

Called from Character.execute_cmd() before every command. Handles:
  - Exact command match: pass through unchanged
  - Alias expansion: substitutes $1/$2/$*/$@ tokens, chains up to 3 commands (D-16)
  - Prefix resolution: unique prefix expands; ambiguous prefix sends "Did you mean?" error (D-14)
  - No match: pass through to Evennia's own "unknown command" handler

Exports:
    preprocess_input(character, raw_string) -> str | list[str] | None
    expand_alias(character, alias_key, raw_args) -> list[str] | None
    resolve_prefix(raw_word, all_cmd_keys) -> tuple[str | None, list[str]]
"""


def resolve_prefix(raw_word, all_cmd_keys):
    """
    Resolve a (possibly abbreviated) word against a list of known command keys.

    Args:
        raw_word (str): The word the player typed (may be a prefix).
        all_cmd_keys (list[str]): All known command key strings (lowercase expected).

    Returns:
        tuple: (resolved_key, matches)
            - (key, [])       — exact or unique prefix match
            - (None, matches) — ambiguous; matches is sorted list of 2+ candidates
            - (None, [])      — no match at all (pass through)
    """
    raw_word = raw_word.lower().strip()

    # Exact match wins immediately
    if raw_word in all_cmd_keys:
        return (raw_word, [])

    # Prefix scan
    matches = sorted([k for k in all_cmd_keys if k.startswith(raw_word)])

    if len(matches) == 0:
        return (None, [])
    if len(matches) == 1:
        return (matches[0], [])
    # Ambiguous — return None + sorted candidates (D-14)
    return (None, matches)


def _substitute(cmd_str, parts, raw_args):
    """
    Substitute argument tokens in a command string.

    Tokens:
        $*  and  $@  → full raw_args string
        $1, $2, $N   → individual space-split parts (empty string if missing)

    Args:
        cmd_str (str): The template command string.
        parts (list[str]): raw_args split on whitespace.
        raw_args (str): The raw argument string.

    Returns:
        str: cmd_str with tokens replaced.
    """
    result = cmd_str
    result = result.replace("$*", raw_args.strip())
    result = result.replace("$@", raw_args.strip())
    # Replace positional tokens highest-index first to avoid partial overlap
    # (e.g., $10 before $1). Practical cap at 9 positional args.
    for i in range(9, 0, -1):
        token = f"${i}"
        value = parts[i - 1] if i - 1 < len(parts) else ""
        result = result.replace(token, value)
    return result


def expand_alias(character, alias_key, raw_args):
    """
    Expand an alias to a list of command strings.

    Checks character.db.aliases for alias_key. Returns None if not found.
    Splits expansion by ";" and caps at 3 commands (D-16).
    Performs $1/$2/$*/$@ token substitution.

    Args:
        character: The Evennia character object (must have db.aliases).
        alias_key (str): The alias name to look up.
        raw_args (str): Arguments the player typed after the alias key.

    Returns:
        list[str] | None: Expanded command list, or None if alias not found.
    """
    aliases = character.db.aliases or {}
    if alias_key not in aliases:
        return None

    expansion = aliases[alias_key]
    # Split by semicolon, strip whitespace, cap at 3 (D-16)
    commands = [c.strip() for c in expansion.split(";") if c.strip()][:3]
    parts = raw_args.strip().split() if raw_args.strip() else []
    return [_substitute(c, parts, raw_args) for c in commands]


def _get_all_cmd_keys(character):
    """
    Collect all command keys and aliases from the character's current CmdSets.

    Iterates character.cmdset.all() → each cmdset's .commands list.
    Returns a sorted list of lowercase strings for stable prefix matching.
    No DB queries — fast path only.

    Args:
        character: Evennia character object.

    Returns:
        list[str]: Sorted list of all command key/alias strings.
    """
    keys = set()
    for cmdset in character.cmdset.all():
        for cmd in cmdset.commands:
            if cmd.key:
                keys.add(cmd.key.lower())
            for alias in (cmd.aliases or []):
                keys.add(alias.lower())
    return sorted(keys)


def preprocess_input(character, raw_string):
    """
    Preprocess a raw command string before routing to Evennia's cmdhandler.

    Processing order (all comparisons are lowercase):
    1. Extract first word and remainder from raw_string.
    2. Collect all command keys from the character's merged CmdSet.
    3. Exact system-command match → return raw_string unchanged (D-17, Pitfall 5).
    4. Alias lookup → return expanded list of 1-3 strings (D-16).
    5. Prefix resolution:
       a. Unique prefix → return reconstructed command string.
       b. Ambiguous prefix → msg "Did you mean: X, Y?" and return None (D-14).
       c. No match → return raw_string (let Evennia handle "unknown command").

    Args:
        character: Evennia character object (must have .cmdset and .db.aliases).
        raw_string (str): Raw input string from the player.

    Returns:
        str        — resolved/unchanged command string (pass to super().execute_cmd)
        list[str]  — alias expansion: multiple commands to execute in sequence
        None       — ambiguity error already sent; caller should abort execution
    """
    parts = raw_string.strip().split(None, 1)
    if not parts:
        return raw_string

    word = parts[0].lower()
    raw_args = parts[1] if len(parts) > 1 else ""

    all_keys = _get_all_cmd_keys(character)

    # Step 3: Exact system command match — skip alias and prefix logic entirely
    if word in all_keys:
        return raw_string

    # Step 4: Alias lookup (only if not an exact system command)
    expanded = expand_alias(character, word, raw_args)
    if expanded is not None:
        return expanded

    # Step 5: Prefix resolution
    resolved, matches = resolve_prefix(word, all_keys)
    if resolved:
        return f"{resolved} {raw_args}".strip()
    if matches:
        # Ambiguous — D-14: send error, return None to abort
        character.msg(f"Did you mean: {', '.join(matches)}?")
        return None

    # No match — let Evennia handle "unknown command"
    return raw_string
