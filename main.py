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

def stopSimulator(currentWindow, windowType):
        if windowType == "user":
            if messagebox.askyesno("Fechar Simulador", "Tem certeza que deseja fechar o simulador?"):
                currentWindow.destroy()
        elif windowType == "surgery":
            if messagebox.askyesno("Fechar Seleção", "Tem certeza que deseja voltar à tela inicial?"):
                currentWindow.destroy()
                initScreen()

def storeStudentName():
    global studentName, inputFrameName

    studentName = studentName.get().strip()
    if studentName == "":
        messagebox.showwarning("Aviso", "Por favor, insira o nome do aluno.")
    else:
        messagebox.showinfo("Bem-vindo", f"Bem-vindo ao Simulador de Cirurgia, {studentName}!")
        inputFrameName.destroy()
        initSelectionSurgeryScreen()


def storeSurgeryName(surgerySelected, inputFrameName=inputFrameName):
    global surgeryName
    surgeryName = None
    if surgerySelected == 0:
        messagebox.showwarning("Aviso", "Por favor, selecione um tipo de cirurgia.")
        return
    surgeryName = f"Cirurgia {chr(64 + surgerySelected)}"
    messagebox.showinfo("Cirurgia Selecionada", "Cirurgia selecionada com sucesso!")
    inputFrameName.destroy()
    initCam()

def initScreen():
    global inputFrameName, studentName

    studentName = None

    inputFrameName = tk.Tk()
    inputFrameName.title("Simulador de Cirurgia - HU")
    inputFrameName.geometry("400x200")

    studentName = tk.StringVar()

    tk.Label(inputFrameName, text="Nome do Aluno:").pack(pady=5)
    tk.Entry(inputFrameName, textvariable=studentName, width=30).pack(pady=5)
    tk.Button(inputFrameName, text="Iniciar Simulador", command=storeStudentName).pack(pady=10)
    tk.Button(inputFrameName, text="Fechar Simulador", command=lambda: stopSimulator(inputFrameName ,"user")).pack(pady=10)
    
    tk.mainloop()

def initSelectionSurgeryScreen():
    inputFrameName = tk.Tk()
    inputFrameName.title("Seleção de Cirurgia - HU")
    inputFrameName.geometry("400x300")

    surgerySelector = tk.IntVar()

    tk.Label(inputFrameName, text="Selecione o Tipo de Cirurgia:").pack(pady=5)
    tk.Radiobutton(inputFrameName, text="Cirurgia A", variable=surgerySelector, value=1).pack(pady=5)
    tk.Radiobutton(inputFrameName, text="Cirurgia B", variable=surgerySelector, value=2).pack(pady=5)
    tk.Radiobutton(inputFrameName, text="Cirurgia C", variable=surgerySelector, value=3).pack(pady=5)
    tk.Button(inputFrameName, text="Confirmar", command=lambda: storeSurgeryName(surgerySelector.get(), inputFrameName)).pack(pady=10)
    tk.Button(inputFrameName, text="Cancelar", command=lambda: stopSimulator(inputFrameName, "surgery")).pack(pady=10)

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
        cv2.putText(img, f"Cirurgia: {surgeryName}", (width - 400, 120),
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
    initSelectionSurgeryScreen()

if __name__ == "__main__":
    main()