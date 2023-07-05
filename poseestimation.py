import mediapipe as mp
import cv2
import numpy as np

# initialize pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
stop_req = False
draw_allowed = False
# link to landmarks image
# https://developers.google.com/static/mediapipe/images/solutions/pose_landmarks_index.png


class Cameras(enumerate):
    BUILTIN = 0
    WEBCAM = 2


class PoseEstimation:
    def __init__(self, camera_num=Cameras.BUILTIN):
        # realtime pose estimation
        self.camera_num = camera_num
        self.cap = None
        self.stop_req = False
        self.pose_data = None
        self.image = None
        self.results = None

    def process(self):
        image = self.image
        # Make detection
        self.results = pose.process(image)

    def analyze(self):
        results = self.results
        # Recolor back to BGR
        if draw_allowed:
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            left_shoulder = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
            ]
            left_elbow = [
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
            ]
            left_wrist = [
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
            ]
            # Calculate angle
            left_elbow_angle = self.calculate_angle(
                left_shoulder, left_elbow, left_wrist
            )

            right_shoulder = [
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
            ]
            right_elbow = [
                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
            ]
            right_wrist = [
                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
            ]
            # Calculate angle
            right_elbow_angle = self.calculate_angle(
                right_shoulder, right_elbow, right_wrist
            )

            right_upperarm_angle = self.calculate_angle(
                left_shoulder, right_shoulder, right_elbow
            )

            if draw_allowed:
                # Visualize angle
                cv2.putText(
                    image,
                    str(left_elbow_angle),
                    tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

                cv2.putText(
                    image,
                    str(right_upperarm_angle),
                    tuple(np.multiply(right_shoulder, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

        except:
            pass

        if draw_allowed:
            # Render detections
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(245, 117, 66), thickness=2, circle_radius=2
                ),
                mp_drawing.DrawingSpec(
                    color=(245, 66, 230), thickness=2, circle_radius=2
                ),
            )

            cv2.imshow("Mediapipe Feed", image)

    def run(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.camera_num)

        ## Setup mediapipe instance
        with mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as pose:
            if self.cap.isOpened():
                ret, frame = self.cap.read()

                # Recolor image to RGB
                self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image.flags.writeable = False

        if cv2.waitKey(10) & 0xFF == ord("q"):
            stop_req = True
            self.cap.release()
            cv2.destroyAllWindows()
            return None

        return self.pose_data

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
            a[1] - b[1], a[0] - b[0]
        )
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def kill(self):
        stop_req = True
        if self.cap != None:
            self.cap.release()
        self.cap = None
        cv2.destroyAllWindows()


if __name__ == "__main__":
    pose_estimation = PoseEstimation()
    pose_estimation.run()
