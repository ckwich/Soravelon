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

    # World-state decay — fires every 24 real hours (86400 seconds)
    TICKER_HANDLER.add(
        interval=86400,
        callback="world.world_state.world_state_decay_tick",
        idstring="world_state_decay",
        persistent=True,
    )

    # Session XP safety flush — fires every 10 minutes (600 seconds)
    TICKER_HANDLER.add(
        interval=600,
        callback="world.world_state.session_xp_safety_flush",
        idstring="session_xp_flush",
        persistent=True,
    )

    # Node failure tick — fires every 30 seconds
    TICKER_HANDLER.add(
        interval=30,
        callback="world.node_helpers.node_failure_tick",
        idstring="node_failure_tick",
        persistent=True,
    )

    # Banking recurring payment processing — daily
    TICKER_HANDLER.add(
        interval=86400,
        callback="world.banking.banking_payment_tick",
        idstring="banking_payment_tick",
        persistent=True,
    )

    # Recover any orphaned Layer 1 rooms from crash/restart
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
