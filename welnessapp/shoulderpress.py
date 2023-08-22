import cv2
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
up_left = False
up_right = False
counter = 0
both_arms_raised = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        points = {}
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            points[id] = (cx,cy)

        # track landmarks for left arm
        cv2.circle(img, points[12], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[14], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[16], 15, (255,0,0), cv2.FILLED)

        # track landmarks for right arm
        cv2.circle(img, points[11], 15, (0,0,255), cv2.FILLED)
        cv2.circle(img, points[13], 15, (0,0,255), cv2.FILLED)
        cv2.circle(img, points[15], 15, (0,0,255), cv2.FILLED)

        # track hammer curls for left arm
        if not up_left and points[12][1] +40 >= points[16][1] :
            print("UP Left")
            up_left = True
        elif points[12][1] +40 < points[16][1]:
            print("Down Left")
            up_left = False

        # track hammer curls for right arm
        if not up_right and points[11][1] +40 >= points[15][1] :
            print("UP Right")
            up_right = True
        elif points[11][1] +40 < points[15][1]:
            print("Down Right")
            up_right = False

        # increment counter when both arms are raised
        if up_left and up_right:
            if not both_arms_raised:
                counter += 1
                both_arms_raised = True
        else:
            both_arms_raised = False

    cv2.putText(img, "Shoulder: " + str(counter), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
    cv2.putText(img, "Press 'x' key to exit", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("img",img)
    key = cv2.waitKey(1)
    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()