from __future__ import annotations


class ExerciseTracker:
    """Simple angle-threshold repetition counter for a single exercise."""

    def __init__(self, exercise: str) -> None:
        allowed = {"squat", "push-up", "bicep-curl"}
        if exercise not in allowed:
            raise ValueError(f"exercise must be one of: {', '.join(sorted(allowed))}")
        self.exercise = exercise
        self.reps = 0
        self._phase = "up"

    def update(self, angle: float | None) -> str:
        """Update the movement state from a joint angle and return a short cue."""
        if angle is None:
            return "Keep the full movement in view"

        if self.exercise == "squat":
            down, up = 105, 160
            low_cue = "Lower under control"
            high_cue = "Stand tall to finish"
        elif self.exercise == "push-up":
            down, up = 95, 155
            low_cue = "Lower with control"
            high_cue = "Press back up"
        else:
            down, up = 55, 150
            low_cue = "Curl smoothly"
            high_cue = "Extend with control"

        if angle <= down and self._phase == "up":
            self._phase = "down"
            return low_cue
        if angle >= up and self._phase == "down":
            self._phase = "up"
            self.reps += 1
            return f"Rep {self.reps} — good, reset smoothly"
        return "Move through a comfortable range"
