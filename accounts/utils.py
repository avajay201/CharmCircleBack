import cv2
import face_recognition
import mediapipe as mp
import numpy as np
import os
from rest_framework.response import Response
from rest_framework import status


face_mesh = mp.solutions.face_mesh
face_mesh_detection = face_mesh.FaceMesh(max_num_faces=2, refine_landmarks=True, min_detection_confidence=0.6)


def detection_process(img):
    result = face_detection_process(img)
    if result == 'Error':
        return Response({'error': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if result:
        if len(result) > 1:
            return Response({'error': 'Multipe face detected!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)

    return Response({'error': 'Face not detected!'}, status=status.HTTP_400_BAD_REQUEST)

def face_detection_process(image):
    try:
        file_bytes = np.frombuffer(image.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            raise FileNotFoundError(f"Image not found")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = face_recognition.face_locations(img_rgb)
        return results
    except Exception as err:
        print('Face detection error:', err)
        return 'Error'

def profile_verification(image1, image2):
    try:
        biden_encoding = face_recognition.face_encodings(image1)[0]
        unknown_encoding = face_recognition.face_encodings(image2)[0]

        results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

        return results[0]
    except:
        return

def verify_profile(video, img):
    cap = cv2.VideoCapture(video)
    face_detected = False
    RIGHT_EYE_INDICES = [33, 133, 160, 159, 158, 157, 173, 153, 154, 155, 144, 163, 7, 246, 161, 160, 159, 158, 157, 173,
                     153, 154, 155, 133, 33]
    LEFT_IRIS_INDICES = [474, 475, 476, 477]
    LEFT_EYE_INDICES = [362, 263, 387, 386, 385, 384, 398, 382, 381, 380, 373, 390, 249, 466, 388, 387, 386, 385, 384, 398,
                        382, 381, 380, 362, 263]
    RIGHT_IRIS_INDICES = [471, 469, 470, 472]

    eyes_results = []
    first_frame = None
    last_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = face_mesh_detection.process(rgb_frame)
        if not results.multi_face_landmarks:
            face_detected = False
            break

        face_detected = True
        if len(results.multi_face_landmarks) > 1:
            face_detected = False
            break

        if first_frame is None:
            first_frame = rgb_frame.copy()

        last_frame = rgb_frame.copy()

        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = frame.shape

        left_eye = []
        right_eye = []

        for idx, landmark in enumerate(face_landmarks.landmark):
            left_iris = []
            right_iris = []
            x, y = int(landmark.x * w), int(landmark.y * h)
            # eyes detection
            if idx in LEFT_IRIS_INDICES:
                left_iris.append((x, y))
            if idx in RIGHT_IRIS_INDICES:
                right_iris.append((x, y))
            if idx in LEFT_EYE_INDICES:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            if idx in RIGHT_EYE_INDICES:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            if idx in [159, 145]:
                right_eye.append((x, y))
            if idx in [386, 374]:
                left_eye.append((x, y))

        # eyes status
        left_eye_status = 'Open'
        right_eye_status = 'Open'
        if (right_eye[0][1] - right_eye[1][1]) < 10:
            right_eye_status = 'Close'
        if (left_eye[0][1] - left_eye[1][1]) < 10:
            left_eye_status = 'Close'
        # cv2.putText(frame, right_eye_status, (right_eye[0][0] - 30, right_eye[0][1] - 40),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(frame, left_eye_status, (left_eye[0][0] - 30, left_eye[0][1] - 40),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        eyes_results.append(left_eye_status)
        eyes_results.append(right_eye_status)

        # cv2.imshow('Video', frame)
        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()
    file_bytes = np.frombuffer(img.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if face_detected and first_frame is not None and last_frame is not None:
        status = verify_eyes_movement(eyes_results)
        if status:
            status = profile_verification(rgb_image, first_frame)
            if status == True:
                status = profile_verification(rgb_image, last_frame)
    else:
        status = False

    return status

def verify_eyes_movement(r):
    if r.count('Close') >= 15 and r.count('Open') > r.count('Close'):
        return True

if __name__ == '__main__':
    try:
        video = r"C:\Projects\CharmCircleB\temps\61291-498228511_large.mp4"
        image = r"C:\Users\ajayv\Downloads\download.jpeg"
        verification = verify_profile(video, image)
        if verification == True:
            print('Verified')
        else:
            print('Not verified')
    except Exception as err:
        print('Error:', err)
    pass
