import cv2
import math as m
import mediapipe as mp

# Функция поиска расстояния между двумя точками по их координатам

def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


# Функция поиска угла

def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

# Константные переменные

good_frames = 0
bad_frames = 0

font = cv2.FONT_HERSHEY_SIMPLEX

blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Основной цикл

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        h, w = frame.shape[:2]
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Поиск лендмарков

        try:
            landmarks = results.pose_landmarks.landmark
        except:
            continue

        # Получение точек тела

        l_shldr_x = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w)
        l_shldr_y = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h)

        r_shldr_x = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w)
        r_shldr_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h)

        l_ear_x = int(landmarks[mp_pose.PoseLandmark.LEFT_EAR].x * w)
        l_ear_y = int(landmarks[mp_pose.PoseLandmark.LEFT_EAR].y * h)

        l_hip_x = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * w)
        l_hip_y = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * h)

        offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)




cv2.destroyAllWindows()
