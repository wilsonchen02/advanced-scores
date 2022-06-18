import tkinter as tk
import tkinter.ttk as ttk

user_input = ""

root = tk.Tk()
root.title("Anilist Advanced Scores")
# Center the window
# window_width = 1000
# window_height = 800
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# center_x = int(screen_width / 2 - window_width / 2)
# center_y = int(screen_height / 2 - window_height / 2)
# root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
# root.resizable(False, False)
root.iconbitmap("./images/amogus.ico")

# UI
# Frame
token_frame = ttk.LabelFrame(root, text = "Access Token")
token_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

token_label = ttk.Label(token_frame, text = "Enter token: ")
token_label.grid(row = 0, column = 0)
access_token = tk.StringVar()
input_box = ttk.Entry(token_frame, textvariable=access_token)
input_box.grid(row=0, column=1)
input_box.focus()

def key_entered():
    global user_input
    user_input = access_token.get()


key_button = ttk.Button(root, text="OK", command=key_entered)
key_button.grid(row=1, column=1)
# key_button.pack(
#     ipadx = 10,
#     ipady = 10,
#     expand = True
# )


# Button to onfirm user inputs for scoring weights
# and perform calculations


# Start the GUI event loop
root.mainloop()

