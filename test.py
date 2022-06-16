import tkinter as tk
import tkinter.ttk as ttk

user_input = ""

root = tk.Tk()
root.title("Anilist Advanced Scores")
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

# UI
key_label = ttk.Label(root, text="Enter key: ")
key_label.grid(column=0, row=0)
access_key = tk.StringVar()
input_box = ttk.Entry(root, textvariable=access_key)
input_box.grid(column=1, row=0)
input_box.focus()

def key_entered():
    global user_input
    user_input = access_key.get()


key_button = ttk.Button(root, text="OK", command=key_entered)
key_button.grid(column=1, row=1)
# key_button.pack(
#     ipadx = 10,
#     ipady = 10,
#     expand = True
# )


# Button to onfirm user inputs for scoring weights
# and perform calculations


# Start the GUI event loop
root.mainloop()