import cv2
import mediapipe as mp

#ts class will be used to track the hand and its position in the video screen (similarr to the drone)
class HandTracker:

    #ts class and function will be used to track the hand and its position in the video screen.
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.7
        )

    def get_hand_position(self, width, height):
        success, frame = self.cap.read()
        if not success or frame is None:
            return None, None, None

        frame = cv2.resize(frame, (width, height))
        #this will flip the frame horizontally (got it from online resources )
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        obj_x, obj_y = None, None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                obj_x = int((1.0 - index_tip.x) * width)
                obj_y = int(index_tip.y * height)

        return obj_x, obj_y, frame

    def release(self):
        """This will release the camera and close the window when the game is closed"""
        self.cap.release()
        cv2.destroyAllWindows()