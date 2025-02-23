from Speech2Text import S2T
from Spracheingabe import Eingabe
from ChatGPT import ChatGPT
from ChatGPT import ChatGPT_temp
#from archiv.Sprachausgabe import Sprachausgabe
from googleTTS import synthesize_text
from PIL import Image, ImageTk
import threading
import tkinter as tk
import keyboard
import time
import os

running = True
global gif_label
gif_label = None  # Initialize gif_label to None

def update_gif():
    try:
        gif_image.seek(gif_image.tell() + 1)
        frame = ImageTk.PhotoImage(gif_image)
        gif_label.configure(image=frame)
        gif_label.image = frame
        delay = gif_image.info['duration']
        fenster.after(delay, update_gif)
    except EOFError:
        gif_image.seek(0)
        update_gif()

def gif_vid():
    global gif_image
    global gif_label
    global running
    if running:
        Order_Verzeichnis = os.path.dirname(os.path.abspath(__file__))
        Gif_Pfad = os.path.join(Order_Verzeichnis, "Reden.gif")
        gif_image = Image.open(Gif_Pfad)
        frame = ImageTk.PhotoImage(gif_image)
        gif_label = tk.Label(fenster, image=frame, bg="black")
        gif_label.pack()
        delay = gif_image.info['duration']
        fenster.after(delay, update_gif)
        fenster.mainloop()

def Error_bei_Speech2text():
    global running
    global gif_label
    Error = "Das habe ich leider nicht verstanden, bitte stelle deine Frage erneut"

    if gif_label is not None:
        gif_label.pack(expand=True)
    synthesize_text(Error)
    if gif_label is not None:
        gif_label.pack_forget()
    
    label2["text"] = "Achtung! Das Gepsrochene wird mit Google TTS bearbeitet."
    label["text"]= "Drücke M zum Aufnehmen deiner Frage"
    if running:
        Hirn()

def GUI():
    global fenster
    global label
    global label2

    def close():
        global running
        running = False
        fenster.destroy()

    fenster = tk.Tk()
    fenster.title("MediBot")
    w, h = fenster.winfo_screenwidth(), fenster.winfo_screenheight()
    #fenster.overrideredirect(1)
    #fenster.geometry("%dx%d+0+0" % (w, h))
    fenster.geometry("1200x800")
    fenster.configure(bg="black")
    label = tk.Label(fenster, text="Halte M gedrückt zum Sprechen", font=("Arial", 24), anchor="center",bg="black", fg="white")
    label.place(relx=0.5, rely=0.5, anchor="center")
   
    label2 = tk.Label(fenster, text="Achtung! Das Gepsrochene wird mit Google TTS bearbeitet.",font=("Arial", 12, "bold"), anchor="center", fg='red', bg="black")
    label2.place(relx=0.5, rely=0.2, anchor="center")
   
    button1 = tk.Button(fenster, text="MediBot Beenden", command=close, width=20, height=3,bg="black", fg="white")
    button1.place(relx=0.5, rely=0.92, anchor="center")

    fenster.mainloop()

def Hirn():
    global gif_label  
    global running

    time.sleep(0.2)
    if gif_label is not None:
        gif_label.pack_forget()
    keyboard.wait("m")
    label2["text"] = ""
    #fenster.after(0, lambda: label.config(text="Recording..."))
    label["text"] = "Recording..."
    WAV_Pfad = Eingabe()
    #gif_label.pack(expand=True)
    label["text"] = "Verarbeiten..."
    Gesprochenes = S2T(WAV_Pfad)
    #gif_label.pack-forget()
    label["text"] = ""
    if Gesprochenes == "Error§$§$§$§$§$§$$$§":
        Error_bei_Speech2text()
    GPT_Antwort = ChatGPT(Gesprochenes)
    #GPT_Antwort = ChatGPT_temp()

    if gif_label is not None:
        gif_label.pack(expand=True)
    synthesize_text(GPT_Antwort)
    if gif_label is not None:
        gif_label.pack_forget()
    time.sleep(0.1)
    #fenster.after(0, lambda: label.config(text="Drücke M zum Aufnehmen deiner Frage"))
    label["text"]= "Halte M gedrückt zum Sprechen"
    label2["text"] = "Achtung! Das Gepsrochene wird mit Google TTS bearbeitet."
    Hirn()

if __name__ == "__main__":
    gif_thread = threading.Thread(target=gif_vid)
    gif_thread.start()
    
    gui_thread = threading.Thread(target=GUI)
    gui_thread.start()

    leglos_thread = threading.Thread(target=Hirn)
    leglos_thread.start()