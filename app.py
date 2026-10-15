from __future__ import annotations

import time
import cv2
import mediapipe as mp

from fitness_coach.angles import angle_degrees
from fitness_coach.exercises import ExerciseTracker

EXERCISES = ("squat", "push-up", "bicep-curl")


def main() -> None:
    print("\nAI Fitness Coach")
    print("Choose an exercise:")
    for index, exercise in enumerate(EXERCISES, start=1):
        print(f"  {index}. {exercise}")
    choice = input("Enter 1-3 [1]: ").strip() or "1"
    if choice not in {"1", "2", "3"}:
        print("Invalid choice. Starting with squat.")
        choice = "1"

    exercise = EXERCISES[int(choice) - 1]
    tracker = ExerciseTracker(exercise)
    mp_pose = mp.solutions.pose
    drawing = mp.solutions.drawing_utils
    started_at = time.monotonic()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open a webcam. Check camera permissions or connection.")
        return

    try:
        with mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as pose:
            while True:
                ok, frame = camera.read()
                if not ok:
                    print("Could not read a frame from the webcam.")
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = pose.process(rgb)
                feedback = "Move into camera view"
                angle = None

                if result.pose_landmarks:
                    landmarks = result.pose_landmarks.landmark
                    height, width = frame.shape[:2]

                    def point(name: str) -> tuple[float, float] | None:
                        landmark = landmarks[getattr(mp_pose.PoseLandmark, name).value]
                        if landmark.visibility < 0.45:
                            return None
                        return (landmark.x * width, landmark.y * height)

                    if exercise == "squat":
                        hip, knee, ankle = point("LEFT_HIP"), point("LEFT_KNEE"), point("LEFT_ANKLE")
                        angle = angle_degrees(hip, knee, ankle)
                    elif exercise == "push-up":
                        shoulder, elbow, wrist = point("LEFT_SHOULDER"), point("LEFT_ELBOW"), point("LEFT_WRIST")
                        angle = angle_degrees(shoulder, elbow, wrist)
                    else:
                        shoulder, elbow, wrist = point("LEFT_SHOULDER"), point("LEFT_ELBOW"), point("LEFT_WRIST")
                        angle = angle_degrees(shoulder, elbow, wrist)

                    feedback = tracker.update(angle)
                    drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                elapsed = int(time.monotonic() - started_at)
                cv2.rectangle(frame, (10, 10), (430, 125), (20, 20, 20), -1)
                cv2.putText(frame, f"Exercise: {exercise}", (22, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"Reps: {tracker.reps}", (22, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (90, 230, 130), 2)
                cv2.putText(frame, f"Angle: {angle:.0f} deg" if angle is not None else "Angle: --", (22, 96), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(frame, feedback[:52], (22, 116), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 220, 255), 1)
                cv2.putText(frame, f"Time: {elapsed}s | q: quit", (10, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.imshow("AI Fitness Coach", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        camera.release()
        cv2.destroyAllWindows()
        print(f"Session complete — {tracker.reps} reps in {int(time.monotonic() - started_at)} seconds.")


if __name__ == "__main__":
    main()
