import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from mpl_toolkits import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk )
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import sqlite3 as sql

class Window() : 
	def __init__(self , database, tableau) :
		"""
		database  : the .sqlite file to put use 
		tableau : the tableau where to serach  """
		self.tableau = tableau
		self.database  =  database 
		self.bd = sql.connect(self.database)
		self.cur = self.bd.cursor()
		self.dic = {
		"Alpha": "listangles", 
		"Cz" :"listcd" ,
		"Cx" : "listcl", 
		"Cp" : "listcm" , 
		"max Cp" : "cmfmax" , 
		"Alpha max" : "anglefmax" , 
		}
		self.root = tk.Tk()
		self.root.geometry("500x300+200+200")
		self.root.wm_title("Hydofoil")
		self.label_error = tk.Label(self.root)
		self.label_error.pack_forget()
		self.mainpage()
		self.root.mainloop()

	def mainpage(self) :
		""" celui crée une interface H/M au debut du program """

		nomprofils = self.get_profils()

		self.type_hydro = tk.StringVar()   # le type de l'hydrofoil
		self.nbr_reynolds = tk.StringVar() # the nbr de reynold choisi 
		self.xaxis = tk.StringVar()        # les variables choisi pour le dessin
		self.yaxis = tk.StringVar()
		
		self.main_page = tk.Frame(self.root) # main frame 
		
		hydro = tk.Frame(self.main_page)
		ttk.Label(hydro , text = "Choose a type of hydrofoil  : ").pack(padx = 2 , ipadx = 10, side = tk.LEFT )
		ttk.OptionMenu(hydro , self.type_hydro ,"---- ----"  , *list(nomprofils) ).pack(side = tk.RIGHT)
		
		renold = tk.Frame(self.main_page)
		ttk.Label(renold , text = "Choose reynolds number     : ").pack(pady = 5 , ipadx  = 10,  side = tk.LEFT)
		ttk.Entry(renold , textvariable = self.nbr_reynolds).pack(side = tk.RIGHT)
		
		coordx = tk.Frame(self.main_page)
		coordy = tk.Frame(self.main_page)
		ttk.Label(coordx , text = "Choisissez l'axe des abcsisses   : ").pack(side = tk.LEFT , ipadx = 10)
		ttk.OptionMenu(coordx , self.xaxis, "---- ----" ,*list(self.dic.keys()) , "Trace" ).pack(side = tk.RIGHT)
		ttk.Label(coordy , text = "Choisissez l'axe des cordonées   : ").pack(side = tk.LEFT , ipadx = 10)
		ttk.OptionMenu(coordy , self.yaxis ,"---- ----"  , *list(self.dic.keys()) , "Trace").pack(side = tk.RIGHT)
		
		butons = tk.Frame(self.main_page)
		ttk.Button(butons , text = "Plot" , command =  self.Plot).pack(side = tk.LEFT)
		ttk.Button(butons , text = "Quit" , command =  self.root.destroy).pack(side = tk.RIGHT)		
		
		hydro.pack() ; renold.pack() ; coordx.pack() ; coordy.pack() ; butons.pack()

		self.main_page.pack()

	def get_profils(self) : 
		self.cur.execute("select distinct nomprofil from " + self.tableau)
		l = self.cur.fetchall()
		l = [e[0] for e in l]
		return l

	def Plot(self , event = None) :
		x =  self.xaxis.get()
		y =  self.yaxis.get()
		if y =="Trace" or x == "Trace" : 
			self.plot_coordinates(typ )
		if x  == "---- ----" or y == "---- ----" or y == x : 
			self.label_error.pack(side = tk.BOTTOM)
			self.label_error["text"] = "Please choose different arguments"
			self.label_error["fg"] = "red"

		else : 
			self.label_error.pack_forget()
			typ = self.type_hydro.get()
			renold = self.nbr_reynolds.get()
			self.main_page.pack_forget()
			self.request(typ , x , y , renold)
	def plot_coordinates(self , typ): 
		"""This function is about to plot the hydrofoils coordinates """
		command = f"select listcoordonesxy from {self.tableau} where nomprofil = '{typ}'"
		self.cur.execute(command)
		L = self.cur.fetchone()[0]
		L = L.split(";")
		X = [] ; Y = []
		for i in range(0  , len(L) , 2):
			X.append(float(L[i].replace(',' , ".")))
			Y.append(float(L[i+1].replace(',' , ".")))
		self.drawcourbe(X , Y  , title = "cootdonnes de Xy de la naca : " + typ)


	def request(self , typ , x , y , renolds) : 
		"""request the database for the coordinates """
		if not typ  : 
			self.label_error["text"] = "Please enter a hydrofoil profil"
		command = f"""
		select  {self.dic[x]} ,  {self.dic[y]}
		 from {self.tableau}
		   where nomprofil = '{typ}' and Re = {renolds} ;"""
		# print(command)
		self.cur.execute(command)
		try  :
			L = self.cur.fetchone()
		except : 
			pass
		X = L[0].split(';')[:-1]
		Y = L[1].split(';')[:-1]
		assert len(Y) == len(X) , "des probleme d'homogenité"

		Y = [e.replace(',' ,'.') for e in Y]
		Y = [float(e) for e in Y]
		X = [e.replace("," , '.' ) for e in X]
		X = [float(e) for e in X]
		self.drawcourbe(X , Y , title = y + "= F(" + x + ") à Re :" + str(renolds)  )

	def drawcourbe(self , x , y , title = "" ) : 
		self.fig = Figure(figsize=(7, 5), dpi=100)
		self.fig.suptitle(title)
		self.graph_frame = tk.Frame(self.root)
		self.canvas = FigureCanvasTkAgg(self.fig, master = self.graph_frame)
		self.sub = self.fig.add_subplot(111)
		def retur(event = None):
			self.graph_frame.destroy()
			self.main_page.pack()
		butons = tk.Frame(self.graph_frame)
		ttk.Button(butons , text = "Return" , command= retur).pack(side = tk.RIGHT)
		ttk.Button(butons , text = "Quit" , command = self.root.destroy).pack(side = tk.LEFT)
		butons.pack(side = tk.BOTTOM)
		self.sub.plot(x  , y )
		self.canvas.draw()
		self.root.geometry("400x400")
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
		self.toolbar.update()
		self.canvas.get_tk_widget().pack(side = tk.TOP ,fill = tk.BOTH  ,  expand = True)
		self.graph_frame.pack()


if __name__ == '__main__':
	Window("DemoFileUnlockAppForCompleteData-2020-01-31-03-36-06-0056.sqlite" , "nacaheliciel3")
