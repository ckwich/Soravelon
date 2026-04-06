"""
FlightScript — per-player Dragon Courier in-flight state machine.

Attached to a Character when they board the Dragon Courier.
Uses evennia.utils.utils.delay() for all timed events — never time.sleep().

Key behaviors:
- start_journey() sets ndb.in_flight=True; begins first leg
- _begin_leg() schedules delay(leg_duration, _arrive_at_stop) and any mid-leg echoes
- _arrive_at_stop() moves player to stop room; gives 10s disembark window at intermediate stops
- _arrive_final() clears ndb.in_flight and calls self.stop()
- do_disembark() called by CmdDisembark; ends flight at current location
- fare_paid initialized False in at_script_creation (set True by book_flight before start_journey)
  This guards against double-deduction on server reload (Pitfall 6)
"""

from typeclasses.scripts import SoravelonScript


class FlightScript(SoravelonScript):
    """
    Manages per-player Dragon Courier flight traversal.

    db.legs: list of leg dicts [{from_point_id, to_point_id, to_room_id, duration, echoes}]
    db.current_leg: index of the currently executing leg
    db.in_transit: True while flight is active
    db.fare_paid: True once fare has been deducted (book_flight sets this before start_journey)
    """

    def at_script_creation(self):
        super().at_script_creation()
        self.key = "flight_script"
        self.persistent = True
        self.interval = 0      # NOT self-ticking — uses delay() for leg timing
        self.repeats = 0
        self.db.legs = []          # list of leg dicts from book_flight()
        self.db.current_leg = 0
        self.db.in_transit = False
        self.db.fare_paid = False  # Pitfall 6: set True in book_flight(), not here
        self.tags.add("flight_script", category="script_type")

    def at_start(self):
        """
        Called on creation AND on server reload. Resume or safely land.

        If the script has persisted flight state (db.in_transit with legs),
        resume from the current leg. Otherwise, if the character was mid-flight,
        safely land them at the last known stop.
        """
        super().at_start()
        character = self.obj
        if not character or not character.pk:
            self.stop()
            return

        if not self.db.in_transit:
            return

        # Server reloaded mid-flight — restore volatile flag
        character.ndb.in_flight = True

        legs = list(self.db.legs or [])
        current = self.db.current_leg or 0

        if current >= len(legs):
            # Was at or past final stop — land immediately
            self._arrive_final()
            return

        # Resume from current leg
        self._begin_leg()

    def start_journey(self):
        """
        Called once by book_flight() after fare deduction.

        Sets ndb.in_flight, sends departure message, begins first leg.
        Does NOT deduct fare — fare_paid flag is already set by book_flight().
        """
        character = self.obj
        if not character:
            return
        character.ndb.in_flight = True
        character.msg("The dragon spreads its wings. You are airborne!")
        self._begin_leg()

    def _begin_leg(self):
        """Schedule current leg: send echo toward destination and arm delay timer."""
        character = self.obj
        if not character or not character.pk:
            self.stop()
            return

        legs = list(self.db.legs or [])
        current = self.db.current_leg
        if current >= len(legs):
            self._arrive_final()
            return

        leg = legs[current]

        # Announce destination
        from world.flight_registry import FlightRegistry
        to_point = FlightRegistry.get_point(leg["to_point_id"])
        dest_name = to_point["name"] if to_point else leg["to_point_id"]
        character.msg(f"Your dragon banks toward {dest_name}.")

        # Schedule any mid-leg atmospheric echo messages
        from evennia.utils.utils import delay
        for echo_def in leg.get("echoes", []):
            echo_delay = echo_def.get("delay", 10)
            echo_msg = echo_def.get("message", "")
            if echo_msg:
                delay(echo_delay, lambda m=echo_msg: self._send_echo(m))

        # Schedule arrival at end of leg duration (D-10: minimum 30s)
        delay(leg["duration"], self._arrive_at_stop)

        # OOB: notify client of flight progress (CLI-06)
        from world import oob_publisher
        total_legs = len(list(self.db.legs or []))
        oob_publisher.push_flight_progress(
            character,
            leg_index=self.db.current_leg,
            total_legs=total_legs,
            destination_name=dest_name,
            disembark_available=False,
        )

    def _send_echo(self, message):
        """Send a mid-leg atmospheric echo message if character still present."""
        character = self.obj
        if character and character.pk:
            character.msg(message)

    def _arrive_at_stop(self):
        """
        Move player to the next stop room.

        At intermediate stops, gives a 10-second disembark window before
        automatically continuing to the next leg (D-11).
        At the final stop, calls _arrive_final().
        """
        character = self.obj
        if not character or not character.pk:
            self.stop()
            return

        legs = list(self.db.legs or [])
        current = self.db.current_leg
        if current >= len(legs):
            self._arrive_final()
            return

        leg = legs[current]

        # Move player to the stop room
        import evennia
        stop_rooms = evennia.search_object(f"#{leg['to_room_id']}", exact=True)
        if stop_rooms:
            character.move_to(stop_rooms[0], quiet=True, move_hooks=False)
            character.msg("Your dragon circles and lands at the courier stop.")

        # Advance leg counter
        self.db.current_leg = current + 1

        # Final stop — land and finish
        if self.db.current_leg >= len(legs):
            self._arrive_final()
        else:
            # Intermediate stop — give player a disembark window (D-11)
            character.msg("Type |wdisembark|n to stay here, or remain seated to continue.")
            # OOB: notify client of intermediate arrival (disembark_available=True) (CLI-06)
            from world import oob_publisher
            _legs = list(self.db.legs or [])
            _cur = self.db.current_leg
            _leg = _legs[_cur - 1] if 0 < _cur <= len(_legs) else {}
            from world.flight_registry import FlightRegistry
            _to_point = FlightRegistry.get_point(_leg.get("to_point_id", ""))
            _dest_name = _to_point["name"] if _to_point else _leg.get("to_point_id", "")
            oob_publisher.push_flight_progress(
                character,
                leg_index=_cur - 1,
                total_legs=len(_legs),
                destination_name=_dest_name,
                disembark_available=True,
            )
            from evennia.utils.utils import delay
            delay(10, self._check_continue)

    def _check_continue(self):
        """
        If player has not disembarked within the window, continue to next leg.
        """
        character = self.obj
        if not character or not character.pk:
            self.stop()
            return
        if not character.ndb.in_flight:
            # Player disembarked during the window
            return
        self._begin_leg()

    def _arrive_final(self):
        """
        End the flight at the final destination.
        Clears ndb.in_flight and stops the script.
        """
        character = self.obj
        if character and character.pk:
            character.ndb.in_flight = False
            character.msg("Your dragon lands. You have arrived at your destination.")
            # OOB: final landing — push flight_progress (complete) and map_update (Pitfall 6)
            from world import oob_publisher
            _total = len(list(self.db.legs or []))
            oob_publisher.push_flight_progress(
                character,
                leg_index=_total,
                total_legs=_total,
                destination_name="",
                disembark_available=False,
            )
            oob_publisher.push_map_update(character)
        self.stop()

    def do_disembark(self):
        """
        Called by CmdDisembark. Ends flight at current location immediately.
        Clears ndb.in_flight and stops the script.
        """
        character = self.obj
        if character:
            character.ndb.in_flight = False
            character.msg("You disembark from the Dragon Courier.")
        self.stop()
