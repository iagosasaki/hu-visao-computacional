import numpy as np
import cv2 
import time
from pynput.keyboard import Controller

keyboard = Controller()

width, height = 1280, 720
cam = cv2.VideoCapture(0)
cam.set(3, width)
cam.set(4, height)

start_time = 0
elapsed_time = 0
running = False

while True:
    success, img = cam.read()
    if not success:
        print("Erro ao acessar camera.")
        break

    if running:
        elapsed_time = time.time() - start_time

    minutos = int(elapsed_time // 60)
    segundos = int(elapsed_time % 60)
    timer = f"{minutos:02}:{segundos:02}"

    cv2.putText(img, f"Tempo: {timer}", (50, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(img, "Pressione:'t' para iniciar/zerar e 'c' para sair",
                (50, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Image", img)
    keyCV = cv2.waitKey(1) & 0xFF

    if keyCV == ord('c'):
        break

    if keyCV == ord('t'):
        if not running:
            start_time = time.time()
            elapsed_time = 0
            running = True
        else:
            running = False
            elapsed_time = 0

cam.release()
cv2.destroyAllWindows()
