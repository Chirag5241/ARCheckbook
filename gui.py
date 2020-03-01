import tkinter as tk
from tkinter import filedialog, Text

root = tk.Tk()

canvas = tk.Canvas(root, height = 700, width = 700, bg = '#5722DA')
canvas.grid(row = 0, column = 0)

frame = tk.Frame(root, bg = "white")
frame.place(relwidth = .8, relheight = .8, relx = .1, rely = .1)

check_demo = tk.Button(root, text = "Run Check Demo", padx = 10, pady = 5, height = 10, width = 66, fg = 'white', bg = '#263D42')
check_demo.grid(row = 0, column = 0)
draw_demo = tk.Button(root, text = "Run Drawing Demo", padx = 10, pady = 5, height = 10, width = 66, fg = 'white', bg = '#263D42')
draw_demo.grid(row = 1, column = 0)
receipt_demo = tk.Button(root, text = "Run Receipt Demo", padx = 10, pady = 5, height = 10, width = 66, fg = 'white', bg = '#263D42')
receipt_demo.grid(row = 2, column = 0)

root.mainloop()
