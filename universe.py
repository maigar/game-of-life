from tkinter import *
import numpy as np
import threading
import json
import codecs

class Life(Tk):
	def __init__(self,config='config',conf=None):
		# pass
		self.conf={}
		super().__init__()
		self.conf=json.load(open(config+'.json'))
		if config=='config':
			self.grid=np.zeros((self.conf["rows"],self.conf["cols"]),dtype=np.int)
		else:
			self.grid=np.load(config+'.npy')
		self.sim=Simulation(self.grid,speed=self.conf["speed"])
		self.makeGrid(self.conf["rows"],self.conf["cols"])	
		self.playGod()

	def importConfig(self,filename=None):
		self.conf=json.load(open('config.json'))
		self.grid=np.load('Examples/'+filename)

	def exportConfig(self,filename='config'):
		# with (open((filename+'.json'),'w')) as file:
		json.dump(self.conf, codecs.open('Examples/'+filename+'.json', 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
		np.save('Examples/'+filename,self.grid)

	def makeGrid(self,m,n):
		frame=Frame(self)
		Left=Frame(self)
		Right=Frame(self)
		frame.grid(row=0, column=0, sticky=N+S+E+W)
		frameLeft=Frame(Left)
		frameRight=Frame(Right)
		Grid.rowconfigure(frameLeft, 0, weight=1)
		Grid.columnconfigure(frameLeft, 0, weight=1)
		frameLeft.grid(row=0, column=0, sticky=N+S+E+W)
		frameRight.grid(row=0,column=0, sticky=N+S+E+W)
		grid=Frame(frameLeft)
		grid.grid(sticky=N+S+E+W, column=0, row=3, columnspan=2)
		Grid.rowconfigure(frameLeft, 3, weight=1)
		Grid.columnconfigure(frameLeft, 0, weight=1)
		self.buttons=[]
		if(m<3 or n<3):
			print("None of the dimensions can not be less than 3")
			m=n=3
		
		for y in range(m):
			for x in range(n):
				def changeState(i,j):
					pos=i*n+j
					if self.buttons[pos].cget('bg') != 'black':
						self.buttons[pos].config(bg='black')
					else:
						self.buttons[pos].config(bg='white')
				btn=Button(frameLeft,fg='blue',height=1,width=1,bg='white',command=lambda i=y,j=x:changeState(i,j))
				btn.grid(column=x,row=y,sticky=S+W+E+N)
				self.buttons.append(btn)

		for x in range(n):
			Grid.columnconfigure(frameLeft,x,weight=1)

		for y in range(m):
			Grid.columnconfigure(frameLeft,y,weight=1)

		self.startButton=Button(frameRight,text="Simulate",command=self.simulate)
		self.stopButton=Button(frameRight,text="Stop",command=self.pauseLife,state="disabled")
		self.stepButton=Button(frameRight,text="1 Step",command=self.nextGen)
		# self.Text
		time=Button(frameRight)
		self.startButton.grid(row=0,column=0,sticky=S+W+E+N)
		self.stopButton.grid(row=1,column=0,sticky=S+W+E+N)
		self.stepButton.grid(row=2,column=0,sticky=S+W+E+N)
		Left.grid(row=0,column=0,sticky=S+W+E+N)
		Right.grid(row=0,column=1,sticky=S+W+E+N)

	def nextGen(self):
		# print(self.grid.shape)

		self.sim.setGrid(self.getGridArray())
		self.grid=self.sim.forward()    
		self.playGod()

	def playGod(self):
		for i in range(self.conf["rows"]):
			for j in range(self.conf["cols"]):
				# temp=self.temp
				if(self.grid[i][j]==0):
					self.buttons[i*self.conf["cols"]+j].config(bg='white')
				else:
					self.buttons[i*self.conf["cols"]+j].config(bg='black')

	def getGridArray(self):
		for y in range(self.conf["rows"]):
			for x in range(self.conf["cols"]):
				if(self.buttons[y*self.conf["cols"]+x].cget('bg')=='black'):
					self.grid[y][x]=1
				else:
					self.grid[y][x]=0
		return self.grid

	def setUniverse(self,grid):
		self.grid=grid
		self.playGod()

	def pauseLife(self):
		self.startButton.config(state="normal")
		self.stepButton.config(state="normal")
		self.sim.stop()

	def simulate(self):
		self.startButton.config(state="disabled")
		self.stepButton.config(state="disabled")
		self.stopButton.config(state="normal")
		self.sim.setGrid(self.getGridArray())
		self.sim.simulate(self.setUniverse)

class Simulation:
	def __init__(self,grid,edit_func=None,pad=3,speed=0.5):
		self.grid=np.zeros((grid.shape[0]+pad*2,grid.shape[1]+pad*2))
		self.timer=None
		self.is_running=False
		self.edit_func=edit_func
		self.pad=pad
		self.speed=speed

	def setGrid(self,grid):
		self.grid[self.pad:-self.pad,self.pad:-self.pad]=grid

	def forward(self):
		assert(type(self.grid)==np.ndarray),"Input to forward should be a numpy array."
		row,col=self.grid.shape
		row=row-2
		col=col-2
		kernel=np.array([[1,1,1],[1,0,1],[1,1,1]])
		gcopy=self.grid.copy()
		# print(self.grid)
		for i in range(0,row):
			for j in range(0,col):
				temp=gcopy[i:i+3,j:j+3]
				neighbs=(temp*kernel).sum()
				if neighbs<2:
					(self.grid[i:i+3,j:j+3])[1][1]=0
				elif (neighbs==2 or neighbs==3) and (temp)[1][1]==1:
					(self.grid[i:i+3,j:j+3])[1][1]=1
				elif neighbs>3:
					(self.grid[i:i+3,j:j+3])[1][1]=0
				elif neighbs==3 and (temp)[1][1]==0:
					(self.grid[i:i+3,j:j+3])[1][1]=1
		return self.grid[self.pad:-self.pad,self.pad:-self.pad]

	def run(self):
		self.is_running=False
		self.simulate()
		self.forward()
		self.edit_func((self.grid[self.pad:-self.pad,self.pad:-self.pad]))


	def simulate(self,edit_func=None):
		if(edit_func!=None):
			self.edit_func=edit_func
		if not self.is_running:
			self.timer=threading.Timer(self.speed,self.run)
			self.timer.start()
			self.is_running=True

	def stop(self):	
		self.timer.cancel()
		self.is_running=False

	
if __name__=="__main__":
	universe = Life("pentadecathlon")
	universe.mainloop()

