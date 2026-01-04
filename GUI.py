from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import speech2text
import action
import sys, os


class GradientButton(Canvas):
    def __init__(self, parent, text="Button", command=None, **kwargs):
        super().__init__(parent, width=220, height=80, highlightthickness=0, **kwargs)

        self.command = command
        self.text = text

        # # Colors
        # self.base_color = "#4a6cf7"
        # self.light_color = "#6f8dfd"
        # self.text_color = "#e5e5e5"

        # Draw button
        self.round_rect = self.create_rounded_rect(
            5, 5, 215, 75, 20, fill=self.base_color
        )
        self.text_item = self.create_text(
            110,
            40,
            text=self.text,
            fill=self.text_color,
            font=("Segoe UI", 16, "bold"),
        )

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def create_rounded_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [
            x1 + r,
            y1,
            x2 - r,
            y1,
            x2,
            y1,
            x2,
            y1 + r,
            x2,
            y2 - r,
            x2,
            y2,
            x2 - r,
            y2,
            x1 + r,
            y2,
            x1,
            y2,
            x1,
            y2 - r,
            x1,
            y1 + r,
            x1,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_hover(self, event):
        self.itemconfig(self.round_rect, fill=self.light_color)
        self.itemconfig(self.text_item, fill="white")

    def on_leave(self, event):
        self.itemconfig(self.round_rect, fill=self.base_color)
        self.itemconfig(self.text_item, fill=self.text_color)

    def on_press(self, event):
        self.itemconfig(self.round_rect, fill=self.base_color)
        self.itemconfig(self.text_item, fill="white")

    def on_release(self, event):
        if self.command:
            self.command()
        self.itemconfig(self.round_rect, fill=self.light_color)
        self.itemconfig(self.text_item, fill=self.text_color)


class StyledInput(Canvas):
    def __init__(
        self, parent, width=190, height=40, placeholder="Type here...", **kwargs
    ):
        bg = kwargs.pop("bg", parent.cget("bg"))
        super().__init__(
            parent, width=width, height=height, highlightthickness=0, bg=bg, **kwargs
        )

        self.border_color = "#8707ff"
        self.text_color = "white"
        self.placeholder_color = "gray"
        self.bg_color = bg
        self.placeholder = placeholder

        self.round_rect = self.create_rounded_rect(
            2, 2, width - 2, height - 2, 10, outline=self.border_color, width=2
        )

        # Entry widget
        self.entry = Entry(
            self,
            bd=0,
            fg=self.placeholder_color,
            bg=self.bg_color,
            insertbackground="white",
            font=("Segoe UI", 12),
            relief="flat",
        )

        self.entry_window = self.create_window(
            width // 2,
            height // 2,
            window=self.entry,
            width=width - 20,
            height=height - 10,
        )

        self.entry.insert(0, self.placeholder)

        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry.bind("<FocusIn>", self.on_active, add="+")
        self.entry.bind("<FocusOut>", self.on_inactive, add="+")

    def create_rounded_rect(self, x1, y1, x2, y2, r=10, **kwargs):
        outline = kwargs.get("outline", self.border_color)
        width = kwargs.get("width", 2)
        points = [
            x1 + r,
            y1,
            x2 - r,
            y1,
            x2,
            y1,
            x2,
            y1 + r,
            x2,
            y2 - r,
            x2,
            y2,
            x2 - r,
            y2,
            x1 + r,
            y2,
            x1,
            y2,
            x1,
            y2 - r,
            x1,
            y1 + r,
            x1,
            y1,
        ]
        return self.create_polygon(
            points, smooth=True, outline=outline, width=width, fill=""
        )

    def on_active(self, event):
        self.itemconfig(self.round_rect, outline=self.border_color, width=3)

    def on_inactive(self, event):
        self.itemconfig(self.round_rect, outline=self.border_color, width=2)

    def on_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg=self.text_color)

    def on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=self.placeholder_color)

    def get(self):
        text = self.entry.get()
        return "" if text == self.placeholder else text

    def delete(self, start, end):
        self.entry.delete(start, end)


# ---- Functions ----
def ask():
    ask_val = speech2text.speech2text()
    bot_val = action.Action(ask_val)
    text.config(state=NORMAL)
    text.insert(END, "🧑 Me → " + ask_val + "\n", "user")
    if bot_val is not None:
        text.insert(END, "🤖 Bot ← " + str(bot_val) + "\n", "bot")
    text.see(END)
    if bot_val == "Okay, Goodbye!":
        root.destroy()
    text.config(state=DISABLED)


def send(event=None):
    send_val = entry.get()
    entry.delete(0, END)
    bot = action.Action(send_val)
    text.config(state=NORMAL)
    text.insert(END, "🧑 Me → " + send_val + "\n", "user")
    if bot is not None:
        text.insert(END, "🤖 Bot ← " + str(bot) + "\n", "bot")
    text.see(END)
    if bot == "Okay, Goodbye!":
        root.destroy()
    text.config(state=DISABLED)
    entry.entry.focus()


def del_text():
    text.config(state=NORMAL)
    text.delete("1.0", "end")
    text.config(state=DISABLED)


def show_commands():
    text.config(state=NORMAL)
    try:
        with open(resource_path("assistant_commands.txt"), "r") as f:
            commands_help = f.read()
        text.insert("1.0", f"🤖 Available Commands:\n\n{commands_help}", "bot")
    except FileNotFoundError:
        text.insert("1.0", "🤖 Available commands file not found.", "bot")
    text.config(state=DISABLED)


def resource_path(rel_path):
    try:
        base = sys._MEIPASS
    except AttributeError:
        base = os.path.abspath(".")
    return os.path.join(base, rel_path)


root = Tk()
root.title("AI Assistant")
root.geometry("1200x1400")
root.resizable(False, False)
root.config(bg="#1e1e2f")

# ---- Layout Grid ----
root.grid_rowconfigure(2, weight=1)
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

image = ImageTk.PhotoImage(
    Image.open(resource_path("image/assistant.png")).resize((200, 200))
)
image_label = Label(frame, image=image, bg="#2b2d42")
image_label.grid(row=1, column=0, pady=5)

# ---- Chat Box (styled) ----
text = Text(
    root,
    font=("Consolas", 12),
    bg="#0f172a",
    fg="white",
    insertbackground="white",
    wrap="word",
    relief="flat",
    highlightthickness=2,
    highlightbackground="#8707ff",
)
text.tag_configure("user", foreground="#3a86ff")
text.tag_configure("bot", foreground="#ffbe0b")
text.grid(row=2, column=0, padx=50, sticky="nsew")

show_commands()

# ---- Entry (StyledInput) ----
entry_frame = Frame(root, bg="#1e1e2f")
entry_frame.grid(row=3, column=0, padx=50, pady=10, sticky="ew")
entry_frame.grid_columnconfigure(0, weight=1)

entry = StyledInput(
    entry_frame, width=1100, height=60, placeholder="Type here...", bg=entry_frame["bg"]
)
entry.grid(row=0, column=0, sticky="ew")


entry.entry.bind("<Return>", send)


# ---- Buttons ----
btn_frame = Frame(root, bg="#1e1e2f")
btn_frame.grid(row=4, column=0, padx=50, pady=10, sticky="ew")
for i in range(4):
    btn_frame.grid_columnconfigure(i, weight=1)

ask_btn = GradientButton(btn_frame, text="🎤 Ask", command=ask, bg="#1e1e2f")
ask_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

send_btn = GradientButton(btn_frame, text="📩 Send", command=send, bg="#1e1e2f")
send_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

del_btn = GradientButton(btn_frame, text="🧹 Clear", command=del_text, bg="#1e1e2f")
del_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

commands_btn = GradientButton(
    btn_frame, text="📜 Commands", command=show_commands, bg="#1e1e2f"
)
commands_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
commands_btn.itemconfig(commands_btn.text_item, font=("Segoe UI", 10, "bold"))


root.mainloop()

if __name__ == "__main__":
    pass
