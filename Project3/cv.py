import numpy as np
import cv2
import glob

skip_frames = 10
frames = []
for vid in glob.glob('videos_small/*'):


    cap = cv2.VideoCapture(vid)
    ret = True

    i = 0
    frame_n = 0
    while ret:
        ret, frame = cap.read()
        i += 1
        if i % skip_frames == 0:
            frame_n += 1
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    frames.append(frame_n)
    cap.release()


print(frames)
cv2.destroyAllWindows()