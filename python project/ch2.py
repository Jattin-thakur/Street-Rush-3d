import tkinter as tk

def show_input():
    user_text = entry.get()
    label.config(text=f"You entered: {user_text}")
    
    root = tk.Tk()
    root.title("entry example")
    root.geometry("392,200")
    
    entry = tk.Entry(root, width=25)
    entry.pack()
    button = tk.Button(root, text="Submit", command=show_input)
    button.pack()
    label = tk.label(root, text="Submit",command=show_input)
    button.pack()
    label = tk.Label(root, text="")
    label.pack(paddy=20)
    root.mainloop()