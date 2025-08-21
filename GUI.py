from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import speech2text
import action

root = Tk()
root.title("AI Assistant")
root.geometry("600x700")
root.resizable(False, False)
root.config(bg="#1e1e2f")

# ---- Custom Styles ----
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Modern.TButton",
    font=("Segoe UI", 11, "bold"),
    background="#3a86ff",
    foreground="white",
    padding=(10, 8),
)
style.map("Modern.TButton", background=[("active", "#265dbe")])


# ---- Functions ----
def ask():
    ask_val = speech2text.speech2text()
    bot_val = action.Action(ask_val)
    text.insert(END, "🧑 Me → " + ask_val + "\n", "user")
    if bot_val is not None:
        text.insert(END, "🤖 Bot ← " + str(bot_val) + "\n", "bot")
    if bot_val == "Okay, Goodbye!":
        root.destroy()


def send(event=None):
    send = entry.get()
    entry.delete(0, END)
    bot = action.Action(send)
    text.insert(END, "🧑 Me → " + send + "\n", "user")
    if bot is not None:
        text.insert(END, "🤖 Bot ← " + str(bot) + "\n", "bot")
    if bot == "ok sir":
        root.destroy()
    entry.focus()


def del_text():
    text.delete("1.0", "end")


# ---- Layout Grid Config ----
root.grid_rowconfigure(2, weight=1)  # Chat box expands
root.grid_columnconfigure(0, weight=1)

# ---- Header ----
frame = Frame(root, bg="#2b2d42")
frame.grid(row=0, column=0, sticky="ew", pady=10)
frame.grid_columnconfigure(0, weight=1)

title = Label(
    frame,
    text="🤖 Virtual Assistant",
    font=("Segoe UI", 18, "bold"),
    fg="white",
    bg="#2b2d42",
)
title.grid(row=0, column=0, pady=5)

image = ImageTk.PhotoImage(Image.open("image/assitant.png").resize((120, 120)))
image_label = Label(frame, image=image, bg="#2b2d42")
image_label.grid(row=1, column=0, pady=5)

# ---- Chat Box ----
text = Text(
    root,
    font=("Consolas", 12),
    bg="#0f172a",
    fg="white",
    insertbackground="white",
    wrap="word",
    relief="flat",
)
text.tag_configure("user", foreground="#3a86ff")
text.tag_configure("bot", foreground="#ffbe0b")
text.grid(row=2, column=0, padx=50, sticky="nsew")

# ---- Entry Frame ----
entry_frame = Frame(root, bg="#1e1e2f")
entry_frame.grid(row=3, column=0, padx=50, pady=10, sticky="ew")
entry_frame.grid_columnconfigure(0, weight=1)  # let entry expand

# ---- Entry (styled) ----
entry = Entry(
    entry_frame,
    font=("Segoe UI", 12),
    bg="#2b2d42",  # dark gray background
    fg="gray",  # placeholder color
    insertbackground="white",
    relief="flat",
)
entry.grid(row=0, column=0, sticky="ew", ipady=6, padx=(8, 0), pady=6)

# ---- Placeholder ----
placeholder = "Type here..."


def on_focus_in(event):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg="white")


def on_focus_out(event):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="gray")


entry.insert(0, placeholder)
entry.bind("<FocusIn>", on_focus_in)
entry.bind("<FocusOut>", on_focus_out)
entry.bind("<Return>", send)

# ---- Buttons ----
btn_frame = Frame(root, bg="#1e1e2f")
btn_frame.grid(row=4, column=0, padx=50, pady=10, sticky="ew")
for i in range(4):
    btn_frame.grid_columnconfigure(i, weight=1)

ask_btn = ttk.Button(btn_frame, text="🎤 Ask", command=ask, style="Modern.TButton")
ask_btn.grid(row=0, column=0, padx=5, sticky="ew")

send_btn = ttk.Button(btn_frame, text="📩 Send", command=send, style="Modern.TButton")
send_btn.grid(row=0, column=1, padx=5, sticky="ew")

del_btn = ttk.Button(
    btn_frame, text="🗑️ Clear", command=del_text, style="Modern.TButton"
)
del_btn.grid(row=0, column=2, padx=5, sticky="ew")

exit_btn = ttk.Button(
    btn_frame, text="❎ Exit", command=root.destroy, style="Modern.TButton"
)
exit_btn.grid(row=0, column=3, padx=5, sticky="ew")

root.mainloop()
