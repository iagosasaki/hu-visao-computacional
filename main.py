import numpy as np
import cv2 
import time
from pynput.keyboard import Controller
import tkinter as tk
from tkinter import messagebox

inputFrameName = None
keyboard = Controller()
studentName = None

def main():
    initScreen()

def stopSimulator():
    global inputFrameName
    if messagebox.askyesno("Fechar Simulador", "Tem certeza que deseja fechar o simulador?"):
        if inputFrameName is not None:
            inputFrameName.destroy()
        cv2.destroyAllWindows()
        exit()

def storeStudentName():
    global studentName,inputFrameName

    studentName = studentName.get().strip()
    if studentName == "":
        messagebox.showwarning("Aviso", "Por favor, insira o nome do aluno.")
    else:
        messagebox.showinfo("Bem-vindo", f"Bem-vindo ao Simulador de Cirurgia, {studentName}!")
        inputFrameName.destroy()
        initCam()

def initScreen():
    global inputFrameName, studentName

    studentName = None

    inputFrameName = tk.Tk()
    inputFrameName.title("Simulador de Cirurgia - HU")
    inputFrameName.geometry("300x200")

    studentName = tk.StringVar()

    tk.Label(inputFrameName, text="Nome do Aluno:").pack(pady=5)
    tk.Entry(inputFrameName, textvariable=studentName, width=30).pack(pady=5)
    tk.Button(inputFrameName, text="Iniciar Simulador", command=storeStudentName).pack(pady=10)
    tk.Button(inputFrameName, text="Fechar Simulador", command=stopSimulator).pack(pady=10)
    
    tk.mainloop()

def initCam():
    width, height = 1280, 720
    cam = cv2.VideoCapture(0)
    cam.set(3, width)
    cam.set(4, height)

    startTime = 0
    elapsedTime = 0
    isRunning = False

    while True:
        success, img = cam.read()
        if not success:
            print("Erro ao acessar camera.")
            break

        if isRunning:
            elapsedTime = time.time() - startTime

        minutes = int(elapsedTime // 60)
        seconds = int(elapsedTime % 60)
        timer = f"{minutes:02}:{seconds:02}"

        cv2.putText(img, f"Tempo: {timer}", (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, f"Aluno: {studentName}", (width - 400, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "Pressione:'t' para iniciar/zerar e 'c' para sair",
                    (50, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Image", img)
        keyCV = cv2.waitKey(1) & 0xFF

        if keyCV == ord('c'):
            if(timer == "00:00"):
                break

        if keyCV == ord('t'):
            if not isRunning:
                startTime = time.time()
                elapsedTime = 0
                isRunning = True
            else:
                isRunning = False
                elapsedTime = 0

    cam.release()
    cv2.destroyAllWindows()
    initScreen()

if __name__ == "__main__":
    main()