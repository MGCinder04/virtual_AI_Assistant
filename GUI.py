from tkinter import *
from PIL import Image, ImageTk
import speech2text
import action

root = Tk()
root.title("AI Assistant")
root.geometry("550x675")
root.resizable(False, False)
root.config(bg="#6f8faf")


def ask():
    ask_val = speech2text.speech2text()
    bot_val = action.Action(ask_val)
    text.insert(END, "Me --> " + ask_val + "\n")
    if bot_val != None:
        text.insert(END, "Bot <-- " + str(bot_val) + "\n")
    if bot_val == "Okay, Goodbye!":
        root.destroy()


def send(event = None):
    send = entry.get()
    entry.delete(0, END)
    bot = action.Action(send)
    text.insert(END, "Me --> " + send + "\n")
    if bot != None:
        text.insert(END, "Bot <-- " + str(bot) + "\n")
    if bot == "Okay, Goodbye!":
        root.destroy()


def del_text():
    text.delete("1.0", "end")


frame = LabelFrame(root, padx=100, pady=7, borderwidth=3, relief="raised")
frame.config(bg="#6f8faf")
frame.grid(row=0, column=1, padx=55, pady=10)

text_label = Label(
    frame, text="AI Assistant", font=("comic sans ms", 14, "bold"), bg="#356696"
)
text_label.grid(row=0, column=0, padx=20, pady=10)

image = ImageTk.PhotoImage(Image.open("image/assitant.png"))
image_label = Label(frame, image=image)
image_label.grid(row=1, column=0, pady=20)

text = Text(root, font=("courier 10 bold"), bg="#356696")
text.grid(row=2, column=0)
text.place(x=100, y=375, width=375, height=100)

entry = Entry(root, justify=CENTER)
entry.place(x=100, y=500, width=350, height=30)
entry.bind("<Return>", send)
entry.focus()


Button1 = Button(
    root,
    text="Ask",
    bg="#356696",
    pady=16,
    padx=40,
    borderwidth=3,
    relief=SOLID,
    command=ask,
)
Button1.place(x=70, y=575)

Button2 = Button(
    root,
    text="Send",
    bg="#356696",
    pady=16,
    padx=40,
    borderwidth=3,
    relief=SOLID,
    command=send,
)
Button2.place(x=400, y=575)

Button3 = Button(
    root,
    text="Delete",
    bg="#356696",
    pady=16,
    padx=40,
    borderwidth=3,
    relief=SOLID,
    command=del_text,
)
Button3.place(x=225, y=575)

root.mainloop()
