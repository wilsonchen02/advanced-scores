import tkinter as tk
import tkinter.ttk as ttk

# Create the application window
root = tk.Tk()
root.title("Fard among us")
# Center the window
window_width = 1000
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.resizable(False, False)
root.iconbitmap("./images/amogus.ico")

# Create the user interface
my_label = ttk.Label(text="Hello World!")
my_label.pack(
    ipadx = 10,
    ipady = 10,
    expand = True
)
my_img = tk.PhotoImage(file = "./images/kirbo.gif")
dead_button = ttk.Button(root, image=my_img)
dead_button.pack(
    ipadx = 10,
    ipady = 10,
    expand = True
)

# Start the GUI event loop
root.mainloop()

