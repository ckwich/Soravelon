/*
 * Soravelon compatibility bridge for Evennia's stock webclient.
 *
 * The dedicated player client will own structured status, map, combat, quest,
 * and inventory presentation after hosting. Until then, the stock client must
 * claim these supported events so Evennia does not render their JSON as an
 * unknown-command error. The latest payload remains available to project-owned
 * widgets without exposing hidden numeric state in the story pane.
 */
(function () {
    "use strict";

    const SORAVELON_OOB_EVENTS = Object.freeze([
        "combat_update",
        "flight_progress",
        "inventory_update",
        "map_update",
        "node_event",
        "quest_update",
        "stat_update",
        "status_update",
    ]);

    const latestState = Object.create(null);

    function receive(eventName, args, kwargs) {
        latestState[eventName] = {
            args: Array.isArray(args) ? args.slice() : [],
            data: kwargs && typeof kwargs === "object" ? { ...kwargs } : {},
            receivedAt: Date.now(),
        };
    }

    function init() {
        window.soravelonState = latestState;
        SORAVELON_OOB_EVENTS.forEach(function (eventName) {
            Evennia.emitter.on(eventName, function (args, kwargs) {
                receive(eventName, args, kwargs);
            });
        });
        console.log("Soravelon OOB compatibility bridge initialized.");
    }

    window.plugin_handler.add("soravelon_oob", { init: init });
}());
