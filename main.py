import mediapipe as mp
import cv2

# initialize pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


# pose estimation for video
cap = cv2.VideoCapture('test_video.mp4')
while cap.isOpened() and False:
    # read frame
    _, frame = cap.read()
    try:
        # resize the frame for portrait video
        frame = cv2.resize(frame, (350, 600))
        # convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # process the fram efor pose detection
        pose_results = pose.process(frame_rgb)

        print(pose_results.pose_landmarks)

        # get landmark for specific point

        # draw skeleton on the frame
        mp_drawing.draw_landmarks(
            frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('OUTPUT', frame)
    except:
        break

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# opencv - mediapipe : 3D pose estimation tool

# realtime pose estimation
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(2)
while cap.isOpened():
    # read frame
    _, frame = cap.read()
    try:
        # resize the frame for portrait video
        # frame = cv2.resize(frame, (350, 600))
        # convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # process the frame for pose detection
        pose_results = pose.process(frame_rgb)
        # print(pose_results.pose_landmarks)

        # draw skeleton on the frame
        mp_drawing.draw_landmarks(
            frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # display the frame
        cv2.imshow('Output', frame)
    except:
        break

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
