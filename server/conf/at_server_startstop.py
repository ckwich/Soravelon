"""
Server startstop hooks

This module contains functions called by Evennia at various
points during its startup, reload and shutdown sequence. It
allows for customizing the server operation as desired.

This module must contain at least these global functions:

at_server_init()
at_server_start()
at_server_stop()
at_server_reload_start()
at_server_reload_stop()
at_server_cold_start()
at_server_cold_stop()

"""


def at_server_init():
    """
    This is called first as the server is starting up, regardless of how.
    """
    pass


def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    from evennia import TICKER_HANDLER
    from world.banking import banking_payment_tick
    from world.dialogue_engine import ambient_npc_tick
    from world.mob_spawner import spawn_tick
    from world.social_engine import social_propagation_tick
    from world.node_helpers import node_failure_tick
    from world.wander_system import wander_tick
    from world.world_state import (
        session_xp_safety_flush,
        world_state_decay_tick,
    )

    # World-state decay — fires every 24 real hours (86400 seconds)
    TICKER_HANDLER.add(
        interval=86400,
        callback=world_state_decay_tick,
        idstring="world_state_decay",
        persistent=True,
    )

    # Session XP safety flush — fires every 10 minutes (600 seconds)
    TICKER_HANDLER.add(
        interval=600,
        callback=session_xp_safety_flush,
        idstring="session_xp_flush",
        persistent=True,
    )

    # Node failure tick — fires every 30 seconds
    TICKER_HANDLER.add(
        interval=30,
        callback=node_failure_tick,
        idstring="node_failure_tick",
        persistent=True,
    )

    # Banking recurring payment processing — daily
    TICKER_HANDLER.add(
        interval=86400,
        callback=banking_payment_tick,
        idstring="banking_payment_tick",
        persistent=True,
    )

    # Mob spawn ticker — processes due SpawnRecords every 60s (D-02)
    TICKER_HANDLER.add(
        interval=60,
        callback=spawn_tick,
        idstring="spawn_tick",
        persistent=True,
    )

    # Wandering mob movement — fires every 60 seconds (D-27)
    TICKER_HANDLER.add(
        interval=60,
        callback=wander_tick,
        idstring="wander_tick",
        persistent=True,
    )

    # NPC ambient idle echoes — fires every 15 seconds (NPC-01)
    TICKER_HANDLER.add(
        interval=15,
        callback=ambient_npc_tick,
        idstring="npc_ambient_tick",
        persistent=True,
    )

    # Social Web propagation — moves one bounded graph batch per minute.
    TICKER_HANDLER.add(
        interval=60,
        callback=social_propagation_tick,
        idstring="social_propagation_tick",
        persistent=True,
    )

    # Authored content is applied explicitly through `worldcontent`; startup
    # only proves source/runtime authority and hydrates process-local registries.
    from pathlib import Path
    from django.conf import settings
    from world.content_revisions import load_applied_world_content

    load_applied_world_content(Path(settings.GAME_DIR) / "world" / "areas")

    # Recover dynamic Layer 1 rooms only after immutable content is verified.
    from world.node_helpers import initialize_node_pool
    initialize_node_pool()

def at_server_stop():
    """
    This is called just before the server is shut down, regardless
    of it is for a reload, reset or shutdown.
    """
    pass


def at_server_reload_start():
    """
    This is called only when server starts back up after a reload.
    """
    pass


def at_server_reload_stop():
    """
    This is called only time the server stops before a reload.
    """
    pass


def at_server_cold_start():
    """
    This is called only when the server starts "cold", i.e. after a
    shutdown or a reset.
    """
    pass


def at_server_cold_stop():
    """
    This is called only when the server goes down due to a shutdown or
    reset.
    """
    pass
