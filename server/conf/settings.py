r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *
import os


_social_renderer_enabled = os.environ.get("SOCIAL_RENDERER_ENABLED", "false")
if _social_renderer_enabled.strip().lower() not in {"0", "false", "no", "off", "1", "true", "yes", "on"}:
    raise RuntimeError(
        "SOCIAL_RENDERER_ENABLED must be a boolean value when configured."
    )
SOCIAL_RENDERER_ENABLED = _social_renderer_enabled.strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "soravelon"

# Soravelon custom Django apps
INSTALLED_APPS = INSTALLED_APPS + ["world"]

# Soravelon typeclass defaults
BASE_OBJECT_TYPECLASS = "typeclasses.objects.SoravelonObject"
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"
BASE_ROOM_TYPECLASS = "typeclasses.rooms.SoravelonRoom"
BASE_EXIT_TYPECLASS = "typeclasses.exits.SoravelonExit"
BASE_SCRIPT_TYPECLASS = "typeclasses.scripts.SoravelonScript"
BASE_ACCOUNT_TYPECLASS = "typeclasses.accounts.SoravelonAccount"
FILE_HELP_ENTRY_MODULES = ["world.help_entries"]

SORAVELON_DOMAIN_CHANNELS = (
    "combat",
    "subterfuge",
    "naturalism",
    "resonance",
    "arcana",
    "diplomacy",
    "alchemy",
    "tactics",
    "engineering",
    "remnance",
)

# Staff-only connection log. This must stay separate from DEFAULT_CHANNELS:
# Evennia auto-subscribes every new account to every default channel, while
# MudInfo intentionally denies non-admin listeners.
CHANNEL_MUDINFO = {
    "key": "MudInfo",
    "aliases": "",
    "desc": "Connection log",
    "locks": "control:perm(Admin);listen:perm(Admin);send:false()",
}

# Channel configuration — player auto-subscriptions
DEFAULT_CHANNELS = [
    {
        "key": "Public",
        "aliases": ("pub",),
        "desc": "Public discussion",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
    {
        "key": "OOC",
        "aliases": ("ooc",),
        "desc": "Server-wide out-of-character chat",
        "locks": "control:perm(Admin);listen:all();send:all()",
        "typeclass": "typeclasses.channels.OOCChannel",
    },
]

DEFAULT_CHANNELS.extend(
    {
        "key": domain_name.title(),
        "aliases": (domain_name,),
        "desc": f"{domain_name.title()} domain chat",
        "locks": "control:perm(Admin);listen:all();send:all()",
        "typeclass": "typeclasses.channels.DomainChannel",
        "attrs": [("domain_name", domain_name)],
    }
    for domain_name in SORAVELON_DOMAIN_CHANNELS
)

SORAVELON_ENV = os.environ.get("SORAVELON_ENV", "development").lower()
if SORAVELON_ENV == "production":
    from server.conf.production_settings import *
elif SORAVELON_ENV == "development":
    ######################################################################
    # Development-only settings from an ignored local file.
    ######################################################################
    try:
        from server.conf.secret_settings import *
    except ModuleNotFoundError as exc:
        if exc.name != "server.conf.secret_settings":
            raise
else:
    raise RuntimeError(
        f"Unsupported SORAVELON_ENV '{SORAVELON_ENV}'. "
        "Expected 'development' or 'production'."
    )
