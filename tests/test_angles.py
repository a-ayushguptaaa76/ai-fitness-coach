import unittest

from fitness_coach.angles import angle_degrees
from fitness_coach.exercises import ExerciseTracker


class AngleTests(unittest.TestCase):
    def test_right_angle(self):
        self.assertAlmostEqual(angle_degrees((1, 0), (0, 0), (0, 1)), 90.0)

    def test_straight_angle(self):
        self.assertAlmostEqual(angle_degrees((-1, 0), (0, 0), (1, 0)), 180.0)

    def test_missing_or_degenerate_points(self):
        self.assertIsNone(angle_degrees(None, (0, 0), (1, 1)))
        self.assertIsNone(angle_degrees((0, 0), (0, 0), (1, 1)))

    def test_squat_rep_requires_down_then_up(self):
        tracker = ExerciseTracker("squat")
        tracker.update(100)
        self.assertEqual(tracker.reps, 0)
        tracker.update(170)
        self.assertEqual(tracker.reps, 1)
        tracker.update(100)
        tracker.update(170)
        self.assertEqual(tracker.reps, 2)

    def test_invalid_exercise(self):
        with self.assertRaises(ValueError):
            ExerciseTracker("deadlift")


if __name__ == "__main__":
    unittest.main()
