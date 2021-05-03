# All media file is available for download as a zip file
import tkinter
import cv2  # pip install opencv-python
import PIL.Image
import PIL.ImageTk  # pip install pillow
from functools import partial
import threading
import time
import imutils  # pip install imutils
from tkinter import messagebox as msg
from tkinter.ttk import *
from pathlib import Path
from tkinter.filedialog import askopenfilename, asksaveasfile, askdirectory


stream = cv2.VideoCapture("assets/video_files/clip.mp4")

flag = True


def play(speed):
    global flag
    global stream
    print(f"You clicked on play. Speed is {speed}")

    # Play the video in reverse mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 26, fill="black",
                           font="Times 26 bold", text="Decision Pending")
    flag = not flag


def pending(decision):
    # 1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("assets/images/pending.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    # 2. Wait for 1 second
    time.sleep(1.5)

    # 3. Display sponsor image
    frame = cv2.cvtColor(cv2.imread("assets/images/drs.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    # 4. Wait for 1.5 second
    time.sleep(2.5)
    # 5. Display out/notout image
    if decision == 'out':
        decisionImg = "assets/images/out.jpg"
    else:
        decisionImg = "assets/images/not_out.jpg"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")


def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")


def openFileDialog():
    global stream
    file = askopenfilename(filetypes=(("Video Files", "*"),
                                      ),
                           title='Open File',
                           initialdir=str(Path.home()))
    if file:
        print(file)
        stream = cv2.VideoCapture(file)

    else:
        print('Cancelled')


def vidName():
    ws = tkinter.Tk()
    ws.title("Video Name!!")
    ws.geometry("250x150")
    frame = Frame(ws)
    label = tkinter.Label(frame, text="Enter name of video with file extension(.mp4,.avi)",font=("Arial",8))
    label.grid(row=0, columnspan=2, pady=10)
    userInput = Entry(frame, width=40,)
    userInput.grid(row=1, columnspan=3, padx=5, pady=10)

    Button(frame, text="save ", command=lambda: CaptureVidFromCamera(
        userInput.get())).grid(row=2, columnspan=2)

    frame.pack()

    ws.mainloop()


def CaptureVidFromCamera(vidNames):
    
    print(vidNames)
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("assets/video_files/"+ vidNames, fourcc, 20.0, (640, 480))
    

    while(cap.isOpened()):
        ret, frame = cap.read()
        if(ret == True):
            out.write(frame)
            cv2.imshow("Show Video", frame)
            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


def popupMsg():
    popup = tkinter.Toplevel(window)
    popup.grab_set()
    popup.lift
    popup.geometry("250x100")
    popup.wm_title("!")
    #label = tkinter.Label(popup, text="")
    #label.pack(side="top", fill="x", pady=10)
    B1 = tkinter.Button(
        popup, text="Capture Video From Camera?", command=vidName)
    B1.pack(pady=10)
    B1 = tkinter.Button(popup, text="Take Review", command=openFileDialog)
    B1.pack()
    popup.mainloop()


# Width and height of our main screen
SET_WIDTH = 676
SET_HEIGHT = 368

# Tkinter gui starts here

window = tkinter.Tk()
#window.withdraw
window.title("CodeWithHarry Third Umpire Decision Review Kit")
cv_img = cv2.cvtColor(cv2.imread("assets/images/welcome.jpg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()


# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)",
                     width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)",
                     width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>",
                     width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>",
                     width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()
popupMsg()
window.mainloop()
