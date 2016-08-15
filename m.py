from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import ttk
import youtube_dl
import _thread
import os
import pyperclip


def check(x,y):
	if x==y:
		return True
	else:
		return False

class Application(Frame):
	def __init__(self, master):
	    Frame.__init__(self, master)
	    #self.pack()
	    self.widgets(master)
	
	def widgets(self,master):

		self.logo(master)

		self.Frame1=Frame(master)
		self.Frame1.grid(row=1)
		self.textBox(self.Frame1)
		self.paste_button(self.Frame1)
		
		self.Frame2 = Frame(master)
		self.Frame2.grid(row=2)
		self.checkBoxes(self.Frame2)
		
		self.Frame3=Frame(master)
		self.Frame3.grid(row=3)
		self.Download_Location(self.Frame3)

		self.Frame4=Frame(master)
		self.Frame4.grid(row=4)
		self.executeButton(self.Frame4)
		self.cancelButton(self.Frame4)
		
		self.Progress(master)
		# self.executeButton(master)
		# self.cancelButton(master)

	def show_url(self):
		videos = self.video_url.get().split(",")
		print(self.textbar.get())
		for i in videos:
			print(i.strip())
		if self.inAudio.get()==1 and self.inVideo.get()==1:
			for j in range(1,3):
				self.v.set("Processing")
				_thread.start_new_thread(self.process_from_site, (i,j,))
		elif self.inAudio.get()==1:
			self.v.set("Processing")
			_thread.start_new_thread(self.process_from_site, (i,1,))
		elif self.inVideo.get()==1:
			self.v.set("Processing")
			_thread.start_new_thread(self.process_from_site, (i,2,))



	# def Audio_check_boxes(self):
	# 	print(self.inAudio.get())

	# def Video_check_boxes(self):
	# 	print(self.inVideo.get())
	def will_paste(self):
		y=pyperclip.paste()
		if(check(self.video_url.get(), y )):
			pass
		else:
			if self.video_url.get()=="":
				self.video_url.insert(0, y)
			else:
				x = self.video_url.get() + ", " + y
				self.video_url.delete(0,END)
				self.video_url.insert(0,x)

	def callback(self):
		name=askdirectory()
		if name !="":
			self.textbar.delete(0,END)
			self.textbar.insert(0, name)

	def logo(self, master):
		photo = PhotoImage(file="logo2.png")
		w = ttk.Label(root, image=photo)
		w.photo = photo
		w.grid(row=0, pady=10)
	
	def textBox(self, master):
		ttk.Label( master,text="URL").grid(row=0)#grid(row=0, column=0)
		self.video_url = ttk.Entry(master, width=60)
		self.video_url.grid(row=0, column=1, pady=10, padx=5)

	def paste_button(self, master):
		ttk.Button(master, text="Paste", command=self.will_paste).grid(row=0, column=3)

	def executeButton(self, master):
		ttk.Button( master,text="Start", command=self.show_url).grid(row=0, column=0, pady=10, padx=5)#grid(row=4, column=0)

	def cancelButton(self, master):
		ttk.Button(master, text="Cancel", command=master.quit).grid(row=0, column=1)#grid(row=4, column=1)

	def checkBoxes(self, master):
		self.inAudio=IntVar()
		self.inVideo=IntVar()
		ttk.Checkbutton(master, text="Audio", variable=self.inAudio).grid(row=0, column=0, padx=3, pady=10)#.grid(row=2,column=0)
		ttk.Checkbutton(master, text="Video (with Audio)", variable=self.inVideo).grid(row=0, column=1,padx=10)#grid(row=2, column=1)

	def Download_Location(self, master):
		ttk.Label(master, text="Download Location").grid(row=0, column=0)
		self.textbar = ttk.Entry(master,width=50)
		self.textbar.grid(row=0, column=1, padx=5)#grid(row=3, column=0, padx=5, pady=10)
		self.loc = ttk.Button(master, text="Lookup", command = self.callback).grid(row=0, column=2, pady=10)#grid(row=3, column=0, columnspan=3, padx=3)
		self.textbar.insert(0, os.getcwd())

	def Progress(self, master):
		labelsFrame = ttk.LabelFrame(master, text=' Progress ', height=50, width=350)
		labelsFrame.grid_propagate(0)
		labelsFrame.grid(row=5)
		self.v=StringVar()
		ttk.Label(labelsFrame, textvariable=self.v).grid(column=0, row=0)
		self.v.set("Nothing Here")

	def process_from_site(self,link, num):
		os.chdir(self.textbar.get())
		options={}

		if num==1:
			options = {
		    'format': 'bestaudio/best', # choice of quality
		    'extractaudio' : True,      # only keep the audio
		    'audioformat' : "mp3",      # convert to mp3 
		    'outtmpl': '%(title)s.%(ext)s',        # name the file the ID of the video
		    'noplaylist' : True,        # only download single song, not playlist
			}
		elif num==2:
			options = {
			'f': 'bestaudio+bestvideo/best', # choice of quality
			'outtmpl': '%(title)s.%(ext)s',        # name the file the ID of the video
			'noplaylist' : True,        # only download single song, not playlist
			}

		yd = youtube_dl.YoutubeDL()
		
		try:
			r = yd.extract_info(link, download=False)
			self.v.set("Downloading " + r['title'])
		except:
			self.v.set("ERROR")


		with youtube_dl.YoutubeDL(options) as ydl:
			ydl.download([link])
		self.v.set("Downloaded")
		

    #process the output of your_CLI_program
			



root = Tk()
root.title("Downloader")
root.geometry("600x400")
root.resizable(0, 0)
app = Application(root)
root.mainloop()
