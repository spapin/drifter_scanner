"""
Custom RxPy operator to detect drifter wormhole connections from jump events.
"""
from reactivex import operators as ops
from drifter_scanner.models.drifter_connection import DrifterConnection


DRIFTER_WORMHOLES = {
    "Sentinel MZ",
    "Liberated Barbican",
    "Sanctified Vidette",
    "Conflux Eyrie",
    "Azdaja Redoubt"
}


def detect_drifter_connections():
    """Operator that detects drifter connections from pairs of jump events."""

    def detect_connection(pair):
        if len(pair) != 2:
            return []

        prev, curr = pair

        if prev.system == curr.system:
            return []

        prev_is_drifter = prev.system in DRIFTER_WORMHOLES
        curr_is_drifter = curr.system in DRIFTER_WORMHOLES

        if prev_is_drifter or curr_is_drifter:
            drifter_wh = curr.system if curr_is_drifter else prev.system
            regular_sys = prev.system if curr_is_drifter else curr.system
            return [DrifterConnection(
                system=regular_sys,
                drifter_wormhole=drifter_wh,
                seen_at=curr.visited_at
            )]
        return []

    return ops.compose(
        ops.group_by(lambda jump: jump.character_id),
        ops.flat_map(lambda group: group.pipe(
            ops.buffer_with_count(2, 1),
            ops.flat_map(detect_connection)
        ))
    )
