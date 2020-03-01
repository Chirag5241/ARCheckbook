from tkinter import *
import tkinter as tk
from tkinter import filedialog, Text
import final

def op1():
	app.destroy()
	final.run_check_demo()

def op2():
	app.destroy()
	final.run_sign_demo()

def op3():
	app.destroy()
	final.run_draw_demo()

app = tk.Tk()
app.title("bg attribute")
app.geometry('700x600')
app['bg'] = '#13294B'
frame = tk.Frame( bg = "#E84A27")
frame.place(relwidth = .9, relheight = .9, relx = 0.05, rely = 0.05)
btn1 = Button(app, text = 'CHECK DEMO', font=("fixedsys", 10), width = 20, fg = 'white', height = 3, bg = '#13294B',  bd = '5',  
                          command = op1)
btn1.place(x=265, y=200)
btn2 = Button(app, text = 'SIGNING DEMO ', font=("fixedsys", 10), width = 20, fg = 'white', height = 3, bg = '#13294B',  bd = '5',  
                          command = op2)
btn2.place(x=265, y=300)
btn3 = Button(app, text = 'DRAW ', font=("fixedsys", 10), width = 20, fg = 'white', height = 3, bg = '#13294B',  bd = '5',  
                          command = op3)
btn3.place(x=265, y=400)
company = tk.Text(app,  
background = '#E84A27', 
highlightthickness=0,font=("fixedsys", 32, 'bold') , relief = 'flat', selectborderwidth=0, highlightbackground='#E84A27', heigh=1, width=10)
company.pack()
company.tag_config('centre',justify='center')
company.place(x=310, y=100)
company.insert(tk.END, "PYRO")
tk.mainloop()
app.mainloop()
