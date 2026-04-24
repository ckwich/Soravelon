# Soravelon Wave 2 Commands, Help, Onboarding, and Player Legibility Audit

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-deep-gameplay-code-health-audit-plan.md`
**Follows:** `docs/superpowers/plans/2026-04-22-wave1-lifecycle-remediation.md`

## Scope
Wave 2 audited whether players can discover, understand, and use the existing game surface without unnecessary confusion. This pass focused on:

- command registration and command ergonomics
- command-help coverage and help-topic truthfulness
- first-session onboarding and guided breadcrumbs
- runtime/help drift that creates false confidence

## Evidence Reviewed

- `commands/default_cmdsets.py`
- `commands/cmd_help.py`
- `commands/cmd_group.py`
- `commands/cmd_guild.py`
- `commands/cmd_abilities.py`
- `commands/cmd_vendor.py`
- `commands/cmd_loot.py`
- `commands/skill_commands.py`
- `typeclasses/characters.py`
- `world/help_entries.py`
- `world/group_engine.py`
- `tests/test_help_entries.py`
- `tests/test_command_preprocessor.py`
- `tests/test_action_vocabulary.py`
- `tests/test_content_integration.py`

## Validation Run

- `python scripts/run_tests.py tests.test_help_entries tests.test_command_preprocessor tests.test_action_vocabulary tests.test_content_integration`
- Result: `93` tests passed

This confirms the help and command surface is import-clean and structurally stable, but it does **not** mean the player-legibility layer is complete.

## Current-State Baseline

- `commands/default_cmdsets.py` registers a wide custom character surface and includes the custom `CmdHelp`.
- `world/help_entries.py` currently ships `110` help entries.
- Static command-help parity scan found `68` custom command keys across the `commands/` directory.
- Direct help coverage for those commands is only about `60.3%`.
- `27` custom commands currently have no direct help topic keyed to the actual command name or alias.

## Findings

### Blocker
- **The code-driven new-player breadcrumb layer is absent in live character hooks.**
  - `typeclasses/characters.py` currently routes `at_post_puppet()` straight into `world.session_lifecycle.on_login()` and does not call `_send_new_player_guidance()` or any equivalent onboarding helper.
  - Multiple planning and verification artifacts still claim that `_send_new_player_guidance()` exists and is wired, including:
    - `.planning/phases/12-launch-polish-help/12-01-SUMMARY.md`
    - `.planning/phases/12-launch-polish-help/12-VERIFICATION.md`
    - `.claude/skills/ancestry-engine/skill.md`
  - Impact: new players still spawn in the correct hub and can use help manually, but there is no actual runtime ancestry prompt, guild breadcrumb, or first-quest conversation hint.
  - For launch readiness, this is a real first-session usability gap, not just stale documentation.

### High-Value Fix
- **Command help coverage is materially incomplete for the live surface.**
  - Static parity scan found `27` custom commands with no direct help topic:
    - `appraise`
    - `blessing`
    - `butcher`
    - `buy`
    - `charge`
    - `chop`
    - `compare`
    - `fish`
    - `forage`
    - `harvest`
    - `inspect`
    - `list`
    - `loot`
    - `mine`
    - `prospect`
    - `quest`
    - `reel`
    - `repair`
    - `rest`
    - `sell`
    - `shout`
    - `sleep`
    - `tools`
    - `view`
    - `wake`
    - `whisper`
    - `who`
  - The biggest gaps are in systems players are likely to need during their first few sessions:
    - vendors and item inspection
    - gathering and fishing
    - recovery commands
    - social visibility commands
    - quest journal usage
  - Existing help tests do not check command parity, so this gap currently passes unnoticed.

### High-Value Fix
- **Several command help topics are authored under the wrong keys, which hides usage guidance behind system entries.**
  - `world/help_entries.py` uses command-topic keys like:
    - `domains command`
    - `abilities command`
    - `skills command`
    - `quest command`
  - Meanwhile the actual live commands are:
    - `domains`
    - `abilities`
    - `skills`
    - `quest`
  - Impact: `help domains` and similar queries are likely to land on broader system overviews rather than the command-usage pages a player expects.
  - This is especially costly because those commands are core progression surfaces.

### High-Value Fix
- **Some live help text does not match actual command syntax.**
  - `world/help_entries.py` documents `group loot <mode>`, but `commands/cmd_group.py` only accepts `group lootmode <mode>`.
  - `world/help_entries.py` describes `joinguild <guild name>` as the main usage, but `commands/cmd_guild.py` also requires or strongly depends on the `secondary_domain` step in the real join flow.
  - Impact: a player can read help, type what it says, and still hit the wrong syntax path.

### Improvement Opportunity
- **`domains` claiming the alias `skills` makes the command surface noisier than it needs to be.**
  - `commands/cmd_domains.py` aliases `domains` to `skills`.
  - `commands/skill_commands.py` also defines a real `skills` command.
  - Even if the runtime resolves the exact command key safely, this overlap complicates help discoverability, command mental models, and future maintenance.

### Improvement Opportunity
- **Ability help is less forgiving than ability use.**
  - `commands/cmd_help.py` only resolves abilities by exact ability id or exact full ability name.
  - `commands/cmd_abilities.py` uses a more flexible ability-resolution path for `use`.
  - Result: players can often use an ability more easily than they can ask for help about it.
  - This is not a blocker, but it is a real UX rough edge.

### Already Strong / Protect With Regression Coverage
- **The command surface is centralized and reviewable.**
  - `commands/default_cmdsets.py` gives a single trustworthy registration point for most player commands.
  - This made the audit tractable and will make remediation safer.

### Already Strong / Protect With Regression Coverage
- **The custom help pipeline is structurally solid.**
  - `CmdHelp` is registered.
  - `world.help_entries` imports cleanly.
  - Dynamic ability help exists.
  - The test suite confirms the surface is structurally healthy even though content parity is incomplete.

## Recommended Fix Directions

### Onboarding
- Restore a real runtime onboarding helper in the character login path.
- Keep it light and contextual:
  - ancestry prompt for brand-new characters
  - guild breadcrumb for ancestry-set but guildless characters
  - starter quest / NPC conversation hint after guild discovery
- Add direct tests for the message ladder so plans cannot drift from live behavior again.

### Help parity
- Add direct help topics for the missing live commands, especially:
  - vendor loop
  - recovery
  - quest journal
  - gathering/fishing
  - social visibility
  - inspection/compare
- Add a test that command keys and aliases in the live custom command surface have matching help entries.

### Help truthfulness
- Rename command help topics so the help key matches the real command whenever practical.
- Fix syntax mismatches like `group loot` versus `group lootmode`.
- Expand `joinguild` help so it reflects the secondary-domain decision point.

## Wave 2 Verdict

- **Wave 2 is structurally stable but not player-legibility clean yet.**
- The biggest problem is not missing systems; it is missing and mis-keyed guidance for systems that already exist.
- The absence of live new-player breadcrumb prompts is the most important Wave 2 issue to fix before launch-facing polish can be considered complete.
