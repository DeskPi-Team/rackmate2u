import tkinter
import RPi.GPIO as GPIO
import time
import subprocess as sp
import threading


led = 14
btn = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(btn, GPIO.IN)

def callback():
    for i in range(0, 10):
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.2)


def shut():
    sp.getoutput('shutdown -h now')


i = ''
def update():
    global i
    while True:
        i = sp.getoutput('vcgencmd measure_temp')
        newlabel['text'] = str(i)
        time.sleep(1)
        if GPIO.input(btn) == 0:
            GPIO.output(led, GPIO.LOW)
            time.sleep(3)
            if GPIO.input(btn) == 0:
                newlabel['text'] = 'system is going to shutdown'
                time.sleep(3)
                sp.getoutput("shutdown -h now")

try:
    root = tkinter.Tk()
    root.title("Raspberry Pi ID check")

    root.geometry('300x150')

    label = tkinter.Label(root, text="ID Button Check")
    label.pack()

    idBtn = tkinter.Button(root, text="ID Button", command=callback)
    idBtn.pack()

    btn2 = tkinter.Button(root, text="Shutdown", command=shut)
    btn2.pack()

    newlabel = tkinter.Label(root, text="Temperature")
    newlabel.pack()

    update_thread = threading.Thread(target=update)
    update_thread.start()

    root.mainloop()
except KeyboardInterrupt:
    print("Quit")

