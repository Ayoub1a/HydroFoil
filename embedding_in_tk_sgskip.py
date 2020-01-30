import tkinter as tk 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from numpy import *

class Widget():
    def __init__(self) :
        """
        the initiation function  :
        definnig a tkinter widget 
        """
        table = [[2 , 3 , 4] , [3 , 4 , 5]]
        self.once = True 
        self.root = tk.Tk()
        self.root.title("Embedding in Tk")
        self.quit_button = tk.Button(master=self.root, text="Quit", command=self._quit)
        self.draw_button_plot_2D = tk.Button(master=self.root, text="Plot", command=self.Plot)
        self.quit_button.pack(side=tk.BOTTOM)
        self.draw_button_plot_2D.pack(side = tk.BOTTOM)

        self.entr = tk.StringVar()
        self.entr.set("Enter a function")
        self.entry = tk.Entry(self.root  , textvariable = self.entr )
        self.entry.pack()
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.sub = self.fig.add_subplot(111)

        tk.mainloop()

    def Plot(self , event = None ) :
        string = self.entr.get()
        Liste = string.split(":")
        function = Liste[0] # this is the function 
        x_interval = eval(Liste[1])
        if len(Liste) == 3 :
            y_interval = eval(Liste[2])
            self.ploting3D(function , x_interval , y_interval)
        else :
            self.ploting2D(function ,x_interval)

    def ploting2D(self ,f , x_int, n = 100) :
        """
        the plotting function 
        create a plot object 
        with function given in the entries
        x_int : the intervalle where to plot  
        """
        function = f
        x0 , xf = x_int
        x_values = linspace(x0 , xf , n+1)
        y_values = []
        for x in x_values :
            y_values.append(eval(function))
        self.drawcourbe(x_values , y_values )
    
    def ploting3D(self ,f , x_int ,y_int , n = 100) :
        function = f 
        x0 , xf = x_int
        y0 , yf = y_int
        x_values = linspace(x0 , xf ,n+1)
        y_values = linspace(y0 , yf ,n+1)
        z_values = []
        for i in range(len(x_values)) :
            x = x_values[i]
            y = y_values[i]
            z_values.append(eval(function))
        self.drawcourbe(x_values , y_values , z_values)


    def drawcourbe(self , x , y , z = None) :
        self.fig.delaxes(self.sub)
        if not z:
            self.sub = self.fig.add_subplot(111)
            self.sub.plot(x , y)
        else : 
            self.sub = self.fig.add_subplot(111 , projection = "3d")
            self.sub.plot(x , y , z)
        self.fig.suptitle(str(self.entr.get().split(":")[0]))
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
