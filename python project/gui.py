import tkinter as tk
root = tk.Tk()
root.title("My First GUI")
root.geometry("700x499")

label = tk.Label(root, text="Hello, World!",bg="lightblue",relief="ridge", borderwidth=10,font=("Arial", 16,),foreground ="red")
label.pack(anchor="nw",side="top",)

root.mainloop()

