import tkinter as tk 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from numpy import *

class Widget():
    def __init__(self , table = None  , function = None) :
        """
        the initiation function  :
        definnig a tkinter widget 
        """
        table = [[2 , 3 , 4] , [3 , 4 , 5]]
        self.once = True 
        self.root = tk.Tk()
        self.root.title("Embedding in Tk")
        self.quit_button = tk.Button(master=self.root, text="Quit", command=self._quit)
        self.draw_button_plot_2D = tk.Button(master=self.root, text="Plot 2D", command=self.ploting)
        self.draw_button_plot_3D = tk.Button(master=self.root, text="Plot 3D", command=self.ploting3)
        self.quit_button.pack(side=tk.BOTTOM)
        self.draw_button_plot_2D.pack(side = tk.BOTTOM)
        self.draw_button_plot_3D.pack(side = tk.BOTTOM)

        self.entr = tk.StringVar()
        self.entry = tk.Entry(self.root  , textvariable = self.entr )
        self.entry.pack()
        self.function = function
        self.table = table
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.sub = self.fig.add_subplot(111)
        self.plott(table)

        tk.mainloop()
    def plott(self , tab) :
        shape = len(tab[1])
        if shape == 3 :
            x_values = [e[0] for e in tab]
            y_values = [e[1] for e in tab]
            z_values = [e[2] for e in tab]
            self.drawcourbe(x_values , y_values , z_values)
    def ploting3(self , n = 100) :
        y_values = [] ;x_values = [] ; function = list(self.entr.get())
        i = 0 # la valeur final
        try :
            b = pi # la valuer final
            n = b / n # le pas 
            while i < b :
                x_values.append(i)
                d = ''
                for k in range(len(function)) :
                    if function[k] == 'x' :
                        function[k] = 'i'
                    d+=function[k]
                y_values.append(eval(d))
                i += n 
        finally : 
            z_values = [1 for i in y_values]
            self.drawcourbe(x_values , y_values , z_values)
    def ploting(self , n = 100) :
        """
        the plotting function 
        create a plot object 
        with function given in the entries 
        """
        y_values = [] ;x_values = [] ; function = list(self.entr.get())
        i = 0 # la valeur final
        try :
            b = pi # la valuer final
            n = b / n # le pas 
            while i < b :
                x_values.append(i)
                d = ''
                for k in range(len(function)) :
                    if function[k] == 'x' :
                        function[k] = 'i'
                    d+=function[k]
                y_values.append(eval(d))
                i += n 
        finally : 
            self.drawcourbe(x_values , y_values )
    def drawcourbe(self , x , y , z = None) :
        self.fig.delaxes(self.sub)
        if not z:
            self.sub = self.fig.add_subplot(111)
            self.sub.plot(x , y)
        else : 
            self.sub = self.fig.add_subplot(111 , projection = "3d")
            self.sub.plot(x , y , z)
        self.fig.suptitle(str(self.entr.get()))
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        if self.once : 
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
            self.toolbar.update()
            self.once = False 
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect("key_press_event", self.on_key_press)


    def on_key_press(self , event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)

    def _quit(self):
        root.quit()
        root.destroy()  
Widget()