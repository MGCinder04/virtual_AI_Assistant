from tkinter import *

root = Tk()
root.title("AI Assistant")
root.geometry("550x675")
root.resizable(False, False)
root.config(bg="#6f8faf")

frame = LabelFrame(root, padx=100, pady=7, borderwidth=3, relief="raised")
frame.grid(row=0, column=1, padx=55, pady=10)

text_label = Label(
    frame, text="AI Assistant", font=("comic sans ms", 14, "bold"), bg="#356696"
)
text_label.grid(row=0, column=0, padx=20, pady=10)


root.mainloop()
