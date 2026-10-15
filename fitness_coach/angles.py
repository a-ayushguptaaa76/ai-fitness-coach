from __future__ import annotations

import math
from typing import Sequence


def angle_degrees(
    a: Sequence[float] | None,
    b: Sequence[float] | None,
    c: Sequence[float] | None,
) -> float | None:
    """Return the angle ABC in degrees, or None for missing/degenerate points."""
    if a is None or b is None or c is None:
        return None

    ba = (float(a[0]) - float(b[0]), float(a[1]) - float(b[1]))
    bc = (float(c[0]) - float(b[0]), float(c[1]) - float(b[1]))
    mag_ba = math.hypot(*ba)
    mag_bc = math.hypot(*bc)
    if mag_ba == 0 or mag_bc == 0:
        return None

    cosine = (ba[0] * bc[0] + ba[1] * bc[1]) / (mag_ba * mag_bc)
    cosine = max(-1.0, min(1.0, cosine))
    return math.degrees(math.acos(cosine))
