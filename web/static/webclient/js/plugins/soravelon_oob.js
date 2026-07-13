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
    let accessibilityPassScheduled = false;

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

    function applyAccessibilityLabels() {
        document.querySelectorAll(".inputfield").forEach(function (input) {
            input.setAttribute("aria-label", "Command input");
            input.setAttribute("autocomplete", "off");
            input.setAttribute("spellcheck", "false");
        });
        document.querySelectorAll(".inputsend").forEach(function (button) {
            button.setAttribute("aria-label", "Send command");
            button.setAttribute("title", "Send command");
        });
        document.querySelectorAll(".content").forEach(function (output) {
            output.setAttribute("role", "log");
            output.setAttribute("aria-live", "polite");
            if (!output.hasAttribute("aria-label")) {
                output.setAttribute("aria-label", "Game output");
            }
        });
    }

    function bindAccessibilityToLayout() {
        const layoutPlugin = window.plugins && window.plugins.goldenlayout;
        const layout = layoutPlugin && layoutPlugin.getGL();
        if (!layout || layout.soravelonAccessibilityBound) {
            return;
        }
        layout.soravelonAccessibilityBound = true;
        layout.on("stateChanged", scheduleAccessibilityPass);
    }

    function scheduleAccessibilityPass() {
        if (accessibilityPassScheduled) {
            return;
        }
        accessibilityPassScheduled = true;
        window.setTimeout(function () {
            accessibilityPassScheduled = false;
            bindAccessibilityToLayout();
            applyAccessibilityLabels();
        }, 0);
    }

    function postInit() {
        bindAccessibilityToLayout();
        applyAccessibilityLabels();
    }

    function onLayoutChanged() {
        bindAccessibilityToLayout();
        scheduleAccessibilityPass();
    }

    window.plugin_handler.add("soravelon_oob", {
        init: init,
        postInit: postInit,
        onLayoutChanged: onLayoutChanged,
    });
}());
