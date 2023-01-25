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

        # Инструкция, которая регулирует положение пользователя

        if offset < 100:
            cv2.putText(image, ' Aligned', (w - 200, 30), font, 0.9, green, 2)
        else:
            cv2.putText(image, ' Turn sideways', (w - 300, 30), font, 0.9, red, 2)

        # Поиск углов

        neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
        torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

        # Прорисовка точек на экране

        cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
        cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
        cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
        cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)
        cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, blue, -1)

        # Вывод углов на экран

        angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

        # Блок кода, который соединяет точки на теле, при этом если выполняется "условие 1", то программа выводи
        # информацию обуглах начинает вести отсчет времени, в течении которого пользователь сидит ровно

        if neck_inclination < 40 and torso_inclination < 7:  # условие 1
            bad_frames = 0
            good_frames += 1

            cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

        # Блок кода, который соединяет точки на теле, при этом если выполняется "условие 2", то программа выводи
        # информацию обуглах начинает вести отсчет времени, в течении которого пользователь сидит криво

        else:  # Условие 2
            good_frames = 0
            bad_frames += 1

            cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

        good_time = (1 / fps) * good_frames
        bad_time = (1 / fps) * bad_frames

        # Вывод счетчика времени на экран

        if good_time > 0:
            time_string_good = 'Good Posture : ' + str(round(good_time, 1)) + 's'
            cv2.putText(image, time_string_good, (10, h - 20), font, 0.9, green, 2)
        else:
            time_string_bad = 'Bad Posture : ' + str(round(bad_time, 1)) + 's'
            cv2.putText(image, time_string_bad, (10, h - 20), font, 0.9, red, 2)

        # Нужно вывести предупрежждение о том, чтобы человек сел ровно, если он сиди криво уже минуту

        if bad_time > 60:
            cv2.putText(image, 'Sit properly!', (400, 400), font, 3, red, 2)

        cv2.imshow('frame', image)
        cv2.waitKey(1)

cv2.destroyAllWindows()
